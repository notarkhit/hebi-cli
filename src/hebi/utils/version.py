import shutil
import subprocess

from hebi.utils.paths import config_dir


def print_version() -> None:
    try:
        hebi_dir = config_dir / "hebi"
        hebi_ver = subprocess.check_output(
            ["git", "--git-dir", hebi_dir / ".git", "rev-list", "--format=%B", "--max-count=1", "HEAD"], text=True, stderr=subprocess.DEVNULL
        )
        print("Hebi Shell:")
        print("    Last commit:", hebi_ver.split()[1])
        print("    Commit message:", *hebi_ver.splitlines()[1:])
    except subprocess.CalledProcessError:
        print("Hebi Shell: not installed (or not a git repo)")

    print()
    if shutil.which("qs"):
        print("Quickshell:")
        print("   ", subprocess.check_output(["qs", "--version"], text=True).strip())
    else:
        print("Quickshell: not in PATH")
