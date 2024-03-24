from pydantic import BaseModel, EmailStr

from domain.constants import EmailSubject
from domain.schemas.email_subject import (
    ActivationContextSchema,
    ResetPasswordContextSchema,
)


class EmailSendSchema(BaseModel):
    to: EmailStr
    subject: EmailSubject
    context: ActivationContextSchema | ResetPasswordContextSchema
