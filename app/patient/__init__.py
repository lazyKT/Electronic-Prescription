from flask import Blueprint

bp = Blueprint('patient_bp', __name__)

from app.patient import routes
