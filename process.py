"""
Process data from the API into a Result object.
"""

from datetime import datetime
from model import (
    Assessment,
    Folder,
    Metadata,
    Participant,
    Result,
    WorkType,
)


def parse_json(data: dict) -> Result:
    """Parse JSON data from the API into a Result object.

    Args:
        data (dict): JSON data from the API

    Returns:
        Result: Result object containing assessments and metadata
    """

    assessment_data = data["data"]
    metadata = data["metadata"]

    result_metadata = Metadata(metadata["count"], metadata["cursor"])

    assessments = []
    for task in assessment_data:
        work_type = WorkType(task["workType"]["id"], task["workType"]["name"])

        folder = Folder(
            task["folder"]["id"],
            task["folder"]["name"],
            task["folder"]["code"],
            task["folder"]["yearLevel"],
        )

        participants = []
        if task["participants"] is None or len(task["participants"]) == 0:
            result_metadata.count -= 1  # Keep the count accurate
            continue
        for student in task["participants"]:
            # change format of date from 2023-02-24T14:40:24+11:00 to YYYY-MM-DD
            # raw_p_date = datetime.strptime(p["response"]["date"], "%Y-%m-%dT%H:%M:%S%z")
            # p_date = raw_p_date.strftime("%Y-%m-%d")

            if "feedback" not in student or student["feedback"] is None:
                continue

            participant = Participant(
                student["learner"]["id"],
                student["learner"]["externalId"],
                student["learner"]["title"],
                student["learner"]["firstName"],
                student["learner"]["preferredName"],
                student["learner"]["lastName"],
                student["feedback"]["mark"],
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

        if assessment.weight == 0 or assessment.weight is None:
            result_metadata.count -= 1
            continue

        assessments.append(assessment)

    result = Result(assessments, result_metadata)
    return result
