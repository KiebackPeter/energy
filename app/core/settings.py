from dataclasses import dataclass
from os import getenv

from dotenv import load_dotenv

load_dotenv()


@dataclass
class env:
    # host: str  = getenv("HOST") #type: ignore
    app_log_level: str = getenv("APP_LOG_LEVEL")  # type: ignore

    class API:
        # url: str = getenv("API_URL") #type: ignore
        secretKey: str = getenv("SECRET_KEY")  # type: ignore
        # BUG: only for alembic upgrades you need to disable the float operator
        tokenExpireMinutes: float = float(getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))  # type: ignore

    class DB:
        user: str = getenv("POSTGRES_USER")  # type: ignore
        password: str = getenv("POSTGRES_PASSWORD")  # type: ignore
        name: str = getenv("POSTGRES_DB_NAME")  # type: ignore
        driver: str = "postgresql"
        host: str = getenv("DB_HOST")  # type: ignore
        port: str = getenv("DB_PORT")  # type: ignore
        url: str = f"{driver}://{user}:{password}@{host}:{port}/"  # type: ignore
