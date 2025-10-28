from parser import parse

from cmds import _cmdr
from utils.shellenv import ShellEnv


class Sigyx:
    def __init__(self):
        self.shell = ShellEnv()

    def main(self):
        sigyx = True
        while sigyx:
            try:
                inp = input(f"[{self.shell.pwd}] $ ").strip()
                if not inp:
                    continue
                if inp in ("exit", "quit"):
                    sigyx = False

                parsed = parse(inp)
                cmd, args = parsed.cmd, parsed.args
                func = _cmdr.all.get(cmd)

                if func:
                    func(args, self.shell)
                else:
                    print(f"Unknown command: {cmd}")
            except (KeyboardInterrupt, EOFError):
                print()
                sigyx = False
            except Exception as e:
                print(f"Error: {e}")


if __name__ == "__main__":
    shell = Sigyx()
    shell.main()
