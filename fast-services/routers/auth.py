from fastapi import APIRouter

from models.base_response import BaseResponse
from models.login_request import EmailLoginRequest
from models.user import User
from services import user_services
from utils.constants import CrudMessages

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)


@router.post('/login')
async def login(request: EmailLoginRequest) -> BaseResponse[User]:
    try:
        res_user = user_services.verify_user(request)
        return BaseResponse.ok(res_user, CrudMessages.verified.value)
    except ValueError as e:
        return BaseResponse.fail(str(e), CrudMessages.verification_failed.value)
