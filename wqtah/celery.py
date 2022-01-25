"""
    Celery configuration.
"""

from __future__ import absolute_import, unicode_literals

import os

from celery import Celery
from dotenv import load_dotenv

load_dotenv()

load_dotenv(verbose=True)
env_path = os.path.join(os.path.abspath(os.path.join('.env', os.pardir)), '.env')
load_dotenv(dotenv_path=env_path)

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', os.getenv('WEB_SETTINGS'))

app = Celery('wqtah')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    """
    To debug task
    :param self: self
    :return: print log
    """
    print('Request: {0!r}'.format(self.request))
