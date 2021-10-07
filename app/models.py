"""
: Database Models and Schemas
"""
from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User (UserMixin, db.Model):
    """
    : User Database Model and Schema
    """
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(200), index=True)
    email = db.Column(db.String(100), index=True, unique=True)
    mobile = db.Column(db.String(10))
    password = db.Column(db.String(128))
    type = db.Column(db.String(20))


    def __repr__(self):
        return '<User:Obj> {}_id:{}, fullname:{}, email:{}'.format(self.type, self.id, self.fullname, self.email)


    def set_password (self, pwd):
        """
        : hash and store user password
        """
        self.password = generate_password_hash(pwd)


    def check_password (self, pwd) -> bool:
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
