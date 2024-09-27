from datetime import datetime, timedelta

from config import settings
from fastapi import HTTPException, Request
from models import Account, BlockedRefreshToken, Profile
from passlib.hash import bcrypt
from pytz import UTC
from sqladmin import ModelView
from sqladmin.authentication import AuthenticationBackend

SESSION_LIFETIME = timedelta(minutes=settings.SESSION_LIFETIME_MINUTES)


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request):
        form = await request.form()
        username, password = form["username"], form["password"]

        if username != settings.ADMIN_USERNAME or password != settings.ADMIN_PASSWORD:
            raise HTTPException(401, detail={"message": "Bad credentials"})

        request.session.update(
            {
                "authenticated": True,
                "admin_username": username,
                "last_activity": datetime.utcnow().isoformat(),
            }
        )
        return True

    async def logout(self, request: Request):
        request.session.clear()
        return True

    async def authenticate(self, request: Request):
        if not request.session.get("authenticated", False):
            return False

        last_activity = datetime.fromisoformat(request.session.get("last_activity", ""))
        if datetime.utcnow() - last_activity > SESSION_LIFETIME:
            request.session.clear()
            return False

        request.session["last_activity"] = datetime.utcnow().isoformat()
        return True


class AccountsAdmin(ModelView, model=Account):
    @staticmethod
    def date_format(value):
        if value.tzinfo is None:
            value = value.replace(tzinfo=UTC)
        return value.astimezone(settings.moscow_timezone).strftime(
            "%d.%m.%Y %H:%M:%S %Z"
        )

    name = "Account"
    name_plural = "Accounts"
    icon = "fa-solid fa-user"
    category = "Users"
    # отображение полей
    column_labels = {"password_hash": "Password"}
    # отображение списка
    column_list = [Account.email, Account.role, Account.is_active]
    column_searchable_list = [Account.email]
    column_sortable_list = [Account.is_active, Account.role]
    column_default_sort = [(Account.id, True)]
    # форматирование
    column_type_formatters = {
        datetime: date_format,
        **ModelView.column_type_formatters,
    }

    # отображение объекта
    column_details_exclude_list = [
        Account.password_hash,
        Account.id,
    ]
    # отображение форм
    form_excluded_columns = [
        Account.created_at,
        Account.updated_at,
        Account.last_login,
        Account.profile,
    ]

    async def on_model_change(self, data, model, is_created, request) -> None:
        if is_created:
            data["password_hash"] = bcrypt.hash(data["password_hash"])
            data["created_at"] = datetime.now(settings.moscow_timezone)


class ProfilesAdmin(ModelView, model=Profile):
    name = "Profile"
    name_plural = "Profiles"
    icon = "fa-solid fa-address-card"
    category = "Users"
    # отображение списка
    column_list = [Profile.account, Profile.last_name]
    column_searchable_list = [Profile.last_name]
    column_default_sort = [(Profile.id, True)]
    # отображение объекта
    column_details_exclude_list = [
        Profile.account_id,
    ]


class BlockedRefreshTokensAdmin(ModelView, model=BlockedRefreshToken):
    name = "Blocked Refresh Token"
    name_plural = "Blocked Refresh Tokens"
    icon = "fa-solid fa-skull-crossbones"
    category = "Users"
    # отображение списка
    column_list = [BlockedRefreshToken.email]
    column_searchable_list = [BlockedRefreshToken.email]
    column_default_sort = [(BlockedRefreshToken.id, True)]
    # отображение объекта
    column_details_exclude_list = [
        BlockedRefreshToken.id,
    ]
