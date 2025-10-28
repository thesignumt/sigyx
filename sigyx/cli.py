from .cmds import _cmdr
from .parser import parse
from .utils.err import Err
from .utils.shellenv import ShellEnv


class Sigyx:
    def __init__(self):
        self.shell = ShellEnv()

    def main(self):
        while True:
            try:
                inp = input(f"[{self.shell.pwd}] $ ").strip()
                if not inp:
                    continue
                if inp in ("exit", "quit"):
                    break

                parsed = parse(inp)
                cmd, args = parsed.cmd, parsed.args
                func = _cmdr.all.get(cmd)

                if func:
                    func(args, self.shell)
                else:
                    Err.msg(cmd, "testing")
            except (KeyboardInterrupt, EOFError):
                print()
                break
            except Exception as e:
                print(f"Error: {e}")


def main():
    shell = Sigyx()
    shell.main()


if __name__ == "__main__":
    main()
