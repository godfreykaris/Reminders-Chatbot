# Standard Library Imports
from datetime import datetime, time, timedelta, timezone
import json
import os
import random
import string
import threading
import logging

from dotenv import load_dotenv

load_dotenv()

# Third-Party Library Imports
from werkzeug.security import check_password_hash, generate_password_hash
from flask import Flask, jsonify, redirect, request, render_template, session, url_for
from flask_login import LoginManager, UserMixin, current_user, login_required,  login_user, logout_user
from flask_wtf.csrf import CSRFProtect,  generate_csrf
from twilio.twiml.messaging_response import MessagingResponse
import pytz
import requests
import psycopg2.extras  # If psycopg2 is a third-party library

from flask_mail import Mail, Message

# Custom Module Imports
from modules.database_initializer import DatabaseInitializer
from modules.register_user import UserRegistration
from modules.login import UserLogin
from modules.messaging.send_message import MessageSender
from modules.goals.goal_data_retriever import UserGoalData
from modules.goals.goal_data_store import StoreGoalData
from modules.goals.goal_retriever import UserGoal
from modules.goals.cron_manager import CronJobManager
from modules.goals.user_retriever import UserHandler
from modules.goals.scheduler import GoalScheduler, ReportScheduler
from modules.chatbot.chatgpt_response import ChatGPTResponse
from report_cron_job import ReportGenerator


# Create a Flask application
app = Flask(__name__)

app.config['BASE_URL'] = 'http://localhost:5000'

app.config.update(
    DEBUG=True,
    SECRET_KEY="secret_sauce",
    SESSION_COOKIE_HTTPONLY=True,
    REMEMBER_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Strict",
)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = "strong"
login_manager.needs_refresh_message = (u"Session timedout, please re-login")
login_manager.needs_refresh_message_category = "info"


csrf = CSRFProtect(app)


app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=60)



# Set the static folder relative to the project directory
static_folder_path = os.path.join(os.path.dirname(__file__), 'reminders-svelte', 'public')
#static_folder_path = os.path.join(os.path.dirname(__file__), 'templates', 'static')
app.static_folder = static_folder_path


# Initialize the database connection using the configuration from 'config.json'
database_initializer = DatabaseInitializer('config.json')

#configure flask-mail for sending emails
app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # Use your email provider's SMTP server
app.config['MAIL_PORT'] = 587  # Port for SMTP (587 for TLS)
app.config['MAIL_USE_TLS'] = True  # Use TLS encryption
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')  # Your email address
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')  # Your email password
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER')  # Default sender for emails

mail = Mail(app)

@app.route('/')
def index():
    return render_template('index.html')

class User(UserMixin):
    def __init__(self, id):
        self.id = id

    def get_id(self):
        return str(self.id)

    def update_last_activity(self):
        self.last_activity = datetime.utcnow()

@login_manager.user_loader
def load_user(id: int):
    user_handler = UserHandler(database_initializer)
    response = user_handler.get_user(id)
    user = json.loads(response)
    user_data =  user.get('user_info')

    if user:
        user_model = User(id=user_data['id'])  # Assuming 'id' is a property of the User class
        return user_model
    return None
    

      
@app.route("/api/user_data", methods=["GET"])
def user_data():
    try:
        user_handler = UserHandler(database_initializer)
        result = user_handler.get_user(user_id=current_user.id)
        # Parse the JSON string into a Python dictionary
        result = json.loads(result)
        print(result)
        return result, 200
    
    except Exception as e:
        # Handle any exceptions that may occur and return as JSON
       return jsonify({'error': str(e)}), 500

@app.route("/api/getsession")
def check_session():
    if current_user.is_authenticated:
        return jsonify({"login": True})

    return jsonify({"login": False})

@app.route("/api/logout")
@login_required
def logout():
    logout_user()
    return jsonify({"logout": True})

# Define a route for user registration
@app.route('/api/register', methods=['POST'])
def register():
    try:
        # Create an instance of UserRegistration with the database connection
        user_registrar = UserRegistration(database_initializer=database_initializer)
        # Call the register_user method to handle user registration
        return user_registrar.register_user()
    except Exception as e:
         # Handle any exceptions that may occur and return as JSON
        return jsonify({'error': str(e)}), 500
    
# Define a route for user login
@app.route('/api/login', methods=['POST'])
def login():
    try:
        # Create an instance of UserLogin with the database connection
        user_authenticator = UserLogin(database_initializer=database_initializer)
        # Call the login_user method to handle user login
        result = user_authenticator.login_user()
        status = result.json['status']
        if status == 200:
            response_data = result.json
            # Access specific properties from the response
            user_id = response_data['user_id']
            # Use Flask-Login's login_user function to set the current_user
            login_user(User(int(user_id)))

        return result, status
    except Exception as e:
        print(str(e))
         # Handle any exceptions that may occur and return as JSON
        return jsonify({'error': str(e)}), 500

#generate new password for user
def generate_password(length):
    #definne character set for password generation
    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    digits = string.digits
    special_chars = "!@#$%^&*()_+=-[]{}|:;<>,.?/~"
    
    #ensure that password length is atleast 8 chars
    if length < 8:
        length = 8
    
    #combine character sets
    all_chars = lowercase + uppercase + digits + special_chars
    
    #generate password with random chars
    password = ''.join(random.choice(all_chars) for _ in range(length))
    
    return password

#send new password to user
def send_password_reset_email(email, new_password, user_name):
    try:
        # Create a message object for the email
        msg = Message('Password Reset Instructions', recipients=[email])  # Use the provided email parameter
        
        # Customize the email content with the temporary password
        msg.body = f'Dear {user_name},\n\nWe recently received a request to reset the password for your Reminder App account. To help ensure the security of your account, we have generated a temporary password for you to use:\n\nTemporary Password: {new_password}\n\nPlease follow these steps to reset your password:\n\n1. Go to the Reminder App login page \n2. Enter email, then the temporary password in their respective fields. \n\nFor security reasons, we recommend that you change your password immediately after logging in. If you did not request a password reset or have any concerns about the security of your account, please contact our support team immediately.\n\nThank you for choosing Reminder App for your needs. We apologize for any inconvenience this may have caused and appreciate your understanding as we work to ensure the security of your account.\n\nBest regards,\n Reminder App'
        
        # Send the email
        mail.send(msg)
    
    except Exception as e:
        return jsonify({'error': 'Failed to send password reset email'}), 500


#reset password
@app.route('/api/reset_password', methods=['POST'])
def reset_password():
    try:
        data = request.get_json()
        email = data.get('email')
        phone_number = data.get('phone_number')
        
        # Check if email and phone_number are provided
        if not email or not phone_number:
            return jsonify({'message': 'Invalid input data'}), 400
        
        logging.info(f"Received data: email={email}, phone_number={phone_number}")
        
        # Get a database connection using a context manager
        with database_initializer.get_database_connection() as conn:
            with conn.cursor() as cursor:
                # Check if the user exists in the database
                user_query = """
                    SELECT name
                    FROM users
                    WHERE email = %s
                    AND phone_number = %s
                """
                cursor.execute(user_query, (email, phone_number,))
                user = cursor.fetchone()
                
                if not user:
                    return jsonify({'message': 'User not found!'}), 404
                
                user_name = user[0]
                
                # Generate a new password
                new_password = generate_password(8)
                new_pswd_hash = generate_password_hash(new_password)
                
                # Update the user's password in the database
                update_password = """
                    UPDATE users
                    SET password_hash = %s
                    WHERE email = %s
                    AND phone_number = %s
                """
                cursor.execute(update_password, (new_pswd_hash, email, phone_number))
                
                # Commit the transaction
                conn.commit()
                
                if cursor.rowcount == 0:
                    return jsonify({'message': 'Failed to update password'}), 500
                
                # Send password reset email
                try:
                    send_password_reset_email(email, new_password, user_name)
                except Exception as e:
                    logging.error(f"Failed to send password reset email: {str(e)}")
                    return jsonify({'error': 'Failed to send password reset email'}), 500
                
                return jsonify({'message': 'Password reset was successful'}), 200
    
    except psycopg2.Error as e:
        return jsonify({'error': 'Network error while trying to reset password'}), 500


#route to change user password
@app.route('/api/change_password', methods=['POST'])
@login_required
def change_password():
    try:
        data = request.get_json()
        email = data.get('email')
        phone_number = data.get('phone_number')
        old_password = data.get('oldPassword')
        new_password = data.get('newPassword')
        
        if not phone_number or not old_password or not new_password:
            return jsonify(message="Something went wrong")

        with database_initializer.get_database_connection() as conn:
            # Query to find the user with the given email and phone number
            user_query = """
                SELECT password_hash
                FROM users
                WHERE email = %s
                AND phone_number = %s
            """
            
            with conn.cursor() as cursor:
                cursor.execute(user_query, (email, phone_number))
                user = cursor.fetchone()
                
                if user is None:
                    return jsonify(message="User not found!"), 404
                
                stored_password_hash = user[0]

                # Verify the old password
                if not check_password_hash(stored_password_hash, old_password):
                    return jsonify(message="Incorrect old password"), 401

                # Generate a new password hash
                new_password_hash = generate_password_hash(new_password)
                
                # Update the password in the database
                update_password = """
                    UPDATE users
                    SET password_hash = %s
                    WHERE email = %s
                    AND phone_number = %s
                """
                
                cursor.execute(update_password, (new_password_hash, email, phone_number,))
                conn.commit()  # Commit the transaction
            
        return jsonify(message="Password change was successful"), 200
    
    except psycopg2.Error as e:
        logging.error(f"Error while trying to change password: {str(e)}")
        return jsonify(error="Network error while trying to change password"), 500
    
# Define a route to a user
@app.route('/api/user/retrieve_user', methods=['POST'])
def retrieve_user():
    try:
        # Get user ID from the request parameters
        data = request.get_json()
        user_id = int(data.get('user_id'))

        user_handler = UserHandler(database_initializer)
        return user_handler.get_user(user_id=user_id)

    except Exception as e:
         # Handle any exceptions that may occur and return as JSON
        return jsonify({'error': str(e)}), 500

# Define a route for sending user messages
@app.route('/api/send_message', methods=['POST'])
def send_user_message():
    data = request.get_json()
    recipient = data.get('recipient')
    message = data.get('message')
    message_type = data.get('type')  # 'sms' or 'whatsapp'

    # Create an instance of MessageSender
    message_sender = MessageSender()
    # Call the send_message method to handle message sending
    response = message_sender.send_message(recipient=recipient, message=message, message_type=message_type)

    return response

# Define a route for getting user messages
@app.route('/api/webhook', methods=['POST'])
@csrf.exempt 
def webhook():
    # Get the incoming message from Twilio
    incoming_message = request.form['Body'].lower()
    from_phone_parts = request.form.get('From', '').strip().split(':')
    from_phone = from_phone_parts[1]
    # Handle incoming messages
    user_message_response = MessagingResponse()

    message_type = "whatsapp"
    recipient = from_phone
     # Create an instance of MessageSender
    message_sender = MessageSender()
   
    # Validate message format
    parts = incoming_message.split('=')
    
    # Check if there are exactly two parts
    if len(parts) == 2:
        goal = parts[0]
        report = parts[1]
    else:
        # Tell the user to use the correct format
        message = "Your message should be as follows: \nGoal = Report. \nExample: Yoga = Yes i did my yoga"
        response = message_sender.send_message(recipient=recipient, message=message, message_type=message_type)
        return response

    if not report or not goal or report.isspace() or report == "":
        # Tell the user to use the correct format
        message = "Your message should be as follows: \nGoal = Report. \nExample: Yoga = Yes i did my yoga"
        response = message_sender.send_message(recipient=recipient, message=message, message_type=message_type)
        return response        
        
    
    # Retrieve a user by the phone number
    user_retriever = UserHandler(database_initializer=database_initializer);
    response = user_retriever.get_user_by_phone(from_phone)

    response_data = json.loads(response)
    status_code = response_data['status']

    # Check the response
    if status_code == 200:
        # Successful response
        user_data = response_data['user_info']
    else:
        message = "We are experiencing a problem retrieving your details. \nPlease contact suport."
        response = message_sender.send_message(recipient=recipient, message=message, message_type=message_type)
        return response
    
    # Retrieve the user goals
    goals_retriever = UserGoal(database_initializer=database_initializer)
    response = goals_retriever.get_user_goals(user_data['id'])

    response_data = json.loads(response)
    status_code = response_data['status']

    # Check the response
    if status_code == 200:
        # Successful response
        goals_data = response_data['goals_titles']
    else:
        message = "We are experiencing a problem retrieving your details. \nPlease contact suport."
        response = message_sender.send_message(recipient=recipient, message=message, message_type=message_type)
        return response
    

    # Check if the goal provided by the user is valid
    goal_matched = goals_retriever.find_matching_goal(goal, goals_data)

    if not goal_matched:
       # Inform the user that the goal is invalid
       message = f"The goal: '{goal}' does not exist in your goals. \nCorrect format: Goal = Report. \nExample: Yoga = Yes i did my yoga"
       response = message_sender.send_message(recipient=recipient, message=message, message_type=message_type)
       return response
    
    # Initialize ChatGPTResponse with credentials file
    chatgpt = ChatGPTResponse('config.json')

    # Fetch the conversation history from the database
    history = chatgpt.fetch_history_from_database(database_initializer, user_data['id'], goal_matched['id'])  # Implement this function to retrieve the history from your database

    if not history or history is None:
        history = []
    else:    
        history = json.loads(history)
        
    # Generate a response based on user input and history
    user_input_string = "Goal:" + goal_matched['title'] + ", Report:" + report
    
  
    # Append the new message to the conversation history
    history.append({"role": "user", "content": user_input_string}) 

    response_max_tokens = 256
    response = chatgpt.chat_with_user(history=history, response_max_tokens=response_max_tokens)

    response_data = json.loads(response)
    status_code = response_data['status']

    if status_code == 200:
        bot_message = response_data['bot_response']

        # Append the new message to the conversation history
        history.append({"role": "assistant", "content": bot_message})
    else:
        bot_message = "I am experiencing an error. I am not able to chat with you currently"
    
    # Inform the user that the goal is invalid
    message = bot_message
    response = message_sender.send_message(recipient=recipient, message=message, message_type=message_type)

     # Convert the updated history back to a JSON string
    history_json = json.dumps(history)
    chatgpt.store_history_to_database(database_initializer, user_data['id'], goal_matched['id'], history_json)

    # Store the data
    goal_id = goal_matched['id']
    store_goal_data = StoreGoalData(database_initializer=database_initializer)   
    store_goal_data.store_user_goal_data(report, goal_id, user_data['id'])

    return str(user_message_response)
    
# Define a route for scheduling user goals
@app.route('/api/schedule_goal', methods=['POST'])
@login_required
def schedule_user_goal():
    try:
        # Create an instance of GoalScheduler with the username of the os given by 'whoami' command
        scheduler = GoalScheduler()
        # Schedule a goal using the GoalScheduler
        response = scheduler.schedule_task_cron()


        return response
    except Exception as e:
        # Handle any exceptions that may occur and return as JSON
        return jsonify({'error': str(e)}), 500

# Define a route for scheduling user goals
@app.route('/api/schedule_report', methods=['POST'])
@login_required
def schedule_user_report():
    try:
        # Create an instance of ReportScheduler with the username of the os given by 'whoami' command
        scheduler = ReportScheduler()
        # Schedule a goal using the ReportScheduler
        response = scheduler.schedule_task_cron()


        return response
    except Exception as e:
        # Handle any exceptions that may occur and return as JSON
        return jsonify({'error': str(e)}), 500

# Define a route for getting an anylysis report for user data from ChatGPT to be sent via message
@app.route('/api/chat/generate_report', methods=['POST'])
@login_required
def get_chatgpt_analysis_message_report():
    try:
        # Parse the user's input from the request JSON
        user_data = request.json['user_data']

        # Initialize ChatGPTResponse with credentials file
        chatgpt = ChatGPTResponse('config.json')

        # Generate a response using ChatGPT
        prompt_message = f"Analyze the following user data for {user_data['name']}. Summarize the data and address the user about your analysis. Make sure you give recommendations and guidance to the user. Address the user as 'You'. Strictly use 120 to 150 words: {user_data}"
        response_max_tokens=256
        response = chatgpt.generate_analysis_report(prompt_message=prompt_message, response_max_tokens=response_max_tokens)

        # Return the response to the client as JSON
        return response

    except Exception as e:
        # Handle any exceptions that may occur and return as JSON
        return jsonify({'error': str(e)}), 500
    

# Define a route for getting messages from ChatGPT that you can send to users
@app.route('/api/chat/generate_message', methods=['POST'])
def get_chatgpt_sample_message():
    try:
        # Parse the template message from the request JSON
        template_message = request.json['template_message']

        # Initialize ChatGPTResponse with credentials file
        chatgpt = ChatGPTResponse('config.json')

        # Generate a response using ChatGPT
        prompt_message = f"Rephrase this question:{template_message}"
        response_max_tokens=30
        response = chatgpt.generate_user_message(prompt_message=prompt_message, response_max_tokens=response_max_tokens)

        # Return the response to the client as JSON
        return response

    except Exception as e:
        # Handle any exceptions that may occur and return as JSON
        return jsonify({'error': str(e)}), 500        

# Define a route for chating with the users
@app.route('/api/chat/chat_with_user', methods=['POST'])
def chat_with_user():
    try:
        # User input
        user_input = request.json['user_input']

        # Initialize ChatGPTResponse with credentials file
        chatgpt = ChatGPTResponse('config.json')

        # Generate a response based on user input
        user_input_string = f"{user_input}"
        response_max_tokens = 4096  # Adjust max_tokens as needed
        response = chatgpt.chat_with_user(user_input=user_input_string, response_max_tokens=response_max_tokens)


        if response.status_code == 200:            
            bot_message = response.json['bot_response']        

        else:
            bot_message = "I am experiencing an error. I am not able to chat with you currently"
        
        # Return the bot's response to the client as JSON
        return jsonify({'bot_response': bot_message}), 200

    except Exception as e:
        bot_message = "I am experiencing an error. I am not able to chat with you currently"
        #return jsonify({'bot_response': bot_message})
    
        # For testing only
        return jsonify({'bot_response': str(e)}), 500

# Define a route to retrieve a goal
@app.route('/api/user/retrieve_goal', methods=['POST'])
def retrieve_user_goal():
    try:
        data = request.get_json()
        user_id = int(data.get('user_id'))
        goal_id = int(data.get('goal_id'))
    
        user_goal = UserGoal(database_initializer)
        return user_goal.get_user_goal(user_id=user_id, goal_id=goal_id)

    except Exception as e:
         # Handle any exceptions that may occur and return as JSON
        return jsonify({'error': str(e)}), 500
    

# Define a route to retrieve  goal data
@app.route('/api/user/retrieve_goal_data', methods=['POST'])
def retrieve_user_goal_data():
    try:
        data = request.get_json()
        user_id = int(data.get('user_id'))
        goal_id = int(data.get('goal_id'))

        user_goal_data = UserGoalData(database_initializer)
        return user_goal_data.get_user_goal_data(user_id=user_id, goal_id=goal_id)

    except Exception as e:
         # Handle any exceptions that may occur and return as JSON
        return jsonify({'error': str(e)}), 500


#serialize the data fetched from the database that isnt json serializable
def serialize_time_to_str(time_obj):
    if isinstance(time_obj, time):
        return time_obj.strftime("%H:%M:%S")
    return time_obj

#get timezones
@app.route('/api/get_timezones', methods=['GET'])
@login_required
def get_timezones():
    timezones = pytz.all_timezones
    return jsonify(timezones)

#validate timezones
def validate_timezone(time_zone):
    try:
        pytz.timezone(time_zone)
        return True
    except pytz.UnknownTimeZoneError:
        return False

# goal data analysis report
@app.route('/api/get_report/<int:id>', methods=['GET'])
@login_required
def get_report(id):
    try:
        user_id = current_user.id
        
        if not user_id or not id:
            return jsonify(message="Invalid user or goal id"), 400

        report_generator = ReportGenerator(database_initializer=database_initializer)
        # Retrieve user information
        user = report_generator.retrieve_user(user_id)

        # Retrieve goal information
        goal = report_generator.retrieve_goal(user_id, id)

        # Retrieve goal data entries
        goal_data = report_generator.retrieve_goal_data(user_id, id)

        # Generate the report
        report = report_generator.generate_report(user, goal, goal_data)


        
        logging.info(f'Script executed successfully for user {user_id}')
    
        if report:
            return report, 200
        else:
            return jsonify(message="Data not found"), 404

    except psycopg2.Error as e:
        logging.error(f'Script encountered an error: {str(e)} for user {user_id}')
        return jsonify(message="Database error"), 500

#add goal
@app.route('/api/add_goal', methods=['POST'])
@login_required
def add_goal():
    
    data = request.get_json().get('goal_data')
    user_id = current_user.id
    report_frequency = data.get('report_frequency')
    goal_title = data.get('goal_title')
    goal_description = data.get('goal_description')
    time_of_day = data.get('time_of_day')
    time_zone = data.get('time_zone')
    contact_choice = data.get('contact_choice')    
    
    if not user_id or not report_frequency or not goal_title or not goal_description or not time_of_day or not time_zone or not contact_choice:
        return jsonify(message="Invalid user Data"), 400
    
    if not validate_timezone(time_zone):
        return jsonify(message="Invalid timezone"), 400

    try:
        conn = database_initializer.get_database_connection()
        cursor = conn.cursor()
        
        # Check if the goal with the same details exists in the database
        check_query = """
            SELECT id
            FROM goals
            WHERE user_id = %s AND goal_title = %s AND goal_description = %s
                AND time_of_day = %s AND time_zone = %s AND contact_choice = %s AND report_frequency = %s
        """
        
        cursor.execute(check_query, (user_id, goal_title, goal_description, time_of_day, time_zone, contact_choice, report_frequency))
        existing_goal = cursor.fetchone()
        
        if existing_goal:
            return jsonify(message="This goal already exists in the database"), 400

        insert_query = """
            INSERT INTO goals (user_id, goal_title, goal_description, time_of_day, time_zone, contact_choice, report_frequency)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """

        cursor.execute(insert_query, (user_id, goal_title, goal_description, time_of_day, time_zone, contact_choice, report_frequency))
        conn.commit()

        # Find the last inserted goal's ID
        cursor.execute("SELECT lastval()")
        goal_id = cursor.fetchone()[0]

        # Schedule the cron job
        goal_data = {
            "user_id": user_id,
            "goal_id": goal_id,  # Get the ID of the inserted goal
            "timezone": time_zone,  # Use the user's provided timezone
            "scheduled_time": {
                "hour": int(time_of_day.split(':')[0]),  # Extract hour from time_of_day
                "minute": int(time_of_day.split(':')[1])  # Extract minute from time_of_day
            },
            "report_frequency": report_frequency
        }

        # Create an instance of the Scheduler class for goals
        goal_scheduler = GoalScheduler()
        # Schedule the goal cron job using the Scheduler
        response = goal_scheduler.schedule_task_cron(goal_data)
        # Check the response (you may want to handle this differently)
        print(response)

        # Create an instance of the Scheduler class for reports
        report_scheduler = ReportScheduler()

        # Schedule a report using the Scheduler
        response = report_scheduler.schedule_task_cron(goal_data)

        # Check the response
        print(response)

        cursor.close()
        conn.close()

        return jsonify(message='Goal submitted successfully'), 200
    
    except psycopg2.Error as e:
        # Log the error for debugging
        print(e)
        return jsonify(message='Error adding goal'), 500

#edit goal
@app.route('/api/edit_goal', methods=['POST'])
@login_required
def edit_goal():
    data = request.get_json().get('goal_data')  
    user_id = current_user.id    
    goal_id = data.get('id')
    goal_title = data.get('goal_title')
    goal_description = data.get('goal_description')
    time_of_day = data.get('time_of_day')
    time_zone = data.get('time_zone')
    contact_choice = data.get('contact_choice')  
    report_frequency = data.get('report_frequency')  
    
    if not user_id or not goal_id or not report_frequency or not goal_title or not goal_description or not time_of_day or not time_zone or not contact_choice:
        return jsonify(message="Invalid user data"), 400
    
    if not validate_timezone(time_zone):
        return jsonify(message="Invalid timezone"), 400
    
    try:
        conn = database_initializer.get_database_connection()
        cursor = conn.cursor()
        
        # Check if the goal with the same details exists in the database
        check_query = """
            SELECT id
            FROM goals
            WHERE user_id = %s AND goal_title = %s AND goal_description = %s
                AND time_of_day = %s AND time_zone = %s AND contact_choice = %s AND report_frequency = %s
        """
        
        cursor.execute(check_query, (user_id, goal_title, goal_description, time_of_day, time_zone, contact_choice, report_frequency))
        existing_goal = cursor.fetchone()
        
        if existing_goal:
            return jsonify(message="This goal already exists in the database"), 400

        update_query = """
            UPDATE goals
            SET goal_title = %s, goal_description = %s, time_of_day = %s, time_zone = %s, contact_choice = %s, report_frequency = %s
            WHERE user_id = %s AND id = %s
        """

        cursor.execute(update_query, (goal_title, goal_description, time_of_day, time_zone, contact_choice, report_frequency, user_id, goal_id))
        conn.commit()

        
        cursor.close()
        conn.close()

        # Schedule the cron job
        goal_data = {
            "user_id": user_id,
            "goal_id": goal_id,  # Get the ID of the inserted goal
            "timezone": time_zone,  # Use the user's provided timezone
            "scheduled_time": {
                "hour": int(time_of_day.split(':')[0]),  # Extract hour from time_of_day
                "minute": int(time_of_day.split(':')[1])  # Extract minute from time_of_day
            },
            "report_frequency": report_frequency
        }

        # Create an instance of the Scheduler class for goals
        goal_scheduler = GoalScheduler()
        # Schedule the goal cron job using the Scheduler
        response = goal_scheduler.schedule_task_cron(goal_data)
        # Check the response (you may want to handle this differently)
        print(response)

        # Create an instance of the Scheduler class for reports
        report_scheduler = ReportScheduler()

        # Schedule a report using the Scheduler
        response = report_scheduler.schedule_task_cron(goal_data)

        # Check the response
        print(response)

        return jsonify(message="Goal time updated successfully"), 200
    
    except psycopg2.Error as e:
        # Log the error for debugging
        print(e)
        return jsonify(message="Error editing goal"), 500
    
# Delete a goal
@app.route('/api/delete_goal', methods=['POST'])
@login_required
def delete_goal():
    data = request.get_json()
    goal_id = data.get('id')

    if not isinstance(goal_id, int) or goal_id <= 0:
        return jsonify(message="Invalid goal ID"), 400
    
    try:
        conn = database_initializer.get_database_connection()
        cursor = conn.cursor()

        # Get the goal
        cursor.execute("SELECT id, user_id FROM goals WHERE id = %s;", (goal_id,))
        user_goal = cursor.fetchone()
       

        # Create an instance of CronJobManager
        cron_manager = CronJobManager(user=True)
        # Remove report cron job
        comment_report = f'{user_goal[1]}-{user_goal[0]}-report'
        cron_manager.remove_jobs_by_comment(comment_report)

        # Remove goal cron job
        comment_goal = f'{user_goal[1]}-{user_goal[0]}-goal'
        cron_manager.remove_jobs_by_comment(comment_goal)

        # Delete goal
        delete_query = """
            DELETE FROM goals
            WHERE id = %s
        """

        cursor.execute(delete_query, (goal_id,))
        conn.commit()

        cursor.close()
        conn.close()

        return jsonify(message="Goal deleted successfully"), 200
    
    except psycopg2.Error as e:
        # Log the error for debugging
        print(e)
        return jsonify(message="Failed to delete goal"), 500

#fetch goals
@app.route('/api/get_goals', methods=['GET'])
@login_required
def get_goals():
    user_id = current_user.id
    
    if user_id is None:
        return jsonify(message="User ID is required"), 400
    
    try:
        conn = database_initializer.get_database_connection()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        select_query = """
            SELECT id, user_id, goal_title, goal_description, time_of_day, time_zone, contact_choice, report_frequency
            FROM goals 
            WHERE user_id = %s
        """

        cursor.execute(select_query, (user_id,))
        goals = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        goals_dict_list = []
        for goal in goals:
            goal_dict = {
                "id": goal[0],
                "user_id" : goal[1],
                "goal_title": goal[2],
                "goal_description": goal[3],
                "time_of_day": serialize_time_to_str(goal[4]),
                "time_zone": goal[5],
                "contact_choice": goal[6],
                "report_frequency": goal[7]
            }
            goals_dict_list.append(goal_dict)
        
        return jsonify(goals_dict_list), 200
    
    except psycopg2.Error as e:
        # Log the error for debugging
        print(e)
        return jsonify(message="Failed to fetch goals"), 500
    



@app.route('/api/get_user', methods=['GET'])
@login_required
def get_user():
    
    user_id = current_user.id

    if not isinstance(user_id, int) or user_id <= 0:
        return jsonify(message="Invalid user id")
    
    try:
        conn = database_initializer.get_database_connection()
        cursor = conn.cursor()

        user_query = """
            SELECT id, email, phone_number
            FROM users
            WHERE id = %(user_id)s
        """

        cursor.execute(user_query, {"user_id": user_id})
        user = cursor.fetchone()

        cursor.close()
        conn.close()       

        if user:
            user_data = {
                "id": user[0],
                "email": user[1],
                "phone_number": user[2]
            }
            return jsonify(user_data), 200
        else:
            return jsonify(message="User not found")
    
    except psycopg2.Error as e:
        # Log the error for debugging
        print(e)
        return jsonify(message="Failed to fetch user"), 500



@app.route('/api/get_users', methods=['GET'])
def get_users():
    
    try:
        conn = database_initializer.get_database_connection()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        select_query = """
            SELECT id, email, phone_number
            FROM users 
        """

        cursor.execute(select_query)
        users = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        users_list = []
        for user in users:
            user_dict = {
                "id": user['id'],
                "email": user['email'],
                "phone_number": user['phone_number']
            }
            users_list.append(user_dict)
        
        return jsonify(users_list), 200
    
    except psycopg2.Error as e:
        # Log the error for debugging
        print(e)
        return jsonify(message="Failed to fetch users"), 500


@app.route('/api/edit_user', methods=['POST'])
@login_required
def edit_user():
    data = request.get_json().get('user')

    id = current_user.id
    email = data.get('email')
    phone_number = data.get('phone')
    name = data.get('name')    
    
    if not id or not email or not phone_number or not name:
        return jsonify(message="Invalid User data"), 400    
    
    
    try:
        conn = database_initializer.get_database_connection()
        cursor = conn.cursor()
        
        #check if the new key exists in the database
        check_query = """
            SELECT id
            FROM users
            WHERE email = %s AND id != %s
        """
        
        cursor.execute(check_query, (email, id))
        existing_key = cursor.fetchone()
        
        if existing_key:
            return jsonify(message="These details already exist in the database")

        update_query = """
            UPDATE users
            SET email = %s, phone_number = %s, name = %s
            WHERE id = %s
        """

        cursor.execute(update_query, (email, phone_number, name, id,))
        conn.commit()

        cursor.close()
        conn.close()

        return jsonify(message="User time updated successfully"), 200
    
    except psycopg2.Error as e:
        # Log the error for debugging
        print(e)
        return jsonify(message="Error editing user"), 500
        # For Testing only
        #return jsonify({"message" : str(e)}), 500
    
    

@app.route('/api/delete_user', methods=['POST'])
@login_required
def delete_user():

    user_id = request.get_json().get('id')
    
    if not user_id:
        return jsonify(message="Invalid user ID"), 400
    
    try:
        conn = database_initializer.get_database_connection()
        cursor = conn.cursor()

        # Create a thread to run the deletion process
        #delete_thread = threading.Thread(target=lambda: CronJobManager(user=True).remove_jobs_by_user_id(f"{user_id}-"))
        #delete_thread.start()

        delete_query = """
            DELETE FROM users
            WHERE id = %s
        """

        cursor.execute(delete_query, (user_id,))
        conn.commit()

        cursor.close()
        conn.close()

        return jsonify(message="User deleted successfully"), 200
    
    except psycopg2.Error as e:
        # Log the error for debugging
        print(e)
        return jsonify(message="Failed to delete user"), 500
    
  
#receiving and sending message to the database
@app.route('/api/store_feedback', methods=['POST'])
def store_user_feedback():
    try:
        # Goal data
        goal_data = request.json
        store_goal_data = StoreGoalData(database_initializer=database_initializer)
       
        response = store_goal_data.store_user_goal_data(goal_data['message'], goal_data['goal_id'], goal_data['user_id'])

        return response
    
    except Exception as e:
         # Handle any exceptions that may occur and return as JSON
        return jsonify({'error': str(e)}), 500


# Start the Flask application in debug mode if executed as the main script
if __name__ == '__main__':
    app.run(debug=True)
