from flask import jsonify, request
import requests

class StoreGoalData:
    def __init__(self, database_initializer):
        self.database_initializer = database_initializer

    #validating message
    def validate_message_content(self, message):
        if not message:
            return False
        return True  
    
    def store_user_goal_data(self, message, goal_id, user_id):
        
        MAX_MESSAGE_LENGTH = 256 

        if not user_id or not goal_id:
            return jsonify({'message': 'Invalid input data'}), 400

        try:
            database_connection = self.database_initializer.get_database_connection()
            cursor = database_connection.cursor()

            #insert the message into the goal data table
            insert_query = """
                INSERT INTO goal_data (goal_id, user_id, feedback) VALUES (%s, %s, %s)
            """       

            if len(message) <= MAX_MESSAGE_LENGTH and self.validate_message_content(message):
                cursor.execute(insert_query, (goal_id, user_id, message))
                database_connection.commit()
                cursor.close()

                return jsonify(message="Message stored successfully"), 200
            else:
                return jsonify(message="Message has invalid format"), 400
            

        except Exception as e:
            # Handle database errors or other exceptions
            return jsonify({'message': str(e), 'error': str(e)}), 500
        finally:
            cursor.close()
            database_connection.close()

    def store_user_data_request(self, store_data_url, goal_data):
        # Make a POST request to the schedule_goal route
        response = requests.post(store_data_url, json=goal_data)        

        # Check the response
        if response.status_code != 200:
            # Successful response
            result = response.json()
            print(result)
        