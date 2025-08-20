from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Database components
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str

    # Computed property
    @property
    def DATABASE_URL(self) -> str:
        return f"mysql+pymysql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    # App settings
    SECRET_KEY: str
    DEBUG: bool = True

    # JWT settings
    JWT_SECRET_KEY: str = "your-secret-key"  # Замените на сложный ключ в продакшене
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "extra": "allow"  # игнорировать лишние переменные окружения
    }


settings = Settings()
