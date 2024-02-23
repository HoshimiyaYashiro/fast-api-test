from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from models.user import User, Profile, UserCreate
from .models import ProfileDb, UserDb
import uuid
import bcrypt
import time
import copy


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
    db.add(db_user)
    db.flush()
    db.refresh(db_user)
    return copy.deepcopy(db_user)


def update_profile(db: Session, user_id: str, profile: Profile):
    db_profile = db.get(ProfileDb, user_id)
    [setattr(db_profile, key, value) for key, value in profile.dict().items() if value is not None]
    db.add(db_profile)
    db.flush()
    db.refresh(db_profile)
    return copy.deepcopy(db_profile)
