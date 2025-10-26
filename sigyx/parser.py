from lark import Lark, Transformer
from utils.objable import OT

shell_grammar = r"""
start: command (";" command)*

command: WORD argument*

argument: NUMBER | STRING | WORD

STRING: ESCAPED_STRING | SINGLE_QUOTED_STRING
NUMBER: SIGNED_NUMBER

WORD: /(?!\d)[\w.\-]+/
SINGLE_QUOTED_STRING: /'([^'\\]*(\\.[^'\\]*)*)'/

%import common.ESCAPED_STRING
%import common.SIGNED_NUMBER
%ignore " "
%ignore "\t"
%ignore "\n"
%ignore /\s+/
"""


class ShellTransformer(Transformer):
    def command(self, items):
        cmd_name = str(items[0])
        args = [self._parse_arg(arg) for arg in items[1:]]
        return OT({"cmd": cmd_name, "args": args})

    def argument(self, items):
        return items[0]

    def STRING(self, token):
        val = str(token)
        if len(val) >= 2 and val[0] in "'\"" and val[-1] == val[0]:
            return bytes(token[1:-1], "utf-8").decode("unicode_escape")
        return val

    def NUMBER(self, token):
        val = str(token)
        try:
            num = float(token)
            return int(num) if num.is_integer() else num
        except ValueError:
            return val  # fallback

    def WORD(self, token):
        return str(token)

    def _parse_arg(self, arg):
        # Already parsed by respective methods
        return arg

    def start(self, items):
        return items[0]


_parser = Lark(shell_grammar, start="start", parser="lalr")
_transformer = ShellTransformer()


class ParsedCmd(OT):
    def __init__(self, cmd: str, args: list[str | int | float]) -> None:
        super().__init__({"cmd": cmd, "args": args})


def parse(cmd: str) -> ParsedCmd:
    return _transformer.transform(_parser.parse(cmd))
