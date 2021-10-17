from flask_admin.contrib.sqla import ModelView
from flask_admin import expose
from flask_login import current_user


from app import db, admin
from app.models import User, Patient


class MyAdminView(ModelView):

    @expose('/')
    def index(self):
        return 'Admin'

    def is_accessible(self):
        return True


class AdminUserView(MyAdminView):

    @expose('/')
    def index(self):
        return 'User'


class AdminPatientView(MyAdminView):

    @expose('/')
    def index(self):
        return 'Patient'


admin.add_view(AdminUserView(User, db.session))
admin.add_view(AdminPatientView(Patient, db.session))
