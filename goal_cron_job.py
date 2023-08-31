#!/usr/bin/python3

import os
import sys
import logging
import requests

class GoalReminderCron:
    def __init__(self):
        self.base_url = "http://localhost:5000"

    def retrieve_user(self, user_id):
        url = f"{self.base_url}/api/user/retrieve_user"
        data = {"user_id": user_id}
        response = requests.post(url, json=data)
        response.raise_for_status()
        return response.json().get('user_info')

    def retrieve_goal(self, user_id, goal_id):
        url = f"{self.base_url}/api/user/retrieve_goal"
        data = {"user_id": user_id, "goal_id": goal_id}
        response = requests.post(url, json=data)
        response.raise_for_status()
        return response.json().get('goal_data')

    def generate_message(self, goal_data):
        url = f"{self.base_url}/api/chat/generate_message"
        template_message = f"Did you do your {goal_data['title']}?"
        payload = {"template_message": template_message}
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json().get('user_message')

    def send_message(self, user, message, goal, contact_choice):
        url = f"{self.base_url}/api/send_message"
        data = {
            "recipient": user['phone'],
            "message": message + "\nGoal: " + goal,
            "type": contact_choice.lower()
        }
        response = requests.post(url, json=data)
        response.raise_for_status()
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
    goal_reminder_cron = GoalReminderCron()
    goal_reminder_cron.main(sys.argv)
