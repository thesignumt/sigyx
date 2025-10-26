from .cli import Sigyx


def main():
    shell = Sigyx()
    shell.main()


__all__ = ["main"]
