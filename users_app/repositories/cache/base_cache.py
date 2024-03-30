from abc import abstractmethod

from pydantic import BaseModel


class IBaseCache:
    @abstractmethod
    def get(self, key: str) -> BaseModel:
        pass

    @abstractmethod
    def set(self, key: str, schema: BaseModel) -> None:
        pass

    @abstractmethod
    async def delete(self, key: str) -> None:
        pass


class IUserBaseCache(IBaseCache):
    pass


class IUserCodeCache(IUserBaseCache):
    pass
