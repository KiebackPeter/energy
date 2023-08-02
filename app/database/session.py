from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker, scoped_session


from app.core.settings import env

Base = declarative_base()

session_factory = sessionmaker(
    autoflush=False, bind=create_engine(env.db_driver + env.db_url + env.db_name)
)
session = session_factory()


def pg_session():
    try:
        return session
    except Exception as err:
        session.rollback()
        raise err
    finally:
        session.commit()
        session.close()


# from sqlalchemy.ext.asyncio import (
#     create_async_engine,
#     async_sessionmaker,
# )
# async_engine = create_async_engine(
#     env.db_async_driver + env.db_url + env.db_name,
#     echo=True,
# )
# async_session_factory = async_sessionmaker(async_engine, expire_on_commit=False)

# async def async_pg_session():
#     session = async_sessionmaker(async_engine, expire_on_commit=False)
#     try:
#         return session()
#     except Exception as err:
#         raise err
#     finally:
#         await async_engine.dispose()
