from flask import render_template, redirect, url_for, request, jsonify, flash
from flask_login import login_required, current_user
from datetime import datetime

from app import db
from app.home import bp
from app.email import send_prescription_email
from app.models import User, Patient, Doctor, Pharmacist, Admin
from app.auth.forms import AdminEditUserForm



@bp.before_app_first_request
def before_app():
    db.create_all()
    create_master_admin_if_not_exist()


def create_master_admin_if_not_exist():

    user = User.get_user_by_username('admin')
    if user:
        return

    user = Admin.get_user_by_email('admin@site.com')
    if user:
        return

    admin = Admin(
      username='admin',
      email = 'admin@site.com',
      fName='Admin',
      lName='Admin',
      role='admin',
      mobile='83210054',
      gender='Male',
      dob=datetime.strptime('1996-12-09', '%Y-%m-%d')
    )

    admin.set_password('admin')
    db.session.add(admin)
    db.session.commit()


@bp.route ('/')
@bp.route ('/index')
def index():
  """
  : Web Site Root/Home Page
  """
  if current_user.is_authenticated:
      if current_user.get_role() == 'doctor':
          return redirect(url_for('doctor.index'))
      if current_user.get_role() == 'admin':
          return redirect(url_for('admin.index'))
      if current_user.get_role() == 'pharmacist':
          return redirect(url_for('pharmacist.index'))
      if current_user.get_role() == 'patient':
          return redirect(url_for('patient_bp.index'))
  return render_template ('home/index.html')

@bp.route('/profile')
@login_required
def profile():
    return render_template ('home/profile.html')


@bp.route('/edit/<id>', methods=['GET', 'PUT'])
@login_required
def edit_user(id):
    if request.method == 'PUT':
        data = request.get_json()
        user = User.get_user_by_id(id)
        if user is None:
            return "User Not Found", 404
        if not validate_request(data):
            return "Missing Required Data", 400
        if user.get_role() == 'patient':
            # update patient
            patient = Patient.update_patient_profile(id, data)
            return jsonify(patient()), 201
        if user.get_role() == 'admin':
            # update admin
            admin = Admin.update_admin_profile(id, data)
            return jsonify(admin()), 201
        if user.get_role() == 'pharmacist':
            # update pharmacist
            pharmacist = Pharmacist.update_pharmacist_profile(id, data)
            return jsonify(pharmacist()), 201
        if user.get_role() == 'doctor':
            # update doctor
            doctor = Doctor.update_doctor_profile(id, data)
            return jsonify(doctor()), 201
        return "Invalid user role", 400


@bp.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    try:
        form = AdminEditUserForm(activated='Active' if current_user.activated else 'Inactive')
        if form.validate_on_submit():
            data = form_data_to_dict (form.username.data, form.email.data, form.fName.data, form.lName.data, form.activated.data)
            if validate_request(data):
                if current_user.get_role() == 'admin':
                    admin = Admin.update_admin(current_user.id, data)
                elif not validate_mobile_number (form.mobile.data):
                    error = "Mobile number must be 8 numbers long"
                    return render_template ('home/edit_profile.html', form=form, error=error)
                elif current_user.get_role() == 'doctor':
                    data['mobile'] = form.mobile.data
                    doctor = Doctor.update_doctor(current_user.id, data)
                elif current_user.get_role() == 'patient':
                    data['mobile'] = form.mobile.data
                    patient = Patient.update_patient(current_user.id, data)
                elif current_user.get_role() == 'pharmacist':
                    data['mobile'] = form.mobile.data
                    pharmacist = Pharmacist.update_pharmacist(current_user.id, data)
                flash('Profile Updated Successfully')
                return redirect(url_for('home.profile'))

            error = "Data Validation Failed"
            return render_template ('home/profile.html', form=form, error=error)

        return render_template ('home/edit_profile.html', form=form)

    except KeyError as ke:
        print('Exception occured during profile update. Key Error: {}'.format(str(ke)))
        return render_template ('home/edit_profile.html', form=form, error='Internal Server Error: {}'.format(str(ke)))
    except AttributeError as ae:
        print('Exception occured during profile update. Attribute Error: {}'.format(str(ae)))
        return render_tempalte ('home/edit_profile.html', form=form, error='Internal Server Error: {}'.format(str(ae)))
    except Exception as e:
        print('Exception occured during profile update. Error: {}'.format(str(e)))
        return render_template ('home/edit_profile.html', form=form, error='Internal Server Error: {}'.format(str(e)))


@bp.route('/test/email', methods=['POST'])
def test_email():
    json_data = request.get_json()
    recipient = json_data['recipient']
    subject = json_data['subject']
    body = json_data['body']
    send_prescription_email (subject, recipient, body)
    return "Test Email Sent. Please check your inbox"

# convert form data to dictionary
def form_data_to_dict (username, email, fName, lName, activated):
    return {
        'username'   : username,
        'email'     : email,
        'fName'     : fName,
        'lName'     : lName,
        'activated' : activated
    }



def validate_request(req: dict):
    if 'fName' not in req or 'lName' not in req or 'username' not in req or  'email' not in req:
        return False
    return True



def validate_mobile_number (mobile: str):
    if not mobile:
        return False
    if len(mobile) != 8:
        return False
    return True
