# from pytest import fixture
# from fastapi.testclient import TestClient
# from sqlalchemy import create_engine
# from sqlalchemy.orm import Session, sessionmaker, declarative_base

# from app.main import api
# from app.core.settings import env
# from app.database.session import use_db

# engine = create_engine(env.DB.url + env.DB.name)
# TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# @fixture
# def client() -> TestClient:
#     return TestClient(api)

# def override_use_db():
#     connection = engine.connect()

#     transaction = connection.begin()


#     db = Session(bind=connection)
#     # db = Session(engine)

#     yield db

#     db.close()
#     transaction.rollback()
#     connection.close()

# api.dependency_overrides[use_db] = override_use_db
