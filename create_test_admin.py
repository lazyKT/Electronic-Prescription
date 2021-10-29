from app import db, init_app
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
    role='admin'
  )

  admin.set_password('admin')
  db.session.add(admin)
  db.session.commit()
