from django_crontab import CronJobBase, Schedule

class MyCronJob(CronJobBase):
    RUN_EVERY_MINS = 5  # run every 5 minutes

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'blood_donation_app.my_cron_job'  # path to your management command

    def do(self):
        print("hello")
        
