from flask import jsonify, request

class UserHandler:
    def __init__(self, database_initializer):
        self.database_initializer = database_initializer

    def get_user(self):
        try:
            # Get user ID from the request parameters
            data = request.get_json()
            user_id = int(data.get('user_id'))


            if not user_id:
                return jsonify({'message': 'Invalid user ID'}), 400

            database_connection = self.database_initializer.get_database_connection()
            cursor = database_connection.cursor()

            # Retrieve the user's information based on user_id
            cursor.execute("SELECT name, email FROM users WHERE id = %s;", (user_id,))
            user_data = cursor.fetchone()

            if user_data:
                # If the user exists, return their information as JSON
                user_info = {
                    'name': user_data[0],
                    'email': user_data[1],
                }
                return jsonify({'message': 'User retrieved successfully', 'user_info': user_info})
            else:
                return jsonify({'message': 'User not found'}), 404

        except Exception as e:
            # Handle database errors or other exceptions
            return jsonify({'message': str(e), 'error': str(e)}), 500
        # finally:
        #     cursor.close()
        #     database_connection.close()
