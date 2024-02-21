from fastapi.encoders import jsonable_encoder
from fastapi import Depends
from sqlalchemy.orm import Session

from models.user import UserCreate, User
from sql_apps import user_cruds, database


def create_user(user: UserCreate):
    db = database.SessionLocal()
    db_user = user_cruds.get_user_by_email(db, email=user.email)
    if db_user:
        raise ValueError('Email already registered')
    res_user = user_cruds.create_user(db, user)
    db.close()
    return res_user


def get_users(db: Session, page: int = 1, size: int = 20):
    skip = page - 1 if page > 0 else 0
    db_users, total = user_cruds.get_users(db, skip, size)
    users = []
    for db_user in db_users:
        user = User(**jsonable_encoder(db_user))
        users.append(user)
    return users, total
