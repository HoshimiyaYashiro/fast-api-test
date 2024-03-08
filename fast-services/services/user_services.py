from typing import Optional

from fastapi.encoders import jsonable_encoder

from models.user import UserCreate, User, Profile
from models.login_request import EmailLoginRequest
from sql_apps import user_cruds, database

from utils import pass_helper


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
    users = []
    for db_user in db_users:
        user = User(**jsonable_encoder(db_user))
        users.append(user)
    return users, total


def get_user(user_id: str):
    with database.SessionLocal() as db:
        db_user = user_cruds.get_user(db, user_id)
    return User(**jsonable_encoder(db_user)) if db_user else None


def update_profile(user_id: str, profile: Profile):
    with database.SessionLocal() as db, db.begin():
        db_profile = user_cruds.update_profile(db, user_id, profile)
    return Profile(**jsonable_encoder(db_profile))


def delete_user(user_id: str):
    with database.SessionLocal() as db, db.begin():
        db_user = user_cruds.get_user(db, user_id)
        if not db_user:
            raise ValueError('User not found')
        user_cruds.delete_user(db, user_id)
    return True


def verify_user(request: EmailLoginRequest) -> Optional[User]:
    with database.SessionLocal() as db:
        db_user = user_cruds.get_user_by_email(db, email=request.email)
        if not db_user:
            raise ValueError('User not found')
        if not pass_utils.verify_password(request.password, db_user.password):
            raise ValueError('Invalid password')
    return User(**jsonable_encoder(db_user))
