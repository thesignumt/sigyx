"""registry"""

from typing import Any, Callable, Optional


class Reg:
    __slots__ = ("_registry",)

    def __init__(self):
        self._registry: dict[str, Callable[..., Any]] = {}

    def __call__(self, f: Optional[Callable[..., Any]] = None, *, name: str = ""):
        def decorator(inner_f: Callable[..., Any]):
            key = name or inner_f.__name__
            self._registry[key] = inner_f
            return inner_f

        if f is not None and callable(f):
            return decorator(f)
        return decorator

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
