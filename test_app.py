import sys
import os
import pytest

# garante que o app.py seja encontrado
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import app, db, User


@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()


# -------------------------
# TESTE 1: CADASTRO OK
# -------------------------
def test_register_success(client):
    response = client.post('/register', json={
        "name": "João",
        "email": "joao@email.com",
        "password": "123456"
    })

    assert response.status_code == 201


# -------------------------
# TESTE 2: EMAIL DUPLICADO
# -------------------------
def test_register_duplicate_email(client):
    client.post('/register', json={
        "name": "João",
        "email": "joao@email.com",
        "password": "123456"
    })

    response = client.post('/register', json={
        "name": "Outro",
        "email": "joao@email.com",
        "password": "123456"
    })

    assert response.status_code == 400


# -------------------------
# TESTE 3: LOGIN OK
# -------------------------
def test_login_success(client):
    client.post('/register', json={
        "name": "João",
        "email": "joao@email.com",
        "password": "123456"
    })

    response = client.post('/login', json={
        "email": "joao@email.com",
        "password": "123456"
    })

    assert response.status_code == 200


# -------------------------
# TESTE 4: LOGIN INVÁLIDO
# -------------------------
def test_login_invalid(client):
    response = client.post('/login', json={
        "email": "naoexiste@email.com",
        "password": "123"
    })

    assert response.status_code == 401