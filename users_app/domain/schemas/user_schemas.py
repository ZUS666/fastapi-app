from typing import Annotated, Self

from pydantic import BaseModel, ConfigDict, EmailStr, Field, model_validator

from domain.constants.user_constants import MaxLength
from domain.custom_types.types_users import UIDType


class UserSchema(BaseModel):
    """User schema."""

    model_config = ConfigDict(from_attributes=True)

    user_id: UIDType
    email: EmailStr
    is_active: bool
    is_admin: bool


class ProfileSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    first_name: str | None = None
    last_name: str | None = None


class UserRegistrationInputSchema(BaseModel):
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


class UserRegistrationOutputSchema(BaseModel):
    """Schema for user registration response."""

    model_config = ConfigDict(from_attributes=True)

    user_id: UIDType
    email: EmailStr
    profile: ProfileSchema


class UserInfoSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    user_id: UIDType
    email: EmailStr
    profile: ProfileSchema


# class UserQueriesSchema(BaseModel):
#     """Schema for query parameters."""

#     limit: Annotated[int, Query(min_value=1, max_value=20, default=10)]
#     offset: Annotated[int, Query(min_value=0, default=0)]
#     order_by: Annotated[UsersOrderBy, Query(default=UsersOrderBy.user_id)]


class UserLoginSchema(BaseModel):
    """Schema for user login."""

    email: EmailStr
    password: str


class UserCredentialsSchema(UserLoginSchema):
    user_id: UIDType


class ProfileSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    first_name: Annotated[str, Field(max_length=MaxLength.FIRST_NAME)] | None = None
    last_name: Annotated[str, Field(max_length=MaxLength.FIRST_NAME)] | None = None


class ProfileUpdateSchema(ProfileSchema):
    @model_validator(mode='after')
    def all_values_none(self) -> Self:
        if self.first_name is None and self.last_name is None:
            raise ValueError('One or more values must be set')
        return self
