from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import Session, declarative_base, sessionmaker


from app.core.settings import env

Base = declarative_base()

engine = create_engine(env.db_driver + env.db_url + env.db_name)
async_engine = create_async_engine(
    env.db_async_driver + env.db_url + env.db_name,
    echo=True,
)


def pg_session():
    session = sessionmaker(autoflush=False, bind=engine)()
    try:
        yield session
        session.commit()
    except Exception as err:
        session.rollback()
        raise err
    finally:
        session.close()


async def async_pg_session():
    async_session = async_sessionmaker(bind=async_engine)
    try:
        async with async_session.begin() as connection:
            async with connection.begin() as session:
                yield connection
    except Exception as err:
        await session.rollback()
        raise err
    finally:
        await session.close()
