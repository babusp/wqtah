#!/usr/bin/env python3
import os
from sendgrid.helpers.mail import Mail
from sendgrid import SendGridAPIClient


# update to your dynamic template id from the UI
TEMPLATE_ID = os.getenv("TEMPLATE_ID")

FROM_EMAIL = os.getenv("FROM_EMAIL")


def password_updated_email(to_email):
    message = Mail(from_email=FROM_EMAIL, to_emails=to_email)
    # pass custom values for our HTML placeholders
    message.dynamic_template_data = {
        "subject": "PASSWORD UPDATE",
        "place": "WQTAH",
    }
    message.template_id = TEMPLATE_ID
    # create our sendgrid client object, pass it our key, then send and return our response objects
    try:
        sg = SendGridAPIClient(os.environ.get("SENDGRID_API_KEY"))
        response = sg.send(message)

    except Exception as e:
        print("Error: {0}".format(e))
    return str(response.status_code)
