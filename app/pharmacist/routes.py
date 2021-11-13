from app.pharmacist import bp
from flask import render_template, request, jsonify, flash, redirect, url_for
from flask_login import login_required, current_user
from flask_paginate import Pagination, get_page_parameter
from app.models import Prescription, Pharmacist, Medicine
from app.auth.forms import TokenIDForm

@bp.route('/pharmacist/dashboard', methods=['GET', 'POST'])
@login_required
def index():
    form = TokenIDForm()
    if form.validate_on_submit():
        tokenid = Prescription.query.filter_by (identifier=form.tokenid.data).first()
        return redirect(url_for('prescription.get_prescription_by_id', id=tokenid.pres_id))
    medList = Medicine.get_medicine()
    return render_template('pharmacist/dashboard.html', form=form, medList=medList)

@bp.route('/pharmacist/filter/<q>')
def filter_pharmacists(q):
    """
    # Filter pharmacists by keyword
    """
    pharmacists = Pharmacist.filter_pharmacist(q)
    return jsonify([p() for p in pharmacists]), 200


@bp.route('/pharmacist/<id>')
def get_pharmacist(id):
    """
    # Get pharmacist by acc_id
    """
    pharmacist = Pharmacist.get_pharmacist_by_acc_id(id)
    return jsonify(pharmacist()), 200

