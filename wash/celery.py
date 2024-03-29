import os

from celery import Celery
from celery.schedules import crontab

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wash.settings')

app = Celery('wash')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


app.conf.beat_schedule = {
    # Execute daily at midnight
    'inform-users-for-soon-expiration': {
        'task': 'wash.tasks.alert_soon_expired',
        'schedule': crontab(minute=0, hour=0),
    },

}


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')