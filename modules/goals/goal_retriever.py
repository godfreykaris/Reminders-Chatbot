import Levenshtein
from flask import jsonify, request
import traceback

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
            cursor.execute("SELECT goal_title, goal_description, contact_choice FROM goals WHERE user_id = %s AND id = %s;", (user_id, goal_id))
            user_goal = cursor.fetchone()

            if user_goal:
                # If the goal exists, return it as JSON
                goal_data = {
                    'title': user_goal[0],
                    'description': user_goal[1],
                    'contact_choice': user_goal[2],
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

    def get_user_goals(self, user_id):
        
        if not user_id :
            return jsonify({'message': 'Invalid user id'}), 400

        try:
            user_id = int(user_id)

            database_connection = self.database_initializer.get_database_connection()
            cursor = database_connection.cursor()

            # Retrieve the user's goal based on user_id and goal_id
            cursor.execute("SELECT id, goal_title FROM goals WHERE user_id = %s;", (user_id,))
            user_goals = cursor.fetchall()

            if user_goals:
                # Initialize an empty list to store multiple goal entries
                goals_titles = []

                # Loop through each goal data entry
                for row in user_goals:
                    goal_data = {
                        'id': row[0],
                        'title': row[1],
                    }
                    # Append the goal entry to the list
                    goals_titles.append(goal_data)
            
                return jsonify({'message': 'Goal retrieved successfully', 'goals_titles': goals_titles, 'status': 200})
            else:
                return jsonify({'message': 'Goals not retrieved', 'status': 404})

        except Exception as e:
            traceback.print_exc()
            # Handle database errors or other exceptions
            return jsonify({'message': str(e), 'error': str(e), 'status': 500})
        finally:
            cursor.close()
            database_connection.close()

    def find_matching_goal(self, user_input, goals):
        # Function to find a goal that closely matches the user's input
        def match_goal(input_str, goal):
            input_str = input_str.strip().lower()  # Remove leading and trailing whitespace
            goal_title = goal['title'].strip().lower()  # Remove leading and trailing whitespace
    
            # Check for an exact match
            if input_str == goal_title:
                return True
    
            # Calculate the Levenshtein distance
            distance = Levenshtein.distance(input_str, goal_title)
    
            # Check if the distance is 1, indicating a single-character spelling mistake correction
            if distance <= 1:
                return True
    
            return False
    
        for goal in goals:
            if match_goal(user_input, goal):
                return goal  # Return the first matching goal
        
        return[]