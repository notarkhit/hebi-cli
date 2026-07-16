import subprocess
from argparse import Namespace


class Command:
    args: Namespace

    def __init__(self, args: Namespace) -> None:
        self.args = args

    def run(self) -> None:
        if self.args.delete:
            subprocess.run(["hebi", "menu", "clipboard"])
            # Note: native UI handles deletion internally
        else:
            subprocess.run(["hebi", "menu", "clipboard"])
