# Import the necessary Flask modules
import logging
from flask import Flask, jsonify, request
import pytz
import requests

import threading


from twilio.twiml.messaging_response import MessagingResponse


from modules.chatbot.chatgpt_reponse import ChatGPTResponse

# Import custom modules for database initialization, user registration, login, messaging, and goal scheduling
from modules.database_initializer import DatabaseInitializer
from modules.goals.goal_data_retriever import UserGoalData
from modules.goals.goal_data_store import StoreGoalData
from modules.goals.goal_retriever import UserGoal
from modules.goals.cron_manager import CronJobManager
from modules.goals.user_retriever import UserHandler
from modules.messaging.send_message import MessageSender
from modules.register_user import UserRegistration
from modules.login import UserLogin
from modules.goals.scheduler import GoalScheduler, ReportScheduler

import psycopg2.extras
from datetime import time

from report_cron_job import ReportGenerator


# Create a Flask application
app = Flask(__name__)

# Initialize the database connection using the configuration from 'config.json'
database_initializer = DatabaseInitializer('config.json')

# Define a route for user registration
@app.route('/api/register', methods=['POST'])
def register():
    # Create an instance of UserRegistration with the database connection
    user_registrar = UserRegistration(database_initializer=database_initializer)
    # Call the register_user method to handle user registration
    user_registrar.register_user()

# Define a route for user login
@app.route('/api/login', methods=['POST'])
def login():
    # Create an instance of UserLogin with the database connection
    user_authenticator = UserLogin(database_initializer=database_initializer)
    # Call the login_user method to handle user login
    user_authenticator.login_user()

# Define a route to a user
@app.route('/api/user/retrieve_user', methods=['POST'])
def retrieve_user():
    try:
        user_handler = UserHandler(database_initializer)
        return user_handler.get_user()

    except Exception as e:
         # Handle any exceptions that may occur and return as JSON
        return jsonify({'error': str(e)}), 500

# Define a route for sending user messages
@app.route('/api/send_message', methods=['POST'])
def send_user_message():
    # Create an instance of MessageSender
    message_sender = MessageSender()
    # Call the send_message method to handle message sending
    response = message_sender.send_message()

    return response

# Define a route for getting user messages
@app.route('/webhook', methods=['POST'])
def webhook():
    # Get the incoming message from Twilio
    incoming_message = request.form['Body'].lower()
    from_phone_parts = request.form.get('From', '').strip().split(':')
    from_phone = from_phone_parts[1]
    # Handle incoming messages
    user_message_response = MessagingResponse()


    # Validate message format
    parts = incoming_message.split('=')
    
    # Check if there are exactly two parts
    if len(parts) == 2:
        goal = parts[0]
        report = parts[1]
    else:
        # Tell the user to use the correct format
        user_message_response.message("Your message should be as follows: \nGoal = Report. \nExample: Yoga = Yes i did my yoga")
        return str(user_message_response)

    if not report or not goal or report.isspace() or report == "":
        # Tell the user to use the correct format
        user_message_response.message("Your message should be as follows: \nGoal = Report. \nExample: Yoga = Yes i did my yoga")
        return str(user_message_response)
    
    # Retrieve a user by the phone number
    user_retriever = UserHandler(database_initializer=database_initializer);
    response = user_retriever.get_user_by_phone(from_phone)

    response_data = response.json
    status_code = response_data.get('status', None)

    # Check the response
    if status_code == 200:
        # Successful response
        user_data = response.json['user_info']
    else:
        user_message_response.message("We are experiencing a problem retrieving your details. \nPlease contact suport.")
        return str(user_message_response)
    
    # Retrieve the user goals
    goals_retriever = UserGoal(database_initializer=database_initializer)
    response = goals_retriever.get_user_goals(user_data['id'])

    response_data = response.json
    status_code = response_data.get('status', None)

    print(response_data)
    # Check the response
    if status_code == 200:
        # Successful response
        goals_data = response.json['goals_titles']
    else:
        user_message_response.message("We are experiencing a problem retrieving your details. \nPlease contact suport.")
        return str(user_message_response)
    

    # Check if the goal provided by the user is valid
    goal_matched = goals_retriever.find_matching_goal(goal, goals_data)

    if not goal_matched:
       # Inform the user that the goal is invalid
       user_message_response.message(f"The goal: '{goal}' does not exist in your goals. \nCorrect format: Goal = Report. \nExample: Yoga = Yes i did my yoga")
       return str(user_message_response)

    # Store the data
    goal_id = goal_matched['id']

    # Define the goal data
    goal_data = {
        "user_id": user_data['id'],  # Replace with the actual user ID
        "goal_id": goal_id, 
        "message": report, 
    }

    store_goal_data = StoreGoalData(database_initializer=database_initializer)
    store_data_url = "http://localhost:5000/api/store_feedback"

    data_thread = threading.Thread(target=store_goal_data.store_user_data_request, args=(store_data_url, goal_data, ))
    
    # Generate a response from ChatGPT
    chatgpt_url = "http://localhost:5000/api/chat/chat_with_user"
   
    # JSON payload
    chatgpt_payload = {"user_input": "Goal:" + goal + ", Report:" + report}

    try:
        # Send a POST request to your chat_with_user API
        chatgpt_response = requests.post(chatgpt_url, json=chatgpt_payload)
        
        if chatgpt_response.status_code == 200:
            # If the request to the chat_with_user API was successful, get the bot's response
            chatgpt_data = chatgpt_response.json()
            bot_message = chatgpt_data.get('bot_response')

            # Send the bot's response back to the user via Twilio
            user_message_response.message(bot_message)
        else:
            # Handle any errors that may occur during the API request
            user_message_response.message("An error occurred while processing your request.")
    
    except Exception as e:
        # Handle exceptions that may occur during the API request
        user_message_response.message("An error occurred while processing your request.")
    
    # Start the thread
    data_thread.start()

    return str(user_message_response)
    
# Define a route for scheduling user goals
@app.route('/api/schedule_goal', methods=['POST'])
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
        user_goal = UserGoal(database_initializer)
        return user_goal.get_user_goal()

    except Exception as e:
         # Handle any exceptions that may occur and return as JSON
        return jsonify({'error': str(e)}), 500
    

# Define a route to retrieve  goal data
@app.route('/api/user/retrieve_goal_data', methods=['POST'])
def retrieve_user_goal_data():
    try:
        user_goal_data = UserGoalData(database_initializer)
        return user_goal_data.get_user_goal_data()

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
@app.route('/api/get_report/<int:id>/<int:user_id>', methods=['GET'])
def get_report(id, user_id):
    try:

        if not user_id or not id:
            return jsonify(message="Invalid user or goal id"), 400

        report_generator = ReportGenerator()
        # Retrieve user information
        user = report_generator.retrieve_user(user_id)

        # Retrieve goal information
        goal = report_generator.retrieve_goal(user_id, id)

        # Retrieve goal data entries
        goal_data = report_generator.retrieve_goal_data(user_id, id)

        # Generate the report
        report = report_generator.generate_report(user, goal, goal_data)


        # Now you have the report as a string, and you can do whatever you want with it
        print(report)

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
def add_goal():
    
    data = request.get_json()
    user_id = data.get('user_id')
    report_frequency = data.get('report_frequency')
    goal_title = data.get('goal_title')
    goal_description = data.get('goal_description')
    time_of_day = data.get('time_of_day')
    time_zone = data.get('time_zone')
    contact_choice = data.get('contact_choice')    
    
    if not isinstance(user_id, int) or user_id <= 0:
        return jsonify(message="Invalid user ID"), 400
    
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
def edit_goal():
    data = request.get_json()
    user_id = data.get('user_id')
    goal_id = data.get('id')
    goal_title = data.get('goal_title')
    goal_description = data.get('goal_description')
    time_of_day = data.get('time_of_day')
    time_zone = data.get('time_zone')
    contact_choice = data.get('contact_choice')  
    report_frequency = data.get('report_frequency')  
    
    if not isinstance(goal_id, int) or goal_id <= 0:
        return jsonify(message="Invalid goal ID"), 400
    
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
       

        # Create an ins
        # tance of CronJobManager
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
def get_goals():
    user_id = 6
    
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
    



@app.route('/api/get_user/<int:user_id>', methods=['GET'])
def get_user(user_id):
        
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
def edit_user():
    data = request.get_json()
    
    id = data.get('id')
    email = data.get('email')
    phone_number = data.get('phone_number')    
    
    if not isinstance(id, int) or id <= 0:
        return jsonify(message="Invalid user ID"), 400    
    
    
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
            SET email = %s, phone_number = %s
            WHERE id = %s
        """

        cursor.execute(update_query, (email, phone_number, id,))
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
def delete_user():
    data = request.get_json()
    user_id = data.get('id')
    
    if not isinstance(user_id, int) or user_id <= 0:
        return jsonify(message="Invalid goal ID"), 400
    
    try:
        conn = database_initializer.get_database_connection()
        cursor = conn.cursor()

        # Create a thread to run the deletion process
        delete_thread = threading.Thread(target=lambda: CronJobManager(user=True).remove_jobs_by_user_id(f"{user_id}-"))
        delete_thread.start()

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

