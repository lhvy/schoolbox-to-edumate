"""
Takes a Result object and generates a CSV files for tasks and marks.
"""

import csv
from typing import List

from model import Assessment, Participant


def generate_assessments_csv(
    assessments: List["Assessment"], year_group: int, start_date: str, end_date: str
) -> None:
    """Generate a CSV file for tasks.

    Args:
        assessments (List["Assessment"]): List of assessments
        year_group (int): Year group to put in the filename
        start_date (str): Start date to put in the filename
        end_date (str): End date to put in the filename
    """

    with open(
        f"{year_group}_{start_date}_{end_date}_tasks.txt",
        "w",
        newline="",
        encoding="UTF-8",
    ) as tasks_file:
        writer = csv.writer(tasks_file, delimiter="\t")
        written_rows = set()
        writer.writerow(
            [
                "coursework_task",
                "task_kind",
                "coursework_category",
                "description",
                "academic_year",  # year in which the assessment is given
                "course",
                "weighting",
                "mark_out_of",
                "dmy_set_date",
                "dmy_due_date",
                "into_markbook_flag",
                "record_marks_flag",
                "grade_only",
                "criteria_only",
                "status_flag",
                "release_marks_flag",
                "task_dropdown_flag",
                "do_not_allow_comments",
            ]
        )
        assessment: Assessment
        for assessment in assessments:
            # assessment.participants contains all students,
            # which have a mark in the format "X / Y" or "X %" or "Not Assessed"
            mark = "Not Assessed"
            for participant in assessment.participants:
                if " %" in participant.mark:
                    mark = "100"
                    break
                if " / " in participant.mark:
                    mark = participant.mark.split(" / ")[1]
                    break

            if mark == "Not Assessed":
                # skip assessment if no students have a mark
                continue

            # example course name "9 My Subject Name 1C", remove " 1C"
            course = " ".join(assessment.folder.name.split(" ")[:-1])

            row = [
                assessment.title,
                "Test / Examination",  # task kind, read documentation
                "Coursework / IA",  # coursework category, read documentation
                "",  # description
                # get year from due date in format 2022-03-09
                assessment.due_date.split("-")[0],
                course,
                assessment.weight,
                mark,
            ]
            row_tuple = tuple(row)

            if row_tuple in written_rows:
                continue

            writer.writerow(
                row
                + [
                    assessment.due_date,  # set date, for now just using the due date
                    assessment.due_date,
                    1,  # Set to 1 if you want task to appear in the markbook
                    1,  # Set to 1 to record marks for this task
                    0,  # Set to 1 if you only want record grades.
                    0,  # Set to 1 to record criteria only.
                    0,  # Set to 1 to not show this task in the portal
                    0,  # Set to 0 if you want task marks / results to appear on the portal
                    0,  # Set to 1 to allow online submission to the dropdown box
                    0,  # Set to 1 to check the do not allow comments in markbook dropdown box
                ]
            )
            written_rows.add(row_tuple)


def generate_marks_csv(
    assessments: List["Assessment"], year_group: int, start_date: str, end_date: str
) -> None:
    """Generate a CSV file for marks.

    Args:
        assessments (List["Assessment"]): List of assessments
        year_group (int): Year group to put in the filename
        start_date (str): Start date to put in the filename
        end_date (str): End date to put in the filename
    """

    with open(
        f"{year_group}_{start_date}_{end_date}_marks.txt",
        "w",
        newline="",
        encoding="UTF-8",
    ) as marks_file:
        writer = csv.writer(marks_file, delimiter="\t")
        writer.writerow(
            [
                "student_number",
                "coursework_task",
                "raw_mark",
                "raw_mark_date",  # date in which the mark was given
                "course",
                "academic_year",
            ]
        )
        assessment: Assessment
        for assessment in assessments:
            participant: Participant
            for participant in assessment.participants:
                if " %" in participant.mark:
                    # "86.42 %"
                    mark = participant.mark.split(" %")[0]
                elif " / " in participant.mark:
                    # "43 / 55"
                    mark = participant.mark.split(" / ")[0]
                else:
                    # Probably "Not Assessed"
                    # skip participant if no mark
                    continue
                # example course name "9 My Subject Name 1C", remove " 1C"
                course = " ".join(assessment.folder.name.split(" ")[:-1])
                writer.writerow(
                    [
                        participant.external_id,
                        assessment.title,
                        # take mark from "43 / 55" to 43
                        mark,
                        assessment.due_date,
                        course,
                        # get year from due date in format 2022-03-09
                        assessment.due_date.split("-")[0],
                    ]
                )


def generate_comments_csv(
    assessments: List["Assessment"], year_group: int, start_date: str, end_date: str
) -> None:
    """Generate a CSV file for comments.

    Args:
        assessments (List["Assessment"]): List of assessments
        year_group (int): Year group to put in the filename
        start_date (str): Start date to put in the filename
        end_date (str): End date to put in the filename
    """

    with open(
        f"{year_group}_{start_date}_{end_date}_comments.csv",
        "w",
        newline="",
        encoding="UTF-8",
    ) as marks_file:
        writer = csv.writer(marks_file, delimiter=",")
        writer.writerow(
            [
                "student_number",
                "course",
                "coursework_task",
                "raw_mark",
                "comment",
            ]
        )
        assessment: Assessment
        for assessment in assessments:
            participant: Participant
            for participant in assessment.participants:
                if " %" in participant.mark:
                    # "86.42 %"
                    mark = participant.mark.split(" %")[0]
                elif " / " in participant.mark:
                    # "43 / 55"
                    mark = participant.mark.split(" / ")[0]
                else:
                    # Probably "Not Assessed"
                    # skip participant if no mark
                    continue
                # example course name "9 My Subject Name 1C", remove " 1C"
                course = " ".join(assessment.folder.name.split(" ")[:-1])
                if participant.comment == "":
                    comment = "NO COMMENT PROVIDED"
                else:
                    comment = participant.comment
                writer.writerow(
                    [
                        participant.external_id,
                        course,
                        assessment.title,
                        # take mark from "43 / 55" to 43
                        mark,
                        comment,
                    ]
                )
