from flask import render_template, request, jsonify, flash, redirect, url_for
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

# API
@bp.route('/patient/filter/<q>')
def filter_user(q):
    try:
        patients = Patient.filter_patient(q)
        return jsonify([patient() for patient in patients]), 200

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

# Tempalte and API
@bp.route('/patients')
def search_patients():
    q = request.args.get('filter')
    if q and q != '':
        patients = Patient.filter_patient(q)
        if len(patients) == 0:
            return jsonify({'message' : 'Not Found'}), 404
        return jsonify([patient() for patient in patients]), 200
    else:
        patients = Patient.get_all_patients()
        return {'patients': [p() for p in patients]}, 200


@bp.route('/patient/all')
def get_all_patients():
    patients = Patient.get_all_patients()
    return {'patients': [p() for p in patients]}, 200



@bp.route('/patients/prescriptions/<id>')
def get_patient_prescriptions(id):
    try:
        patient = Patient.get_patient_by_acc_id(id)
        if not patient:
            flash ("Patient Not Found!")
            return redirect(url_for('doctor.search_patients'));
        fullname = '{} {}'.format(patient.fName, patient.lName)
        prescriptions = [p() for p in Prescription.get_all_prescriptions_by_patient(id)]
        print(prescriptions)
        # return jsonify(prescriptions)
        return render_template ('patient/prescriptions.html', p_name=fullname, prescriptions=prescriptions)

    except ValueError as ke:
        print(ke)
        flash('Internal Server Error [ValueErorr], {}'.format(str(ve)))
        return redirect(url_for('doctor.search_patients'));
    except KeyError as ke:
        print(ke)
        flash('Internal Server Error [KeyErorr], {}'.format(str(ke)))
        return redirect(url_for('doctor.search_patients'));
    except AttributeError as ae:
        print(ae)
        flash('Internal Server Error [AttributeErorr], {}'.format(str(ae)))
        return redirect(url_for('doctor.search_patients'));
    except Exception as e:
        print(e)
        flash('Internal Server Error [Error], {}'.format(str(e)))
        return redirect(url_for('doctor.search_patients'));
