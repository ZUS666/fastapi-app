import uuid

from domain.constants.user_constants import LEN_CONFIRMATION_CODE


def create_code() -> str:
    """Creates a random confirmation code."""
    return str(uuid.uuid4().int)[:LEN_CONFIRMATION_CODE]
