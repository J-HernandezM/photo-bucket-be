from logging import Logger, getLogger
import os
from typing import Optional
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    fake_aws: bool = False

    pg_password: Optional[str] = fake_aws or os.getenv("PG_PASSWORD")
    pg_user: Optional[str] = fake_aws or os.getenv("PG_USER")
    pg_dbname: Optional[str] = fake_aws or os.getenv("PG_DBNAME")
    database_url: Optional[str] = fake_aws or os.getenv("DATABASE_URL")

    aws_endpoint_url: Optional[str] = os.getenv(
        "AWS_ENDPOINT_URL"
    )  # Do not set on prod
    aws_region: str = os.getenv("AWS_REGION") or "us-east-1"
    # model_config = SettingsConfigDict(env_file=".env")

    logger: Logger = getLogger("photobucket")


settings = Settings()
