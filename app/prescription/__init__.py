from flask import Blueprint


bp = Blueprint('prescription', __name__)


from app.prescription import routes
