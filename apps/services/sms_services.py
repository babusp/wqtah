"""
File containing sms configuration.
"""
# Django import
from django.conf import settings

# Django app import
from apps.services.twilio_services import TwilioService


def send_sms(country_code, to_phone, message):
    """
    This code is used for sending sms via twilio.
    """
    client = TwilioService().get_client()
    try:
        response = client.messages.create(
                              body=message,
                              from_=settings.TWILIO_FROM_CONTACT,
                              to='+{}{}'.format(country_code, to_phone)
                          )
        print(response)

    except Exception as e:
        print(str(e))
