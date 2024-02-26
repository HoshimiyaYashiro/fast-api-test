from sqlalchemy import ForeignKey, FetchedValue, func, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship
from typing_extensions import Annotated

from .database import Base
import datetime


timestamp = Annotated[
    datetime.datetime,
    mapped_column(DateTime(timezone=True), server_default=FetchedValue())
]


class UserDb(Base):
    __tablename__ = 'users'

    id: Mapped[str] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True)
    profile: Mapped['ProfileDb'] = relationship('ProfileDb', lazy='joined')
    updated_at: Mapped[timestamp] = mapped_column(nullable=True)
    created_at: Mapped[timestamp] = mapped_column(nullable=True)


class ProfileDb(Base):
    __tablename__ = 'profiles'

    id: Mapped[str] = mapped_column(ForeignKey('users.id'), primary_key=True)
    user: Mapped[UserDb] = relationship('UserDb', back_populates='profile')
    name: Mapped[str] = mapped_column(nullable=True)
    phone: Mapped[str] = mapped_column(nullable=True)
    updated_at: Mapped[timestamp] = mapped_column(nullable=True)
    created_at: Mapped[timestamp] = mapped_column(nullable=True)
