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

        # # Get the user id
        # user_id = args[2]
        # # Get the goal id
        # goal_id = args[4]

        # Get the user id
        user_id = args[1]
        # Get the goal id
        goal_id = args[2]
        
        # retrieve the user
        # Define the URL of your Flask application
        url = "http://localhost:5000/api/user/retrieve_user"  # Update the URL as needed  

        # Define the data to be sent in the request's JSON body
        data = {
            "user_id": user_id,   
        }  

        # Send an HTTP POST request to the retrieve goal route
        response = requests.post(url, json=data)    

        if response.status_code == 200:
            data = response.json()
            user = data.get('user_info')
        else:
            print(f"Error: {response.status_code}, {response.json()}")


        # retrieve the goal
        # Define the URL of your Flask application
        url = "http://localhost:5000/api/user/retrieve_goal"  # Update the URL as needed  

        # Define the data to be sent in the request's JSON body
        data = {
            "user_id": user_id,  
            "goal_id": goal_id,  
        }  

        # Send an HTTP POST request to the retrieve goal route
        response = requests.post(url, json=data)    

        if response.status_code == 200:
            data = response.json()
            goal = data.get('goal_data')
        else:
            print(f"Error: {response.status_code}, {response.json()}")

        # retrieve the goal data
        # Define the URL of your Flask application
        url = "http://localhost:5000/api/user/retrieve_goal_data"  # Update the URL as needed  

        # Define the data to be sent in the request's JSON body
        data = {
            "user_id": user_id,  
            "goal_id": goal_id,  
        }  

        # Send an HTTP POST request to the retrieve goal route
        response = requests.post(url, json=data)    


        if response.status_code == 200:
            data = response.json()
            goal_data = data.get('goal_data_entries')
        else:
            print(f"Error: {response.status_code}, {response.json()}")

        # Define the URL of your Flask application
        url = 'http://localhost:5000/api/chat/generate_report'        

       
        # Create a dictionary with the user data
        request_data = {
            "user_data":
                {
                    "name": user['name'],
                    "goal": goal,
                    "data": goal_data
                }           
            
        }     

        # Send a POST request to your Flask application
        response = requests.post(url, json=request_data)      

        # Check the response
        if response.status_code == 200:
            # Successful response
            result = response.json()
            report = result['bot_response']
            # print(report)
        else:
            # Error response
            print(f"Error: {response.status_code}")
            print(response.json())

        # Define the URL of your Flask application
        url = "http://localhost:5000/api/send_message"  # Update the URL as needed  

        # Define the data to be sent in the request's JSON body
        data = {
            "recipient": "+254759741544",  # Replace with the recipient's phone number
            "message": report, 
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

