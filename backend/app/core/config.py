from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "UWD Converter API"
    database_url: str = "postgresql+psycopg2://uwd:uwd@db:5432/uwd_db"
    local_database_url: str = "sqlite:///./uwd_local.db"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
