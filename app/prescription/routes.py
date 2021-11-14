# -----
# Prescriptions Routes
# CREATE, RETERIVE, UPDATE, DELETE
# -----
from datetime import datetime
from flask import render_template, request, jsonify, flash, redirect, url_for
from flask_login import login_required, current_user

from app.prescription import bp
from app.models import Doctor, Patient, Pharmacist, Prescription, Medicine
from app.auth.forms import TokenIDForm
from app.utilities import validate_prescription, prepare_new_prescription_email
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
                total_price=data['totalPrice'],
                from_date=datetime.now() if 'from_date' not in data else datetime.strptime(data['from_date'], '%Y-%m-%d'),
                to_date=datetime.now() if 'to_date' not in data else datetime.strptime(data['to_date'], '%Y-%m-%d')
            )
            prescription.save()
            patient = Patient.get_patient_by_acc_id(data['patient'])

            if not patient:
                error='Invalid Patient Data'
                return jsonify({'message' : error})

            # prepare_new_prescription_email(patient, prescription.pres_id)
            flash ('New Prescription Created!')
            return redirect(url_for('doctor.index'))
        return render_template('prescription/create_prescriptions.html')

    except ValueError as ke:
        error = 'Internal Server Error [ValueErorr], {}'.format(str(ve))
        print(error)
        return jsonify({'message' : error}), 500
    except KeyError as ke:
        print(ke)
        error = 'Internal Server Error [KeyErorr], {}'.format(str(ke))
        print(error)
        return jsonify({'message' : error}), 500
    except AttributeError as ae:
        print(ae)
        error = 'Internal Server Error [AttributeErorr], {}'.format(str(ae))
        print(error)
        return jsonify({'message' : error}), 500
    except Exception as e:
        print(e)
        error = 'Internal Server Error [Error], {}'.format(str(e))
        print(error)
        return jsonify({'message' : error}), 500


@bp.route('/prescriptions')
# @login_required
def get_all_prescriptions():
    prescriptions = Prescription.get_all_prescriptions()
    return jsonify([p() for p in prescriptions]), 200


@bp.route('/medicines')
@login_required
def get_medicines():
    medicines = Medicine.get_medicine()
    return jsonify([med() for med in medicines]), 200


@bp.route('/prescription/<id>', methods=['POST', 'GET'])
@login_required
def get_prescription_by_id(id):
    try:
        p = Prescription.query.filter_by(pres_id=id).first()
        if request.method == "POST":
            p.status='Active'
            p.collected='Y'
            try:
                db.session.commit()
                flash ('Prescription Dispensed')
                form = TokenIDForm()
                return render_template('pharmacist/dashboard.html', form=form)
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
            pres_id=p.pres_id,
            total_price=p.total_price
        )
    except Exception as e:
        flash ('Error Encountered Viewing Prescription, {}'.format(str(e)))
        if current_user.role == "doctor":
            return redirect(url_for('doctor.index'))
        elif current_user.role == "pharmacist":
            return redirect(url_for('pharmacist.index'))


@bp.route('/prescription-qr/<id>')
def get_prescription_from_qr (id):
    try:
        p = Prescription.query.filter_by(pres_id=id).first()
        if request.method == "POST":
            p.status='Active'
            p.collected='Y'
            try:
                db.session.commit()
                form = TokenIDForm()
                flash ('Prescription Dispensed')
                return render_template('pharmacist/dashboard.html', form=form)
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
        qr_link = 'http://127.0.0.1:5000/prescription-qr/{}'.format(id)
        return render_template(
            'prescription/view_prescription_via_qr.html',
            prescription=p(),
            doctor=doctor_name,
            pharmacist=pharmacist_name,
            medications=medications,
            from_date=from_date_str,
            to_date=to_date_str,
            qr_link=qr_link,
            pres_id=p.pres_id,
            total_price=p.total_price
        )

    except Exception as e:
        flash ('Error Encountered Viewing Prescription, {}'.format(str(e)))
        if current_user.role == "doctor":
            return redirect(url_for('doctor.index'))
        elif current_user.role == "pharmacist":
            return redirect(url_for('pharmacist.index'))
