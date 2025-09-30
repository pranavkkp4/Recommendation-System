from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Personalized Recommender"
    secret_key: str = "super-secret-key-change-me"
    access_token_expire_minutes: int = 60 * 24
    algorithm: str = "HS256"
    database_url: str = "sqlite:///./recommender.db"

    class Config:
        env_file = ".env"


settings = Settings()
