# Import necessary libraries
import os
import pytz
from flask import jsonify, request
from croniter import croniter
from crontab import CronTab
from datetime import datetime

# Define a class named GoalScheduler for scheduling user goals
class GoalScheduler:
    def __init__(self, username):
        # Initialize the GoalScheduler with a username
        self.username = username

    # Define a method to schedule a user's goal as a cron job
    def schedule_goal_cron(self):
        try:
            # Retrieve goal data from the Flask request
            goal_data = request.get_json()

            # Check if goal_data is available and contains the required fields
            if not goal_data or "user_id" not in goal_data or "timezone" not in goal_data:
                return jsonify({'message': 'Goal scheduling failed. Provide all required goal data.'}), 500

            # Get the current date and time
            now = datetime.now()

            # Convert the user's local time to UTC time
            local_time = pytz.timezone(goal_data["timezone"]).localize(now)
            utc_time = local_time.astimezone(pytz.utc)

            # Set the desired time for the goal (e.g., 7:00 AM)
            next_occurrence = utc_time.replace(hour=13, minute=14, second=0)

            # Calculate the cron expression based on the desired time
            cron = croniter("0 {} {} * *".format(next_occurrence.minute, next_occurrence.hour), now)
            cron_expression = cron.get_next(datetime)

            # Create a new cron tab object
            cron = CronTab(user=self.username)

            # # Get the current directory of the script
            # current_dir = os.path.dirname(os.path.abspath(__file__))

            # # Navigate two directories up to reach the location of test.py
            # script_path = os.path.abspath(os.path.join(current_dir, '..', '..', 'test.py'))

            # # Create a new cron job for the goal, specifying the script and goal_id
            # job = cron.new(command=f'python "{script_path}" --goal_id {goal_data["user_id"]}')

            # # Set the cron expression to run at 7:00 AM
            # job.setall(cron_expression.strftime('%M %H * * *'))

            # # Write the cron job to the crontab
            # cron.write()

            # Return a success message and status code 200
            return jsonify({'message': 'Goal scheduled successfully', 'goal_data': goal_data}), 200
        except Exception as e:
            # Return an error message and status code 500 in case of an exception
            #return jsonify({'message': 'Failed to schedule goal'}), 500
            # Get the current directory of the script
            current_dir = os.path.dirname(os.path.abspath(__file__))

            # Navigate two directories up to reach the location of test.py
            script_path = os.path.abspath(os.path.join(current_dir, '..', '..', 'test.py'))

            return jsonify({'message': str(e)}), 500 # For testing only
