# config.py
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    mongo_uri: str
    mongo_db: str
    secret_key: str

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()