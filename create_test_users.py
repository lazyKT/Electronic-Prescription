from app import init_app, db
from app.models import Admin, Patient, Pharmacist, Doctor

app = init_app()

admins = (
  {
    'fName': 'Admin',
    'lName': 'Admin',
    'email': 'admin@site.com',
    'role': 'admin',
    'password' : 'admin'
  },
  {
    'fName': 'Admin2',
    'lName': 'Admin2',
    'email': 'admin2@site.com',
    'role': 'admin',
    'password' : 'admin'
  }
)


with app.app_context():
  db.create_all()
  i = 0
  for a in admins:
    admin = Admin(fName=a['fName'], lName=a['lName'], email=a['email'], role=['role'])
    admin.set_password(a['password'])
    db.session.add(admin)
    db.session.commit()
    i += 1
  pritn("### {} admin(s) created".format(i)) 

