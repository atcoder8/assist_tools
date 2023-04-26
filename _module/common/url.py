from . import problem_id_information


PROBLEM_URL_FORMAT = "https://atcoder.jp/contests/{contest_id}/tasks/{task_id}"
PROBLEM_NUMBER_BOUNDARY = {"abc": 20, "arc": 35, "agc": 1}


def get_problem_url(
    problem_id_info: problem_id_information.ProblemIdInformation,
) -> str:
    if (
        problem_id_info.contest_class == "abc"
        and 42 <= problem_id_info.contest_index <= 50
        and problem_id_info.problem_index in {"c", "d"}
    ):
        ref_contest_class = "arc"
        ref_contest_index = problem_id_info.contest_index + 16
        ref_problem_index = {"c": "a", "d": "b"}[problem_id_info.problem_index]

        task_id = f"{ref_contest_class}{ref_contest_index:03d}_{ref_problem_index}"
    else:
        if (
            problem_id_info.contest_index
            >= PROBLEM_NUMBER_BOUNDARY[problem_id_info.contest_class]
        ):
            problem_index = problem_id_info.problem_index
        else:
            problem_index = ord(problem_id_info.problem_index) - ord("a") + 1

        task_id = f"{problem_id_info.contest_id}_{problem_index}"

    return PROBLEM_URL_FORMAT.format(
        contest_id=problem_id_info.contest_id,
        task_id=task_id,
    )
