from functools import cached_property
from typing import Any, Self

from punq import Container


class Impl:
    _instances: set[Self] = {}

    def __init__(self) -> None:
        self.container: Container = Container()

    def __call__(self, *args, **kwargs) -> Self:
        if self not in self._instances:
            self._instances.add(self)
        return self._instances[0]

    def register_all(self, objs: tuple[tuple[Any, Any], ...]) -> None:
        for obj in objs:
            self.container.register(*obj)

    @cached_property
    def container(self) -> Container:
        return self.container


impl = Impl()
