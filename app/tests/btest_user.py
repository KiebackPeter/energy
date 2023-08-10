from pytest import fixture
from app.api.v1.user import UserCreateDTO
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
