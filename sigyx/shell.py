from dataclasses import dataclass, field
from pathlib import Path


@dataclass(slots=True)
class _shell:
    cwd: Path = field(default_factory=Path.cwd)


__all__ = ["_shell"]
