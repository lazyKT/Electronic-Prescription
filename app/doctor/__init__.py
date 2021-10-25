from flask import Blueprint

bp = Blueprint('doctor', __name__)

from app.doctor import routes
