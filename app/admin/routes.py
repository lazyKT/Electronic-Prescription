from flask import request, flash, redirect, url_for
from flask_admin.contrib.sqla import ModelView
from flask_admin import expose, BaseView
from flask_login import current_user


from app import db, admin
from app.models import User, Patient, Doctor, Pharmacist
from app.auth.forms import AdminCreateUserForm



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
        # Admin User Pannel to manage users
        """
        users = User.get_all_users()
        # return "users"
        # return {'users': [user() for user in users]}
        return self.render('admin/user.html', users=users)


    @expose('/add', methods=['GET', 'POST'])
    def create_user(self):
        form = AdminCreateUserForm()
        
        if form.validate_on_submit():
            """
            # Create New User
            """
            try:
                if form.user_role.data == 'Doctor':
                    # Create new doctor
                    new_doctor = Doctor(
                        username = form.username.data,
                        email = form.email.data,
                        role = 'doctor',
                        fName = form.fName.data,
                        lName = form.lName.data,
                        mobile = form.mobile.data,
                        gender = form.gender.data
                    )
                    new_doctor.set_password(form.password.data)
                    new_doctor.save()

                    flash ('New User Created. [info] {}'.format(new_doctor))
                    return redirect(url_for('user.index'))
                elif form.user_role.data == 'Pharmacist':
                    # Create new doctor
                    new_pharmacist = Pharmacist(
                        username = form.username.data,
                        email = form.email.data,
                        role = 'pharmacist',
                        fName = form.fName.data,
                        lName = form.lName.data,
                        mobile = form.mobile.data,
                        gender = form.gender.data
                    )
                    new_pharmacist.set_password(form.password.data)
                    new_pharmacist.save()

                    flash ('New User Created. [info] {}'.format(new_pharmacist))
                    return redirect(url_for('user.index'))

            except ValueError as ve:
                return self.render('admin/user_regis_form.html', form=form, error='Internal Server Error: [ValueError] {}'.format(str(ve)))
            except KeyError as ke:
                return self.render('admin/user_regis_form.html', form=form, error='Internal Server Error: [KeyError] {}'.format(str(ke)))
            except AttributeError as ae:
                return self.render('admin/user_regis_form.html', form=form, error='Internal Server Error: [AttrubuteError] {}'.format(str(ae)))
            except Exception as e:
                return self.render('admin/user_regis_form.html', form=form, error='Internal Server Error. Please try again')

        return self.render('admin/user_regis_form.html', form=form)


    @expose('/<id>', methods=['PUT', 'GET'])
    def updateUser(self, id):
        print('request method', request.method)
        if request.method == 'PUT':
            try:
                user = User.get_user_by_id(id)
                print(user)
                if user is None:
                    return "User not found!", 404
                json_data = request.get_json();
                print(json_data)
                user.update_user(json_data)
                return user(), 200
            except KeyError as ke:
                print(ke)
                return "KeyError", 500
            except AttributeError as ae:
                print(ae)
                return "AttributeError", 500
            except:
                return "Update Failed. Internal Serve Error", 500
        elif request.method == 'GET':
            return "Updating user"


class AdminPatientView(MyAdminView):

    @expose('/')
    def index(self):
        return 'Patient'


# admin.add_view(AdminIndexView(name="E Prescription", endpoint="index"))
admin.add_view(AdminUserView(User, db.session, endpoint='user'))
admin.add_view(AdminPatientView(Patient, db.session))
