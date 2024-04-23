import asyncio

from adapters.broker.notify_base import INotifyService
from domain.schemas.notify_schemas import NotifySendSchema


class MockNotifyService(INotifyService):
    async def notify(self, schema: NotifySendSchema, expires: bool = True):
        await asyncio.sleep(0)
        print(schema.model_dump())
