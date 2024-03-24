import logging
import pathlib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from aiosmtplib import SMTP, SMTPDataError, SMTPResponseException
from jinja2 import Environment, FileSystemLoader

from core.settings import settings
from domain.constants import TEMPLATE_MAPPING, EmailSubject
from domain.schemas.email_schema import EmailSendSchema
from domain.schemas.email_subject import BaseContextSchema


class EmailSender:
    def __init__(self) -> None:
        self.client = SMTP(
            hostname=settings.smtp.email_host,
            port=settings.smtp.email_port,
            use_tls=settings.smtp.email_use_tls,
        )

    async def login(self):
        await self.client.login(
            settings.smtp.email_username,
            settings.smtp.email_password
        )

    async def send_email(self, schema: EmailSendSchema):
        try:
            await self.client.send_message(self._create_message(schema))
        except (SMTPDataError, SMTPResponseException) as error:
            logging.error(f'SMTP error: {error.code} {error.message}')

    def _create_message(self, schema: EmailSendSchema) -> MIMEMultipart:
        message = MIMEMultipart("alternative")
        message["From"] = settings.smtp.email_username
        message["To"] = schema.to
        message["Subject"] = schema.subject

        html_message = MIMEText(
            self._render_message(schema.context, schema.subject),
            "html",
            "utf-8"
        )
        message.attach(html_message)
        return message

    def _render_message(self, context: BaseContextSchema, subject: EmailSubject) -> str:
        path = pathlib.Path(__file__).parent.parent / 'templates'
        template_loader = FileSystemLoader(path)
        template_env = Environment(loader=template_loader)
        template = template_env.get_template(TEMPLATE_MAPPING[subject])
        context = context.model_dump()
        return template.render(context)
