from datetime import datetime

from fastapi import APIRouter, Security
from fastapi_jwt import JwtAuthorizationCredentials

from models.base_response import BaseResponse
from models.login_request import EmailLoginRequest
from models.user import User
from services import user_services
from utils import jwt_helper
from utils.constants import CrudMessages, ModelMsgs
from utils.jwt_helper import access_security

router = APIRouter(
    prefix='/auth',
    tags=['auth'],
)


@router.post('/login')
async def login(request: EmailLoginRequest) -> BaseResponse[dict]:
    try:
        auth = user_services.verify_user(request)
        return BaseResponse.ok(auth, CrudMessages.verified.value)
    except ValueError as e:
        return BaseResponse.fail(str(e), CrudMessages.verification_failed.value)

