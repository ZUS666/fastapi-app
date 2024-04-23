from typing import Annotated, Self

from pydantic import BaseModel, ConfigDict, EmailStr, Field, model_validator

from core.settings import settings
from domain.constants.avatar_constants import AVATAR_BUCKET
from domain.constants.user_constants import MaxLength
from domain.custom_types.types_users import UIDType
from domain.schemas.auth_schemas import UserLoginSchema


class UserSchema(BaseModel):
    """User schema."""
    user_id: UIDType
    email: EmailStr
    is_active: bool
    is_admin: bool


class ProfileSchema(BaseModel):
    first_name: Annotated[str, Field(max_length=MaxLength.FIRST_NAME)] | None = None
    last_name: Annotated[str, Field(max_length=MaxLength.FIRST_NAME)] | None = None


class ProfileInfoSchema(ProfileSchema):
    avatar: str | None = None

    @property
    def prefix(self) -> str:
        return settings.storage.storage_path + AVATAR_BUCKET

    def add_path_avatar(self) -> None:
        if self.avatar is not None:
            self.avatar = self.prefix + self.avatar

    def remove_path_avatar(self) -> None:
        if self.avatar is not None:
            self.avatar = self.avatar.replace(self.prefix, '')


class UserPasswordsSchema(BaseModel):
    model_config = ConfigDict(
        regex_engine='python-re',
    )
    password: Annotated[
        str,
        Field(
            min_length=8, pattern=r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[@#$%^&+=]).*$'
        ),
    ]
    re_password: str

    @model_validator(mode='after')
    def check_passwords(self) -> Self:
        if self.password != self.re_password:
            raise ValueError('Passwords do not match')
        return self


class UserRegistrationInputSchema(UserPasswordsSchema):
    """Schema for user registration."""
    email: EmailStr
    profile: ProfileSchema | None = None


class UserInfoSchema(BaseModel):
    user_id: UIDType
    email: EmailStr
    profile: ProfileInfoSchema


class UserInfoSchemaActive(UserInfoSchema):
    is_active: bool


class UserCredentialsSchema(UserLoginSchema):
    user_id: UIDType
    is_active: bool


class ProfileUpdateSchema(ProfileSchema):
    @model_validator(mode='after')
    def all_values_none(self) -> Self:
        if self.first_name is None and self.last_name is None:
            raise ValueError('One or more values must be set')
        return self


class EmailSchema(BaseModel):
    email: EmailStr


class ConfirmationUserSchema(EmailSchema):
    code: str


class ResetPasswordSchema(ConfirmationUserSchema, UserPasswordsSchema):
    pass
