from fastapi import APIRouter
from models.base_pagination import BasePagination
from models.user import User, UserCreate, Profile
from models.base_response import BaseResponse
from services import user_services
from utils.constants import ModelMsgs

router = APIRouter(
    prefix='/users',
    tags=['users']
)
users: list[User] = []


@router.get('/')
async def read_users(page: int = 1, size: int = 20) -> BaseResponse[BasePagination]:
    res_users, total = user_services.get_users(page, size)
    return BaseResponse.ok(BasePagination.init(res_users, total, page, size), ModelMsgs.users_retrieved)


@router.get('/{user_id}')
async def read_users(user_id) -> BaseResponse[User]:
    return BaseResponse.ok([x for x in users if x.id == user_id][0] if len(users) > 0 else None,
                           'User retrieved successfully')


@router.post('/')
async def create_user(user: UserCreate) -> BaseResponse[User]:
    try:
        res_user = user_services.create_user(user)
        return BaseResponse.ok(res_user, 'User created successfully')
    except ValueError as e:
        return BaseResponse.fail(str(e), 'User creation failed')


@router.put('/profile/{user_id}')
async def update_user(user_id, profile: Profile) -> BaseResponse[Profile]:
    try:
        res_user = user_services.update_profile(user_id, profile)
        return BaseResponse.ok(res_user, 'User profile updated successfully')
    except ValueError as e:
        return BaseResponse.fail(str(e), 'User profile updated failed')
