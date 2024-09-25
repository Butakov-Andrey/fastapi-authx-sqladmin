import datetime
from typing import Optional

from sqlalchemy import TIMESTAMP, ForeignKey, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    type_annotation_map = {
        datetime.datetime: TIMESTAMP(timezone=True),
    }


class Accounts(Base):
    __tablename__ = "accounts"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[Optional[str]] = mapped_column(String(100))
    password_hash: Mapped[str] = mapped_column(String(100))

    role: Mapped[Optional[str]] = mapped_column(String(50))
    is_active: Mapped[bool] = mapped_column(default=True)

    last_login: Mapped[datetime.datetime]
    created_at: Mapped[datetime.datetime]
    updated_at: Mapped[Optional[datetime.datetime]]

    # Profile
    profile: Mapped["Profile"] = relationship(
        "Profile", back_populates="account", uselist=False
    )


class Profile(Base):
    __tablename__ = "profiles"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    first_name: Mapped[Optional[str]] = mapped_column(String(100))
    last_name: Mapped[Optional[str]] = mapped_column(String(100))

    phone: Mapped[Optional[str]] = mapped_column(String(50))
    birth_date: Mapped[Optional[datetime.datetime]]
    bio: Mapped[Optional[str]] = mapped_column(Text)

    # Accounts
    account_id: Mapped[int] = mapped_column(ForeignKey("accounts.id"))
    account: Mapped["Accounts"] = relationship("Accounts", back_populates="profile")
