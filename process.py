"""
Process data from the API into a Result object.
"""

from datetime import datetime

from progress.bar import Bar

from model import Assessment, Folder, Participant, Result, WorkType


def parse_json(assessment_data: list[dict], mode: str) -> Result:
    """Parse JSON data from the API into a Result object.

    Args:
        data (dict): JSON data from the API
        mode (str): Mode of the program

    Returns:
        Result: Result object containing assessments and metadata
    """

    count = len(assessment_data)
    bar = Bar("Processing data from API", max=count)

    assessments = []
    for task in assessment_data:
        bar.next()
        if task["workType"] is None:
            work_type = WorkType(None, None)
        else:
            work_type = WorkType(task["workType"]["id"], task["workType"]["name"])

        folder = Folder(
            task["folder"]["id"],
            task["folder"]["name"],
            task["folder"]["code"],
            task["folder"]["yearLevel"],
        )

        participants = []
        if mode != "All tasks overview":
            if task["participants"] is None or len(task["participants"]) == 0:
                count -= 1  # Keep the count accurate
                continue
            for student in task["participants"]:
                # change format of date from 2023-02-24T14:40:24+11:00 to YYYY-MM-DD
                # raw_p_date = datetime.strptime(p["response"]["date"], "%Y-%m-%dT%H:%M:%S%z")
                # p_date = raw_p_date.strftime("%Y-%m-%d")

                if "feedback" not in student or student["feedback"] is None:
                    continue

                if (
                    student["instructor"] is not None
                    and student["learner"]["externalId"]
                    == student["instructor"]["externalId"]
                ):
                    continue

                if (
                    student["feedback"]["instructor"] is not None
                    and student["learner"]["externalId"]
                    == student["feedback"]["instructor"]["externalId"]
                ):
                    continue

                participant = Participant(
                    student["learner"]["id"],
                    student["learner"]["externalId"],
                    student["learner"]["title"],
                    student["learner"]["firstName"],
                    student["learner"]["preferredName"],
                    student["learner"]["lastName"],
                    student["feedback"]["mark"],
                    student["feedback"]["comment"],
                    # p_date,
                )
                participants.append(participant)

        raw_date = datetime.strptime(task["dueDate"], "%Y-%m-%dT%H:%M:%S%z")
        date = raw_date.strftime("%Y-%m-%d")
        assessment = Assessment(
            task["id"],
            task["title"],
            task["assessmentType"],
            task["commonAssessment"],
            work_type,
            folder,
            task["subjectCode"],
            task["project"],
            task["weight"],
            date,
            participants,
        )

        if mode != "All tasks overview" and (
            assessment.weight == 0 or assessment.weight is None
        ):
            count -= 1
            continue

        assessments.append(assessment)

    assert count == len(assessments)
    result = Result(assessments)
    bar.finish()
    return result
