# -----
# Prescriptions Routes
# CREATE, RETERIVE, UPDATE, DELETE
# -----
from datetime import datetime
from flask import render_template, request, jsonify, flash, redirect, url_for
from flask_login import login_required, current_user

from app.prescription import bp
from app.models import Doctor, Patient, Pharmacist, Prescription
from app.utilities import validate_prescription
from app import db


@bp.route('/create-prescriptions', methods=['GET', 'POST'])
@login_required
def create_get_prescriptions():
    try:
        if request.method == 'POST':
            data = request.get_json()
            if not validate_prescription(data):
                error='Missing Required Data!'
                return jsonify({'message' : error})
            prescription = Prescription(
                identifier=data['identifier'],
                medication=data['medication'],
                doc_id=current_user.id,
                status='Pending',
                pat_id=data['patient'],
                phar_id=data['pharmacist'],
                collected='N',
                from_date=datetime.now() if 'from_date' not in data else datetime.strptime(data['from_date'], '%Y-%m-%d'),
                to_date=datetime.now() if 'to_date' not in data else datetime.strptime(data['to_date'], '%Y-%m-%d')
            )
            prescription.save()
            flash ('New Prescription Created!')
            return redirect(url_for('doctor.index'))
        return render_template('prescription/create_prescriptions.html')

    except ValueError as ke:
        print(ke)
        error = 'Internal Server Error [ValueErorr], {}'.format(str(ve))
        return jsonify({'message' : error})
    except KeyError as ke:
        print(ke)
        error = 'Internal Server Error [KeyErorr], {}'.format(str(ke))
        return jsonify({'message' : error})
    except AttributeError as ae:
        print(ae)
        error = 'Internal Server Error [AttributeErorr], {}'.format(str(ae))
        return jsonify({'message' : error})
    except Exception as e:
        print(e)
        error = 'Internal Server Error [Error], {}'.format(str(e))
        return jsonify({'message' : error})


@bp.route('/prescriptions')
@login_required
def get_all_prescriptions():
    prescriptions = Prescription.get_all_prescriptions()
    return jsonify([p() for p in prescriptions]), 200

@bp.route('/prescription/<id>', methods=['POST', 'GET'])
def get_prescription_by_id(id):
    try:
        p = Prescription.query.filter_by(pres_id=id).first()
        if request.method == "POST":
            p.status='Active'
            p.collected='Y'
            try:
                db.session.commit()
                flash ('Prescription Dispensed')
                return render_template('pharmacist/dashboard.html')
            except Exception as e:
                flash ('Error Encountered Viewing Prescription, {}'.format(str(e)))
                return redirect(url_for('pharmacist.index'))
        doctor = Doctor.get_doctor_by_acc_id(p.doc_id)
        pharmacist = Pharmacist.get_pharmacist_by_acc_id(p.phar_id)
        doctor_name = doctor.fName if doctor else 'NA' # if the doctor is not in the system anymore (acc deleted), show NA as doctor name
        pharmacist_name = pharmacist.fName if pharmacist else 'NA' # if the pharmacist is not in the system anymore (acc deleted), show NA as pharmacist name
        medications = p.get_medication_list()
        from_date_str = datetime.strftime(p.from_date, '%Y-%m-%d')
        to_date_str = datetime.strftime(p.to_date, '%Y-%m-%d')
        qr_link = 'http://127.0.0.1:5000/prescription/{}'.format(id)
        return render_template(
            'prescription/view_prescription.html',
            prescription=p(),
            doctor=doctor_name,
            pharmacist=pharmacist_name,
            medications=medications,
            from_date=from_date_str,
            to_date=to_date_str,
            qr_link=qr_link,
            pres_id=p.pres_id
        )
    except Exception as e:
        flash ('Error Encountered Viewing Prescription, {}'.format(str(e)))
        if current_user.role == "doctor":
            return redirect(url_for('doctor.index'))
        elif current_user.role == "pharmacist":
            return redirect(url_for('pharmacist.index'))
