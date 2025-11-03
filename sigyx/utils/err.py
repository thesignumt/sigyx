from .color import Color


class Err:
    _styles = {
        "msg": "red",
        "warn": "yellow",
        "info": "cyan",
    }

    @staticmethod
    def _print(cmd: str, message: str, style: str) -> None:
        Color.print(f"{cmd}: {message}", color=style, bold=True)

    @classmethod
    def msg(cls, cmd: str, message: str) -> None:
        cls._print(cmd, message, cls._styles["msg"])

    @classmethod
    def warn(cls, cmd: str, message: str) -> None:
        cls._print(cmd, message, cls._styles["warn"])

    @classmethod
    def info(cls, cmd: str, message: str) -> None:
        cls._print(cmd, message, cls._styles["info"])
