from argparse import Namespace
from hebi.subcommands.shell import Command as ShellCommand

class Command:
    args: Namespace

    def __init__(self, args: Namespace) -> None:
        self.args = args

    def run(self) -> None:
        shell = ShellCommand(Namespace(message=["menu", self.args.mode], show=False, log=False, kill=False, daemon=False, log_rules=None))
        shell.run()
