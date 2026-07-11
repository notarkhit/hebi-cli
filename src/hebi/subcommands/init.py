import subprocess
from argparse import Namespace

from hebi.utils.io import fatal, info, log


class Command:
    args: Namespace

    def __init__(self, args: Namespace) -> None:
        self.args = args

    def run(self) -> None:
        info("Initializing system dependencies...")
        self.install_dependencies()
        info("System dependencies initialization complete! ✨")

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
