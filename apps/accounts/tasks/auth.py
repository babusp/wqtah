"""
    Asynchronous task of auth
"""
# python import imports
import logging

# Third party import
from celery import shared_task
from django.contrib.auth import get_user_model

USER = get_user_model()
LOGGER = logging.getLogger('LOGGER')


@shared_task()
def logout(user_id, access_token):
    """
    remove access_token and registration_token
    """
    try:
        LOGGER.info("going to logout user with id-{id}".format(id=user_id))
        LOGGER.info("user logged-out successfully")
    except Exception as e:
        LOGGER.error(e)
