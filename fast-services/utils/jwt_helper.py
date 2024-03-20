from datetime import timedelta

from fastapi.encoders import jsonable_encoder
from fastapi_jwt import JwtAuthorizationCredentials, JwtAccessBearer, JwtRefreshBearer
from config import auth
from models.user import User

EXPIRES_DELTA = timedelta(hours=auth.settings.EXPIRES_DELTA)
REFRESH_EXPIRES_DELTA = timedelta(hours=auth.settings.REFRESH_EXPIRES_DELTA)

access_security = JwtAccessBearer(secret_key=auth.settings.SECRET_KEY, auto_error=True,
                                  access_expires_delta=EXPIRES_DELTA,
                                  refresh_expires_delta=REFRESH_EXPIRES_DELTA)
refresh_security = JwtRefreshBearer.from_other(access_security)


def create_access_token(user: User):
    access_token = access_security.create_access_token(subject=jsonable_encoder(user))
    refresh_token = refresh_security.create_refresh_token(subject=jsonable_encoder(user))
    return {'access_token': access_token, 'refresh_token': refresh_token, 'token_type': 'bearer',
            'expires_in': EXPIRES_DELTA.total_seconds()}


def refresh(credentials: JwtAuthorizationCredentials):
    access_token = access_security.create_access_token(subject=credentials.subject)
    refresh_token = refresh_security.create_refresh_token(subject=credentials.subject)
    return {'access_token': access_token, 'refresh_token': refresh_token, 'token_type': 'bearer',
            'expires_in': EXPIRES_DELTA.total_seconds()}


def get_user_from_token(credentials: JwtAuthorizationCredentials) -> User:
    return User(**credentials.subject)


def get_credentials_from_token(token: str) -> JwtAuthorizationCredentials:
    credentials = access_security._decode(token)
    return JwtAuthorizationCredentials(subject=credentials['subject'], jti=credentials['jti'])
