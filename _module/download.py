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
    check_returncode: bool = True,
) -> subprocess.CompletedProcess[bytes]:
    remove_testcase(testcase_dir_path)

    cmd_args = [str(oj_command), "download", problem_url]

    return subprocess.run(cmd_args, check_returncode)


class DownloadTestcase(command.Command):
    COMMAND_DESCRIPTION = "Download the testcase for the specified problem."

    @classmethod
    def add_arguments(cls, parser: argparse.ArgumentParser) -> None:
        super().add_arguments(parser)

    def __init__(self, cmdline_args: argparse.Namespace) -> None:
        super().__init__(cmdline_args)

    def run_command(self) -> subprocess.CompletedProcess[bytes]:
        return download_testcase(
            self.config.command.online_judge_tools,
            url.get_problem_url(self.problem_id_info),
            self.config.path.testcase_dir_path,
            check_returncode=True,
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=DownloadTestcase.COMMAND_DESCRIPTION)
    DownloadTestcase.add_arguments(parser)
    cmdline_args = parser.parse_args()
    DownloadTestcase(cmdline_args).run_command()
