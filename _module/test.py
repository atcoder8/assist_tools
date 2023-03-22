import argparse
import subprocess

from .common import command


DEFAULT_TIME_LIMIT = 2.0


def test_solution(
    oj_command: str,
    problem_id: str,
    *,
    error: float | None = None,
    time_limit: float = DEFAULT_TIME_LIMIT,
    debug: bool = False,
    check_returncode: bool = True,
) -> subprocess.CompletedProcess[bytes]:
    if debug:
        build_cmd_args = ["cargo", "build", "--bin", problem_id]
    else:
        build_cmd_args = ["cargo", "build", "--release", "--bin", problem_id]

    subprocess.run(build_cmd_args, check=True)

    test_cmd_args = [oj_command, "test"]

    if debug:
        test_cmd_args.extend(["-c", f"./target/debug/{problem_id}"])
    else:
        test_cmd_args.extend(["-c", f"./target/release/{problem_id}"])

    if error is not None:
        test_cmd_args.extend(["--error", str(error)])

    test_cmd_args.extend(["--tle", str(time_limit)])

    return subprocess.run(test_cmd_args, check=check_returncode)


class TestSolution(command.Command):
    COMMAND_DESCRIPTION = "Test the solution program."

    @classmethod
    def add_arguments(cls, parser: argparse.ArgumentParser) -> None:
        super().add_arguments(parser)

        parser.add_argument(
            "-e",
            "--error",
            type=float,
            help="Allowable absolute or relative error.",
        )

        parser.add_argument(
            "-t",
            "--time-limit",
            type=float,
            default=DEFAULT_TIME_LIMIT,
            help="The maximum execution time of the program."
            f" (default: {DEFAULT_TIME_LIMIT})",
        )

        parser.add_argument(
            "-d",
            "--debug",
            action="store_true",
            help="If this option is specified, the test is performed in debug mode.",
        )

    def __init__(self, cmdline_args: argparse.Namespace) -> None:
        super().__init__(cmdline_args)

        assert hasattr(cmdline_args, "error")
        assert hasattr(cmdline_args, "time_limit")
        assert hasattr(cmdline_args, "debug")

        assert cmdline_args.error is None or isinstance(cmdline_args.error, float)
        assert isinstance(cmdline_args.time_limit, float)
        assert isinstance(cmdline_args.debug, bool)

        self.error: float | None = cmdline_args.error
        self.time_limit = cmdline_args.time_limit
        self.debug = cmdline_args.debug

    def run_command(self) -> subprocess.CompletedProcess[bytes]:
        return test_solution(
            self.config.command.online_judge_tools,
            self.problem_id_info.problem_id,
            error=self.error,
            time_limit=self.time_limit,
            debug=self.debug,
            check_returncode=True,
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=TestSolution.COMMAND_DESCRIPTION)
    TestSolution.add_arguments(parser)
    cmdline_args = parser.parse_args()
    TestSolution(cmdline_args).run_command()
