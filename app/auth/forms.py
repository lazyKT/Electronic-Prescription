from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, DateField, SelectField, validators
from wtforms.fields.html5 import TelField

from app.models import User


class LoginForm (FlaskForm):
    """
    : User Login Form
    """
    username = StringField ("Username", validators=[
        validators.DataRequired(),
        validators.Length(max=20)
    ])
    password = PasswordField ("Password", validators=[validators.DataRequired()])
    remember_me = BooleanField ("Remember Me")
    submit = SubmitField ("Sign In")


class PatientRegisterForm (FlaskForm):
    """
    : User Registration Form
    """
    username = StringField ("Username", validators=[
        validators.DataRequired(),
        validators.Length(min=4)
    ])
    fName = StringField ("First Name", validators=[
        validators.DataRequired()
    ])
    lName = StringField ("Last Name", validators=[
        validators.DataRequired()
    ])
    email = StringField ("Email Address", validators=[
        validators.DataRequired(),
        validators.Length(min=4, max=50)
    ])
    mobile = TelField ("Phone Number (8-digits without country code)", validators=[
        validators.DataRequired(),
        validators.Length(min=8, max=8)
    ])
    gender = SelectField ("Gender", choices=[
        ('Male'),
        ('Female')
    ])
    dob = DateField(
        "Date of Birth",
        render_kw={'placeholder': 'YYYY-MM-DD'},
        format='%Y-%m-%d')
    password = PasswordField ("Password", validators=[
        validators.DataRequired(),
        validators.Length(min=8),
        validators.EqualTo("confirm", message="Password must match")
    ])
    confirm = PasswordField ("Confirm Password")
    submit = SubmitField ("Create Account")

    def email_validation (self, email: str):
        """
        : Email Address is unique and one account per one email.
        : If existing user tries to register again, show him/her an error.
        """
        user = User.query.filter_by (email=email).first()
        if user is not None:
            raise ValidationError('User already exists. Please use different email')


class PatientMedicationProfileForm (FlaskForm):
    """
    : Information about Patient Medication Profile
    """
    allergy = TextAreaField ("Are you allergic to any medication? If so, please fill in the textbox below.")
    history = TextAreaField ("Do you have anything special to tell us about your medication history?")
    accept_tc = BooleanField ("I accept and agree on Terms and Conditions")
    create_account = SubmitField ("Create an Account")
