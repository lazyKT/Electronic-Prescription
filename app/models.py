"""
: Database Models and Schemas
"""
from datetime import datetime
from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User (UserMixin, db.Model):
    """
    : Base User Model and Schema for Admin, Doctor, Patient, Pharmacist
    """
    __tablename__ = 'user'
    id = db.Column (db.Integer, primary_key=True)
    username = db.Column (db.String(20), unique=True, nullable=False)
    password = db.Column (db.String(50), nullable=False)
    role = db.Column (db.String(10))
    activated = db.Column (db.Boolean, default=False)

    __mapper_args__ = {
        'polymorphic_identity' : 'user',
        'polymorphic_on' : role
    }

    def __repr__(self):
        return '[User] id: {}, username: {}'.format(self.id, self.username)

    def __call__(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'role': self.role,
            'status': self.activated
        }

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

    def save (self):
        """
        : Add user to database
        """
        print ('registering new user', self)
        db.session.add(self)
        db.session.commit()

    def get_role (self):
        return self.role


    def update_user(self, updated_user):
        self.username = updated_user['username']
        self.email = updated_user['email']
        self.role = updated_user['role']
        self.activated = True if updated_user['status'] == 'active' else False
        db.session.commit()


    @classmethod
    def delete_user_by_id(cls, id):
        try:
            cls.query.filter_by(id=id).delete()
            # db.session.delete(user)
            db.session.commit()
        except Exception as e:
            raise(e)


    def delete_user(self):
        db.session.delete(self)
        db.session.commit()


    def get_account_status(self):
        return 'active' if self.activated else 'inactive'


    @classmethod
    def get_user_by_username (cls, username: str) -> object:
        """
        # Get User Object by username
        """
        return cls.query.filter_by(username=username).frist()


    @classmethod
    def get_user_by_id (cls, id):
        """
        # Get user by id
        """
        return cls.query.filter_by(id=id).first()

    @classmethod
    def get_all_users (cls):
        return cls.query.all()


@login.user_loader
def load_user(id: int) -> object:
    """
    : Get Current Logged In User via flask-login
    """
    return User.query.get (id)


class Patient (User):
    __tablename__ = 'patient'
    pat_id = db.Column (db.Integer, primary_key=True)
    fName = db.Column (db.String(100))
    lName = db.Column (db.String(100))
    mobile = db.Column (db.String(16), nullable=False)
    gender = db.Column (db.String(8))
    email = db.Column (db.String(100), unique=True)
    dob = db.Column (db.DateTime, nullable=False)
    # on deletion, cascade="all,delete" is executed when we use db.session.delete()
    # account = db.relationship (User, backref=db.backref('patient_account', cascade="all,delete"), uselist=False)
    # on deletion, ondelete='CASCADE' is executed when we use query.filter_by('').delete()
    acc_id = db.Column(db.ForeignKey(User.id, ondelete='CASCADE'))

    __mapper_args__ = {
        'polymorphic_identity': 'patient'
    }

    def __repr__(self):
        return 'Patient: {}'.format(self.lName)

    @classmethod
    def delete_patient(cls, acc_id):
        try:
            patient = cls.query.filter_by(acc_id=acc_id).delete()
            db.session.delete(patient)
            db.session.commit()
        except Exception as e:
            raise(e)

    def save(self):
        """
        : Save Patient to database
        """
        print ('saving patient data', self)
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_patient_by_email (cls, email: str) -> object:
        """
        : Get Patient by email address
        """
        return Patient.query.filter_by (email=email)


class Allergy (db.Model):
    """
    : Patient_Allergy Model and Schema
    """
    __tablename__ = 'allergy'
    allergy_id = db.Column (db.Integer, primary_key=True)
    allergy = db.Column (db.String(100))
    pat_id = db.Column (db.ForeignKey(Patient.pat_id))
    patient = db.relationship (Patient, backref=db.backref('patient_allergy'), uselist=False)


class MedHistory (db.Model):
    """
    : Patient_Mediacation_History Model and Schema
    """
    __tablename__ = 'medhistory'
    medHist_id = db.Column (db.Integer, primary_key=True)
    medHistory = db.Column (db.String(256))
    pat_id = db.Column (db.ForeignKey(Patient.pat_id))
    patient = db.relationship (Patient, backref=db.backref('patient_med_history'), uselist=False)


class Admin (User):
    """
    : Admin Model and Schema
    """
    __tablename__ = 'admin'
    adm_id = db.Column (db.Integer, primary_key=True)
    fName = db.Column (db.String(100), nullable=False)
    lName = db.Column (db.String(100), nullable=False)
    email = db.Column (db.String(100), unique=True)
    # account = db.relationship (User, backref=db.backref('admin_account', cascade="all,delete"), uselist=False)
    acc_id = db.Column (db.ForeignKey(User.id, ondelete='CASCADE'))

    __mapper_args__ = {
        'polymorphic_identity': 'admin'
    }

    def __repr__(self):
        return 'Admin: {}'.format(self.lName)


    @classmethod
    def delete_admin(cls, acc_id):
        try:
            admin = cls.query.filter_by(acc_id=acc_id).first()
            db.session.delete(admin)
            db.session.commit()
        except Exception as e:
            raise(e)


class Doctor (User):
    """
    : Docter Model and Schema
    """
    __tablename__ = 'doctor'
    doc_id = db.Column (db.Integer, primary_key=True)
    fName = db.Column (db.String(100), nullable=False)
    lName = db.Column (db.String(100), nullable=False)
    mobile = db.Column (db.String(16), nullable=False)
    gender = db.Column (db.String(8))
    email = db.Column (db.String(100), unique=True)
    # account = db.relationship (User, backref=db.backref('doctor_account', cascade="all,delete"), uselist=False)
    acc_id = db.Column(db.ForeignKey(User.id, ondelete='CASCADE'))

    __mapper_args__ = {
        'polymorphic_identity': 'doctor'
    }

    def __repr__(self):
        return 'Doctor: {}'.format(self.lName)


    def getIssuedPrescriptions(self):
        return [
                  {
                    'id': 1,
                    'doctor': "OG King",
                    'patient': "Susan",
                    'pharmacist': "Guardians",
                    'medicine': ["Panadol", "Biogesic", "Number 1", "Dicogen"],
                    'meds': 4,
                    'from_date': "2021-10-14",
                    'to_date': "2021-11-14",
                    'status': "active"
                  },
                  {
                    'id': 2,
                    'doctor': "OG King",
                    'patient': "David",
                    'pharmacist': "Watsons",
                    'medicine': ["Panadol", "Biogesic", "Number 1", "Dicogen"],
                    'meds': 4,
                    'from_date': "2021-09-21",
                    'to_date': "2021-12-14",
                    'status': "active"
                  },
                  {
                    'id': 3,
                    'doctor': "OG King",
                    'patient': "Guzman",
                    'pharmacist': "NTUC",
                    'medicine': ["Panadol", "Biogesic", "Number 1", "Dicogen", "Fluza"],
                    'meds': 5,
                    'from_date': "2021-08-14",
                    'to_date': "2021-11-14",
                    'status': "expired"
                  },
                  {
                    'id': 4,
                    'doctor': "OG King",
                    'patient': "Salmon",
                    'pharmacist': "NTUC",
                    'medicine': ["Panadol", "Fluza"],
                    'meds': 2,
                    'from_date': "2021-08-14",
                    'to_date': "2021-11-14",
                    'status': "active"
                  },
                  {
                    'id': 5,
                    'doctor': "OG King",
                    'patient': "Serah",
                    'pharmacist': "NTUC",
                    'medicine': ["Panadol", "Dicogen", "Fluza"],
                    'meds': 3,
                    'from_date': "2021-10-14",
                    'to_date': "2021-10-24",
                    'status': "expired"
                  }
                ]


    @classmethod
    def delete_doctor(cls, acc_id):
        try:
            doc = cls.query.filter_by(acc_id=acc_id).first()
            db.session.delete(doc)
            db.session.commit()
        except Exception as e:
            raise(e)



class Pharmacist (User):
    """
    : Pharmacist Model and Schema
    """
    __tablename__ = 'pharmacist'
    phar_id = db.Column (db.Integer, primary_key=True)
    fName = db.Column (db.String(100), nullable=False)
    lName = db.Column (db.String(100), nullable=False)
    mobile = db.Column (db.String(16), nullable=False)
    gender = db.Column (db.String(8))
    email = db.Column (db.String(100), unique=True)
    # account = db.relationship (User, backref=db.backref('pharmacist_account', cascade="all,delete"), uselist=False)
    acc_id = db.Column(db.ForeignKey(User.id, ondelete='CASCADE'))

    __mapper_args__ = {
        'polymorphic_identity': 'pharmacist'
    }

    def __repr__(self):
        return 'Pharmacist: {}'.format(self.lName)


    @classmethod
    def get_pharmacist_by_id(cls, id):
        return cls.query.filter_by(phar_id=id).first()


    @classmethod
    def delete_pharmacist(cls, acc_id):
        try:
            phar = cls.query.filter_by(acc_id=acc_id).first()
            db.session.delete(phar)
            db.session.commit()
        except Exception as e:
            raise(e)


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


class Prescription (db.Model):
    """
    : Prescription Model and Schema
    """
    __tablename__ = 'prescription'
    pres_id = db.Column (db.Integer, primary_key=True)
    identifier = db.Column (db.String(16))
    date = db.Column (db.DateTime, default=datetime.now())
    quantity = db.Column (db.Integer, default=0)
    patient = db.relationship (Patient, backref=db.backref('patient_prescription'), uselist=False)
    doctor = db.relationship (Doctor, backref=db.backref('doctor'), uselist=False)
    pharmacist = db.relationship (Pharmacist, backref=db.backref('pharmacist'), uselist=False)
    medicine = db.relationship (Medicine, backref=db.backref('medcine'), uselist=True)
    doc_id = db.Column (db.ForeignKey(Doctor.doc_id))
    pat_id = db.Column (db.ForeignKey(Patient.pat_id))
    phar_id = db.Column (db.ForeignKey(Pharmacist.phar_id))
    med_id = db.Column (db.ForeignKey(Medicine.med_id))
