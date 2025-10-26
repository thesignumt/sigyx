import json
from collections.abc import ItemsView, Iterator, KeysView, ValuesView
from textwrap import shorten
from typing import Any, Optional, Self

# type aliases
type DictAny = dict[str, Any]


class OT:
    "objable  object table"

    _TRUNCATE_LEN = 100

    def __init__(self, d: Optional[dict[str, Any]] = None, default: Any = None) -> None:
        self._ = {}
        self._default = default
        if d:
            self._.update(self._convert(d))

    def _convert(self, v: Any) -> Any:
        if isinstance(v, dict):
            return {k: self._convert(val) for k, val in v.items()}
        if isinstance(v, list):
            return [self._convert(x) for x in v]
        if isinstance(v, OT):
            return v
        return v

    def __getattr__(self, k: str) -> Any:
        try:
            return self._[k]
        except KeyError:
            if self._default is not None:
                return self._default
            raise AttributeError(f"{type(self).__name__!r} has no attribute {k!r}")

    def __setattr__(self, k: str, v: Any) -> None:
        if k == "_":
            object.__setattr__(self, k, v)
        else:
            self._[k] = self._convert(v)

    def __delattr__(self, k: str) -> None:
        del self._[k]

    def __getitem__(self, k: str) -> Any:
        return self._[k]

    def get(self, key: str, default: Any = None) -> Any:
        return self._.get(key, default)

    def update(self, d: dict[str, Any] | Self) -> None:
        for k, v in d.items() if isinstance(d, dict) else d._.items():
            self._[k] = self._convert(v)

    def merge(self, other: dict[str, Any] | Self) -> None:
        items = other.items() if isinstance(other, dict) else other._.items()
        for k, v in items:
            if isinstance(self._.get(k), OT) and isinstance(v, (dict, OT)):
                self._[k].merge(v)
            else:
                self._[k] = self._convert(v)

    def freeze(self) -> dict[str, Any]:
        return {k: (v.freeze() if isinstance(v, OT) else v) for k, v in self._.items()}

    def __setitem__(self, k: str, v: Any) -> None:
        self._[k] = self._convert(v)

    def __delitem__(self, k: str) -> None:
        del self._[k]

    def __iter__(self) -> Iterator[str]:
        return iter(self._)

    def __len__(self) -> int:
        return len(self._)

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, OT):
            return self._ == other._
        if isinstance(other, dict):
            return self._ == other
        return False

    def items(self) -> ItemsView[str, Any]:
        return self._.items()

    def keys(self) -> KeysView[str]:
        return self._.keys()

    def values(self) -> ValuesView[Any]:
        return self._.values()

    def copy(self) -> Self:
        return type(self)(self.freeze(), self._default)

    def __contains__(self, k: str) -> bool:
        return k in self._

    # allows `if obj.foo:` to check existence
    def __bool__(self) -> bool:
        return bool(self._)

    def __repr__(self) -> str:
        return shorten(f"OT({self._})", width=self._TRUNCATE_LEN, placeholder="...")


def o(d: Optional[str | dict[str, Any] | OT] = None) -> OT:
    if isinstance(d, OT):
        return d
    if isinstance(d, str):
        d = json.loads(d)
    return OT(d or {})  # pyright: ignore
