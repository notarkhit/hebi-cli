import subprocess
import sys
from argparse import Namespace
from pathlib import Path

from hebi.utils.io import info, fatal, log


class Command:
    args: Namespace

    def __init__(self, args: Namespace) -> None:
        self.args = args

    def run(self) -> None:
        info("Installing hebi shell dependencies...")
        self.install_dependencies()
        
        target_dir = Path.home() / ".config" / "hebi"
        info(f"Setting up shell repository at {target_dir}...")
        self.setup_repo(target_dir)
        
        info("Building plugins...")
        self.build_plugins(target_dir)
        
        info("Starting the shell in daemon mode...")
        self.start_shell()
        
        info("Installation complete! ✨ 🌟 ✨")

    def install_dependencies(self) -> None:
        pacman_deps = [
            "cmake", "make", "gcc", "qt6-base", "qt6-declarative",
            "qt6-shadertools", "qt6-svg", "libqalculate", "pipewire", "aubio"
        ]
        yay_deps = ["libcava"]

        log("Installing pacman dependencies...")
        try:
            subprocess.run(["sudo", "pacman", "-S", "--needed", "--noconfirm", *pacman_deps], check=True)
        except subprocess.CalledProcessError as e:
            fatal(f"Failed to install pacman dependencies: {e}")

        log("Installing yay dependencies...")
        try:
            subprocess.run(["yay", "-S", "--needed", "--noconfirm", *yay_deps], check=True)
        except subprocess.CalledProcessError as e:
            fatal(f"Failed to install yay dependencies: {e}")

    def setup_repo(self, target_dir: Path) -> None:
        if target_dir.exists():
            log(f"{target_dir} already exists, pulling latest changes...")
            try:
                subprocess.run(["git", "pull"], cwd=target_dir, check=True)
            except subprocess.CalledProcessError as e:
                fatal(f"Failed to pull latest changes: {e}")
        else:
            log(f"Cloning repository to {target_dir}...")
            try:
                subprocess.run(
                    ["git", "clone", "https://github.com/notarkhit/hebi.git", str(target_dir)],
                    check=True
                )
            except subprocess.CalledProcessError as e:
                fatal(f"Failed to clone repository: {e}")

    def build_plugins(self, target_dir: Path) -> None:
        plugin_dir = target_dir / "plugin"
        if not plugin_dir.exists():
            fatal(f"Plugin directory not found at {plugin_dir}")

        log("Configuring CMake...")
        try:
            subprocess.run(["cmake", "-B", "build", "-S", ".", '-DVERSION=\\"1.0\\"'], cwd=plugin_dir, check=True)
        except subprocess.CalledProcessError as e:
            fatal(f"Failed to configure CMake: {e}")

        log("Building with CMake...")
        try:
            # We use subprocess to find nproc
            nproc = subprocess.check_output(["nproc"], text=True).strip()
            subprocess.run(["cmake", "--build", "build", f"-j{nproc}"], cwd=plugin_dir, check=True)
        except subprocess.CalledProcessError as e:
            fatal(f"Failed to build plugins: {e}")

    def start_shell(self) -> None:
        try:
            subprocess.run(["hebi", "shell", "-t", "-d"], check=True)
        except subprocess.CalledProcessError as e:
            fatal(f"Failed to start the shell: {e}")
