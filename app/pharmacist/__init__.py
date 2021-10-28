from flask import Blueprint

bp = Blueprint('pharmacist', __name__)

from app.pharmacist import routes
