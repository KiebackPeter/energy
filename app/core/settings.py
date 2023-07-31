from dataclasses import dataclass
from os import getenv

from dotenv import load_dotenv

load_dotenv()


@dataclass
class env:
    # App
    app_log_level = getenv("API_LOG_LEVEL")
    if app_log_level is None:
        app_log_level = "INFO"
    broker_url = getenv("BROKER_URL")
    if broker_url is None:
        broker_url = "redis://broker:6379"

    # Token
    token_expire_minutes = getenv("TOKEN_EXPIRE_MINUTES")
    if token_expire_minutes is None:
        token_expire_minutes = "180"
    private_key = getenv("SIGN_KEY")
    if private_key is None:
        private_key = "06b7a95639d25c7aa6cf66aa6c3b099f6f3e881810f4b93f7e8da25e094f56c8"

    # Database
    db_user = getenv("DB_USER")
    if db_user is None:
        db_user = "super_kp"
    db_password = getenv("DB_PASSWORD")
    if db_password is None:
        db_password = "super_kp"

    db_name = getenv("DB_NAME")
    if db_name is None:
        db_name = "energy"
    db_host = getenv("DB_HOST")
    if db_host is None:
        db_host = "database"
    db_port = getenv("DB_PORT")
    if db_port is None:
        db_port = "5432"
    db_driver: str = "postgresql"
    # db_async_driver: str = "postgresql+asyncpg"

    #  prepend driver and append database name
    db_url: str = f"://{db_user}:{db_password}@{db_host}:{db_port}/"
