from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    MYSQL_HOST: str = 'localhost'
    MYSQL_PORT: int = 3306
    MYSQL_USERNAME: str = 'root'
    MYSQL_PASSWORD: str = 'admin'
    MYSQL_DATABASE: str = 'fastapi'

    class Config:
        env_prefix = 'DB_'
        env_file = '.env'
        env_file_encoding = 'utf-8'
        extra = 'ignore'


settings = Settings()
