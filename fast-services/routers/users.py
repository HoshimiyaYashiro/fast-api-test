from fastapi import APIRouter, Security
from fastapi_jwt import JwtAuthorizationCredentials

from models.base_pagination import BasePagination
from models.user import User, UserCreate, Profile
from models.base_response import BaseResponse
from services import user_services
from utils import jwt_helper
from utils.constants import ModelMsgs, CrudMessages
from utils.jwt_helper import access_security

router = APIRouter(
    prefix='/users',
    tags=['users']
)


@router.get('/')
async def read_users(page: int = 1, size: int = 20) -> BaseResponse[BasePagination]:
    res_users, total = user_services.get_users(page, size)
    return BaseResponse.ok(BasePagination.init(res_users, total, page, size), ModelMsgs.users_retrieved)


@router.get('/user/{user_id}')
async def read_users(user_id) -> BaseResponse[User]:
    user = user_services.get_user(user_id)
    if user:
        return BaseResponse.ok(user, ModelMsgs.user_retrieved)
    return BaseResponse.fail(ModelMsgs.user_not_exists, ModelMsgs.user_retrieve_failed)


@router.post('/')
async def create_user(user: UserCreate) -> BaseResponse[User]:
    try:
        res_user = user_services.create_user(user)
        return BaseResponse.ok(res_user, ModelMsgs.user_created)
    except ValueError as e:
        return BaseResponse.fail(str(e), ModelMsgs.user_create_failed)


@router.put('/profile/{user_id}')
async def update_profile(user_id, profile: Profile) -> BaseResponse[Profile]:
    try:
        res_user = user_services.update_profile(user_id, profile)
        return BaseResponse.ok(res_user, ModelMsgs.profile_updated)
    except ValueError as e:
        return BaseResponse.fail(str(e), ModelMsgs.profile_update_failed)


@router.delete('/{user_id}')
async def delete_user(user_id) -> BaseResponse[bool]:
    try:
        is_delete = user_services.delete_user(user_id)
        if is_delete:
            return BaseResponse.ok(True, CrudMessages.deleted.value)
    except ValueError as e:
        return BaseResponse.fail(str(e), CrudMessages.delete_failed.value)


@router.get('/me')
async def read_me(credentials: JwtAuthorizationCredentials = Security(access_security)) -> BaseResponse[User]:
    auth_user = jwt_helper.get_user_from_token(credentials)
    user = user_services.get_user(auth_user.id)
    return BaseResponse.ok(user, CrudMessages.retrieved.value)
