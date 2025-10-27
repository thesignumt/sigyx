"""
ShellEnv – a frozen dataclass that captures the shell/script
environment on Linux, macOS **and** Windows.
"""

from __future__ import annotations

import getpass
import os
import platform
import subprocess
import sys
from dataclasses import dataclass, field
from typing import Optional

# --------------------------------------------------------------------------- #
# Helper functions – defined **before** the dataclass so they can be used in
# default_factory lambdas.
# --------------------------------------------------------------------------- #


def _get_user() -> str:
    """Current username, works on all platforms."""
    return (
        os.getenv("USER")
        or os.getenv("USERNAME")
        or os.getenv("LOGNAME")
        or getpass.getuser()
        or "unknown"
    )


def _get_uid() -> Optional[int]:
    """UID – Unix only."""
    try:
        return os.getuid()  # type: ignore
    except AttributeError:
        return None


def _get_euid() -> Optional[int]:
    """Effective UID – Unix only."""
    try:
        return os.geteuid()  # type: ignore
    except AttributeError:
        return None


def _get_pgid() -> Optional[int]:
    """Process-group ID – Unix only."""
    try:
        return os.getpgid(0)  # type: ignore
    except (AttributeError, OSError):
        return None


def _detect_windows_shell() -> str:
    """Heuristic for the shell on Windows."""
    comspec = os.getenv("COMSPEC")
    if comspec:
        return os.path.basename(comspec).lower().rsplit(".", 1)[0]

    if os.getenv("PSModulePath"):  # PowerShell (classic)
        return "powershell"
    if shutil.which("pwsh"):  # PowerShell Core # type: ignore
        return "pwsh"
    return "cmd"


def _is_windows_login_shell(parent: Optional[str]) -> bool:
    """Very rough guess – started from explorer, winlogon, dwm …"""
    return parent in {"explorer", "winlogon", "dwm"}


def _get_windows_parent_command(ppid: int) -> Optional[str]:
    """Try wmic first, fall back to PowerShell."""
    # wmic
    try:
        out = subprocess.run(
            ["wmic", "process", "where", f"ProcessId={ppid}", "get", "Name", "/value"],
            capture_output=True,
            text=True,
            check=False,
        )
        for line in out.stdout.splitlines():
            if "=" in line:
                k, v = line.split("=", 1)
                if k.strip() == "Name":
                    return v.strip().rsplit(".", 1)[0].lower()
    except Exception:
        pass

    # PowerShell fallback
    try:
        ps = (
            "Get-Process -Id {pid} -ErrorAction SilentlyContinue "
            "| Select-Object -ExpandProperty Name"
        ).format(pid=ppid)
        out = subprocess.run(
            ["powershell", "-Command", ps],
            capture_output=True,
            text=True,
            check=False,
        )
        name = out.stdout.strip()
        return name.rsplit(".", 1)[0].lower() if name else None
    except Exception:
        return None


# --------------------------------------------------------------------------- #
# Dataclass
# --------------------------------------------------------------------------- #


@dataclass(frozen=True)
class ShellEnv:
    """Immutable snapshot of the shell environment."""

    # ---- script ----------------------------------------------------------- #
    script_path: str = field(default_factory=lambda: os.path.abspath(sys.argv[0]))
    script_name: str = field(default_factory=lambda: os.path.basename(sys.argv[0]))

    # ---- shell ------------------------------------------------------------ #
    shell: Optional[str] = field(default_factory=lambda: os.getenv("SHELL"))
    shell_name: str = field(init=False)

    # ---- terminal --------------------------------------------------------- #
    term: Optional[str] = field(default_factory=lambda: os.getenv("TERM"))
    term_program: Optional[str] = field(
        default_factory=lambda: os.getenv("TERM_PROGRAM")
    )

    # ---- user / session --------------------------------------------------- #
    user: str = field(default_factory=_get_user)
    uid: Optional[int] = field(default_factory=_get_uid)
    effective_uid: Optional[int] = field(default_factory=_get_euid)
    home: str = field(default_factory=lambda: os.path.expanduser("~"))
    pwd: str = field(default_factory=os.getcwd)

    # ---- process ---------------------------------------------------------- #
    pid: int = field(default_factory=os.getpid)
    ppid: int = field(default_factory=os.getppid)
    pgid: Optional[int] = field(default_factory=_get_pgid)

    parent_command: Optional[str] = field(init=False)

    # ---- platform --------------------------------------------------------- #
    system: str = field(default_factory=lambda: platform.system())
    release: str = field(default_factory=lambda: platform.release())
    machine: str = field(default_factory=lambda: platform.machine())

    # ---- session type ----------------------------------------------------- #
    is_interactive: bool = field(default_factory=lambda: sys.stdin.isatty())
    is_login_shell: bool = field(init=False)

    # ------------------------------------------------------------------- #
    def __post_init__(self) -> None:
        # shell_name
        name = "unknown"
        if self.shell:
            name = os.path.basename(self.shell)
        elif self.system == "Windows":
            name = _detect_windows_shell()
        object.__setattr__(self, "shell_name", name)

        # parent_command
        parent = None
        if self.system == "Windows":
            parent = _get_windows_parent_command(self.ppid)
        else:
            try:
                out = subprocess.run(
                    ["ps", "-p", str(self.ppid), "-o", "comm="],
                    capture_output=True,
                    text=True,
                    check=False,
                )
                parent = out.stdout.strip() or None
            except Exception:
                parent = None
        object.__setattr__(self, "parent_command", parent)

        # is_login_shell
        login = bool(os.getenv("LOGIN"))
        if self.system == "Windows":
            login = _is_windows_login_shell(parent)
        object.__setattr__(self, "is_login_shell", login)

    # ------------------------------------------------------------------- #
    def __repr__(self) -> str:
        return f"ShellEnv(shell={self.shell_name}, user={self.user}, pwd={self.pwd})"


# --------------------------------------------------------------------------- #
# Optional: import shutil only when needed (avoids ImportError on minimal envs)
# --------------------------------------------------------------------------- #
try:
    import shutil  # type: ignore
except ImportError:
    shutil = None  # type: ignore


# --------------------------------------------------------------------------- #
# Demo
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    env = ShellEnv()
    print(env)
    print(f"Shell: {env.shell or 'N/A'} ({env.shell_name})")
    print(f"User : {env.user}  (uid={env.uid})")
    print(f"Parent: {env.parent_command}")
    print(f"Interactive: {env.is_interactive} | Login shell: {env.is_login_shell}")
    print(f"Platform: {env.system} {env.release} ({env.machine})")
