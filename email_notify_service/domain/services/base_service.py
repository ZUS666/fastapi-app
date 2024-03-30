from abc import ABC, abstractmethod

from domain.schemas.email_schema import EmailSendSchema


class BaseSender(ABC):
    @abstractmethod
    async def send_email(self, schema: EmailSendSchema) -> None:
        raise NotImplementedError
