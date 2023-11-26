import argparse

from .common import (
    config,
    problem_id_information,
    url,
    command,
)
from . import open, download


def prepare_solve_problem(
    config: config.Config,
    problem_id_info: problem_id_information.ProblemIdInformation,
    *,
    open_problem_page: bool = True,
    download_testcase: bool = True,
) -> None:
    target_table_of_submission_file = config.get_target_table_of_submission_file(
        problem_id_info
    )

    cargo_config_text = config.path.cargo_config_file_path.read_text()

    if target_table_of_submission_file not in cargo_config_text:
        print(
            f'Added binary target "{problem_id_info.problem_id}" to `{config.path.cargo_config_file_path}`.'
        )

        with config.path.cargo_config_file_path.open(mode="a") as cargo_config_file:
            cargo_config_file.write(target_table_of_submission_file)

    submission_file_path = config.path.get_submission_file_path(problem_id_info)

    if not submission_file_path.parent.exists():
        print(f"Create directory `{submission_file_path.parent}`.")
        submission_file_path.parent.mkdir(parents=True, exist_ok=True)

    if not submission_file_path.exists():
        print(f"Create file `{submission_file_path}`.")
        with submission_file_path.open(mode="w") as submission_file:
            submission_file.write(config.template.submission_file)

    problem_url = url.get_problem_url(problem_id_info)

    if open_problem_page:
        open.open_problem_page(
            config.command.open_url,
            problem_url,
            check_returncode=True,
        )

    if download_testcase:
        download.download_testcase(
            config.command.online_judge_tools,
            problem_url,
            config.path.testcase_dir_path,
            other_options=None,
            check_returncode=True,
        )


class PrepareProblem(command.Command):
    COMMAND_DESCRIPTION = """\
Make the following preparations:
  * Create a template file for the submission.
  * Open the problem page.
  * Download the test cases.\
"""

    @classmethod
    def add_arguments(cls, parser: argparse.ArgumentParser):
        super().add_arguments(parser)

        parser.add_argument(
            "-o",
            "--open",
            action="store_true",
            help="If this option is specified, the problem page will open.",
        )

        parser.add_argument(
            "--no-download",
            action="store_true",
            help="If this option is specified, the testcase will not download.",
        )

    def __init__(self, cmdline_args: argparse.Namespace) -> None:
        super().__init__(cmdline_args)

        assert hasattr(cmdline_args, "open")
        assert hasattr(cmdline_args, "no_download")

        assert isinstance(cmdline_args.open, bool)
        assert isinstance(cmdline_args.no_download, bool)

        self.open = cmdline_args.open
        self.no_download = cmdline_args.no_download

    def run_command(self):
        prepare_solve_problem(
            self.config,
            self.problem_id_info,
            open_problem_page=self.open,
            download_testcase=not self.no_download,
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=PrepareProblem.COMMAND_DESCRIPTION)
    PrepareProblem.add_arguments(parser)
    cmdline_args = parser.parse_args()
    PrepareProblem(cmdline_args).run_command()
