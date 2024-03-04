from typing import Annotated, Self

from fastapi import Query
from pydantic import BaseModel, ConfigDict, EmailStr, Field, model_validator

from users.constants import UsersOrderBy


class UserSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr
    is_active: bool
    is_admin: bool


class ProfileSchema(BaseModel):
    first_name: str | None = None
    last_name: str | None = None


class UserRegistrationSchema(BaseModel):
    """Schema for user registration."""

    model_config = ConfigDict(
        regex_engine='python-re',
    )

    email: EmailStr
    password: Annotated[
        str,
        Field(
            min_length=8, pattern=r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[@#$%^&+=]).*$'
        ),
    ]
    re_password: str
    profile: ProfileSchema | None = None

    @model_validator(mode='after')
    def check_passwords(self) -> Self:
        if self.password != self.re_password:
            raise ValueError('Passwords do not match')
        return self


class UserRegistrationResponseSchema(BaseModel):
    """Schema for user registration response."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr


class UserQueriesSchema(BaseModel):
    """Schema for query parameters."""

    limit: Annotated[int, Query(min_value=1, max_value=20, default=10)]
    offset: Annotated[int, Query(min_value=0, default=0)]
    order_by: Annotated[UsersOrderBy, Query(default=UsersOrderBy.id)]


class UserLoginSchema(BaseModel):
    """Schema for user login."""

    email: EmailStr
    password: str


class AccessTokenSchema(BaseModel):
    access_token: str
    access_token_expires_in: int


class RefreshToAccessSchema(BaseModel):
    refresh_token: str


class RefreshTokenSchema(RefreshToAccessSchema):
    refresh_token_expires_in: int


class TokenResponseSchema(AccessTokenSchema, RefreshTokenSchema):
    """Response login schema."""
    pass


class UserInfoSchema(BaseModel):
    id: int
    email: EmailStr
    profile: ProfileSchema
