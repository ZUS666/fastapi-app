import asyncio
from functools import partial

from adapter.rabbitmq.configure import ConfigureConsumer
from aio_pika import connect_robust
from aio_pika.abc import AbstractMessage

from core.settings import settings
from domain.schemas.email_schema import EmailSendSchema
from domain.services.email_service import EmailSender


async def dispatch(message: AbstractMessage, smtp_client: EmailSender,):
    await smtp_client.send_email(EmailSendSchema.model_validate_json(message.body.decode()))


async def main():
    connection = await connect_robust(settings.amqp.amqp_url)
    async with connection:
        channel = await connection.channel()
        queue = await ConfigureConsumer.configure_queue(channel)
        email_sender = EmailSender()
        await email_sender.client.connect()
        await email_sender.login()
        async with email_sender.client:
            callback = partial(dispatch, smtp_client=email_sender)
            await queue.consume(callback)
            await asyncio.Future()

if __name__ == '__main__':
    asyncio.run(main())
