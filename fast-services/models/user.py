from pydantic import BaseModel


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class ProfileBase(BaseModel):
    name: str | None = None
    phone: str | None = None


class ProfileCreate(ProfileBase):
    pass


class User(UserBase):
    id: str
    is_active: bool = True
    profile: ProfileBase | None = None

    class Config:
        from_attributes = True


class Profile(ProfileBase):
    pass

    class Config:
        from_attributes = True
