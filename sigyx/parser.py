import shlex
from dataclasses import dataclass


@dataclass
class ParsedCmd:
    cmd: str | None
    args: list[str]


def parse(cmd_str: str) -> ParsedCmd:
    parts = shlex.split(cmd_str)
    if not parts:
        return ParsedCmd(None, [])
    return ParsedCmd(parts[0], parts[1:])
