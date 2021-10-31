from app.home import bp
from app import db
from flask import render_template, redirect, url_for, request, jsonify
from flask_login import login_required, current_user

from app.models import User, Patient, Doctor, Pharmacist, Admin


@bp.before_app_first_request
def before_app():
    print("Before App First Request")
    db.create_all()


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
          return redirect(url_for('patient.index'))
  return render_template ('home/index.html')

@bp.route('/profile')
@login_required
def profile():
    return render_template ('home/profile.html')

@bp.route('/edit/<id>', methods=['GET', 'PUT'])
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
            patient = Patient.update_patient(id, data)
            return jsonify(patient()), 201
        if user.get_role() == 'admin':
            # update admin
            admin = Admin.update_admin(id, data)
            return jsonify(admin()), 201
        if user.get_role() == 'pharmacist':
            # update pharmacist
            pharmacist = Pharmacist.update_pharmacist(id, data)
            return jsonify(pharmacist()), 201
        if user.get_role() == 'doctor':
            # update doctor
            doctor = Doctor.update_doctor(id, data)
            return jsonify(doctor()), 201
        return "Invalid user role", 400


def validate_request(req):
    print(req)
    if 'fName' not in req or 'lName' not in req or 'username' not in req or  'email' not in req:
        return False
    return True
