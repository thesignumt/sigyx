from rich.console import Console
from rich.text import Text

console = Console()


class Color:
    @staticmethod
    def print(text: str, color: str = "white", bold: bool = False) -> None:
        console.print(Text(text, style=f"{color}{' bold' if bold else ''}"))

    @staticmethod
    def format(text: str, color: str = "white", bold: bool = False) -> Text:
        return Text(text, style=f"{color}{' bold' if bold else ''}")
