import asyncio

from aio_pika import DeliveryMode, Message, connect

from domain.schemas.notify_schemas import ActivationContextSchema, NotifySendSchema
from domain.services.notify_service import INotifyService


class RabbitMQNotifyService(INotifyService):
    async def notify(self, schema: NotifySendSchema):
        connection = await connect("amqp://user:password@localhost:5672")
        async with connection:
            channel = await connection.channel()

            exchange = await channel.get_exchange('email_notify_exchange')

            message = Message(
                schema.model_dump_json().encode(),
                delivery_mode=DeliveryMode.PERSISTENT,
            )
            await exchange.publish(message, routing_key="email_routing_key")


if __name__ == '__main__':
    ins = RabbitMQNotifyService()
    schema = NotifySendSchema(
        to='zusss666@yandex.ru',
        subject='Activation code',
        context=ActivationContextSchema(
            first_name='asd',
            last_name='asdasd',
            code='123123',
            expire_time=123
        )
    )
    asyncio.run(ins.notify(schema))
