"""
: Database Models and Schemas
"""
from datetime import datetime
from app import db, login
from flask_login import UserMixin
from sqlalchemy import extract, or_
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
        self.activated = True if updated_user['status'] == 'active' else False
        db.session.commit()


    def delete_user(self):
        db.session.delete(self)
        db.session.commit()


    def get_account_status(self):
        return 'active' if self.activated else 'inactive'


    @classmethod
    def delete_user_by_id(cls, id):
        try:
            cls.query.filter_by(id=id).delete()
            # db.session.delete(user)
            db.session.commit()
        except Exception as e:
            raise(e)


    @classmethod
    def get_user_by_username (cls, username: str) -> object:
        """
        # Get User Object by username
        """
        return cls.query.filter_by(username=username).first()


    @classmethod
    def get_user_by_email (cls, email: str) -> object:
        """
        # Get User Object by email address
        """
        return cls.query.filter_by(email=email).first()


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


    def __call__(self):
        return {
            'id': self.acc_id,
            'fName': self.fName,
            'lName': self.lName,
            'email': self.email,
            'username': self.username
        }


    @classmethod
    def get_patient_by_acc_id(cls, acc_id):
        return cls.query.filter_by(acc_id=acc_id).first()


    @classmethod
    def update_patient(cls, acc_id, data):
        try:
            patient = cls.query.filter_by(acc_id=acc_id).first()
            print(data)
            patient.username = data['username']
            patient.email = data['email']
            patient.fName = data['fName']
            patient.lName = data['lName']
            patient.mobile = data['mobile']
            patient.activated = True if data['activated'] == 'Active' else False
            db.session.commit()
            return patient
        except Exception as e:
            print('Exception occured during update_patient', str(e))
            raise e


    @classmethod
    def get_all_patients(cls):
        return cls.query.all()


    @classmethod
    def filter_patient(cls, q):
        """
        # Filter Users by search query
        """
        print(q)
        patients = cls.query.filter(
            or_(
                cls.username.contains(q),
                cls.email.contains(q),
                cls.fName.contains(q),
                cls.lName.contains(q)
            )
        ).all()
        print(patients)
        return patients


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
    fName = db.Column (db.String(100))
    lName = db.Column (db.String(100))
    mobile = db.Column (db.String(16), nullable=False)
    gender = db.Column (db.String(8))
    email = db.Column (db.String(100), unique=True)
    dob = db.Column (db.DateTime, nullable=False)
    # account = db.relationship (User, backref=db.backref('admin_account', cascade="all,delete"), uselist=False)
    acc_id = db.Column (db.ForeignKey(User.id, ondelete='CASCADE'))

    __mapper_args__ = {
        'polymorphic_identity': 'admin'
    }

    def __repr__(self):
        return 'Admin: {}'.format(self.lName)


    @classmethod
    def get_admin_by_acc_id(cls, acc_id):
        return cls.query.filter_by(acc_id=acc_id).first()


    @classmethod
    def update_admin(cls, acc_id, data):
        admin = cls.query.filter_by(acc_id=acc_id).first()
        admin.username = data['username']
        admin.email = data['email']
        admin.fName = data['fName']
        admin.lName = data['lName']
        admin.activated = True if data['activated'] == 'Active' else False
        db.session.commit()
        return admin


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
    fName = db.Column (db.String(100))
    lName = db.Column (db.String(100))
    mobile = db.Column (db.String(16), nullable=False)
    gender = db.Column (db.String(8))
    email = db.Column (db.String(100), unique=True)
    dob = db.Column (db.DateTime, nullable=False)
    # account = db.relationship (User, backref=db.backref('doctor_account', cascade="all,delete"), uselist=False)
    acc_id = db.Column(db.ForeignKey(User.id, ondelete='CASCADE'))

    __mapper_args__ = {
        'polymorphic_identity': 'doctor'
    }

    def __repr__(self):
        return 'Doctor: {}'.format(self.lName)


    def get_issued_prescriptions(self):
        return Prescription.get_prescriptions_by_doctor(self.id)


    def get_patient_name(self, pat_id):
        patient = Patient.query.filter_by(pat_id=pat_id)
        return patient.fName


    @classmethod
    def get_doctor_by_acc_id(cls, acc_id):
        return cls.query.filter_by(acc_id=acc_id).first()


    @staticmethod
    def get_monthly_issued_presc(doc_id, month=1, year=2021):
        """
        # get prescriptions issued by month, year
        """
        return db.session.query(Prescription).filter(extract('month', Prescription.from_date)==month).filter_by(doc_id=doc_id).all()


    @classmethod
    def get_active_prescriptions(cls, doc_id):
        """
        # get all active Prescriptions by doctor id
        """
        return db.session.query(Prescription).filter_by(doc_id=doc_id).filter(Prescription.to_date > datetime.now()).all()


    @classmethod
    def get_all_doctors(cls):
        return cls.query.all()


    @classmethod
    def update_doctor(cls, acc_id, data):
        doctor = cls.query.filter_by(acc_id=acc_id).first()
        doctor.username = data['username']
        doctor.email = data['email']
        doctor.fName = data['fName']
        doctor.lName = data['lName']
        doctor.mobile = data['mobile']
        doctor.activated = True if data['activated'] == 'Active' else False
        db.session.commit()
        return doctor


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
    fName = db.Column (db.String(100))
    lName = db.Column (db.String(100))
    mobile = db.Column (db.String(16), nullable=False)
    gender = db.Column (db.String(8))
    email = db.Column (db.String(100), unique=True)
    dob = db.Column (db.DateTime, nullable=False)
    # account = db.relationship (User, backref=db.backref('pharmacist_account', cascade="all,delete"), uselist=False)
    acc_id = db.Column(db.ForeignKey(User.id, ondelete='CASCADE'))

    __mapper_args__ = {
        'polymorphic_identity': 'pharmacist'
    }

    def __repr__(self):
        return 'Pharmacist: {}'.format(self.lName)


    def __call__(self):
        return {
            'id': self.acc_id,
            'fName': self.fName,
            'lName': self.lName,
            'email': self.email,
            'username': self.username
        }


    @classmethod
    def get_pharmacist_by_acc_id(cls, acc_id):
        return cls.query.filter_by(acc_id=acc_id).first()


    @classmethod
    def filter_pharmacist(cls, q):
        return cls.query.filter(cls.fName.contains(q))


    @classmethod
    def get_all_pharmacists(cls):
        return cls.query.all()


    @classmethod
    def get_pharmacist_by_id(cls, id):
        return cls.query.filter_by(phar_id=id).first()


    @classmethod
    def update_pharmacist(cls, acc_id, data):
        pharmacist = cls.query.filter_by(acc_id=acc_id).first()
        pharmacist.username = data['username']
        pharmacist.email = data['email']
        pharmacist.fName = data['fName']
        pharmacist.lName = data['lName']
        pharmacist.mobile = data['mobile']
        pharmacist.activated = True if data['activated'] == 'Active' else False
        db.session.commit()
        return pharmacist


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
    medication = db.Column (db.String(256))
    status = db.Column (db.String(20))
    collected = db.Column (db.String(1))
    from_date = db.Column (db.DateTime, default=datetime.now())
    to_date = db.Column (db.DateTime, default=datetime.now())
    doc_id = db.Column (db.ForeignKey(Doctor.doc_id))
    pat_id = db.Column (db.ForeignKey(Patient.pat_id))
    phar_id = db.Column (db.ForeignKey(Pharmacist.phar_id))


    def __call__ (self):
        meds_count = len( self.medication.split(',') )
        if datetime.now() < self.to_date:
            status = self.status
        else:
            status='Expired'
            db.session.commit()
        patient_name = Patient.get_user_by_id(self.pat_id).fName
        return {
            'pres_id' : self.pres_id,
            'id' : self.identifier,
            'medication': self.medication,
            'meds_count': meds_count,
            'doctor': self.doc_id,
            'patient': self.pat_id,
            'p_name': patient_name,
            'phar_id': self.phar_id,
            'from_data': self.from_date,
            'to_date': self.to_date,
            'status': status,
            'collected': self.collected
        }

    def save(self):
        db.session.add(self)
        db.session.commit()


    def get_medication_list(self):
        medications = self.medication.split(',')
        return medications


    @classmethod
    def get_prescriptions_by_doctor(cls, doc_id):
        return cls.query.filter_by(doc_id=doc_id).order_by(cls.pres_id.desc()).all()

    @classmethod
    def get_active_prescriptions_by_patient(cls, pat_id):
        return cls.query.filter_by(pat_id=pat_id,status='Active',collected='Y').order_by(cls.pres_id.desc()).all()

    @classmethod
    def get_expired_prescriptions_by_patient(cls, pat_id):
        return cls.query.filter_by(pat_id=pat_id,status='Expired',collected='Y').order_by(cls.pres_id.desc()).all()

    @classmethod
    def get_all_prescriptions(cls):
        return cls.query.all()
