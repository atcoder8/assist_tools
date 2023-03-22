import argparse
import subprocess

from .common import command


DEFAULT_TIME_LIMIT = 2.0


def run_binary_target(
    problem_id: str,
    *,
    release: bool = False,
    check_returncode: bool = True,
) -> subprocess.CompletedProcess[bytes]:
    if release:
        cmd_args = ["cargo", "run", "--release", "--bin", problem_id]
    else:
        cmd_args = ["cargo", "run", "--bin", problem_id]

    return subprocess.run(cmd_args, check=check_returncode)


class RunSubmissionProgram(command.Command):
    COMMAND_DESCRIPTION = "Run the program for submission."

    @classmethod
    def add_arguments(cls, parser: argparse.ArgumentParser) -> None:
        super().add_arguments(parser)

        parser.add_argument(
            "-r",
            "--release",
            action="store_true",
            help="If this option is specified, the test is performed in release mode.",
        )

    def __init__(self, cmdline_args: argparse.Namespace) -> None:
        super().__init__(cmdline_args)

        assert hasattr(cmdline_args, "release")

        assert isinstance(cmdline_args.release, bool)

        self.release = cmdline_args.release

    def run_command(self) -> subprocess.CompletedProcess[bytes]:
        return run_binary_target(
            self.problem_id_info.problem_id,
            release=self.release,
            check_returncode=True,
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=RunSubmissionProgram.COMMAND_DESCRIPTION)
    RunSubmissionProgram.add_arguments(parser)
    cmdline_args = parser.parse_args()
    RunSubmissionProgram(cmdline_args).run_command()
