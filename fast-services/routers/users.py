from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from models.base_pagination import BasePagination
from models.user import User, UserCreate
from models.base_response import BaseResponse
from services import user_services
from sql_apps import database

router = APIRouter(
    prefix='/users',
    tags=['users']
)
users: list[User] = []


@router.get('/')
async def read_users(page: int = 1, size: int = 20, db: Session = Depends(database.get_db)) -> BaseResponse[BasePagination]:
    res_users, total = user_services.get_users(db, page, size)
    return BaseResponse.ok(BasePagination.init(res_users, total, page, size), 'Users retrieved successfully')


@router.get('/{user_id}')
async def read_users(user_id) -> BaseResponse[User]:
    return BaseResponse.ok([x for x in users if x.id == user_id][0] if len(users) > 0 else None,
                           'User retrieved successfully')


@router.post('/')
async def create_user(user: UserCreate) -> BaseResponse[User]:
    try:
        res_user, total = user_services.create_user(user)
        return BaseResponse.ok(res_user, 'User created successfully')
    except ValueError as e:
        return BaseResponse.fail(str(e), 'User creation failed')


@router.put('/{id}')
async def update_user(user_id, user: User) -> BaseResponse[User]:
    user_index = next((i for i, x in enumerate(users) if x.id == user_id))
    users[user_index] = user
    return BaseResponse.ok(users[user_index], 'User updated successfully')


@router.put('/{id}/attrs')
async def update_user(user_id, user: dict) -> BaseResponse[User]:
    user_index = next((i for i, x in enumerate(users) if x.id == user_id))
    [setattr(users[user_index], key, value) for key, value in user.items()]
    return BaseResponse.ok(users[user_index], 'User updated successfully')
