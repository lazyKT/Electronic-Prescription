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


@bp.route('/create-prescriptions', methods=['GET', 'POST'])
@login_required
def create_get_prescriptions():
    try:
        if request.method == 'POST':
            data = request.get_json()
            
            if not validate_prescription(data):
                flash ('Missing Required Data')
                return render_template('prescription/create_prescriptions.html')

            prescription = Prescription(
                identifier=data['identifier'],
                medication=data['medication'],
                doc_id=current_user.id,
                pat_id=data['patient'],
                phar_id=data['pharmacist'],
                from_date=datetime.now() if 'from_date' not in data else datetime.strptime(data['from_date'], '%Y-%m-%d'),
                to_date=datetime.now() if 'to_date' not in data else datetime.strptime(data['to_date'], '%Y-%m-%d')
            )
            prescription.save()
            flash ('New Prescription Created!')
            return redirect(url_for('doctor.index'))

        return render_template('prescription/create_prescriptions.html')

    except ValueError as ke:
        print(ke)
        flash ('Internal Server Error [ValueErorr], {}'.format(str(ve)))
        return render_template('prescription/create_prescriptions.html')
    except KeyError as ke:
        print(ke)
        flash ('Internal Server Error [KeyErorr], {}'.format(str(ke)))
        return render_template('prescription/create_prescriptions.html')
    except AttributeError as ae:
        print(ae)
        flash ('Internal Server Error [AttributeErorr], {}'.format(str(ae)))
        return render_template('prescription/create_prescriptions.html')
    except Exception as e:
        print(e)
        flash ('Internal Server Error [Error], {}'.format(str(e)))
        return render_template('prescription/create_prescriptions.html')


@bp.route('/prescriptions')
@login_required
def get_all_prescriptions():
    prescriptions = Prescription.get_all_prescriptions()
    return jsonify([p() for p in prescriptions]), 200


@bp.route('/prescription/<id>')
def get_prescription_by_id(id):
    try:
        p = Prescription.query.filter_by(pres_id=id).first()
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
            qr_link=qr_link
        )

    except Exception as e:
        flash ('Error Encountered Viewing Prescription, {}'.format(str(e)))
        return redirect(url_for('doctor.index'))
