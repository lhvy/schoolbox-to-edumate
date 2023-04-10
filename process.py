from datetime import datetime
from model import (
    Assessment,
    Capability,
    Descriptor,
    Folder,
    Indicator,
    Instructor,
    Learner,
    Metadata,
    Participant,
    ParticipantRubric,
    ParticipantCapability,
    ParticipantIndicator,
    Result,
    Rubric,
    WorkType,
)


def parse_json(data) -> Result:
    assessment_data = data["data"]
    metadata = data["metadata"]

    result_metadata = Metadata(metadata["count"], metadata["cursor"])

    assessments = []
    for d in assessment_data:
        work_type = WorkType(d["workType"]["id"], d["workType"]["name"])
        folder = Folder(
            d["folder"]["id"],
            d["folder"]["name"],
            d["folder"]["code"],
            d["folder"]["yearLevel"],
        )
        if d["rubric"] is None:
            d["rubric"] = {"capabilities": []}
        capabilities = []
        for c in d["rubric"]["capabilities"]:
            indicators = []
            for i in c["indicators"]:
                descriptors = []
                for de in i["descriptors"]:
                    descriptor = Descriptor(
                        de["id"], de["description"], de["maxValue"], de["sequence"]
                    )
                    descriptors.append(descriptor)
                indicator = Indicator(i["id"], i["name"], i["maxValue"], descriptors)
                indicators.append(indicator)
            capability = Capability(c["id"], c["name"], c["maxValue"], indicators)
            capabilities.append(capability)
        rubric = Rubric(capabilities)
        participants = []
        if d["participants"] is None or len(d["participants"]) == 0:
            result_metadata.count -= 1  # Keep the count accurate
            continue
        for p in d["participants"]:
            learner = Learner(
                p["learner"]["id"],
                p["learner"]["title"],
                p["learner"]["firstName"],
                p["learner"]["preferredName"],
                p["learner"]["lastName"],
                p["learner"]["externalId"],
            )
            instructor = Instructor(
                p["instructor"]["id"],
                p["instructor"]["title"],
                p["instructor"]["firstName"],
                p["instructor"]["preferredName"],
                p["instructor"]["lastName"],
                p["instructor"]["externalId"],
            )
            if p["rubric"] is None:
                p["rubric"] = {"capabilities": []}
            participant_capabilities = []
            for c in p["rubric"]["capabilities"]:
                participant_indicators = []
                for i in c["indicators"]:
                    # Some indicators don't have descriptors
                    if i["descriptor"] is None:
                        i["descriptor"] = {
                            "id": None,
                            "description": None,
                            "maxValue": None,
                            "sequence": None,
                        }
                    participant_descriptor = Descriptor(
                        i["descriptor"]["id"],
                        i["descriptor"]["description"],
                        i["descriptor"]["maxValue"],
                        i["descriptor"]["sequence"],
                    )
                    participant_indicator = ParticipantIndicator(
                        i["id"],
                        i["name"],
                        i["maxValue"],
                        i["value"],
                        participant_descriptor,
                    )
                    participant_indicators.append(participant_indicator)
                participant_capability = ParticipantCapability(
                    c["id"],
                    c["name"],
                    c["value"],
                    c["maxValue"],
                    c["mark"],
                    participant_indicators,
                )
                participant_capabilities.append(participant_capability)
            participant_rubric = ParticipantRubric(participant_capabilities)
            # change format of date from 2023-02-24T14:40:24+11:00 to YYYY-MM-DD
            raw_p_date = datetime.strptime(p["date"], "%Y-%m-%dT%H:%M:%S%z")
            p_date = raw_p_date.strftime("%Y-%m-%d")
            participant = Participant(
                learner,
                p["mark"],
                p["normalisedMark"],
                p["comment"],
                p_date,
                instructor,
                participant_rubric,
            )
            participants.append(participant)
        raw_date = datetime.strptime(d["dueDate"], "%Y-%m-%dT%H:%M:%S%z")
        date = raw_date.strftime("%Y-%m-%d")
        assessment = Assessment(
            d["id"],
            d["title"],
            d["assessmentType"],
            d["commonAssessment"],
            work_type,
            folder,
            d["subjectCode"],
            d["project"],
            d["weighted"],
            d["weight"],
            date,
            rubric,
            participants,
        )

        if (
            assessment.weight == 0
            or assessment.weight is None
            or assessment.weighted is False
            or assessment.weighted is None
        ):
            result_metadata.count -= 1
            continue

        assessments.append(assessment)

    result = Result(assessments, result_metadata)
    return result
