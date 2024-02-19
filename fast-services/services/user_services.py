from fastapi import Depends
from sqlalchemy.orm import Session

from models.user import UserCreate
from sql_apps import user_cruds, database
from sql_apps.models import UserDb, ProfileDb


def create_user(user: UserCreate):
    db = database.get_db()
    db_user = user_cruds.get_user_by_email(db, email=user.email)
    if db_user:
        raise ValueError('Email already registered')
    return user_cruds.create_user(db, user)
