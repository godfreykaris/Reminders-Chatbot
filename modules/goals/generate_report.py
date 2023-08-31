import os
import logging
import requests
import sys

class ReportGenerator:
    def __init__(self):
        self.base_url = "http://localhost:5000"  # Update with your Flask application's base URL

    def generate_report_and_send(self, user_id, goal_id, report_type):
        try:
            # Retrieve user information
            user = self.retrieve_user(user_id)

            # Retrieve goal information
            goal = self.retrieve_goal(user_id, goal_id)

            # Retrieve goal data entries
            goal_data = self.retrieve_goal_data(user_id, goal_id)

            # Generate the report
            report = self.generate_report(user, goal, goal_data, report_type)

            # Send the report
            self.send_report(user, report, goal['contact_choice'].lower())

            logging.info(f'Script executed successfully for user {user_id}')
        except Exception as e:
            logging.error(f'Script encountered an error: {str(e)} for user {user_id}')

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

    def retrieve_goal_data(self, user_id, goal_id):
        url = f"{self.base_url}/api/user/retrieve_goal_data"
        data = {"user_id": user_id, "goal_id": goal_id}
        response = requests.post(url, json=data)
        response.raise_for_status()
        return response.json().get('goal_data_entries')

    def generate_report(self, user, goal, goal_data, report_type):
        if report_type == 'message':
            url = f"{self.base_url}/api/chat/generate_message_report"
        else:
            url = f"{self.base_url}/api/chat/generate_pdf_report"

        request_data = {
            "user_data": {
                "name": user['name'],
                "goal": goal,
                "data": goal_data
            }
        }

        response = requests.post(url, json=request_data)
        response.raise_for_status()
        return response.json().get('bot_response')

    def send_report(self, user, report, message_type):
        url = f"{self.base_url}/api/send_message"
        data = {
            "recipient": user['phone'],
            "message": report,
            "type": message_type
        }

        response = requests.post(url, json=data)
        response.raise_for_status()
        logging.info(f"Message sent to {user['name']} ({user['phone']})")

def main(args):
    if len(args) < 7:
        print("Usage: python script.py <user_id> <goal_id> <report_type>")
        sys.exit(1)

    user_id = args[1]
    goal_id = args[2]
    report_type = args[3]

    report_generator = ReportGenerator()
    report_generator.generate_report_and_send(user_id, goal_id, report_type)

if __name__ == '__main__':
    main(sys.argv)
