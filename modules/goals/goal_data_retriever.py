import json

class UserGoalData:
    def __init__(self, database_initializer):
        self.database_initializer = database_initializer

    def get_user_goal_data(self, user_id, goal_id):
        
        if not user_id or not goal_id:
            return json.dumps({'message': 'Invalid input data', 'status': 400})

        try:
            database_connection = self.database_initializer.get_database_connection()
            cursor = database_connection.cursor()

            cursor.execute("SELECT created_at, feedback FROM goal_data WHERE user_id = %s AND goal_id = %s ORDER BY created_at DESC", (user_id, goal_id))
            
            # Initialize a list to store the result in the desired format
            goal_entries = []

            # Initialize variables to track total character count
            total_chars = 0

            # Iterate through the records
            for created_at, feedback in cursor:
                # Calculate the length of the current feedback
                feedback_length = len(feedback)

                # Calculate the length of the created_at as a string 
                created_at_length = len(str(created_at))

                # Check if adding the current feedback and created_at exceeds the character limit
                # (limit from the number of required tokens for chatgpt minus the prompt size)
                if total_chars + feedback_length + created_at_length > 3400:
                    break  # Stop if adding more characters would exceed the limit
                
                # Append the current feedback and created_at to the result list
                goal_entries.append({
                    "created_at": str(created_at),  # Convert to string if not already
                    "feedback": feedback
                })

                # Update the total character count
                total_chars += feedback_length + created_at_length

            if len(goal_entries) > 0:
                
                # Return the list of goal entries as JSON
                return json.dumps({'message': 'Goals retrieved successfully', 'goal_data_entries': goal_entries, 'status': 200})
            else:
                return json.dumps({'message': 'Goals not found', 'status': 404})


        except Exception as e:
            # Handle database errors or other exceptions
            return json.dumps({'message': str(e), 'error': str(e), 'status': 500})
        finally:
            cursor.close()
            database_connection.close()
