"""
Model classes to represent data from the API.
"""

from dataclasses import dataclass
import sys
from typing import List


@dataclass
class Participant:
    """
    Represents a student in an assessment.
    """

    internal_id: str
    external_id: str
    title: str
    first_name: str
    preferred_name: str
    last_name: str
    mark: str
    comment: str
    # date: str


@dataclass
class YearLevel:
    """
    Represents a year level, e.g. 7, 8, 9, 10, 11, 12, 13.
    The id is unique, but the name is not.
    """

    internal_id: int
    name: str


@dataclass
class Folder:
    """
    A folder is typically a class, e.g. 7PE1, 13DAT2.
    """

    internal_id: str
    name: str
    code: str
    year_levels: List["YearLevel"]


@dataclass
class WorkType:
    """
    Represents the type of assessment, e.g. "Assessment task", "Test", "Exam".
    """

    internal_id: str
    name: str


@dataclass
class Assessment:
    """
    Represents an assessment.
    """

    internal_id: int
    title: str
    assessment_type: str
    common_assessment: bool
    work_type: WorkType
    folder: Folder
    subject_code: str
    project: str
    weight: float
    due_date: str
    participants: List[Participant]


@dataclass
class Metadata:
    """
    Stores metadata from an API request.
    """

    count: int
    cursor: int


class Result:
    """
    Stores the processed data from an API request.
    """

    def __init__(self, data: List["Assessment"], metadata: Metadata):
        self.data = data
        self.metadata = metadata

    def filter_by_year_and_date(
        self, year: int, start_date: str, end_date: str
    ) -> List["Assessment"]:
        """Filter results by year group.

        Returns:
            List["Assessment"]: All assessments in the given year group.
        """
        # filter all assessments based on year group
        # uses class code, e.g. 7PE1, 13DAT2, could be null
        return list(
            filter(
                lambda a: a.folder.code is not None
                and (
                    (
                        isinstance(a.folder.code, str)
                        and a.folder.code.startswith(str(year))
                    )
                    or (
                        isinstance(a.folder.code, list)
                        and any(c.startswith(str(year)) for c in a.folder.code)
                    )
                )
                and start_date <= a.due_date
                and a.due_date <= end_date,
                self.data,
            )
        )
