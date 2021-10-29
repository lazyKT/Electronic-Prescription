from flask import render_template, request, jsonify
from flask_login import login_required

from app.models import Patient, User
from app.patient import bp


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
