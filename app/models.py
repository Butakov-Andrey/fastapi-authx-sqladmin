import datetime
from enum import Enum
from typing import Optional

from config import settings
from sqlalchemy import TIMESTAMP
from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    type_annotation_map = {
        datetime.datetime: TIMESTAMP(timezone=True),
        Enum: SQLAlchemyEnum,
    }


class Role(Enum):
    SUPERADMIN = "Superadmin"
    ADMIN = "Admin"
    TEACHER = "Teacher"
    STUDENT = "Student"


class Account(Base):
    __tablename__ = "accounts"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password_hash: Mapped[str] = mapped_column(String(100))

    role: Mapped[Role] = mapped_column(SQLAlchemyEnum(Role))
    is_active: Mapped[bool] = mapped_column(default=True)

    created_at: Mapped[datetime.datetime]
    updated_at: Mapped[Optional[datetime.datetime]]
    last_login: Mapped[Optional[datetime.datetime]]

    # Profile
    profile: Mapped["Profile"] = relationship(
        "Profile", back_populates="account", uselist=False, cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return self.email


class Profile(Base):
    __tablename__ = "profiles"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    first_name: Mapped[Optional[str]] = mapped_column(String(100))
    last_name: Mapped[str] = mapped_column(String(100))

    phone: Mapped[Optional[str]] = mapped_column(String(50))
    birth_date: Mapped[Optional[datetime.datetime]]
    bio: Mapped[Optional[str]] = mapped_column(Text)

    # Accounts
    account_id: Mapped[int] = mapped_column(ForeignKey("accounts.id"))
    account: Mapped["Account"] = relationship("Account", back_populates="profile")

    def __repr__(self) -> str:
        return self.last_name
