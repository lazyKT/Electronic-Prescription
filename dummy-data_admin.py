from app import db, init_app
from datetime import datetime
from app.models import Admin

app = init_app()

admins = (
  {
    'uName': 'Admin1',
    'fName': 'Admin1',
    'lName': 'Admin1',
    'email': 'admin1@site.com',
    'role': 'admin',
    'password' : 'admin',
    'gender' :'Male',
    'mobile': '12345678',
    'dob': datetime(1994, 10, 20, 10, 10, 10)
  },
  {
    'uName': 'Admin2',
    'fName': 'Admin2',
    'lName': 'Admin2',
    'email': 'admin2@site.com',
    'role': 'admin',
    'password' : 'admin',
    'gender' :'Female',
    'mobile': '12345678',
    'dob': datetime(1994, 10, 20, 10, 10, 10)
  }
)


with app.app_context():
  db.create_all()
  i = 0
  for a in admins:
    admin = Admin(
    username=a['uName'],
    fName=a['fName'],
    lName=a['lName'],
    email=a['email'],
    role=a['role'],
    gender=a['gender'],
    mobile=a['mobile'],
    dob=a['dob']
  ) 
    admin.set_password(a['password'])
    db.session.add(admin)
    db.session.commit()
    i += 1
  print("### {} admin(s) created".format(i)) 

