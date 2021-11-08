from flask import render_template, request, jsonify
from flask_login import login_required, current_user

from app.models import Patient, User
from app.patient import bp
from app.models import Prescription, Doctor, Patient, User

@bp.route('/patient/dashboard')
@login_required
def index():
    active_prescriptions = [p() for p in Prescription.get_active_prescriptions_by_patient(current_user.id)]
    expired_prescriptions = [p() for p in Prescription.get_expired_prescriptions_by_patient(current_user.id)]
    return render_template(
        'patient/dashboard.html',
        active_prescriptions=active_prescriptions,
        expired_prescriptions=expired_prescriptions
    )

@bp.route('/patient/filter/<q>')
def filter_user(q):
    print('query', q)
    patients = Patient.filter_patient(q)
    if len(patients) == 0:
        return "Not Found", 404
    return jsonify([patient() for patient in patients]), 200


@bp.route('/patient/all')
def get_all_patients():
    patients = Patient.get_all_patients()
    return {'patients': [p() for p in patients]}, 200
