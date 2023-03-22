import argparse
import pathlib
import subprocess
from abc import ABC, abstractmethod

from . import config, problem_id_information


class Command(ABC):
    COMMAND_DESCRIPTION: str

    @classmethod
    def add_arguments(cls, parser: argparse.ArgumentParser):
        parser.add_argument(
            "problem_id",
            type=str,
            help="Problem ID. (Example: abc123-a)",
        )

        parser.add_argument(
            "-c",
            "--config",
            default=config.DEFAULT_CONFIG_PATHNAME,
            type=str,
            help="Pathname of configuration file for this assist tool."
            f" (default: {config.DEFAULT_CONFIG_PATHNAME})",
        )

    def __init__(self, cmdline_args: argparse.Namespace) -> None:
        assert hasattr(cmdline_args, "problem_id")
        assert hasattr(cmdline_args, "config")

        assert isinstance(cmdline_args.problem_id, str)
        assert isinstance(cmdline_args.config, str)

        self.problem_id_info = problem_id_information.ProblemIdInformation(
            cmdline_args.problem_id
        )
        self.config = config.Config.read_config(pathlib.Path(cmdline_args.config))

    @abstractmethod
    def run_command(self) -> subprocess.CompletedProcess[bytes]:
        ...
