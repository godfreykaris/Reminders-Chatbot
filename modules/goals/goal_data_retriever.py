from flask import jsonify, request

class UserGoalData:
    def __init__(self, database_initializer):
        self.database_initializer = database_initializer

    def get_user_goal_data(self):
        data = request.get_json()
        user_id = int(data.get('user_id'))
        goal_id = int(data.get('goal_id'))

        if not user_id or not goal_id:
            return jsonify({'message': 'Invalid input data'}), 400

        try:
            database_connection = self.database_initializer.get_database_connection()
            cursor = database_connection.cursor()

            # Retrieve the user's goal based on user_id and goal_id
            cursor.execute("SELECT created_at, status, feedback FROM goal_data WHERE user_id = %s AND goal_id = %s;", (user_id, goal_id))
            user_goal_data = cursor.fetchall()

            if user_goal_data:
                # Initialize an empty list to store multiple goal entries
                goal_entries = []

                # Loop through each goal data entry
                for row in user_goal_data:
                    # Create a dictionary for each goal entry
                    goal_entry = {
                        'created_at': row[0],
                        'status': row[1],
                        'feedback': row[2],  # Assuming the report is in the third column
                    }

                    # Append the goal entry to the list
                    goal_entries.append(goal_entry)

                # Return the list of goal entries as JSON
                return jsonify({'message': 'Goals retrieved successfully', 'goal_data_entries': goal_entries})
            else:
                return jsonify({'message': 'Goals not found'}), 404


        except Exception as e:
            # Handle database errors or other exceptions
            return jsonify({'message': str(e), 'error': str(e)}), 500
        finally:
            cursor.close()
            database_connection.close()
