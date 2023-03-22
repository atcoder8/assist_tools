import os
import pathlib
import tomllib

from . import problem_id_information


DEFAULT_CONFIG_PATHNAME = "config_assist_tools.toml"


class Config:
    class Command:
        def __init__(self, command_dict) -> None:
            # Command of online-judge-tools.
            self.online_judge_tools = command_dict["online_judge_tools"]

            # Command to open a URL.
            self.open_url = command_dict["open_url"]

    class Path:
        def __init__(self, path_dict) -> None:
            # Pathname of cargo config pathname.
            self.cargo_config_file_path = pathlib.Path(
                path_dict["cargo_config_file_pathname"]
            )

            # Pathname format of submission file.
            self._submission_file_pathname_format: str = path_dict[
                "submission_file_pathname_format"
            ]
            assert isinstance(self._submission_file_pathname_format, str)

            # Pathname of the directory to download testcase.
            self.testcase_dir_path = pathlib.Path(path_dict["testcase_dir_pathname"])

        def get_submission_file_path(
            self, problem_id_info: problem_id_information.ProblemIdInformation
        ) -> pathlib.Path:
            submission_file_pathname = self._submission_file_pathname_format.format(
                problem_id=problem_id_info.problem_id,
                contest_id=problem_id_info.contest_id,
                contest_class=problem_id_info.contest_class,
                contest_index=problem_id_info.contest_index,
                problem_index=problem_id_info.problem_index,
            )

            return pathlib.Path(submission_file_pathname)

    class Template:
        def __init__(self, template_dict: dict) -> None:
            assert isinstance(template_dict["submission_file"], str)

            self.submission_file: str = template_dict["submission_file"]

    class TargetTable:
        def __init__(self, target_table_dict: dict) -> None:
            assert isinstance(target_table_dict["submission_file_format"], str)

            self._submission_file_format: str = target_table_dict[
                "submission_file_format"
            ]

    @classmethod
    def read_config(
        cls, config_path: os.PathLike = pathlib.Path(DEFAULT_CONFIG_PATHNAME)
    ) -> "Config":
        config_path = pathlib.Path(config_path)

        with config_path.open("br") as config_file:
            config_dict = tomllib.load(config_file)

        return Config(config_dict)

    def __init__(self, config_dict: dict) -> None:
        self.command = Config.Command(config_dict["command"])
        self.path = Config.Path(config_dict["path"])
        self.template = Config.Template(config_dict["template"])
        self.target_table = Config.TargetTable(config_dict["target_table"])

    def get_target_table_of_submission_file(
        self, problem_id_info: problem_id_information.ProblemIdInformation
    ) -> str:
        return self.target_table._submission_file_format.format(
            problem_id=problem_id_info.problem_id,
            submission_file_pathname=self.path.get_submission_file_path(
                problem_id_info
            ),
        )
