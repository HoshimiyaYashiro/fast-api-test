from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship

from .database import Base


class UserDb(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True)


class ProfileDb(Base):
    __tablename__ = "profiles"

    id: Mapped[str] = mapped_column(ForeignKey("users.id"), primary_key=True)
    name: Mapped[str] = mapped_column(nullable=True)
    phone: Mapped[str] = mapped_column(nullable=True)
    user: Mapped[UserDb] = relationship("UserDb")
