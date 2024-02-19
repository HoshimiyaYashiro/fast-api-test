from pydantic import BaseModel


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool = True

    class Config:
        from_attributes = True


class ProfileBase(BaseModel):
    name: str
    phone: str


class ProfileCreate(ProfileBase):
    pass


class Profile(ProfileBase):
    id: str
    user_id: str

    class Config:
        from_attributes = True
