from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, validators
from wtforms.fields.html5 import TelField


class LoginForm (FlaskForm):
    """
    : User Login Form
    """
    email = StringField ("Email Address", validators=[
        validators.DataRequired(),
        validators.Length(min=4, max=50)
    ])
    password = PasswordField ("Password", validators=[validators.DataRequired()])
    remember_me = BooleanField ("Remember Me")
    submit = SubmitField ("Sign In")


class PatientRegisterForm (FlaskForm):
    """
    : User Registration Form
    """
    fullname = StringField ("Full Name as in NRIC", validators=[
        validators.DataRequired(),
        validators.Length(min=5)
    ])
    email = StringField ("Email Address", validators=[
        validators.DataRequired(),
        validators.Length(min=4, max=50)
    ])
    mobile = TelField ("Phone Number", validators=[
        validators.DataRequired(),
        validators.Length(min=8, max=8)
    ])
    password = PasswordField ("Password", validators=[
        validators.DataRequired(),
        validators.Length(min=8),
        validators.EqualTo("confirm", message="Password must match")
    ])
    confirm = PasswordField ("Confirm Password")
    submit = SubmitField ("Continue")


class PatientMedicationProfileForm (FlaskForm):
    """
    : Information about Patient Medication Profile
    """
    allergy = TextAreaField ("Are you allergic to any medication? If so, please fill in the textbox below.")
    history = TextAreaField ("Do you have anything special to tell us about your medication history?")
    accept_tc = BooleanField ("I accept and agree on Terms and Conditions")
    create_account = SubmitField ("Create an Account")
