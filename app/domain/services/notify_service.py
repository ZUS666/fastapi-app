from abc import abstractmethod

from domain.constants.email_constants import EmailSubject
from domain.constants.user_constants import CacheTimeout
from domain.schemas.notify_schemas import ActivationContextSchema, NotifySendSchema
from domain.schemas.user_schemas import UserInfoSchema


class INotifyService:
    @abstractmethod
    async def notify(self, schema: NotifySendSchema) -> None:
        raise NotImplementedError


class CreateNotifySendSchema:
    @staticmethod
    def activation_code(user_schema: UserInfoSchema, code: str) -> NotifySendSchema:
        context = ActivationContextSchema(
            first_name=user_schema.profile.first_name,
            last_name=user_schema.profile.last_name,
            code=code,
            expire_time=CacheTimeout.CONFIRMATION_CODE.value
        )
        return NotifySendSchema(
            to=user_schema.email,
            subject=EmailSubject.activation_code.value,
            context=context
        )
