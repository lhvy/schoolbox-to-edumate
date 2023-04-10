from typing import List


class Descriptor:
    def __init__(self, id: int, description: str, max_value: int, sequence: int):
        self.id = id
        self.description = description
        self.max_value = max_value
        self.sequence = sequence


class Indicator:
    def __init__(
        self, id: int, name: str, max_value: int, descriptors: List[Descriptor]
    ):
        self.id = id
        self.name = name
        self.max_value = max_value
        self.descriptors = descriptors


class ParticipantIndicator:
    def __init__(
        self,
        id: int,
        name: str,
        max_value: int,
        value: int,
        descriptor: "Descriptor",
    ):
        self.id = id
        self.name = name
        self.max_value = max_value
        self.value = value
        self.descriptor = descriptor


class Capability:
    def __init__(self, id: int, name: str, max_value: int, indicators: List[Indicator]):
        self.id = id
        self.name = name
        self.max_value = max_value
        self.indicators = indicators


class ParticipantCapability:
    def __init__(
        self,
        id: int,
        name: str,
        value: int,
        max_value: int,
        mark: str,
        indicators: List["ParticipantIndicator"],
    ):
        self.id = id
        self.name = name
        self.value = value
        self.max_value = max_value
        self.mark = mark
        self.indicators = indicators


class Instructor:
    def __init__(
        self,
        id: str,
        title: str,
        first_name: str,
        preferred_name: str,
        last_name: str,
        external_id: str,
    ):
        self.id = id
        self.title = title
        self.first_name = first_name
        self.preferred_name = preferred_name
        self.last_name = last_name
        self.external_id = external_id


class Rubric:
    def __init__(self, capabilities: List[Capability]):
        self.capabilities = capabilities


class ParticipantRubric:
    def __init__(self, capabilities: List[ParticipantCapability]):
        self.capabilities = capabilities


class Learner:
    def __init__(
        self,
        id: str,
        title: str,
        first_name: str,
        preferred_name: str,
        last_name: str,
        external_id: str,
    ):
        self.id = id
        self.title = title
        self.first_name = first_name
        self.preferred_name = preferred_name
        self.last_name = last_name
        self.external_id = external_id


class Participant:
    def __init__(
        self,
        learner: Learner,
        mark: str,
        normalised_mark: float,  # should this be a float or a string? it's a string in the json
        comment: str,
        date: str,
        instructor: Instructor,
        rubric: ParticipantRubric,
    ):
        self.learner = learner
        self.mark = mark
        self.normalised_mark = normalised_mark
        self.comment = comment
        self.date = date
        self.instructor = instructor
        self.rubric = rubric


class YearLevel:
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name


class Folder:
    def __init__(self, id: str, name: str, code: str, year_levels: List["YearLevel"]):
        self.id = id
        self.name = name
        self.code = code
        self.year_levels = year_levels


class WorkType:
    def __init__(self, name: str, id: str):
        self.name = name
        self.id = id


class Assessment:
    def __init__(
        self,
        id: int,
        title: str,
        assessment_type: str,
        common_assessment: bool,
        work_type: WorkType,
        folder: Folder,
        subject_code: str,
        project: str,
        weighted: bool,
        weight: float,
        due_date: str,
        rubric: Rubric,
        participants: List[Participant],
    ):
        self.id = id
        self.title = title
        self.assessment_type = assessment_type
        self.common_assessment = common_assessment
        self.work_type = work_type
        self.folder = folder
        self.subject_code = subject_code
        self.project = project
        self.weighted = weighted
        self.weight = weight
        self.due_date = due_date
        self.rubric = rubric
        self.participants = participants


class Metadata:
    def __init__(self, count: int, cursor: int):
        self.count = count
        self.cursor = cursor


class Result:
    def __init__(self, data: List["Assessment"], metadata: Metadata):
        self.data = data
        self.metadata = metadata

    def filter_by_year(self, year: int) -> List["Assessment"]:
        # filter all assessments based on year group. use class code, e.g. 7PE1, 13DAT2, could be null
        return list(
            filter(
                lambda a: a.folder.code is not None
                and a.folder.code.startswith(str(year)),
                self.data,
            )
        )
