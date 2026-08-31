from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_env: str = "development"
    database_url: str = "sqlite+aiosqlite:///./drishti.db"
    jwt_secret: str = "development-only-secret-change-before-deploy"
    allowed_origins: str = "http://localhost:3000"
    max_upload_mb: int = 10
    inference_provider: str = "demo"
    model_path: str | None = None
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def origins(self) -> list[str]: return [x.strip() for x in self.allowed_origins.split(",") if x.strip()]

@lru_cache
def get_settings() -> Settings: return Settings()

