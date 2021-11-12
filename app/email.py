import sendgrid
import os
from sendgrid.helpers.mail import *


API_KEY = os.environ.get('E_PRESC_SENDGRID_API_KEY')


# send email to user
def send_prescription_email (subject, recipient, body):
    """
    # Send new prescription email and link to patient
    """
    sg = sendgrid.SendGridAPIClient(api_key=API_KEY)
    from_email = Email('ktl141@uowmail.edu.au')
    to_email = To(recipient)
    try:
        mail = Mail(from_email, to_email, subject, html_content=HtmlContent(body))
        response = sg.client.mail.send.post(request_body=mail.get())
        # print("email sent response")
        # print(response.status_code)
        # print(response.body)
        # print(response.headers)
    except Exception as e:
        # print(e.body)
        raise(e)
