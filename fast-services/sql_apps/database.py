from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config.database import settings

SQLALCHEMY_DATABASE_URL = f'mysql+pymysql://{settings.MYSQL_USERNAME}:{settings.MYSQL_PASSWORD}@{settings.MYSQL_HOST}:{settings.MYSQL_PORT}/{settings.MYSQL_DATABASE}'

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)

SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()
