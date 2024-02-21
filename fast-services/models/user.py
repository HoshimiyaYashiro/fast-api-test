from pydantic import BaseModel


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: str
    is_active: bool = True
    profile: dict | None = None

    class Config:
        from_attributes = True


class ProfileBase(BaseModel):
    name: str
    phone: str | None = None


class ProfileCreate(ProfileBase):
    pass


class Profile(ProfileBase):
    user: User | None = None

    class Config:
        from_attributes = True
