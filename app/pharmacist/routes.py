from flask import render_template, jsonify
from flask_login import login_required

from app.pharmacist import bp
from app.models import Pharmacist



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
