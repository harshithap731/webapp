import pytest
from app import create_app, db
from app.models import User, Assignment
from datetime import datetime
import base64


@pytest.fixture
def client():
    # Create a Flask app instance
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # In-memory database
    with app.test_client() as client:
        with app.app_context():
            db.create_all()  # Initialize the database
        yield client
        with app.app_context():
            db.session.remove()
            db.drop_all()


def get_auth_header(username, password):
    # Helper function to create Basic Auth header
    auth = f"{username}:{password}"
    auth_bytes = auth.encode('utf-8')
    auth_base64 = base64.b64encode(auth_bytes).decode('utf-8')
    return {"Authorization": f"Basic {auth_base64}"}


def test_create_user(client):
    response = client.post('/users', json={
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "password123"
    })
    assert response.status_code == 201
    assert response.get_json()["username"] == "testuser"


def test_get_users(client):
    # Create a user
    client.post('/users', json={
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "password123"
    })

    # Fetch users
    response = client.get('/users')
    assert response.status_code == 200
    users = response.get_json()
    assert len(users) == 1
    assert users[0]["username"] == "testuser"


def test_create_assignment(client):
    # Create a user
    client.post('/users', json={
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "password123"
    })

    # Authenticate and create an assignment
    response = client.post('/assignments', json={
        "title": "Test Assignment",
        "points": 10
    }, headers=get_auth_header("testuser", "password123"))

    assert response.status_code == 201
    assert response.get_json()["title"] == "Test Assignment"


def test_get_assignments(client):
    # Create a user
    client.post('/users', json={
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "password123"
    })

    # Authenticate and create an assignment
    client.post('/assignments', json={
        "title": "Test Assignment",
        "points": 10
    }, headers=get_auth_header("testuser", "password123"))

    # Fetch assignments
    response = client.get('/assignments')
    assert response.status_code == 200
    assignments = response.get_json()
    assert len(assignments) == 1
    assert assignments[0]["title"] == "Test Assignment"


def test_update_assignment(client):
    # Create a user
    client.post('/users', json={
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "password123"
    })

    # Authenticate and create an assignment
    client.post('/assignments', json={
        "title": "Test Assignment",
        "points": 10
    }, headers=get_auth_header("testuser", "password123"))

    # Authenticate and update the assignment
    response = client.put('/assignments/1', json={
        "title": "Updated Assignment",
        "points": 8
    }, headers=get_auth_header("testuser", "password123"))

    assert response.status_code == 200
    updated_assignment = response.get_json()
    assert updated_assignment["title"] == "Updated Assignment"
    assert updated_assignment["points"] == 8


def test_delete_assignment(client):
    # Create a user
    client.post('/users', json={
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "password123"
    })

    # Authenticate and create an assignment
    client.post('/assignments', json={
        "title": "Test Assignment",
        "points": 10
    }, headers=get_auth_header("testuser", "password123"))

    # Authenticate and delete the assignment
    response = client.delete('/assignments/1', headers=get_auth_header("testuser", "password123"))
    assert response.status_code == 204


def test_patch_not_allowed(client):
    response = client.patch('/assignments/1', json={
        "title": "Updated Assignment",
        "points": 5
    })
    assert response.status_code == 405
    assert response.get_json() == {"error": "PATCH method not allowed"}


def test_database_connection(client):
    with client.application.app_context():  # Push the app context
        result = db.session.execute("SELECT 1")
        assert result is not None

