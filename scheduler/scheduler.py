from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore
from django.utils import timezone
from django_apscheduler.models import DjangoJobExecution
import sys


# This is the function you want to schedule - add as many as you want and then register them in the start() function below
def get_current_weather_conditions():
    today = timezone.now()


# def start():
#     scheduler = BackgroundScheduler()
#     scheduler.add_jobstore(DjangoJobStore(), "default")
#     # run this job every 24 hours
#     scheduler.add_job(get_current_weather_conditions, 'interval', hours=24, name='clean_accounts', jobstore='default')
#     scheduler.start()
#     print("Scheduler started...", file=sys.stdout)