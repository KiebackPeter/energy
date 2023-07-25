from dataclasses import dataclass
from os import getenv

from dotenv import load_dotenv

load_dotenv()


@dataclass
class env:
    app_log_level: str = getenv("API_LOG_LEVEL") or "DEBUG"
    broker_url: str = getenv("BROKER_URL") or "redis://broker:6379"

    token_expire_minutes: str = getenv("TOKEN_EXPIRE_MINUTES")  # type: ignore
    private_key: str = (
        getenv("SIGN_KEY")
        or "06b7a95639d25c7aa6cf66aa6c3b099f6f3e881810f4b93f7e8da25e094f56c8"
    )
    
    db_user: str = getenv("DB_USER") or "super_kp"
    db_password: str = getenv("DB_PASSWORD") or "super_kp"

    db_name: str = getenv("DB_NAME") or "postgres"
    db_driver: str = "postgresql"
    db_async_driver: str = "postgresql+asyncpg"
    db_host: str = getenv("DB_HOST") or "database"
    db_port: str = getenv("DB_PORT") or "5432"
    
    #  prepend driver and append database name
    db_url: str = f"://{db_user}:{db_password}@{db_host}:{db_port}/"
