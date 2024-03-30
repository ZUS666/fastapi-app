import enum


class AMQPValue(enum.StrEnum):
    exchange_name = 'email_notify_exchange'
    routing_key = 'email_routing_key'


EXPIRES_EMAIL: int = 5 * 60
