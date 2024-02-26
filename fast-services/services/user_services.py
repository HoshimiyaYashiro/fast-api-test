import copy
import datetime

from fastapi.encoders import jsonable_encoder

from models.user import UserCreate, User, Profile
from sql_apps import user_cruds, database


def create_user(user: UserCreate):
    with database.SessionLocal() as db, db.begin():
        db_user = user_cruds.get_user_by_email(db, email=user.email)
        if db_user:
            raise ValueError('Email already registered')
        db_user = user_cruds.create_user(db, user)
    return User(**jsonable_encoder(db_user))


def get_users(page: int = 1, size: int = 20):
    skip = page - 1 if page > 0 else 0
    with database.SessionLocal() as db:
        db_users, total = user_cruds.get_users(db, skip, size)
    db.close()
    users = []
    for db_user in db_users:
        user = User(**jsonable_encoder(db_user))
        users.append(user)
    return users, total


def update_profile(user_id: str, profile: Profile):
    with database.SessionLocal() as db, db.begin():
        db_profile = user_cruds.update_profile(db, user_id, profile)
    return Profile(**jsonable_encoder(db_profile))
