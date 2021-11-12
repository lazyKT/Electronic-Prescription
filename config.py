import os


base_dir = os.path.abspath (os.path.dirname(__file__))

class Config:
  TESTING = True
  DEBUG = True
  FLASK_ENV = "development"
  SECRET_KEY = "NobodyKnowsThisShhh!!"
  SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or 'sqlite:///' + os.path.join(base_dir, 'test.db');
  SQLALCHEMY_TRACK_MODIFICATIONS = False
  FLASK_ADMIN_SWATCH = 'cerulean'
  TEMPLATES_AUTO_RELOAD = True
  MAIL_SERVER="smtp.sendgrid.net"
  MAIL_PORT=587
  MAIL_USE_TLS=True
  MAIL_USERNAME='lwin'
  MAIL_PASSWORD=os.environ.get('E_PRESC_SENDGRID_API_KEY')
  MAIL_DEFAULT_SENDER='ktl141@uowmail.edu.au'
