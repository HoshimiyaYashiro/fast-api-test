import datetime

from pydantic import BaseModel


class LoginRequest(BaseModel):
    password: str


class EmailLoginRequest(LoginRequest):
    email: str


class PhoneLoginRequest(LoginRequest):
    phone: str
