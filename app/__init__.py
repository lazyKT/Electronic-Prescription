from flask import Flask
from flask_admin import Admin, AdminIndexView, expose
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from flask_qrcode import QRcode


db = SQLAlchemy ()
qr = QRcode ()
login = LoginManager ()
login.login_view = 'auth.login'


admin = Admin(name='e_prescription')


def init_db():
    """
    : Create and Initialize Database and Tables before the very first request comesin
    """
    db.create_all()



def init_app ():
    """
    : Create and initialise an Flask App instance for the whole application
    """
    app = Flask (__name__, instance_relative_config=False)
    app.config.from_object ("config.Config")

    db.init_app (app)
    login.init_app (app)
    qr.init_app (app)
    admin.init_app (app)

    with app.app_context ():
        # import routes
        from app.home import bp as home_bp
        from app.auth import bp as auth_bp
        from app.admin import bp as admin_bp
        from app.doctor import bp as doctor_bp
        from app.patient import bp as patient_bp
        from app.prescription import bp as pres_bp
        from app.pharmacist import bp as phar_bp

        # register blueprints
        app.register_blueprint (home_bp)
        app.register_blueprint (auth_bp)
        app.register_blueprint (admin_bp)
        app.register_blueprint (doctor_bp)
        app.register_blueprint (patient_bp)
        app.register_blueprint (pres_bp)
        app.register_blueprint (phar_bp)

        return app
