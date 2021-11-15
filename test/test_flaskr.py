import os
import tempfile

import pytest

from flask import url_for, request
from flask_login import current_user
from app import init_app, init_db, admin
from app.models import Admin
from datetime import datetime

app = init_app()

@pytest.fixture
def client():
    db_fd, db_path = tempfile.mkstemp()
    with app.test_client() as client:
        with app.app_context():
            init_db()
        yield client

    os.close(db_fd)
    os.unlink(db_path)


def test_admin_login_logout (client):
    formdata = {'username' : 'admin', 'password': 'admin', 'remember_me': False}
    client.post('/login', data=formdata, follow_redirects=True)
    assert current_user.role == 'admin'
    assert request.path == url_for('admin.index')
    client.post('/logout', follow_redirects=True)

def test_doctor_login_logout(client):
    formdata = {'username': 'doctor1', 'password': 'password123', 'remember_me': False}
    client.post('/login', data=formdata, follow_redirects=True)
    assert current_user.role == 'doctor'
    assert request.path == url_for('doctor.index')
    client.post('/logout', follow_redirects=True)

def test_pharmacist_login_logout(client):
    formdata = {'username': 'pharmacist1', 'password': 'password123', 'remember_me': False}
    client.post('/login', data=formdata, follow_redirects=True)
    assert current_user.role == 'pharmacist'
    assert request.path == url_for('pharmacist.index')
    client.post('/logout', follow_redirects=True)

def test_patient_login_logout(client):
    formdata = {'username': 'patient1', 'password': 'password123', 'remember_me': False}
    client.post('/login', data=formdata, follow_redirects=True)
    assert current_user.role == 'patient'
    assert request.path == url_for('patient_bp.index')
    client.post('/logout', follow_redirects=True)
