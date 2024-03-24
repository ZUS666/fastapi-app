from pydantic import BaseModel, Field

from domain.constants import DefaultName


class BaseContextSchema(BaseModel):
    first_name: str = Field(default=DefaultName.first_name)
    last_name: str = Field(default=DefaultName.last_name)


class ActivationContextSchema(BaseContextSchema):
    code: str
    expire_time: int


class ResetPasswordContextSchema(BaseContextSchema):
    code: str
    expire_time: int
