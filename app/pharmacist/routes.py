from flask import render_template, jsonify
from flask_login import login_required

from app.pharmacist import bp
from app.models import Pharmacist



@bp.route('/pharmacist/filter/<q>')
def filter_pharmacists(q):
    pharmacists = Pharmacist.filter_pharmacist(q)
    return jsonify([p() for p in pharmacists]), 200
