from app.models import User, Assignment
from datetime import datetime


def test_user_model():
    user = User(
        username="testuser",
        email="testuser@example.com",
        password="hashedpassword",
        account_created=datetime.utcnow(),
        account_updated=datetime.utcnow()
    )

    assert user.username == "testuser"
    assert user.email == "testuser@example.com"
    assert user.password == "hashedpassword"


def test_assignment_model():
    assignment = Assignment(
        title="Test Assignment",
        points=10,
        user_id=1,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )

    assert assignment.title == "Test Assignment"
    assert assignment.points == 10
    assert assignment.user_id == 1
