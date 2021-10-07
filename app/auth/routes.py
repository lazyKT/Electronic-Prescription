from flask import render_template, flash, redirect, url_for
from flask_login import current_user, login_user
from app.auth import bp
from app.models import User
from app.auth.forms import LoginForm, PatientRegisterForm, PatientMedicationProfileForm


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
        user = User.query.filter_by (email=form.email.data).first()
        if user is None or not user.check_password (form.password.data):
            # Login Failed
            error = 'Invalid Credentials!'
            return render_template ("auth/login.html", form=form, error=error)
        else:
            login_user (user, remember=form.remember_me.data)
            flash('Login requested for user {}, remember_me={}'.format(
                form.username.data, form.remember_me.data))
            return redirect(url_for('home.index'))
    return render_template ("auth/login.html", form=form)


@bp.route ("/register")
def options ():
    """
    : Registration Options-> Doctor, Patients or Phamarcists
    : Users will have to choose one, before they register.
    : Upon one option has been chosen, the user will be redirected to
    : the registration page of the chosen option.
    """
    return render_template ("auth/options.html")


@bp.route ("/register/patient", methods=["GET", "POST"])
def patient_register ():
    """
    : Patient Registration
    """
    form = PatientRegisterForm()
    if form.validate_on_submit():
        return redirect(url_for('auth.patient_register_info'))
    return render_template ("auth/patient.html", form=form)


@bp.route ("/register/patient/more", methods=["GET", "POST"])
def patient_register_info ():
    """
    : More about Patient Info in Registration Page.
    : Information like Drug Allergies, Medication Profile, etc
    """
    form = PatientMedicationProfileForm()
    return render_template ("auth/patient_medication.html", form=form)
