"""
Uses: for application logs
"""
import os

from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(BASE_DIR, '.env'))

LOG_DIR = os.path.join(BASE_DIR, 'logs')
if not os.path.isdir(LOG_DIR):
    os.mkdir(LOG_DIR)

# 10 MB
log_max_file_size = 10*1024
file_back_up_count = 15
rotating_file_handler = 'logging.handlers.RotatingFileHandler'

# Define log config
LOG_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'formatters': {
        'standard': {
            'format': "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
        'verbose': {
            'format': "[%(asctime)s] [%(levelname)s] [%(name)s] [%(filename)s: %(funcName)s: %(lineno)d] "
                      "[%(process)d: %(processName)s] %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'file': {
            'level': 'DEBUG',
            'class': rotating_file_handler,
            'formatter': 'verbose',
            'filename': LOG_DIR + '/applications.log',
            'maxBytes': log_max_file_size,
            'backupCount': file_back_up_count,
            'encoding': 'utf-8',
            'mode': 'w',
        },
        'celery': {
            'level': 'DEBUG',
            'class': rotating_file_handler,
            'formatter': 'verbose',
            'filename': LOG_DIR + '/celery-task.log',
            'maxBytes': log_max_file_size,
            'backupCount': file_back_up_count,
            'encoding': 'utf-8',
            'mode': 'w',
        },
        'cron_task': {
            'level': 'DEBUG',
            'class': rotating_file_handler,
            'formatter': 'verbose',
            'filename': LOG_DIR + '/cron_task.log',
            'maxBytes': log_max_file_size,
            'backupCount': file_back_up_count,
            'encoding': 'utf-8',
            'mode': 'w',
        },
    },
    'loggers': {
        '': {
            'handlers': ['console', 'file'],
            'level': os.getenv('ROOT_LOG_LEVEL', 'INFO'),
        },
        'django': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': False,
        },
        'celery.logger': {
            'handlers': ['console', 'celery'],
            'level': os.getenv('CELERY_LOG_LEVEL', 'INFO'),
            'propagate': False,
        },
        'cron_task.logger': {
            'handlers': ['console', 'cron_task'],
            'level': os.getenv('ROOT_LOG_LEVEL', 'INFO'),
            'propagate': False,
        },
    }
}
