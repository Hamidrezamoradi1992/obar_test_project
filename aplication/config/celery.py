import os
from celery import Celery

# Django conf
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')

# Read settings.py + get celery config
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()
app.conf.beat_schedule = {
    'my_periodic_task': {
        'task': 'apps.core.tasks.expire_at_advertise',
        'schedule': 60.0,
    },
}
app.conf.timezone = 'UTC'