from parser import parse

from cmds import _cmdr
from utils.shellenv import ShellEnv


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
                cmd = parsed.cmd
                args = parsed.args
                func = _cmdr.all.get(cmd)
                if func:
                    func(args, self)
                else:
                    print(f"Unknown command: {cmd}")
            except (KeyboardInterrupt, EOFError):
                print()
                break
            except Exception as e:
                print(f"Error: {e}")


if __name__ == "__main__":
    shell = Sigyx()
    shell.main()
