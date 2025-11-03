import os
import platform
from pathlib import Path

from .utils.color import Color, console
from .utils.err import Err
from .utils.reg import Reg

_cmdr = Reg()

# +--------------------------------------------------------+
# [                        file nav                        ]
# +--------------------------------------------------------+


@_cmdr.reg
def cd(args: list, shell) -> None:
    if not args:
        os.chdir(os.path.expanduser("~"))
        return
    new_dir = (Path(shell.cwd) / args[0]).resolve()
    if not new_dir.exists():
        Err.msg("cd", f"no such file or directory: {args[0]}")
        return
    if not new_dir.is_dir():
        Err.msg("cd", f"not a directory: {args[0]}")
        return
    try:
        os.chdir(str(new_dir))
        shell.cwd = str(new_dir)
    except Exception as e:
        Err.msg("cd", str(e))


@_cmdr.reg(name="cd..")
def cd_back(args: list, shell) -> None:
    cd([".."], shell)


@_cmdr.reg
def pwd(args: list, shell) -> None:
    console.print(shell.cwd, style="cyan")


@_cmdr.reg
def mkdir(args: list, shell) -> None:
    if not args:
        Err.msg("mkdir", "missing operand")
        return
    for d in args:
        path = os.path.join(shell.cwd, d)
        try:
            os.mkdir(path)
        except FileExistsError:
            Err.warn("mkdir", f"cannot create directory '{d}': File exists")
        except Exception as e:
            Err.msg("mkdir", str(e))


@_cmdr.reg
def ls(args: list, shell) -> None:
    path = os.path.join(shell.cwd, args[0]) if args else shell.cwd
    try:
        for entry in os.listdir(path):
            entry_path = os.path.join(path, entry)
            if os.path.isdir(entry_path):
                Color.print(entry, "blue", bold=True)
            else:
                Color.print(entry, "green")
    except FileNotFoundError:
        Err.msg("ls", f"cannot access '{path}': No such file or directory")


@_cmdr.reg
def cat(args: list, shell) -> None:
    if not args:
        Err.msg("cat", "missing operand")
        return
    for f in args:
        path = os.path.join(shell.cwd, f)
        try:
            with open(path, "r") as file:
                console.print(file.read(), end="")
        except FileNotFoundError:
            Err.msg("cat", f"{f}: No such file")
        except Exception as e:
            Err.msg("cat", f"{f}: {e}")


@_cmdr.reg
def rm(args: list, shell) -> None:
    if not args:
        Err.msg("rm", "missing operand")
        return
    for f in args:
        path = os.path.join(shell.cwd, f)
        try:
            if os.path.isdir(path):
                os.rmdir(path)
            else:
                os.remove(path)
        except FileNotFoundError:
            Err.msg("rm", f"cannot remove '{f}': No such file or directory")
        except OSError:
            Err.msg("rm", f"cannot remove '{f}': Directory not empty")


# +--------------------------------------------------------+
# [                        internal                        ]
# +--------------------------------------------------------+


@_cmdr.reg(aliases=["clear"])
def cls(args: list, shell):
    os.system("cls" if platform.system() == "Windows" else "clear")
