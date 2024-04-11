from functools import cached_property
from typing import Any, Self

from punq import Container


class Impl:
    _instances: dict[Self, Self] = {}

    def __init__(self) -> None:
        self.container: Container = Container()

    def __call__(self, *args, **kwargs) -> Self:
        if self not in self._instances:
            instance = super().__call__(*args, **kwargs)
            self._instances[self] = instance
        return self._instances[self]

    def register_all(self, objs: tuple[tuple[type[Any], type[Any]], ...]) -> None:
        for obj in objs:
            self.container.register(*obj)

    @cached_property
    def container(self) -> Container:
        return self.container


impl = Impl()
