from typing import Any, Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker


from app.core.settings import env

engine = create_engine(env.db_url + env.db_name)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def use_db() -> Session:                            # type:ignore
    try:
        session = SessionLocal()
        yield session
    finally:
        session.close()                             # type: ignore
