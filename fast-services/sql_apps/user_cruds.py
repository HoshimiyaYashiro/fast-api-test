from sqlalchemy.orm import Session

from . import models
from models.user import User, Profile, UserCreate
from .database import SessionLocal
from .models import ProfileDb, UserDb


def get_profile(db: Session, profile_id: str):
    return db.query(ProfileDb).filter(ProfileDb.id == profile_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(UserDb).filter(UserDb.email == email).first()


def create_user(db: Session, user: UserCreate):
    db_user = UserDb(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
