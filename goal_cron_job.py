#!/usr/bin/python3

import os
import sys 

import logging
import requests


def main(args):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    filename = os.path.join(dir_path, 'cron_script.log')

    logging.basicConfig(filename=filename, level=logging.INFO)

    try:

        # Get the user id
        user_id = args[2]
        # Get the goal id
        goal_id = args[4]

        # retrieve the goal
        # Define the URL of your Flask application
        url = "/api/user/retrieve_goal"  # Update the URL as needed  

        # Define the data to be sent in the request's JSON body
        data = {
            "user_id": user_id,  
            "goal_id": goal_id,  
        }  

        # Send an HTTP POST request to the retrieve goal route
        response = requests.post(url, json=data)    

        if response.status_code == 200:
            data = response.json()
            goal_data = data.get('goal_data')
        else:
            print(f"Error: {response.status_code}, {response.json()}")

        # Generate the message
        # URL of the API endpoint
        url = "/api/chat/generate_message"       

        # Template message
        template_message = f"Did you do your {goal_data['title']}?"        

        # JSON payload
        payload = {"template_message": template_message}      

        # Send a POST request
        response = requests.post(url, json=payload)       

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            data = response.json()
            generated_message = data.get('user_message')
        else:
            print(f"Error: {response.status_code}, {response.json()}")

        # Define the URL of your Flask application
        url = "/api/send_message"  # Update the URL as needed  

        # Define the data to be sent in the request's JSON body
        data = {
            "recipient": "+254759741544",  # Replace with the recipient's phone number
            "message": generated_message, # + goal_title + " Goal description: " + goal_description,  # Replace with your message
            "type": "whatsapp"  # Specify the message type (sms or whatsapp)
        }   

        # Send an HTTP POST request to the /api/send_message route
        response = requests.post(url, json=data)    

        # Print the response from the server
        print(response.status_code)  # Print the HTTP status code
        print(response.json())  # Print the JSON response from the server

        logging.info('Script executed successfully' + user_id)
    except Exception as e:
        logging.error(f'Script encountered an error: {str(e)}  + {user_id}')
    # finally:
    #         cursor.close()
    #         database_connection.close()
  
if __name__ == '__main__':
    main(sys.argv)

