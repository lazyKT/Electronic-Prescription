from app import db, init_app
from datetime import datetime
from app.models import Admin


app = init_app()

with app.app_context():
  # create all databases
  db.create_all()

  admin = Admin(
    username='admin',
    email = 'admin@site.com',
    fName='Admin',
    lName='Admin',
    role='admin',
    gender='Male',
    mobile='12345678',
    dob=datetime(1994, 10, 20, 10, 10, 10)
  )

  admin.set_password('admin')
  db.session.add(admin)
  db.session.commit()
