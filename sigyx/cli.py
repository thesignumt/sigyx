from .cmds import _cmdr
from .parser import parse
from .shell import _shell
from .utils.err import Err


class Sigyx:
    def prompt(self, _shell: _shell) -> str:
        return input(f"{_shell.cwd} λ ")

    def main(self):
        shell = _shell()
        while True:
            try:
                inp = self.prompt(shell)
                if not inp:
                    continue
                if inp in ("exit", "quit"):
                    print()
                    break

                parsed = parse(inp)
                cmd, args = parsed.cmd, parsed.args
                func = _cmdr.all.get(cmd)

                if func:
                    func(args, shell)
                else:
                    Err.msg(cmd, "not a command")
            except (KeyboardInterrupt, EOFError):
                print("\n")
                break
            except Exception as e:
                Err.msg("error", str(e))


def main():
    shell = Sigyx()
    shell.main()


if __name__ == "__main__":
    main()
