# Import necessary libraries
import os
import pytz
from flask import jsonify, request
from crontab import CronTab
from datetime import datetime

# Define a class named Scheduler for scheduling tasks (goals or reports)
class Scheduler:
    def __init__(self, username, script_name):
        self.username = username
        self.script_name = script_name

    def schedule_task_cron(self):
        try:
            task_data = request.get_json()

            if not task_data or "user_id" not in task_data or "timezone" not in task_data or "scheduled_time" not in task_data:
                return jsonify({'message': 'Task scheduling failed. Provide all required task data.'}), 500

            cron = CronTab(user=self.username)

            local_time = pytz.timezone(task_data["timezone"]).localize(datetime.now())
            utc_time = local_time.astimezone(pytz.utc)

            scheduled_time = utc_time.replace(hour=task_data["scheduled_time"]["hour"], minute=task_data["scheduled_time"]["minute"])

            current_dir = os.path.dirname(os.path.abspath(__file__))
            script_path = os.path.abspath(os.path.join(current_dir, '..', '..', self.script_name))

            job = cron.new(command=f'python3 "{script_path}" --user_id {task_data["user_id"]} --goal_id {task_data["goal_id"]}')
            job.setall(f'{scheduled_time.minute} {scheduled_time.hour} * * *')

            cron.write()

            return jsonify({'message': 'Task scheduled successfully', 'task_data': task_data}), 200
        except Exception as e:
            
            return jsonify({'message': str(e)}), 500  # For testing only

# Define a class for scheduling goals
class GoalScheduler(Scheduler):
    def __init__(self, username):
        super().__init__(username, 'goal_cron_job.py')

# Define a class for scheduling reports
class ReportScheduler(Scheduler):
    def __init__(self, username):
        super().__init__(username, 'report_cron_job.py')


