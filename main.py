# Import the necessary Flask modules
from flask import Flask, jsonify, request
from flask_cors import CORS
import pytz
import requests

from twilio.twiml.messaging_response import MessagingResponse


from modules.chatbot.chatgpt_reponse import ChatGPTResponse

# Import custom modules for database initialization, user registration, login, messaging, and goal scheduling
from modules.database_initializer import DatabaseInitializer
from modules.goals.goal_data_retriever import UserGoalData
from modules.goals.goal_retriever import UserGoal
from modules.goals.user_retriever import UserHandler
from modules.messaging.send_message import MessageSender
from modules.register_user import UserRegistration
from modules.login import UserLogin
from modules.goals.scheduler import GoalScheduler, ReportScheduler

import psycopg2.extras
from datetime import time


# Create a Flask application
app = Flask(__name__)

# Enable Cross-Origin Resource Sharing (CORS) to allow requests from different origins
CORS(app)

# Initialize the database connection using the configuration from 'config.json'
database_initializer = DatabaseInitializer('config.json')

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
        #return jsonify({'error': "An error occurred. Please contact support"}), 500

        return jsonify({'error': str(e)}), 500   # For testing only
    
# Define a route for user login
@app.route('/api/login', methods=['POST'])
def login():
    try:
        # Create an instance of UserLogin with the database connection
        user_authenticator = UserLogin(database_initializer=database_initializer)
        # Call the login_user method to handle user login
        return user_authenticator.login_user()
    except Exception as e:
         # Handle any exceptions that may occur and return as JSON
        #return jsonify({'error': "An error occurred. Please contact support"}), 500

        return jsonify({'error': str(e)}), 500 # For testing only
# Define a route to a user
@app.route('/api/user/retrieve_user', methods=['POST'])
def retrieve_user():
    try:
        user_handler = UserHandler(database_initializer)
        return user_handler.get_user()

    except Exception as e:
         # Handle any exceptions that may occur and return as JSON
        #return jsonify({'error': "An error occurred. Please contact support"}), 500

        return jsonify({'error': str(e)}), 500 # For testing only

# Define a route for sending user messages
@app.route('/api/send_message', methods=['POST'])
def send_user_message():
    try:
        # Create an instance of MessageSender
        message_sender = MessageSender()
        # Call the send_message method to handle message sending
        response = message_sender.send_message()

        return response
    except Exception as e:
         # Handle any exceptions that may occur and return as JSON
        #return jsonify({'error': "An error occurred. Please contact support"}), 500

        return jsonify({'error': str(e)}), 500 # For testing only

# Define a route for getting user messages
@app.route('/webhook', methods=['POST'])
def webhook():
    
    try:
        # Get the incoming message from Twilio
        incoming_message = request.values.get('Body', '').lower()

        # Handle incoming messages
        response = MessagingResponse()

        # Generate a response from ChatGPT
        chatgpt_url = "http://localhost:5000/api/chat/chat_with_user"
    
        # JSON payload
        chatgpt_payload = {"user_input": incoming_message}

        # Send a POST request to your chat_with_user API
        chatgpt_response = requests.post(chatgpt_url, json=chatgpt_payload)
        
        if chatgpt_response.status_code == 200:
            # If the request to the chat_with_user API was successful, get the bot's response
            chatgpt_data = chatgpt_response.json()
            bot_message = chatgpt_data.get('bot_response')

            # Send the bot's response back to the user via Twilio
            response.message(bot_message)
        else:
            # Handle any errors that may occur during the API request
            response.message("An error occurred while processing your request.")
    
    except Exception as e:
        # Handle exceptions that may occur during the API request
        response.message("An error occurred while processing your request.")
    
    return str(response)
    
# Define a route for scheduling user goals
@app.route('/api/schedule_goal', methods=['POST'])
def schedule_user_goal():
    try:
        # Create an instance of GoalScheduler with the username of the os given by 'whoami' command
        scheduler = GoalScheduler('godfreykaris')
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
        scheduler = ReportScheduler('godfreykaris')
        # Schedule a goal using the ReportScheduler
        response = scheduler.schedule_task_cron()


        return response
    except Exception as e:
        # Handle any exceptions that may occur and return as JSON
        #return jsonify({'error': "An error occurred. Please contact support"}), 500

        return jsonify({'error': str(e)}), 500 # For testing only

# Define a route for getting an anylysis report for user data from ChatGPT
@app.route('/api/chat/generate_report', methods=['POST'])
def get_chatgpt_analysis_report():
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
        #return jsonify({'error': "An error occurred. Please contact support"}), 500

        return jsonify({'error': str(e)}), 500 # For testing only

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
        #return jsonify({'error': "An error occurred. Please contact support"}), 500

        return jsonify({'error': str(e)}), 500 # For testing only

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
        response_max_tokens = 50  # Adjust max_tokens as needed
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
        #return jsonify({'error': "An error occurred. Please contact support"}), 500

        return jsonify({'error': str(e)}), 500 # For testing only
    

# Define a route to retrieve  goal data
@app.route('/api/user/retrieve_goal_data', methods=['POST'])
def retrieve_user_goal_data():
    try:
        user_goal_data = UserGoalData(database_initializer)
        return user_goal_data.get_user_goal_data()

    except Exception as e:
         # Handle any exceptions that may occur and return as JSON
        #return jsonify({'error': "An error occurred. Please contact support"}), 500

        return jsonify({'error': str(e)}), 500 # For testing only


#serialize the data fetched from the database that isnt json serializable
def serialize_time_to_str(time_obj):
    if isinstance(time_obj, time):
        return time_obj.strftime("%H:%M:%S")
    return time_obj

#get timezones
@app.route('/get_timezones', methods=['GET'])
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

# Delete a goal
@app.route('/delete_goal', methods=['POST'])
def delete_goal():
    data = request.get_json()
    goal_id = data.get('id')
    
    if not isinstance(goal_id, int) or goal_id <= 0:
        return jsonify(message="Invalid goal ID"), 400
    
    try:
        conn = database_initializer.get_database_connection()
        cursor = conn.cursor()

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

@app.route('/get_user/<int:user_id>', methods=['GET'])
def get_user(user_id):
        
    if not isinstance(user_id, int) or user_id <= 0:
        return jsonify(message="Invalid user id")
    
    try:
        conn = database_initializer.get_database_connection()
        cursor = conn.cursor()

        user_query = """
            SELECT id, email, phone_number, name
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
                "phone_number": user[2],
                "name": user[3]
            }
            return jsonify(user_data), 200
        else:
            return jsonify(message="User not found")
    
    except psycopg2.Error as e:
        # Log the error for debugging
        print(e)
        return jsonify(message="Failed to fetch user"), 500



@app.route('/get_users', methods=['GET'])
def get_users():
    
    try:
        conn = database_initializer.get_database_connection()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        select_query = """
            SELECT id, email, phone_number, name
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
                "phone_number": user['phone_number'],
                "name": user['name']
            }
            users_list.append(user_dict)
        
        return jsonify(users_list), 200
    
    except psycopg2.Error as e:
        # Log the error for debugging
        print(e)
        return jsonify(message="Failed to fetch users"), 500


@app.route('/edit_user', methods=['POST'])
def edit_user():
    data = request.get_json()
    
    id = data.get('id')
    email = data.get('email')
    phone_number = data.get('phone_number')
    name = data.get('name')    
    
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

@app.route('/delete_user', methods=['POST'])
def delete_user():
    data = request.get_json()
    user_id = data.get('id')
    
    if not isinstance(user_id, int) or user_id <= 0:
        return jsonify(message="Invalid goal ID"), 400
    
    try:
        conn = database_initializer.get_database_connection()
        cursor = conn.cursor()

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
    
 #add goal
@app.route('/add_goal', methods=['POST'])
def add_goal():
    user_id = 6
    data = request.get_json()
    report_frequncy = data.get('report_frequency')
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
        
        cursor.execute(check_query, (user_id, goal_title, goal_description, time_of_day, time_zone, contact_choice, report_frequncy))
        existing_goal = cursor.fetchone()
        
        if existing_goal:
            return jsonify(message="This goal already exists in the database"), 400

        insert_query = """
            INSERT INTO goals (user_id, goal_title, goal_description, time_of_day, time_zone, contact_choice, report_frequency)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """

        cursor.execute(insert_query, (user_id, goal_title, goal_description, time_of_day, time_zone, contact_choice, report_frequncy))
        conn.commit()

        cursor.close()
        conn.close()

        return jsonify(message='Goal submitted successfully'), 200
    
    except psycopg2.Error as e:
        # Log the error for debugging
        print(e)
        return jsonify(message='Error adding goal'), 500

@app.route('/edit_goal', methods=['POST'])
def edit_goal():
    user_id = 6
    data = request.get_json()
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

        return jsonify(message="Goal time updated successfully"), 200
    
    except psycopg2.Error as e:
        # Log the error for debugging
        print(e)
        return jsonify(message="Error editing goal"), 500


#validating message
def validate_message_content(message):
    if not message:
        return False
    return True  
   
#receiving and sending message to the database
@app.route('/receive_message', methods=['POST'])
def receive_message():
    
    MAX_MESSAGE_LENGTH = 100 
    
    data = request.get_json()
    
    phone_number = data.get('phone_number') 
    
    try:
        reason = data.get('reason')
        # sender_phone = request.form['From']
        # message_content = request.form['Body']
        
        conn = database_initializer.get_database_connection()
        cursor = conn.cursor()
        
        #find the user associated with the phone number
        user_query = """
            SELECT id
            FROM users
            WHERE phone_number = %s        
        """
        
        cursor.execute(user_query, (phone_number,))
        user_id_result = cursor.fetchone()
        
        #return jsonify({"message": str(user_id_result)})
        
        if user_id_result:
            user_id = user_id_result[0]
            
            #find goal id associated with the user id
            goal_query = """
                SELECT id
                FROM goals
                WHERE user_id = %s
            """
            
            cursor.execute(goal_query, (user_id,))
            goal_id_result = cursor.fetchone()
            
            if goal_id_result:
                goal_id = goal_id_result[0]
                
                #insert the message into the goal data table
                insert_query = """
                    INSERT INTO goal_data (goal_id, user_id, reason) VALUES (%s, %s, %s)
                """       

                if len(reason) <= MAX_MESSAGE_LENGTH and validate_message_content(reason):
                    cursor.execute(insert_query, (goal_id, user_id, reason))
                    conn.commit()
                    cursor.close()
                    conn.close()

                    return jsonify(message="Message received ond stored"), 200
                else:
                    conn.close()
                    return jsonify(message="Message has invalid format"), 400
            else:
                conn.close()
                #return jsonify({"message" : str(e)}), 500
                return jsonify({"message" : str(user_id)}), 400
        
        else:
            conn.close()
            return jsonify(message="User not found"), 404
    
    except psycopg2.Error as e:
        print(e)
        return jsonify(message="Error receiving message")      


#fetch goals
#fetch goals
@app.route('/get_goals', methods=['GET'])
def get_goals():
    user_id = 6
    
    if user_id is None:
        return jsonify(message="User ID is required"), 400
    
    try:
        conn = database_initializer.get_database_connection()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        select_query = """
            SELECT id, goal_title, goal_description, time_of_day, time_zone, contact_choice, report_frequency
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
                "goal_title": goal[1],
                "goal_description": goal[2],
                "time_of_day": serialize_time_to_str(goal[3]),
                "time_zone": goal[4],
                "contact_choice": goal[5],
                "report_frequency": goal[6]
            }
            goals_dict_list.append(goal_dict)
        
        return jsonify(goals_dict_list), 200
    
    except psycopg2.Error as e:
        # Log the error for debugging
        print(e)
        return jsonify(message="Failed to fetch goals"), 500
    

# Start the Flask application in debug mode if executed as the main script
if __name__ == '__main__':
    app.run(debug=True)

