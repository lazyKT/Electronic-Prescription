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
