from asyncio import current_task

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker,
    async_scoped_session,
    AsyncSessionTransaction,
)
from sqlalchemy.orm import Session, declarative_base, sessionmaker, scoped_session


from app.core.settings import env

Base = declarative_base()

engine = create_engine(env.db_driver + env.db_url + env.db_name)
session_factory = sessionmaker(autoflush=False, bind=engine)

async_engine = create_async_engine(
    env.db_async_driver + env.db_url + env.db_name,
    echo=True,
)
async_session_factory = async_sessionmaker(async_engine, expire_on_commit=False)


def pg_session():
    session = scoped_session(session_factory)
    try:
        yield session()
        session.commit()
    except Exception as err:
        session.rollback()
        raise err
    finally:
        session.close()


async def async_pg_session():
    session = async_scoped_session(async_session_factory, scopefunc=current_task)
    try:
        async with session() as transaction:
            yield transaction
            await session.commit()

    except Exception as err:
        await session.rollback()
        raise err
    finally:
        await session.remove()
