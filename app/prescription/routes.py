# -----
# Prescriptions Routes
# CREATE, RETERIVE, UPDATE, DELETE
# -----
from flask import render_template, request, jsonify
from flask_login import login_required

from app.prescription import bp
from app.models import Doctor, Patient, Pharmacist, Prescription


@bp.route('/create-prescriptions', methods=['GET', 'POST'])
def create_get_prescriptions():
    if request.method == 'POST':
        data = request.get_json()
        prescription = Prescription(
            identifier=data['identifier'],
            medication=data['medication'],
            doc_id=data['doctor'],
            pat_id=data['patient'],
            phar_id=data['pharmacist']
        )
        if 'from_date' in data:
            prescription.from_date = data['from_date']
        if 'to_date' in data:
            prescription.to_date = data['to_date']
        prescription.save()
        return jsonify(prescription()), 201

    return render_template('prescription/create_prescriptions.html')


@bp.route('/prescriptions')
def get_all_prescriptions():
    prescriptions = Prescription.get_all_prescriptions()
    return jsonify([p() for p in prescriptions]), 200


@bp.route('/prescription/<id>')
def get_prescription_by_id(id):
    p = Prescription.query.filter_by(pres_id=id).first()
    return jsonify(p()), 200
