"""registry"""

from typing import Any, Callable, overload


class Reg:
    __slots__ = ("_registry",)

    def __init__(self):
        self._registry: dict[str, Callable[..., Any]] = {}

    @overload
    def reg[F: Callable[..., Any]](self, f: F) -> F: ...
    @overload
    def reg[F: Callable[..., Any]](self, *, name: str = "") -> Callable[[F], F]: ...

    def reg[F: Callable[..., Any]](
        self, f: F | None = None, *, name: str = ""
    ) -> Callable[[F], F]:
        def decorator(real_f: F) -> F:
            self._registry[name or real_f.__name__] = real_f
            return real_f

        return decorator if f is None else decorator(f)

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
