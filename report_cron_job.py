import json
import os
import logging
import sys
from modules.chatbot.chatgpt_reponse import ChatGPTResponse
from modules.database_initializer import DatabaseInitializer
from modules.goals.goal_data_retriever import UserGoalData

from modules.goals.goal_retriever import UserGoal
from modules.goals.user_retriever import UserHandler
from modules.messaging.send_message import MessageSender

class ReportGenerator:
    def __init__(self, database_initializer):
        self.database_initializer = database_initializer
        
    def generate_report_and_send(self, user_id, goal_id):
        try:
            # Retrieve user information
            user = self.retrieve_user(user_id)

            # Retrieve goal information
            goal = self.retrieve_goal(user_id, goal_id)

            # Retrieve goal data entries
            goal_data = self.retrieve_goal_data(user_id, goal_id)

            # Generate the report
            report = self.generate_report(user, goal, goal_data)

            # Send the report
            self.send_report(user, report, goal['contact_choice'].lower())

            logging.info(f'Script executed successfully for user {user_id}')
        except Exception as e:
            logging.error(f'Script encountered an error: {str(e)} for user {user_id}')

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

    def retrieve_goal_data(self, user_id, goal_id):
       
        user_goal_data = UserGoalData(self.database_initializer)
        result = user_goal_data.get_user_goal_data(user_id=user_id, goal_id=goal_id)

        # Parse the JSON string into a Python dictionary
        result = json.loads(result)

        if result.get('status') == 404:
            return []
        
        return result.get('goal_data_entries')

    def generate_report(self, user, goal, goal_data):

        user_data = {           
            "name": user['name'],
            "goal": goal,
            "data": goal_data
        }
        
        # Initialize ChatGPTResponse with credentials file
        chatgpt = ChatGPTResponse('config.json')

        # Generate a response using ChatGPT
        prompt_message = f"Analyze the following user data for {user_data['name']}. Summarize the data and address the user about your analysis. Make sure you give recommendations and guidance to the user. Address the user as 'You'. Strictly use 120 to 150 words: {user_data}"
        response_max_tokens=256
        response = chatgpt.generate_analysis_report(prompt_message=prompt_message, response_max_tokens=response_max_tokens)

        # Parse the JSON string into a Python dictionary
        result = json.loads(response)       
        
        return result.get('bot_response')        

    def send_report(self, user, report, message_type):
        
        recipient = user['phone']        

        # Create an instance of MessageSender
        message_sender = MessageSender()
        # Call the send_message method to handle message sending
        response = message_sender.send_message(recipient=recipient, message=report, message_type=message_type)

        return response

def main(args):
    
    user_id = args[2]
    goal_id = args[4]

    # Initialize the database connection using the configuration from 'config.json'
    database_initializer = DatabaseInitializer('config.json')

    report_generator = ReportGenerator(database_initializer=database_initializer)
    report_generator.generate_report_and_send(user_id, goal_id)

if __name__ == '__main__':
    main(sys.argv)
