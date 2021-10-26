from app.doctor import bp
from app import db
from flask import render_template
from flask_login import login_required


@bp.route ('/dispense-prescription', methods=['GET', 'POST'])
@login_required
def create_prescriptions():
    return render_template('pharmacist/dispense_prescriptions.html')
