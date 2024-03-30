import typing

from pydantic import BaseModel, field_validator

from domain.constants import DefaultName


class BaseContextSchema(BaseModel):
    first_name: str
    last_name: str

    @field_validator('first_name', mode='before')
    @classmethod
    def replace_none_value_first_name(cls, value: typing.Any) -> str | typing.Any:
        if value is None:
            return DefaultName.first_name.value
        return value

    @field_validator('last_name', mode='before')
    @classmethod
    def replace_none_value_last_name(cls, value: typing.Any) -> str | typing.Any:
        if value is None:
            return DefaultName.last_name.value
        return value


class ActivationContextSchema(BaseContextSchema):
    code: str
    expire_time: int


class ResetPasswordContextSchema(BaseContextSchema):
    code: str
    expire_time: int
