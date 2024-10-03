import os

from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")

app = Celery("shipmate")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()
app.conf.beat_schedule = {
    'fetch_emails_periodically': {
        'task': 'shipmate.mails.tasks.fetch_emails_task',
        'schedule': 30,  # Fetch emails every 30 seconds
    },
    'follow_up_quotes_task': {
        'task': 'shipmate.quotes.tasks.follow_up_quotes',
        'schedule': 60,  # Run every minute
    },
}
