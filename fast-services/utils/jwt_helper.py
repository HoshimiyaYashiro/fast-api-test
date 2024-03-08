from fastapi_jwt import JwtAuthorizationCredentials, JwtAccessBearer
from fastapi import Security
from models.user import User

access_security = JwtAccessBearer(secret_key="secret_key", auto_error=True)


def create_access_token(user: User):
    return {'access_token': access_security.create_access_token(subject=user.dict())}


def get_user_from_token(credentials: JwtAuthorizationCredentials = Security(access_security)) -> User:
    return User(**credentials.subject)