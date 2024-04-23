from abc import ABC, abstractmethod


class IStorage(ABC):
    @abstractmethod
    async def upload_avatar(self, object: bytes, obj_name: str) -> None:
        raise NotImplementedError()
