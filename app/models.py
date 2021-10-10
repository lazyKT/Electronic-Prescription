"""
: Database Models and Schemas
"""
from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User (UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column (db.Integer, primary_key=True)
    username = db.Column (db.String(20), unique=True)
    password = db.Column (db.String(50))
    role = db.Column (db.String(10))
    activated = db.Column (db.Boolean, default=False)

    def set_password(self, pwd: str):
        """
        : Hash Password and Store in DB
        """
        self.password = generate_password_hash (pwd)

    def check_password(self, pwd: str) -> bool:
        """
        : check and compare passwords
        : @param (pwd) -> password provided by user during authentication
        : pwd will be compared against the hash password stored in database
        """
        return check_password_hash(self.password, pwd)


@login.user_loader
def load_user(id: int) -> object:
    """
    : Get Current Logged In User via flask-login
    """
    return User.query.get (id)


class Patient (User, db.Model):
    __tablename__ = 'patient'
    pat_id = db.Column (db.Integer, primary_key=True)
    fName = db.Column (db.String(100))
    lName = db.Column (db.String(100))
    # gender = db.Column (db.String(8))
    # email = db.Column (db.String(100), unique=True)
    # dob = db.Column (db.DateTime, nullable=False)
    account = db.relationship (User, backref=db.backref('patient_account'), uselist=False)
    acc_id = db.Column(db.ForeignKey(User.id))


    def __repr__(self):
        return 'Patient: {}'.format(self.lName)


class Allergy (db.Model):
    __tablename__ = 'allergy'
    allergy_id = db.Column (db.Integer, primary_key=True)
    allergy = db.Column (db.String(100))
    pat_id = db.Column (db.ForeignKey(Patient.pat_id))
    patient = db.relationship (Patient, backref=db.backref('patient'), uselist=True)


class Doctor (User, db.Model):
    __tablename__ = 'doctor'
    doc_id = db.Column (db.Integer, primary_key=True)
    fName = db.Column (db.String(100), nullable=False)
    lName = db.Column (db.String(100), nullable=False)
    # gender = db.Column (db.String(8))
    # email = db.Column (db.String(100), unique=True)
    account = db.relationship (User, backref=db.backref('doctor_account'), uselist=False)
    acc_id = db.Column(db.ForeignKey(User.id))

    def __repr__(self):
        return 'Doctor: {}'.format(self.lName)


class Pharmacist (User, db.Model):
    __tablename__ = 'pharmacist'
    phar_id = db.Column (db.Integer, primary_key=True)
    fName = db.Column (db.String(100), nullable=False)
    lName = db.Column (db.String(100), nullable=False)
    # gender = db.Column (db.String(8))
    # email = db.Column (db.String(100), unique=True)
    account = db.relationship (User, backref=db.backref('pharmacist_account'), uselist=False)
    acc_id = db.Column(db.ForeignKey(User.id))

    def __repr__(self):
        return 'Pharmacist: {}'.format(self.lName)


class Medicine (db.Model):
    """
    : Medicine Model and Schema
    """
    __tablename__ = 'medicine'
    med_id = db.Column (db.Integer, primary_key=True)
    medName = db.Column (db.String(256), nullable=False)
    expDate = db.Column (db.DateTime, nullable=False)
    price = db.Column (db.Float, nullable=False)
    description = db.Column (db.String(256))
    instructions = db.Column (db.String(256))
    quantity = db.Column (db.Integer, default=0)
