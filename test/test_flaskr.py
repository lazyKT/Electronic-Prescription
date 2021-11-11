import os
import tempfile

import pytest

from app import init_app, init_db
from datetime import datetime

@pytest.fixture
def client():
    db_fd, db_path = tempfile.mkstemp()
    app = init_app()

    with app.test_client() as client:
        with app.app_context():
            init_db()
        yield client

    os.close(db_fd)
    os.unlink(db_path)

def test_hello(client):
    response = client.get('/')
    assert response.status_code == 200