import datetime
from enum import Enum
from typing import Optional

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

    @classmethod
    def get_by_email(cls, session, email: str):
        return session.query(cls).filter_by(email=email).first()

    @classmethod
    def get_admin_by_email(cls, session, email: str):
        account = cls.get_by_email(session, email)
        if account and account.role in (Role.ADMIN, Role.SUPERADMIN):
            return account
        return None

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


class BlockedRefreshToken(Base):
    __tablename__ = "blocked_refresh_tokens"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[Optional[str]] = mapped_column(String(100), unique=True)
    refresh_token: Mapped[Optional[str]] = mapped_column(String(500), unique=True)

    @classmethod
    def get_by_email(cls, session, email: str):
        return session.query(cls).filter_by(email=email).first()

    @classmethod
    def get_by_refresh_token(cls, session, refresh_token: str):
        return session.query(cls).filter_by(refresh_token=refresh_token).first()

    def __repr__(self) -> str:
        return self.email
