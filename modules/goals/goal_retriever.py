from flask import jsonify, request

class UserGoal:
    def __init__(self, database_initializer):
        self.database_initializer = database_initializer

    def get_user_goal(self):
        data = request.get_json()
        user_id = int(data.get('user_id'))
        goal_id = int(data.get('goal_id'))

        if not user_id or not goal_id:
            return jsonify({'message': 'Invalid input data'}), 400

        try:
            database_connection = self.database_initializer.get_database_connection()
            cursor = database_connection.cursor()

            # Retrieve the user's goal based on user_id and goal_id
            cursor.execute("SELECT goal_title, goal_description FROM goals WHERE user_id = %s AND id = %s;", (user_id, goal_id))
            user_goal = cursor.fetchone()

            if user_goal:
                # If the goal exists, return it as JSON
                goal_data = {
                    'title': user_goal[0],
                    'description': user_goal[1],
                }
                return jsonify({'message': 'Goal retrieved successfully', 'goal_data': goal_data})
            else:
                return jsonify({'message': 'Goal not found'}), 404

        except Exception as e:
            # Handle database errors or other exceptions
            return jsonify({'message': str(e), 'error': str(e)}), 500
        finally:
            cursor.close()
            database_connection.close()
