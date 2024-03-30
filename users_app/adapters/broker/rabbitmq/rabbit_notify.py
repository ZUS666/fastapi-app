from adapters.broker.base import INotifyService
from adapters.broker.rabbitmq.constants import EXPIRES_EMAIL, AMQPValue
from aio_pika import DeliveryMode, Message, connect

from core.settings import settings
from domain.schemas.notify_schemas import NotifySendSchema


class RabbitMQNotifyService(INotifyService):
    async def notify(self, schema: NotifySendSchema, expires: bool = True) -> None:
        connection = await connect(settings.amqp.amqp_url)
        async with connection:
            channel = await connection.channel()

            exchange = await channel.get_exchange(AMQPValue.exchange_name.value)

            message = Message(
                schema.model_dump_json().encode(),
                delivery_mode=DeliveryMode.PERSISTENT,
                expiration=EXPIRES_EMAIL if expires else None,
            )
            await exchange.publish(
                message,
                routing_key=AMQPValue.routing_key.value,
            )
