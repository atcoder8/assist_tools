import argparse

from .common import (
    config,
    problem_id_information,
    command,
)


def remove_submission_file(
    config: config.Config,
    problem_id_info: problem_id_information.ProblemIdInformation,
) -> None:
    target_table_of_submission_file = config.get_target_table_of_submission_file(
        problem_id_info
    )

    cargo_config_text = config.path.cargo_config_file_path.read_text()

    if target_table_of_submission_file in cargo_config_text:
        cargo_config_text = cargo_config_text.replace(
            target_table_of_submission_file, ""
        )
        config.path.cargo_config_file_path.write_text(cargo_config_text)

    submission_file_path = config.path.get_submission_file_path(problem_id_info)

    if submission_file_path.exists():
        print(f"Delete file `{submission_file_path}`.")
        submission_file_path.unlink()


class RemoveSubmissionFile(command.Command):
    COMMAND_DESCRIPTION = "Remove file for submission."

    @classmethod
    def add_arguments(cls, parser: argparse.ArgumentParser):
        super().add_arguments(parser)

    def __init__(self, cmdline_args: argparse.Namespace) -> None:
        super().__init__(cmdline_args)

    def run_command(self):
        remove_submission_file(self.config, self.problem_id_info)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=RemoveSubmissionFile.COMMAND_DESCRIPTION
    )
    RemoveSubmissionFile.add_arguments(parser)
    cmdline_args = parser.parse_args()
    RemoveSubmissionFile(cmdline_args).run_command()
