import pytest
from fastapi import HTTPException
from .config_test import app, db_session, client  # pylint: disable=unused-import

from app.schemas.user import UserCreateDTO
from app.database.crud.user import user_crud
from pytest import fixture
from app.schemas.user import UserCreateDTO
from .config_test import app, db_session, client  # pylint: disable=unused-import
from app.core.logger import log

@fixture
def user():
    user = UserCreateDTO(
        full_name="pytest_user", email="user@example.com", password="%20"
    )
    return user


def test_create_user(client, user):
    response = client.post(
        "api/v1/login/register",
        json={
            "full_name": user.full_name,
            "email": user.email,
            "password": user.password,
        },
    )
    assert response.status_code == 200


class TestCreateUser:
    # Tests that a new user can be created with valid data
    def test_create_user_valid_data(self):
        user_data = UserCreateDTO(
            full_name="John Doe", email="johndoe@example.com", password="password123"
        )
        response = user_crud.create(db_session, user_data)
        assert response.email == user_data.email
        assert response.full_name == user_data.full_name

    # Tests that a new user can be created with valid data and password
    def test_create_user_valid_data_and_password(self):
        user_data = UserCreateDTO(
            full_name="John Doe", email="johndoe@example.com", password="password123"
        )
        response = user_crud.create(db_session, user_data)
        assert response.email == user_data.email
        assert response.full_name == user_data.full_name
        assert response.password != user_data.password

    # Tests that an error is raised when creating a new user with an email that already exists
    def test_create_user_email_already_exists(self):
        user_data = {
            "full_name": "John Doe",
            "email": "johndoe@example.com",
            "password": "password123",
        }
        with pytest.raises(HTTPException):
            user_crud.create(db_session, user_data)
            user_crud.create(db_session, user_data)

    # Tests that an error is raised when creating a new user with an empty email
    def test_create_user_empty_email(self):
        user_data = {"full_name": "John Doe", "email": "", "password": "password123"}
        with pytest.raises(HTTPException):
            user_crud.create(db_session, user_data)

    # Tests that an error is raised when creating a new user with an empty password
    def test_create_user_empty_password(self):
        user_data = {
            "full_name": "John Doe",
            "email": "johndoe@example.com",
            "password": "",
        }
        with pytest.raises(HTTPException):
            user_crud.create(db_session, user_data)

    # Tests that an error is raised when creating a new user with an invalid email format
    def test_create_user_invalid_email_format(self):
        user_data = {
            "full_name": "John Doe",
            "email": "johndoeexample.com",
            "password": "password123",
        }
        with pytest.raises(HTTPException):
            user_crud.create(db_session, user_data)
