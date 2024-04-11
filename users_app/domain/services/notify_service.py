from adapters.broker.notify_base import INotifyService
from core.dependency import impl
from domain.constants.email_constants import EmailSubject
from domain.constants.user_constants import CacheTimeout
from domain.schemas.notify_schemas import (
    ActivationContextSchema,
    NotifySendSchema,
    ResetPasswordContextSchema,
)
from domain.schemas.user_schemas import UserInfoSchema
from domain.services.common_service import ConfirmationCodeService


class CreateCodeNotifyUserService:
    def __init__(self) -> None:
        self._notify_adapter: INotifyService = impl.container.resolve(INotifyService)
        self._code_service: 'ConfirmationCodeService' = ConfirmationCodeService()

    async def activation_notify(
        self,
        user_schema: UserInfoSchema,
    ) -> None:
        code = await self._code_service.create_code(user_schema.user_id)
        schema = self._get_activation_schema(user_schema, code)
        await self._notify_adapter.notify(schema)

    async def reset_password_notify(
        self,
        user_schema: UserInfoSchema,
    ) -> None:
        code = await self._code_service.create_code(user_schema.user_id)
        schema = self._get_reset_password_schema(user_schema, code)
        await self._notify_adapter.notify(schema)

    @staticmethod
    def _get_activation_schema(user_schema: UserInfoSchema, code: str) -> NotifySendSchema:
        """Create notification for activation code."""
        context = ActivationContextSchema(
            first_name=user_schema.profile.first_name,
            last_name=user_schema.profile.last_name,
            code=code,
            expire_time=CacheTimeout.CONFIRMATION_CODE.value,
        )
        return NotifySendSchema(
            to=user_schema.email,
            subject=EmailSubject.ACTIVATION,
            context=context,
        )

    @staticmethod
    def _get_reset_password_schema(user_schema: UserInfoSchema, code: str) -> NotifySendSchema:
        """Create notification for activation code."""
        context = ResetPasswordContextSchema(
            first_name=user_schema.profile.first_name,
            last_name=user_schema.profile.last_name,
            code=code,
            expire_time=CacheTimeout.CONFIRMATION_CODE.value,
        )
        return NotifySendSchema(
            to=user_schema.email,
            subject=EmailSubject.RESET_PASSWORD,
            context=context,
        )
