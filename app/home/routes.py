from app.home import bp
from app import db
from flask import render_template
from flask_login import login_required


@bp.before_app_first_request
def before_app():
    print("Before App First Request")
    db.create_all()


@bp.route ('/')
@bp.route ('/index')
def index():
  """
  : Web Site Root/Home Page
  """
  return render_template ('home/index.html')


@bp.route('/contact')
def contact():
    return render_template ('home/contact.html')


@bp.route('/profile')
@login_required
def profile():
    return render_template ('home/profile.html')
