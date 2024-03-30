from abc import ABC, abstractmethod

from domain.schemas.user_schemas import UserInfoSchema


class IUserBaseCache(ABC):
    @abstractmethod
    async def get(self, key: str) -> UserInfoSchema | None:
        raise NotImplementedError

    @abstractmethod
    async def set(self, key: str, schema: UserInfoSchema) -> None:
        raise NotImplementedError


class IUserCodeCache(ABC):
    @abstractmethod
    async def get(self, key: str) -> str | None:
        raise NotImplementedError

    @abstractmethod
    async def set(self, key: str, code: str) -> None:
        raise NotImplementedError
