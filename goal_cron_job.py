#!/usr/bin/python3

import json
import os
import sys
import logging
import requests
from modules.chatbot.chatgpt_reponse import ChatGPTResponse

from modules.database_initializer import DatabaseInitializer
from modules.goals.goal_retriever import UserGoal
from modules.goals.user_retriever import UserHandler
from modules.messaging.send_message import MessageSender

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
        # Initialize ChatGPTResponse with credentials file
        chatgpt = ChatGPTResponse('config.json')

        # Generate a response using ChatGPT
        prompt_message = f"Rephrase this question:{template_message}"
        response_max_tokens=30
        response = chatgpt.generate_user_message(prompt_message=prompt_message, response_max_tokens=response_max_tokens)

        # Parse the JSON string into a Python dictionary
        result = json.loads(response)

        return result.get('user_message')

    def send_message(self, user, message, goal, contact_choice):
        
        recipient = user['phone']
        message = message + "user['phone']\nGoal: " + goal
        message_type = contact_choice.lower()

        # Create an instance of MessageSender
        message_sender = MessageSender()
        # Call the send_message method to handle message sending
        response = message_sender.send_message(recipient=recipient, message=message, message_type=message_type)

        return response

    def main(self, args):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        filename = os.path.join(dir_path, 'cron_script.log')
        logging.basicConfig(filename=filename, level=logging.INFO)

        try:
            user_id = args[2]
            goal_id = args[4]

            user = self.retrieve_user(user_id)
            goal_data = self.retrieve_goal(user_id, goal_id)
            generated_message = self.generate_message(goal_data)

            response = self.send_message(user, generated_message,goal_data['title'], goal_data['contact_choice'])
            print(response.status_code)
            print(response.json())
            print(goal_data['contact_choice'].lower())

            logging.info('Script executed successfully. User ID:' + user_id)
        except Exception as e:
            logging.error(f'Script encountered an error: {str(e)} + User ID: + {user_id}')

if __name__ == '__main__':
    # Initialize the database connection using the configuration from 'config.json'
    database_initializer = DatabaseInitializer('config.json')

    goal_reminder_cron = GoalReminderCron(database_initializer=database_initializer)
    goal_reminder_cron.main(sys.argv)
