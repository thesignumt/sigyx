"""registry"""

from typing import Any, Callable


class Reg:
    __slots__ = ("_registry",)

    def __init__(self):
        self._registry: dict[str, Callable[..., Any]] = {}

    def __call__(self, func: Callable[..., Any]):
        self._registry[func.__name__] = func
        return func

    def __getitem__(self, name: str) -> Callable[..., Any]:
        return self._registry[name]

    def __getattr__(self, name: str) -> Callable[..., Any]:
        try:
            return self._registry[name]
        except KeyError:
            raise AttributeError(name)

    @property
    def all(self) -> dict[str, Callable[..., Any]]:
        return self._registry
