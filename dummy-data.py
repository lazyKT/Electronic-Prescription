from data_scripts.doctor_data import *
from data_scripts.patient_data import *
from data_scripts.admin_data import *
from data_scripts.pharmacist_data import *
from data_scripts.med_data import *
from app import db, init_app
from app.models import Admin, Doctor, Patient, Pharmacist, Medicine

app = init_app()

with app.app_context():
  db.create_all()
  uCount = 0
  mCount = 0
  for a in admin:
    user = Admin(
    username=a['uName'],
    fName=a['fName'],
    lName=a['lName'],
    email=a['email'],
    role=a['role'],
    gender=a['gender'],
    mobile=a['mobile'],
    dob=a['dob']
    ) 
    user.set_password(a['password'])
    db.session.add(user)
    db.session.commit()
    uCount += 1
  for a in pharmacist:
    user = Pharmacist(
    username=a['uName'],
    fName=a['fName'],
    lName=a['lName'],
    email=a['email'],
    role=a['role'],
    gender=a['gender'],
    mobile=a['mobile'],
    dob=a['dob']
    ) 
    user.set_password(a['password'])
    db.session.add(user)
    db.session.commit()
    uCount += 1
  for a in doctor:
    user = Doctor(
    username=a['uName'],
    fName=a['fName'],
    lName=a['lName'],
    email=a['email'],
    role=a['role'],
    gender=a['gender'],
    mobile=a['mobile'],
    dob=a['dob']
    ) 
    user.set_password(a['password'])
    db.session.add(user)
    db.session.commit()
    uCount += 1
  for a in patient:
    user = Patient(
    username=a['uName'],
    fName=a['fName'],
    lName=a['lName'],
    email=a['email'],
    role=a['role'],
    gender=a['gender'],
    mobile=a['mobile'],
    dob=a['dob']
    ) 
    user.set_password(a['password'])
    db.session.add(user)
    db.session.commit()
    uCount += 1
  for a in medicine:
    med = Medicine(
    medName=a['medName'],
    expDate=a['expDate'],
    price=a['price'],
    description=a['description'],
    instructions=a['instructions'],
    quantity=a['quantity']
    ) 
    db.session.add(med)
    db.session.commit()
    mCount += 1
  print("### {} user(s) created".format(uCount)) 
  print("### {} medicine(s) created".format(mCount)) 

