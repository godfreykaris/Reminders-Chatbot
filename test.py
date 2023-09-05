

import requests
import json

from modules.goals.scheduler import GoalScheduler

# # URL of the API endpoint
# url = "http://localhost:5000/api/retrieve_goal_data"

# # Template message
# template_message = "Did you do your Yoga?"

# # JSON payload
# payload = {"template_message": template_message}

# # Send a POST request
# response = requests.post(url, json=payload)

# # Check if the request was successful (status code 200)
# if response.status_code == 200:
#     data = response.json()
#     generated_message = data.get('user_message')
#     print(f"Generated Message: {generated_message}")
# else:
#     print(f"Error: {response.status_code}, {response.json()}")

# # URL of the API endpoint
# url = "http://localhost:5000/api/chat/generate_message"

# # Template message
# template_message = "Did you do your Yoga?"

# # JSON payload
# payload = {"template_message": template_message}

# # Send a POST request
# response = requests.post(url, json=payload)

# # Check if the request was successful (status code 200)
# if response.status_code == 200:
#     data = response.json()
#     generated_message = data.get('user_message')
#     print(f"Generated Message: {generated_message}")
# else:
#     print(f"Error: {response.status_code}, {response.json()}")

# # URL of the API endpoint
# url = "http://localhost:5000/api/chat/chat_with_user"

# # Template message
# template_message = "Did you do your Yoga?"

# # JSON payload
# payload = {"user_input": template_message}

# # Send a POST request
# response = requests.post(url, json=payload)

# # Check if the request was successful (status code 200)
# if response.status_code == 200:
#     data = response.json()
#     generated_message = data.get('bot_response')
#     print(f"Generated Message: {generated_message}")
# else:
#     print(f"Error: {response.status_code}, {response.json()}")


# # Define the URL of your Flask application
# url = 'http://localhost:5000/api/chat/generate_message_report'

# # Sample user data for the "Yoga" goal
# user_data = {
#     "name": "John Doe",
#     "data": [
#         {
#             "date": "2023-08-15",
#             "time": "06:30 AM",
#             "feedback": "Executed the Yoga routine smoothly. Feeling refreshed afterward."
#         },
#         {
#             "date": "2023-08-16",
#             "time": "07:00 AM",
#             "feedback": "Yoga session went well, but felt a bit stiff in the morning."
#         },
#         {
#             "date": "2023-08-17",
#             "time": "06:45 AM",
#             "feedback": "Enjoyed the Yoga today. It's becoming a routine now."
#         },
#         {
#             "date": "2023-08-18",
#             "time": "06:15 AM",
#             "feedback": "Had some difficulty with a pose today, but managed to finish the session."
#         },
#         {
#             "date": "2023-08-19",
#             "time": "08:00 AM",
#             "feedback": "Morning Yoga practice helps me start the day with energy."
#         },
#         {
#             "date": "2023-08-20",
#             "time": "10:30 AM",
#             "feedback": "Tried a new Yoga routine today. It was challenging but rewarding."
#         },
#         {
#             "date": "2023-08-21",
#             "time": "05:45 AM",
#             "feedback": "Missed Yoga yesterday due to work, but back on track today."
#         },
#         {
#             "date": "2023-08-22",
#             "time": "07:15 AM",
#             "feedback": "Practiced Yoga by the beach. The view was inspiring."
#         }
#     ]
# }


# # Create a dictionary with the user data
# data = {
#     "user_data": user_data
# }

# # Send a POST request to your Flask application
# response = requests.post(url, json=data)

# # Check the response
# if response.status_code == 200:
#     # Successful response
#     result = response.json()
#     print(f"ChatGPT Response:{result['bot_response']}")
# else:
#     # Error response
#     print(f"Error: {response.status_code}")
#     print(response.json())


# import logging
# import requests

# import os

# dir_path = os.path.dirname(os.path.realpath(__file__))
# filename = os.path.join(dir_path, 'cron_script.log')

# logging.basicConfig(filename=filename, level=logging.INFO)

# try:
#     # Define the URL of your Flask application
#     url = "http://localhost:5000/api/send_message"  # Update the URL as needed  

#     # Define the data to be sent in the request's JSON body
#     data = {
#         "recipient": "+254759741544",  # Replace with the recipient's phone number
#         "message": "Hello, this is a test message from  reminders app",  # Replace with your message
#         "type": "whatsapp"  # Specify the message type (sms or whatsapp)
#     }   

#     # Send an HTTP POST request to the /api/send_message route
#     response = requests.post(url, json=data)    

#     # Print the response from the server
#     print(response.status_code)  # Print the HTTP status code
#     print(response.json())  # Print the JSON response from the server

#     logging.info('Script executed successfully')
# except Exception as e:
#     logging.error(f'Script encountered an error: {str(e)}')



import requests

# Define the URL of your Flask application
flask_url = "http://127.0.0.1:5000"  # Update with your actual Flask app URL

# Define the data you want to send in the POST request
data = {
    "user_id": 6,
    "report_frequency": 10,
    "goal_title": "Chess",
    "goal_description": "I wand to be a grnd master",
    "time_of_day": "12:31",
    "time_zone": "America/New_York",
    "contact_choice": "whatsapp"
}

# Define the data you want to send in the POST request
data1 = {
    "user_id": 6,
    "id": 30,
    "report_frequency": 10,
    "goal_title": "Tea picking",
    "goal_description": "I like to pick tea",
    "time_of_day": "13:31",
    "time_zone": "America/New_York",
    "contact_choice": "whatsapp"
}

# Send an HTTP POST request to the /add_goal route
# response = requests.post(f"{flask_url}/api/edit_goal", json=data1)

# Send an HTTP POST request to the /add_goal route
response = requests.post(f"{flask_url}/api/add_goal", json=data)

# Check the response
if response.status_code == 200:
    print("Goal submitted successfully")
    print(response.json())
else:
    print(f"Error: {response.status_code}")
    print(response.json())



# import Levenshtein

# def find_matching_goal(user_input, goals):
#     # Function to find a goal that closely matches the user's input
#     def match_goal(input_str, goal):
#         input_str = input_str.strip().lower()  # Remove leading and trailing whitespace
#         goal_title = goal['title'].strip().lower()  # Remove leading and trailing whitespace

#         # Check for an exact match
#         if input_str == goal_title:
#             return True

#         # Calculate the Levenshtein distance
#         distance = Levenshtein.distance(input_str, goal_title)

#         # Check if the distance is 1, indicating a single-character spelling mistake correction
#         if distance <= 2:
#             return True

#         return False

#     matching_goals = [goal for goal in goals if match_goal(user_input, goal)]

#     if matching_goals:
#         return matching_goals
#     else:
#         return []

# # Define your goals JSON object
# goals_json = [
#     {"id": 1, "title": "Yoga"},
#     {"id": 2, "title": "Running"},
#     {"id": 3, "title": "Swimming"}
# ]

# # User input
# user_input = "  runingk"  # Replace with the user's input

# # Query the chatbot to find a matching goal
# result = find_matching_goal(user_input, goals_json)

# if result:
#     print("Matching Goal(s):")
#     for goal in result:
#         print(f"ID: {goal['id']}, Title: {goal['title']}")
# else:
#     print("No matching goals found.")


# # Define the goal data
# goal_data = {
#     "user_id": 6,  # Replace with the actual user ID
#     "goal_id": 16, 
#     "message": "I had a nice experience",  # Replace with the user's timezone
    
# }

# # Make a POST request to the schedule_goal route
# response = requests.post("http://127.0.0.1:5000/api/store_feedback", json=goal_data)

# # Check the response
# if response.status_code == 200:
#     # Successful response
#     result = response.json()
#     print(result)
# else:
#     # Error response
#     print(f"Error: {response.status_code}")
#     print(response.json())

# from crontab import CronTab

# # Create a new CronTab object
# cron = CronTab(user=True)

# for job in cron:
#     if job.comment and job.comment.startswith('6'):
#         cron.remove(job)

# # Write the updated crontab
# cron.write()

# import requests

# # Define the user_id and goal_id for testing
# user_id = 6  # Replace with a valid user ID
# goal_id = 16  # Replace with a valid goal ID

# # Define the URL of your Flask application and the route
# url = f"http://localhost:5000/api/get_report/{goal_id}/{user_id}"

# # Send an HTTP GET request to retrieve the report
# response = requests.get(url)

# # Check the response
# if response.status_code == 200:
#     # Successful response
#     report = response.text
#     print(report)
# elif response.status_code == 404:
#     # Data not found
#     print("Data not found")
# else:
#     # Error response
#     print(f"Error: {response.status_code}, {response.text}")
