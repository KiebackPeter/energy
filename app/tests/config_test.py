from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.settings import env
from app.database.models.base import BaseModel
from app.database.session import use_db
from app.api.routers import api_router


def start_application():
    app = FastAPI()
    app.include_router(api_router)
    return app


engine = create_engine(env.DB.url + env.DB.name)
SessionTesting = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@fixture(scope="function")
def app() -> Generator[FastAPI, Any, None]:
    """
    Create a fresh database on each test case.
    """
    _app = start_application()
    yield _app


@fixture(scope="function")
def db_session(app: FastAPI) -> Generator[Session, Any, None]:
    connection = engine.connect()
    transaction = connection.begin()
    session = SessionTesting(bind=connection)
    yield session  # use the session in tests.
    session.close()
    transaction.rollback()
    connection.close()


@fixture(scope="function")
def client(app: FastAPI, db_session: Session) -> Generator[TestClient, Any, None]:
    """
    Create a new FastAPI TestClient that uses the `db_session` fixture to override
    the `use_db` dependency that is injected into routes.
    """

    def _get_test_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[use_db] = _get_test_db
    with TestClient(app) as client:
        yield client
from app.main import api

engine = create_engine(
    env.DB.url + env.DB.name,
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# really needed?
BaseModel.metadata.create_all(bind=engine)


def use_test_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close() #type: ignore 


api.dependency_overrides[use_db] = use_test_db

client = TestClient(api)


def test_create_user():
    response = client.post(
        "/api/v1/login/register",
        json={
            "full_name": "deadpool", 
            "email": "deadpool@example.com", 
            "password": "chimichangas4life"},
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["email"] == "deadpool@example.com"

    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["email"] == "deadpool@example.com"
    return response

def test_is_existing_user():
    response = test_create_user()
    assert response.status_code == 400, response.text
    data = response.json()
    assert data["detail"] == "This email already registered to a user"
