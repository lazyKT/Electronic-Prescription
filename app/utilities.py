"""
# Utitlies functions such as data validation, regex etc
"""
from flask import render_template
from app.email import send_prescription_email

def validate_prescription (data):
    """
    # Validate the prescription create request
    """
    if 'patient' not in data or 'identifier' not in data or 'pharmacist' not in data or 'medication' not in data or 'from_date' not in data or 'to_date' not in data:
        return False
    return True



def prepare_new_prescription_email (patient, pres_id):
    """
    # Prepare the subject and body for the new prescription email and send email after that
    """
    subject = '[Electronic Prescription] New Prescription Issued'
    recipient = patient.email
    fullname = '{} {}'.format(patient.fName, patient.lName)
    url = 'http://127.0.0.1:5000//prescription-qr/{}'.format(pres_id)
    body = render_template('prescription/email.html', patient=fullname, url=url)
    send_prescription_email(subject, recipient, body)
