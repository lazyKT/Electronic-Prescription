from app.doctor import bp
from flask import render_template, request, jsonify
from flask_login import login_required, current_user

from app.models import Prescription, Doctor, Patient, Pharmacist


@bp.route('/doctor/dashboard')
@login_required
def index():
    issued_prescriptions = [p() for p in Prescription.get_prescriptions_by_doctor(current_user.id)]
    monthly_issued_prescs = Doctor.get_monthly_issued_presc(month=10, doc_id=current_user.id)
    active_presc = Doctor.get_active_prescriptions(current_user.id)
    return render_template(
        'doctor/dashboard.html',
        issued_prescriptions=issued_prescriptions,
        total_issued=len(issued_prescriptions),
        monthly_issued=len(monthly_issued_prescs),
        active_presc=len(active_presc)
    )


@bp.route ('/doctor/filter/<q>')
def filter_doctor(q):
    return "Filter Doctor Route"


@bp.route ('/doctor/all')
def get_all_doctors():
    doctors = Doctor.get_all_doctors()
    return {'doctors': [d() for d in doctors]}, 200


@bp.route ('/doctor/prescriptions/<id>')
def get_all_prescriptions(id):
    # prescriptions = Prescription.get_prescriptions_by_doctor(id)
    doctor = Doctor.get_user_by_id(id)
    prescriptions = doctor.get_issued_prescriptions()
    return jsonify([pres() for pres in prescriptions]), 200
