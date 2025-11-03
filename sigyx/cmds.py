import os
import platform
import stat
from datetime import datetime
from pathlib import Path

from .cli import _shell
from .utils.color import console
from .utils.err import Err
from .utils.reg import Reg

_cmdr = Reg()

# +--------------------------------------------------------+
# [                        file nav                        ]
# +--------------------------------------------------------+


@_cmdr.reg
def cd(args: list, shell: _shell) -> None:
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
        shell.cwd = new_dir
    except Exception as e:
        Err.msg("cd", str(e))


@_cmdr.reg(name="cd..")
def cd_back(args: list, shell: _shell) -> None:
    cd([".."], shell)


@_cmdr.reg
def pwd(args: list, shell: _shell) -> None:
    console.print(shell.cwd, style="cyan")


@_cmdr.reg
def mkdir(args: list, shell: _shell) -> None:
    if not args:
        Err.msg("mkdir", "missing operand")
        return
    for d in args:
        path = shell.cwd / d
        try:
            path.mkdir()
        except FileExistsError:
            Err.warn("mkdir", f"cannot create directory '{d}': File exists")
        except Exception as e:
            Err.msg("mkdir", str(e))


@_cmdr.reg
def ls(args: list, shell: _shell) -> None:
    path = Path(args[0]) if args else shell.cwd
    try:
        entries = [e.name for e in path.iterdir()]
        for entry in entries:
            full_path = path / entry
            info = full_path.stat()

            # File type
            ftype = "d" if stat.S_ISDIR(info.st_mode) else "-"

            # Permissions (like rwxr-xr-x)
            perms = "".join(
                [
                    "r" if info.st_mode & mask else "-"
                    for mask in [
                        stat.S_IRUSR,
                        stat.S_IWUSR,
                        stat.S_IXUSR,
                        stat.S_IRGRP,
                        stat.S_IWGRP,
                        stat.S_IXGRP,
                        stat.S_IROTH,
                        stat.S_IWOTH,
                        stat.S_IXOTH,
                    ]
                ]
            )

            # Size in bytes
            size = info.st_size

            # Modification time
            mtime = datetime.fromtimestamp(info.st_mtime).strftime("%b %d %H:%M")

            print(f"{ftype}{perms} {size:>8} {mtime} {entry}")

    except FileNotFoundError:
        Err.msg("ls", f"path '{path}' not found.")
    except PermissionError:
        Err.msg("ls", f"permission denied for '{path}'.")


@_cmdr.reg
def cat(args: list, shell: _shell) -> None:
    if not args:
        Err.msg("cat", "missing operand")
        return
    for f in args:
        path = shell.cwd / f
        try:
            with open(path, "r") as file:
                console.print(file.read(), end="")
        except FileNotFoundError:
            Err.msg("cat", f"{f}: No such file")
        except Exception as e:
            Err.msg("cat", f"{f}: {e}")


@_cmdr.reg
def rm(args: list, shell: _shell) -> None:
    if not args:
        Err.msg("rm", "missing operand")
        return
    for f in args:
        path = shell.cwd / f
        try:
            if path.is_dir():
                path.rmdir()
            else:
                path.unlink()
        except FileNotFoundError:
            Err.msg("rm", f"cannot remove '{f}': No such file or directory")
        except OSError:
            Err.msg("rm", f"cannot remove '{f}': Directory not empty")


# +--------------------------------------------------------+
# [                        internal                        ]
# +--------------------------------------------------------+


@_cmdr.reg(aliases=["clear"])
def cls(args: list, shell: _shell):
    os.system("cls" if platform.system() == "Windows" else "clear")
