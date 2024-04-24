from functools import cache
from typing import Any

from punq import Container


@cache
class Impl:
    def __init__(self) -> None:
        self._container: Container = Container()

    def register_all(self, objs: tuple[tuple[type[Any], type[Any]], ...]) -> None:
        for obj in objs:
            if not issubclass(obj[1], obj[0]):
                raise AttributeError(f"{obj[1]} must be subclass of {obj[0]}")
            self.container.register(*obj)

    @property
    def container(self) -> Container:
        return self._container


impl = Impl()
