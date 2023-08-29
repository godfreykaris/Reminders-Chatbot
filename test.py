

# import requests
# import json

# # URL of the API endpoint
# url = "/api/retrieve_goal_data"

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
# url = "/api/chat/generate_message"

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
# url = "/api/chat/chat_with_user"

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
# url = '/api/chat/generate_report'

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


import logging
import requests

import os

dir_path = os.path.dirname(os.path.realpath(__file__))
filename = os.path.join(dir_path, 'cron_script.log')

logging.basicConfig(filename=filename, level=logging.INFO)

try:
    # Define the URL of your Flask application
    url = "/api/send_message"  # Update the URL as needed  

    # Define the data to be sent in the request's JSON body
    data = {
        "recipient": "+254759741544",  # Replace with the recipient's phone number
        "message": "Hello, this is a test message from  reminders app",  # Replace with your message
        "type": "whatsapp"  # Specify the message type (sms or whatsapp)
    }   

    # Send an HTTP POST request to the /api/send_message route
    response = requests.post(url, json=data)    

    # Print the response from the server
    print(response.status_code)  # Print the HTTP status code
    print(response.json())  # Print the JSON response from the server

    logging.info('Script executed successfully')
except Exception as e:
    logging.error(f'Script encountered an error: {str(e)}')



# import requests

# # Define the goal data
# goal_data = {
#     "user_id": 6,  # Replace with the actual user ID
#     "goal_id": 16, 
#     "timezone": "Africa/Nairobi",  # Replace with the user's timezone
#     "scheduled_time": {
#         "hour": 21,
#         "minute": 4
#     }
# }

# # Make a POST request to the schedule_goal route
# response = requests.post("http://127.0.0.1:5000/api/schedule_goal", json=goal_data)

# # Check the response
# if response.status_code == 200:
#     # Successful response
#     result = response.json()
#     print(result)
# else:
#     # Error response
#     print(f"Error: {response.status_code}")
#     print(response.json())



