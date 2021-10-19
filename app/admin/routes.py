from flask import request, flash
from flask_admin.contrib.sqla import ModelView
from flask_admin import expose, BaseView
from flask_login import current_user


from app import db, admin
from app.models import User, Patient, Doctor, Pharmacist


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

    @expose('/', methods=['GET', 'POST'])
    def index(self):
        """
        # Admin User Pannel or Create new User by admin
        """
        if request.method == 'POST':
            """
            # Create New User
            """
            try:
                json_data = requset.get_json();
                if json_data['role'] == 'doctor':
                    # Create new doctor
                    new_doctor = Doctor(
                        username = json_data['username'],
                        email = json_data['email'],
                        role = json_data['role'],
                        fName = json_data['fName'],
                        lName = json_data['lName'],
                        mobile = json_data['mobile'],
                        gender = json_data['gender']
                    )
                    new_doctor.set_password(json_data['password'])
                    new_doctor.save()
                    return new_doctor(), 201
                elif json_data['role'] == 'pharmacist':
                    # Create new doctor
                    new_pharmacist = Pharmacist(
                        username = json_data['username'],
                        email = json_data['email'],
                        role = json_data['role'],
                        fName = json_data['fName'],
                        lName = json_data['lName'],
                        mobile = json_data['mobile'],
                        gender = json_data['gender']
                    )
                    new_pharmacist.set_password(json_data['password'])
                    new_pharmacist.save()
                    return new_pharmacist(), 201
            except ValueError as ve:
                return ve, 500
            except KeyError as ke:
                return ke, 500
            except AttributeError as ae:
                return ae, 500
            except:
                return "Error Creating New User.", 500

        users = User.get_all_users()
        return self.render('admin/user.html', users=users)


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
                flash('Successfully Updated for {}'.format(user))
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
admin.add_view(AdminUserView(User, db.session))
admin.add_view(AdminPatientView(Patient, db.session))
