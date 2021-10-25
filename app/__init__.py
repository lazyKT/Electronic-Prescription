from flask import Flask
from flask_admin import Admin, AdminIndexView, expose
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user


db = SQLAlchemy ()
login = LoginManager ()
login.login_view = 'auth.login'


class MyAdminIndexView(AdminIndexView):
    """
    # Overriding Flask AdminIndexView
    # This is the entry point to the admin pannel or Admin Home Page
    """

    @expose('/')
    def index(self):
        return self.render('admin/index.html')

    def is_accessible(self):
        if current_user.is_authenticated:
            return current_user.get_role() == 'admin'
        return False


# admin = Admin(name='e_prescription')
admin = Admin(name='e_prescription', index_view=MyAdminIndexView(
        name='Home',
        template='admin/index.html',
        url='/admin'
    ))


def init_db():
    """
    : Create and Initialize Database and Tables before the very first request comesin
    """
    print ("Creating Database ...")
    db.create_all()



def init_app ():
    """
    : Create and initialise an Flask App instance for the whole application
    """
    app = Flask (__name__, instance_relative_config=False)
    app.config.from_object ("config.Config")

    db.init_app (app)
    login.init_app (app)
    admin.init_app(app)

    with app.app_context ():
        # import routes
        from app.home import bp as home_bp
        from app.auth import bp as auth_bp
        from app.admin import bp as admin_bp
        from app.doctor import bp as doctor_bp

        # register blueprints
        app.register_blueprint (home_bp)
        app.register_blueprint (auth_bp)
        app.register_blueprint (admin_bp)
        app.register_blueprint (doctor_bp)

        return app
