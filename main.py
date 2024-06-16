"""
Entry point for the program.
1. Takes input from user and makes request to API.
2. Parses JSON data from the API into a Result object.
3. Generates CSV files for tasks and marks.
"""

import concurrent.futures
import json
import sys
import time

from progress.spinner import Spinner

from export import (
    generate_assessments_csv,
    generate_assessments_simple_csv,
    generate_comments_csv,
    generate_marks_csv,
)
from input import input_and_req
from model import Result
from process import parse_json


def save(data):
    # save data to file
    with open("data.json", "w", encoding="UTF-8") as f:
        json.dump(data, f, indent=4)


year_group, start_date, end_date, mode, data, status = input_and_req()

spinner = Spinner("Saving raw API data to file... ")
with concurrent.futures.ThreadPoolExecutor() as executor:
    future = executor.submit(save, data)
    while not future.done():
        spinner.next()
        time.sleep(0.1)
spinner.finish()

if status != 200:
    print("Error: " + str(status))
    print("Check data.json for the full error message")
    sys.exit(1)

result: Result = parse_json(data, mode)

# Verify number of assessments matches metadata
assert len(result.data) == result.metadata.count

# Print result (destructure the object)
# print(json.dumps(result.__dict__, default=lambda o: o.__dict__, indent=4))

# The API returns tasks for all year groups, so we need to filter them
# Daylight savings means we might match 1 or 2 results outside of the date range
assessments = result.filter_by_year_and_date(year_group, start_date, end_date)

if mode == "All tasks overview":
    generate_assessments_simple_csv(assessments, year_group, start_date, end_date)
elif mode == "Comments export":
    generate_comments_csv(assessments, year_group, start_date, end_date)
elif mode == "Markbook export":
    generate_assessments_csv(assessments, year_group, start_date, end_date)
    generate_marks_csv(assessments, year_group, start_date, end_date)

print("Generated marks.txt, tasks.txt and comments.csv for year " + str(year_group))
