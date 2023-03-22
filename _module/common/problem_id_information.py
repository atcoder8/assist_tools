import re


PROBLEM_NAME_PATTERN = re.compile(r"^(a[brg]c)([0-9]{3})-([a-h]|(?:ex))$")

PROBLEM_NUMBER_BOUNDARY = {"abc": 20, "arc": 35, "agc": 1}

SUBMISSION_FILE_PATHNAME_FORMAT = (
    "src/bin/{contest_class}-{problem_number}/{problem_name}.rs"
)


class InvalidContestNameException(Exception):
    def __init__(self, problem_id: str, *args: object) -> None:
        super().__init__(*args)

        self.problem_id = problem_id


class ProblemIdInformation:
    def __init__(self, problem_id: str) -> None:
        match_obj = PROBLEM_NAME_PATTERN.fullmatch(problem_id)

        if match_obj is None:
            raise InvalidContestNameException(problem_id)

        match_groups = match_obj.groups()

        self.problem_id = problem_id
        self.contest_id = match_groups[0] + match_groups[1]
        self.contest_class = match_groups[0]
        self.contest_index = int(match_groups[1])
        self.problem_index = match_groups[2]
