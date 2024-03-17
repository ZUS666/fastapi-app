from pydantic import BaseModel, EmailStr


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


class UserLoginSchema(BaseModel):
    """Schema for user login."""

    email: EmailStr
    password: str
