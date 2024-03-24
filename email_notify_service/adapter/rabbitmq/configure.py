from adapter.rabbitmq.constants import AMQPValue
from aio_pika.abc import AbstractChannel
from aio_pika.exchange import Exchange, ExchangeType
from aio_pika.queue import Queue


class ConfigureConsumer:
    @staticmethod
    async def _declare_exchange(channel: AbstractChannel) -> Exchange:
        return await channel.declare_exchange(
            AMQPValue.exchange_name.value, ExchangeType.TOPIC, durable=True
        )

    @staticmethod
    async def _declare_queue(channel: AbstractChannel) -> Queue:
        return await channel.declare_queue(name=AMQPValue.queue_name.value, durable=True)

    @classmethod
    async def configure_queue(cls, channel: AbstractChannel) -> Queue:
        exchange = await cls._declare_exchange(channel)
        queue = await cls._declare_queue(channel)
        await queue.bind(exchange, routing_key=AMQPValue.routing_key.value)
        return queue
