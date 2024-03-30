from abc import abstractmethod

from pydantic import BaseModel

from domain.schemas.user_schemas import UserInfoSchema


class IBaseCache:
    @abstractmethod
    async def get(self, key: str) -> BaseModel:
        pass

    @abstractmethod
    async def set(self, key: str, schema: BaseModel) -> None:
        pass

    @abstractmethod
    async def delete(self, key: str) -> None:
        pass


class IUserBaseCache(IBaseCache):
    @abstractmethod
    async def get(self, key: str) -> UserInfoSchema:
        pass

    @abstractmethod
    async def set(self, key: str, schema: UserInfoSchema) -> None:
        pass


class IUserCodeCache(IUserBaseCache):
    pass
