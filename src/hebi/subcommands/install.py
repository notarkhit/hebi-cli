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
        info("Installing system and shell dependencies...")
        self.install_dependencies()
        
        target_dir = Path.home() / ".config" / "hebi"
        info(f"Setting up shell repository at {target_dir}...")
        needs_build = self.setup_repo(target_dir)
        
        if needs_build:
            info("Building plugins...")
            self.build_plugins(target_dir)
            
            info("Starting the shell in daemon mode...")
            self.start_shell()
            
            info("Installation complete! ✨ 🌟 ✨")
        else:
            info("Hebi shell is already up to date! Nothing to do.")

    def install_dependencies(self) -> None:
        pacman_deps = [
            "cmake", "make", "gcc", "qt6-base", "qt6-declarative",
            "qt6-shadertools", "qt6-svg", "libqalculate", "pipewire", "aubio",
            "cliphist", "fuzzel", "wl-clipboard", "slurp", "grim", "swappy",
            "dart-sass", "dconf", "psmisc", "libnotify", "procps-ng"
        ]
        yay_deps = ["libcava", "papirus-folders", "app2unit"]

        try:
            missing_pacman = subprocess.run(["pacman", "-T", *pacman_deps], stdout=subprocess.PIPE, text=True).stdout.split()
            if missing_pacman:
                log(f"Installing missing pacman dependencies: {' '.join(missing_pacman)}")
                subprocess.run(["sudo", "pacman", "-S", "--needed", "--noconfirm", *missing_pacman], check=True)
            else:
                log("All pacman dependencies are already installed.")
        except subprocess.CalledProcessError as e:
            fatal(f"Failed to install pacman dependencies: {e}")

        try:
            missing_yay = subprocess.run(["yay", "-T", *yay_deps], stdout=subprocess.PIPE, text=True).stdout.split()
            # Filter out yay's extra output lines like "-> exit status 127"
            missing_yay = [pkg for pkg in missing_yay if not pkg.startswith("->") and pkg != "exit" and pkg != "status" and pkg != "127"]
            
            if missing_yay:
                log(f"Installing missing yay dependencies: {' '.join(missing_yay)}")
                subprocess.run(["yay", "-S", "--needed", "--noconfirm", *missing_yay], check=True)
            else:
                log("All yay dependencies are already installed.")
        except subprocess.CalledProcessError as e:
            fatal(f"Failed to install yay dependencies: {e}")

    def setup_repo(self, target_dir: Path) -> bool:
        if target_dir.exists():
            log(f"{target_dir} already exists, checking for updates...")
            try:
                subprocess.run(["git", "fetch"], cwd=target_dir, check=True)
                local = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=target_dir, text=True).strip()
                remote = subprocess.check_output(["git", "rev-parse", "@{u}"], cwd=target_dir, text=True).strip()
                
                if local != remote:
                    log("Pulling latest changes...")
                    subprocess.run(["git", "pull"], cwd=target_dir, check=True)
                    return True
                else:
                    log("Repository is up to date.")
                    # Only build if the build directory doesn't exist yet
                    if not (target_dir / "plugin" / "build").exists():
                        return True
                    return False
            except subprocess.CalledProcessError as e:
                fatal(f"Failed to check or pull latest changes: {e}")
        else:
            log(f"Cloning repository to {target_dir}...")
            try:
                subprocess.run(
                    ["git", "clone", "https://github.com/notarkhit/hebi.git", str(target_dir)],
                    check=True
                )
                return True
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
