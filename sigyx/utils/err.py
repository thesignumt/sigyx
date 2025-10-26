from .color import console


class Err:
    @staticmethod
    def msg(cmd: str, message: str) -> None:
        console.print(f"[red]{cmd}:[/red] {message}")

    @staticmethod
    def warn(cmd: str, message: str) -> None:
        console.print(f"[yellow]{cmd}:[/yellow] {message}")

    @staticmethod
    def info(cmd: str, message: str) -> None:
        console.print(f"[cyan]{cmd}:[/cyan] {message}")
