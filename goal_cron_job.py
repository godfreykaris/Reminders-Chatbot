#!/usr/bin/python3

import json
import os
import sys
import logging
import requests
from modules.chatbot.chatgpt_response import ChatGPTResponse

from modules.database_initializer import DatabaseInitializer
from modules.goals.goal_retriever import UserGoal
from modules.goals.user_retriever import UserHandler
from modules.messaging.send_message import MessageSender

def get_credentials(filename):
        # Determine the absolute path to the script's directory
        script_dir = os.path.dirname(os.path.realpath(__file__))

        # Define the absolute path to the config.json file based on the parent directory
        config_file_path = os.path.join(script_dir, filename)

        dir_path = os.path.dirname(os.path.realpath(__file__))
        filename = os.path.join(dir_path, 'cron_script.log')
        logging.basicConfig(filename=filename, level=logging.INFO)
        try:
            with open(config_file_path, "r") as config_file:
                logging.error("Credentials file found: " + config_file_path)
                config = json.load(config_file)
            return config
        except FileNotFoundError:
            logging.error("Credentials file not found: " + config_file_path)
            raise
        except json.JSONDecodeError as e:
            logging.error(f"Error decoding JSON from credentials file: {str(e)}")
            raise

class GoalReminderCron:
    def __init__(self, database_initializer):
        self.database_initializer = database_initializer

    def retrieve_user(self, user_id):

        user_handler = UserHandler(self.database_initializer)
        result = user_handler.get_user(user_id=user_id)

        # Parse the JSON string into a Python dictionary
        result = json.loads(result)

        return result.get('user_info')
    

    def retrieve_goal(self, user_id, goal_id):
           
        user_goal = UserGoal(self.database_initializer)
        result = user_goal.get_user_goal(user_id=user_id, goal_id=goal_id)    
        # Parse the JSON string into a Python dictionary
        result = json.loads(result)

        return result.get('goal_data')

    def generate_message(self, goal_data):
        
        template_message = f"Did you do your {goal_data['title']}?"

        # Initialize ChatGPTResponse with credentials
        credentials = get_credentials('config.json');
        chatgpt = ChatGPTResponse(credentials_file_path='', credentials=credentials)

        # Generate a response using ChatGPT
        prompt_message = f"Rephrase this question:{template_message}"
        response_max_tokens=30
        response = chatgpt.generate_user_message(prompt_message=prompt_message, response_max_tokens=response_max_tokens)

        # Parse the JSON string into a Python dictionary
        result = json.loads(response)

        return result.get('user_message')

    def send_message(self, user, message, goal, contact_choice):
        
        recipient = user['phone']
        message = message + "\nGoal: " + goal
        message_type = contact_choice.lower()

        # Create an instance of MessageSender
        message_sender = MessageSender()
        # Call the send_message method to handle message sending
        credentials = get_credentials('config.json');
        response = message_sender.send_message(recipient=recipient, message=message, message_type=message_type, credentials=credentials)

        return response



def main(args):
    
    user_id = args[2]
    goal_id = args[4]

    dir_path = os.path.dirname(os.path.realpath(__file__))
    filename = os.path.join(dir_path, 'cron_script.log')

    logging.basicConfig(filename=filename, level=logging.INFO)
    try:
        credentials = get_credentials('config.json');
        database_initializer = DatabaseInitializer(credentials_file_path='', credentials=credentials)
        
        goal_reminder_cron = GoalReminderCron(database_initializer=database_initializer)
        
        user = goal_reminder_cron.retrieve_user(user_id)
        goal_data = goal_reminder_cron.retrieve_goal(user_id, goal_id)
        generated_message = goal_reminder_cron.generate_message(goal_data)
        response = goal_reminder_cron.send_message(user, generated_message,goal_data['title'], goal_data['contact_choice'])
    
        logging.info('Script executed successfully. User ID:' + user_id + response)
    except Exception as e:
        logging.error(f'Script encountered an error: {str(e)} + User ID: + {user_id}')  

if __name__ == '__main__':
    main(sys.argv)
