from pydantic import BaseModel, EmailStr

from domain.constants.email_constants import EmailSubject


class BaseContextSchema(BaseModel):
    """Base schema for sending emails."""
    first_name: str | None = None
    last_name: str | None = None


class ActivationContextSchema(BaseContextSchema):
    code: str
    expire_time: int


class ResetPasswordContextSchema(BaseContextSchema):
    code: str
    expire_time: int


class NotifySendSchema(BaseModel):
    """Schema for sending emails."""
    to: EmailStr
    subject: EmailSubject
    context: ActivationContextSchema | ResetPasswordContextSchema
