import enum


class AMQPValue(enum.StrEnum):
    exchange_name = 'email_notify_exchange'
    queue_name = 'email_notify_queue'
    routing_key = 'email_routing_key'
