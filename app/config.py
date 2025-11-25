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

    # model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
