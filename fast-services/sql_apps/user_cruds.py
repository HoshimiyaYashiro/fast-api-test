from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from models.user import User, Profile, UserCreate
from .models import ProfileDb, UserDb
import uuid
import bcrypt
import time


def get_user(db: Session, user_id: str):
    return db.query(UserDb).filter(UserDb.id == user_id).first()


def get_users(db: Session, skip: int = 0, limit: int = 20):
    total = db.query(UserDb).count()
    db_users = db.query(UserDb).offset(skip*limit).limit(limit).all()
    return db_users, total


def get_user_by_email(db: Session, email: str):
    return db.query(UserDb).filter(UserDb.email == email).first()


def create_user(db: Session, user: UserCreate):
    db_user = UserDb(**user.dict())
    db_user.id = str(uuid.uuid4())
    db_user.password = bcrypt.hashpw(db_user.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    db_user.profile = ProfileDb(name=db_user.email.split('@')[0])
    db.begin(nested=True)
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    except Exception as e:
        db.rollback()
        raise e
    else:
        return User(**jsonable_encoder(db_user))
