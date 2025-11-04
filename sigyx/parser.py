import shlex
from dataclasses import dataclass


@dataclass
class ParsedCmd:
    cmd: str
    args: list[str]


def parse(cmd_str: str) -> ParsedCmd:
    parts = shlex.split(cmd_str)
    return ParsedCmd(parts[0], parts[1:])
