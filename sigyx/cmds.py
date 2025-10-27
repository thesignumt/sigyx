import os

from .utils.color import Color, console
from .utils.err import Err
from .utils.reg import Reg

_cmdr = Reg()


@_cmdr
def cd(args: list, shell):
    if not args:
        Err.msg("cd", "missing operand")
        return
    new_dir = os.path.abspath(os.path.join(shell.cwd, args[0]))
    try:
        os.chdir(new_dir)
        shell.cwd = new_dir
    except FileNotFoundError:
        Err.msg("cd", f"no such file or directory: {args[0]}")
    except NotADirectoryError:
        Err.msg("cd", f"not a directory: {args[0]}")


@_cmdr
def pwd(args: list, shell):
    console.print(shell.cwd, style="cyan")


@_cmdr
def mkdir(args: list, shell):
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


@_cmdr
def ls(args: list, shell):
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


@_cmdr
def cat(args: list, shell):
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


@_cmdr
def rm(args: list, shell):
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
