from app import db
from app.models import Admin

# create all databases
db.create_all()

admin = Admin(
  username='admin',
  email = 'admin@site.com',
  fName='Admin',
  lName='Admin',
  role='admin'
)

admin.set_password('admin')
db.session.add(admin)
db.session.commit()
