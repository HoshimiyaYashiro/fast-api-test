import datetime

from pydantic import BaseModel


class CustomBase(BaseModel):
    class Config:
        from_attributes = True
        json_encoders = {
            datetime.datetime: lambda v: v.isoformat('T', 'milliseconds'),
        }


class UserBase(CustomBase):
    email: str


class UserCreate(UserBase):
    password: str


class ProfileBase(CustomBase):
    name: str | None = None
    phone: str | None = None
    created_at: datetime.datetime | None = None
    updated_at: datetime.datetime | None = None


class ProfileCreate(ProfileBase):
    pass


class User(UserBase, CustomBase):
    id: str
    is_active: bool = True
    profile: ProfileBase | None = None
    created_at: datetime.datetime | None = None
    updated_at: datetime.datetime | None = None


class Profile(ProfileBase):
    pass
