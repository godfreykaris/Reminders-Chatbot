# Import necessary libraries
import os
import pytz
from flask import jsonify, request
from crontab import CronTab
from datetime import datetime, timedelta

import requests

from modules.goals.cron_manager import CronJobManager

# Define a class named Scheduler for scheduling tasks (goals or reports)
class Scheduler:
    def __init__(self, script_name, script_job):
        self.script_name = script_name
        self.script_job = script_job

    def schedule_task_cron(self, task_data):
        try:
            
            if not task_data or "user_id" not in task_data or "timezone" not in task_data or "scheduled_time" not in task_data or "report_frequency" not in task_data:
                return jsonify({'message': 'Task scheduling failed. Provide all required task data.'}), 500

            # Create an instance of CronJobManager
            cron_manager = CronJobManager(user=True)
        
            local_time = pytz.timezone(task_data["timezone"]).localize(datetime.now())
            utc_time = local_time.astimezone(pytz.utc)

            scheduled_time = utc_time.replace(hour=task_data["scheduled_time"]["hour"], minute=task_data["scheduled_time"]["minute"])

            current_dir = os.path.dirname(os.path.abspath(__file__))
            script_path = os.path.abspath(os.path.join(current_dir, '..', '..', self.script_name))

        
            if self.script_job == 'report':
                # Remove the job if it exists
                comment = f'{task_data["user_id"]}-{task_data["goal_id"]}-report'
                cron_manager.remove_jobs_by_comment(comment)

                report_frequency = task_data["report_frequency"]

                cron_manager.add_cron_job(
                    command=f'python3 "{script_path}" --user_id {task_data["user_id"]} --goal_id {task_data["goal_id"]}',
                    comment=f'{task_data["user_id"]}-{task_data["goal_id"]}-report',
                    minute=scheduled_time.minute,
                    hour=scheduled_time.hour,
                    job_type='report',  # Specify job type
                    report_frequency=report_frequency  # Pass report_frequency
                )
            else:
                # Remove the job if it exists
                comment = f'{task_data["user_id"]}-{task_data["goal_id"]}-goal'
                cron_manager.remove_jobs_by_comment(comment)

                cron_manager.add_cron_job(
                    command=f'python3 "{script_path}" --user_id {task_data["user_id"]} --goal_id {task_data["goal_id"]}',
                    comment=f'{task_data["user_id"]}-{task_data["goal_id"]}-goal',
                    minute=scheduled_time.minute,
                    hour=scheduled_time.hour,
                    job_type='goal'  # Specify job type
                )


            return jsonify({'message': 'Task scheduled successfully', 'task_data': task_data}), 200
        except Exception as e:
            
            return jsonify({'message': str(e)}), 500  # For testing only
    
    def schedule_goal_cron(goal_data):
        scheduler = GoalScheduler()
        return scheduler.schedule_task_cron(goal_data)

    def schedule_report_cron(report_data):
        scheduler = ReportScheduler()
        return scheduler.schedule_task_cron(report_data)
    
# Define a class for scheduling goals
class GoalScheduler(Scheduler):
    def __init__(self):
        super().__init__('goal_cron_job.py', 'goal')

# Define a class for scheduling reports
class ReportScheduler(Scheduler):
    def __init__(self):
        super().__init__('report_cron_job.py', 'report')


