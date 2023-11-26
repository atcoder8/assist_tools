import os
import subprocess
import argparse
import shutil

from .common import url, command


def remove_testcase(testcase_dir_path: os.PathLike):
    if os.path.exists(testcase_dir_path):
        shutil.rmtree(testcase_dir_path)


def download_testcase(
    oj_command: str,
    problem_url: str,
    testcase_dir_path: os.PathLike,
    *,
    other_options: list[str] | None = None,
    check_returncode: bool = True,
) -> subprocess.CompletedProcess[bytes]:
    remove_testcase(testcase_dir_path)

    cmd_args = [oj_command, "download", problem_url]

    if other_options is not None:
        cmd_args.extend(other_options)

    return subprocess.run(cmd_args, check_returncode)


class DownloadTestcase(command.Command):
    COMMAND_DESCRIPTION = "Download the testcase for the specified problem."

    @classmethod
    def add_arguments(cls, parser: argparse.ArgumentParser) -> None:
        super().add_arguments(parser)

        parser.add_argument(
            "other_options",
            type=str,
            nargs="*",
            help="Other options to pass to `online-judge-tools`. (Example: --ignore-spaces)",
        )

    def __init__(self, cmdline_args: argparse.Namespace) -> None:
        super().__init__(cmdline_args)

        assert hasattr(cmdline_args, "other_options")

        assert isinstance(cmdline_args.other_options, list)

        self.other_options: list[str] = cmdline_args.other_options

    def run_command(self) -> subprocess.CompletedProcess[bytes]:
        return download_testcase(
            self.config.command.online_judge_tools,
            url.get_problem_url(self.problem_id_info),
            self.config.path.testcase_dir_path,
            other_options=self.other_options,
            check_returncode=True,
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=DownloadTestcase.COMMAND_DESCRIPTION)
    DownloadTestcase.add_arguments(parser)
    cmdline_args = parser.parse_args()
    DownloadTestcase(cmdline_args).run_command()
