import argparse
import subprocess

from .common import url, command


def open_problem_page(
    open_url_command: str,
    problem_url: str,
    *,
    check_returncode: bool = True,
) -> subprocess.CompletedProcess[bytes]:
    cmd_args = [open_url_command, problem_url]

    return subprocess.run(cmd_args, check=check_returncode)


class OpenProblemPage(command.Command):
    COMMAND_DESCRIPTION = "Open the specified problem page."

    @classmethod
    def add_arguments(cls, parser: argparse.ArgumentParser) -> None:
        super().add_arguments(parser)

        parser.add_argument(
            "-p",
            "--print",
            action="store_true",
            help="Output the URL to standard output instead of opening the problem page.",
        )

    def __init__(self, cmdline_args: argparse.Namespace) -> None:
        super().__init__(cmdline_args)

        assert hasattr(cmdline_args, "print")

        assert isinstance(cmdline_args.print, bool)

        self.print = cmdline_args.print

    def run_command(self):
        problem_url = url.get_problem_url(self.problem_id_info)

        if self.print:
            print(problem_url)
        else:
            open_problem_page(
                self.config.command.open_url,
                problem_url,
                check_returncode=True,
            )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=OpenProblemPage.COMMAND_DESCRIPTION)
    OpenProblemPage.add_arguments(parser)
    cmdline_args = parser.parse_args()
    OpenProblemPage(cmdline_args).run_command()
