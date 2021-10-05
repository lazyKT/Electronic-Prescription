from app.home import bp
from flask import render_template


@bp.route ("/")
@bp.route ("/index")
def index():
  """
  : Web Site Root/Home Page
  """
  return render_template ('home/index.html')
