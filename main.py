"""
Entry point for the program.
1. Takes input from user and makes request to API.
2. Parses JSON data from the API into a Result object.
3. Generates CSV files for tasks and marks.
"""

import json
import sys

from export import generate_assessments_csv, generate_marks_csv, generate_comments_csv
from input import input_and_req
from model import Result
from process import parse_json

year_group, start_date, end_date, data, status = input_and_req()

# save data to file
with open("data.json", "w", encoding="UTF-8") as f:
    json.dump(data, f, indent=4)

if status != 200:
    print("Error: " + str(status))
    print("Check data.json for the full error message")
    sys.exit(1)

result: Result = parse_json(data)

# Verify number of assessments matches metadata
assert len(result.data) == result.metadata.count

# Print result (destructure the object)
# print(json.dumps(result.__dict__, default=lambda o: o.__dict__, indent=4))

assessments = result.filter_by_year(year_group)

generate_assessments_csv(assessments, year_group, start_date, end_date)
generate_marks_csv(assessments, year_group, start_date, end_date)
generate_comments_csv(assessments, year_group, start_date, end_date)

print("Generated marks.txt and tasks.txt for Year " + str(year_group) + ".")
