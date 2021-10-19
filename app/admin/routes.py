from flask_admin.contrib.sqla import ModelView
from flask_admin import expose, BaseView
from flask_login import current_user


from app import db, admin
from app.models import User, Patient


class MyAdminView(ModelView):

    @expose('/')
    def index(self):
        return self.render('admin/index.html')

    def is_accessible(self):
        print(current_user.is_authenticated)
        if current_user.is_authenticated:
            return current_user.get_role() == 'admin'
        return False



class AdminUserView(MyAdminView):

    @expose('/')
    def index(self):
        """
        # Admin User Pannel
        """
        users = User.get_all_users()
        return self.render('admin/user.html', users=users)


class AdminPatientView(MyAdminView):

    @expose('/')
    def index(self):
        return 'Patient'


# admin.add_view(AdminIndexView(name="E Prescription", endpoint="index"))
admin.add_view(AdminUserView(User, db.session))
admin.add_view(AdminPatientView(Patient, db.session))
