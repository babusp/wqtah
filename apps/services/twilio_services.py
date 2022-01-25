"""
Twilio Service
"""
# Django import
from django.conf import settings

# Third party imports
from twilio.rest import Client


class TwilioService(object):
    """
    Twilio Service
    """
    _client = None

    def __init__(self):
        if not TwilioService._client:
            print(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
            TwilioService._client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

    @classmethod
    def get_client(cls):
        if not cls._client:
            cls()
        return cls._client
