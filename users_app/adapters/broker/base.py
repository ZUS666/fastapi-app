from abc import abstractmethod

from domain.schemas.notify_schemas import NotifySendSchema


class INotifyService:
    @abstractmethod
    async def notify(self, schema: NotifySendSchema, expires: bool = True) -> None:
        raise NotImplementedError
