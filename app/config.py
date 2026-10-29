from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "WorkSphere HRMS Phase 4"
    database_url: str = "sqlite:///./worksphere.db"
    secret_key: str = "replace-this-with-a-long-random-secret"
    access_token_expire_minutes: int = 60
    smtp_host: str | None = None
    smtp_port: int = 587
    smtp_username: str | None = None
    smtp_password: str | None = None
    smtp_from_email: str | None = None
    smtp_use_tls: bool = True
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
