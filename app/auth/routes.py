from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user
from app import db
from app.auth import bp
from app.models import User, Patient
from app.auth.forms import LoginForm, PatientRegisterForm, PatientMedicationProfileForm, LogOutConfirmationForm


@bp.route ("/login", methods=["GET", "POST"])
def login ():
    """
    : Sign In Route
    """
    if current_user.is_authenticated:
        """
        : if user is already logged in, redirect to the protected index page
        """
        return redirect(url_for('home.index'))
    form = LoginForm()
    if form.validate_on_submit():
        # Form validation successful
        user = User.query.filter_by (username=form.username.data).first()
        if user is None or not user.check_password (form.password.data):
            # Login Failed
            error = 'Invalid Credentials!'
            return render_template ("auth/login.html", form=form, error=error)
        else:
            login_user (user, remember=form.remember_me.data)
            print(user.get_role())
            if user.get_role() == 'admin':
                return redirect(url_for('admin.index'))
            flash('Login requested for user {}, remember_me={}'.format(
                form.username.data, form.remember_me.data))
            return redirect(url_for('home.index'))
    return render_template ("auth/login.html", form=form)


@bp.route ("/register/options")
def options ():
    """
    : Registration Options-> Doctor, Patients or Phamarcists
    : Users will have to choose one, before they register.
    : Upon one option has been chosen, the user will be redirected to
    : the registration page of the chosen option.
    """
    return render_template ("auth/options.html")


@bp.route ("/register/patient", methods=["GET", "POST"])
def register ():
    """
    : Patient Registration
    """
    if current_user.is_authenticated:
        return redirect(url_for('home.index'))
    form = PatientRegisterForm()
    if form.validate_on_submit():
        # return redirect(url_for('auth.patient_register_info'))
        _user = User.query.filter_by(username=form.username.data).first()
        print ('user', _user)
        if _user:
            print ('User Already Exists!')
            error = 'Username has already taken. Please choose another.'
            return render_template ("auth/register.html", form=form, error=error)
        _patient = Patient.query.filter_by(email=form.email.data).first()
        if _patient:
            print ('Patient Already Exists')
            error = 'User already exists with email'
            return render_template ('auth/register.html', form=form, error=error)
        print ('successful register!')
        patient = Patient (
            username=form.username.data,
            role='patient',
            fName=form.fName.data,
            lName=form.lName.data,
            mobile=form.mobile.data,
            email = form.email.data,
            dob=form.dob.data,
            gender=form.gender.data
        )
        patient.set_password(form.password.data)
        patient.save()
        flash ('Welcome, {}. Please log in.'.format(form.lName.data))
        return redirect(url_for('auth.login'))
    print ('Form validation Failed!')
    return render_template ("auth/register.html", form=form)


@bp.route ("/register/patient/more", methods=["GET", "POST"])
def patient_register_info ():
    """
    : More about Patient Info in Registration Page.
    : Information like Drug Allergies, Medication Profile, etc
    """
    form = PatientMedicationProfileForm()
    return render_template ("auth/patient_medication.html", form=form)


@bp.route ("/logout")
def logout ():
    logout_user()
    return redirect(url_for('home.index'))
