from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SECRET_KEY: str = 'secret-key'
    EXPIRES_DELTA: int = 1
    REFRESH_EXPIRES_DELTA: int = 24

    class Config:
        env_prefix = 'JWT_'
        env_file = '.env'
        env_file_encoding = 'utf-8'
        extra = 'ignore'


settings = Settings()
