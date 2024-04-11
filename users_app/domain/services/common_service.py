import uuid

from core.dependency import impl
from domain.constants.user_constants import LEN_CONFIRMATION_CODE
from domain.custom_types.types_users import UIDType
from repositories.cache.base_cache import IUserCodeCache


class ConfirmationCodeService:
    def __init__(self):
        self.cache: IUserCodeCache = impl.container.resolve(IUserCodeCache)

    @staticmethod
    def _get_random_code() -> str:
        """Creates a random confirmation code."""
        return str(uuid.uuid4().int)[:LEN_CONFIRMATION_CODE]

    async def create_code(self, user_id: UIDType) -> str:
        code = self._get_random_code()
        await self.cache.set(str(user_id), code)
        return code

    async def verify_code(self, user_id: UIDType, code: str) -> bool:
        cached_code = await self.cache.get(str(user_id))
        return code == cached_code
