"""
    Asynchronous task of auth
"""
# python import imports
import logging

# Third party import
from celery import shared_task
from django.contrib.auth import get_user_model

# Django app import
from apps.accounts.messages import SMS_TEMPLATE, SUCCESS_CODE
from apps.services.sms_services import send_sms

USER = get_user_model()
LOGGER = logging.getLogger("LOGGER")


@shared_task()
def logout(user_id, access_token):
    """
    remove access_token and registration_token
    """
    try:
        LOGGER.info("going to logout user with id-{id}".format(id=user_id))
        LOGGER.info({"detail": SUCCESS_CODE["2004"]})

    except Exception as e:
        LOGGER.error(e)


@shared_task
def send_sms_otp_task(phone_obj):
    """
    Send SMS
    """
    try:
        sms = SMS_TEMPLATE["0001"]
        user = phone_obj.user
        message = sms["message"].format(
            first_name=user.first_name, last_name=user.last_name, otp=phone_obj.otp
        )
        send_sms(phone_obj.country_code, phone_obj.phone_no, message)

    except Exception as e:
        print(str(e))
