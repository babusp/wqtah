"""
Twilio Service
"""
# Django import
from django.conf import settings


# Third party imports
from twilio.rest import Client
TWILIO_CLIENT = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)


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


def send_twilio_otp(country_code, to_phone, channel):
    """
    This method is used to create twilio client and send otp.
    """
    TWILIO_CLIENT.verify.services(settings.TWILIO_SERVICE_SID).verifications.create(to='+{}{}'.format(country_code,
                                                                                                      to_phone),
                                                                                    channel=channel)


def verify_twilio_otp(country_code, to_phone, code):
    """
    This method is used to create twilio client and verify otp.
    """
    verification = (TWILIO_CLIENT.verify.services(settings.TWILIO_SERVICE_SID)
                    .verification_checks.create(to='+{}{}'.format(country_code, to_phone), code=code))
    return verification.status
