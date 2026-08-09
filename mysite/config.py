from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):

    mongodb_url: str = Field(alias="MONGO_URL")

    mongodb_db_name: str = Field(
        default="booking",
        alias="MONGO_DB_NAME"
    )

    auth_service_url: str = "http://127.0.0.1:8001"

    post_service_url: str = "http://127.0.0.1:8002"


    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
        populate_by_name=True
    )


settings = Settings()


print("Mongo URL:", settings.mongodb_url)
print("DB:", settings.mongodb_db_name)