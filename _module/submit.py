import os
import argparse
import subprocess

from .common import url
from . import test


DEFAULT_SLEEP_TIME = 0.0


def run_submit(
    oj_command: str,
    submission_file_path: os.PathLike,
    *,
    problem_url: str | None,
    wait: float = DEFAULT_SLEEP_TIME,
    confirm: bool = False,
    check_returncode: bool = True,
):
    cmd_args = [
        oj_command,
        "submit",
        "--wait",
        str(wait),
    ]

    if not confirm:
        cmd_args.append("--yes")

    if problem_url is not None:
        cmd_args.append(problem_url)

    cmd_args.append(str(submission_file_path))

    return subprocess.run(cmd_args, check=check_returncode)


class SubmitSolution(test.TestSolution):
    COMMAND_DESCRIPTION = "Submit the solution program."

    @classmethod
    def add_arguments(cls, parser: argparse.ArgumentParser) -> None:
        super().add_arguments(parser)

        parser.add_argument(
            "--no-test",
            action="store_true",
            help="If this option is specified, do not test before submission.",
        )

        parser.add_argument(
            "-w",
            "--wait",
            type=float,
            default=DEFAULT_SLEEP_TIME,
            help="Sleep time until submission." f" (default: {DEFAULT_SLEEP_TIME})",
        )

        parser.add_argument(
            "-C",
            "--confirm",
            action="store_true",
            help="If this option is specified,"
            " confirmation will be made before submission.",
        )

    def __init__(self, cmdline_args: argparse.Namespace) -> None:
        super().__init__(cmdline_args)

        assert hasattr(cmdline_args, "no_test")
        assert hasattr(cmdline_args, "wait")
        assert hasattr(cmdline_args, "confirm")

        assert isinstance(cmdline_args.no_test, bool)
        assert isinstance(cmdline_args.wait, float)
        assert isinstance(cmdline_args.confirm, bool)

        self.no_test = cmdline_args.no_test
        self.wait = cmdline_args.wait
        self.confirm = cmdline_args.confirm

    def run_command(self) -> subprocess.CompletedProcess[bytes]:
        if not self.no_test:
            test.test_solution(
                self.config.command.online_judge_tools,
                self.problem_id_info.problem_id,
                error=self.error,
                time_limit=self.time_limit,
                debug=self.debug,
                check_returncode=True,
            )

        return run_submit(
            self.config.command.online_judge_tools,
            self.config.path.get_submission_file_path(self.problem_id_info),
            problem_url=url.get_problem_url(self.problem_id_info),
            wait=self.wait,
            confirm=self.confirm,
            check_returncode=True,
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=SubmitSolution.COMMAND_DESCRIPTION)
    SubmitSolution.add_arguments(parser)
    cmdline_args = parser.parse_args()
    SubmitSolution(cmdline_args).run_command()
