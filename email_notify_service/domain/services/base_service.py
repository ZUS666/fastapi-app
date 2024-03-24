from abc import abstractmethod


class BaseSender:
    @abstractmethod
    async def send(self, message, message_type):
        raise NotImplementedError
