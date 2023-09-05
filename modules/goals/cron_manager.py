from crontab import CronTab

class CronJobManager:
    def __init__(self, user=True):
        self.cron = CronTab(user=user)

    def remove_jobs_by_comment(self, comment):
        jobs = self.cron.find_comment(comment)
        jobs_list = list(jobs)
        if len(jobs_list) != 0:
            self.cron.remove(jobs_list[0])
            self.cron.write()
            
    def remove_jobs_by_user_id(self, user_id):
        """
        Remove all cron jobs associated with a specific user ID.

        Args:
            user_id (str): The user ID to identify the cron jobs to be removed.

        Returns:
            None
        """
        cron = self.cron

        # Iterate over all cron jobs
        for job in cron:
            if job.comment and job.comment.startswith(user_id):
                cron.remove(job)

        # Write the updated crontab
        cron.write()


    def add_cron_job(self, command, comment, minute, hour, job_type, report_frequency=None):
        """
        Add a new cron job to the user's crontab.

        Args:
            command (str): The shell command to be executed by the cron job.
            comment (str): A unique comment to identify the cron job.
            minute (str): The minute field for scheduling (0-59).
            hour (str): The hour field for scheduling (0-23).
            job_type (str): The type of the job, e.g., 'goal' or 'report'.
            report_frequency (str): The report frequency for report jobs (days), or None for other job types.

        Returns:
            None
        """
        job = self.cron.new(command=command, comment=comment)

        
        if job_type == 'report' and report_frequency:
            # For report jobs, use the specified report frequency
            job.setall(f'{minute} {hour} */{report_frequency} * *')
        else:
            # For other job types (e.g., 'goal'), use a standard cron scheduling
            job.setall(f'{minute} {hour} * * *')

        self.cron.write()