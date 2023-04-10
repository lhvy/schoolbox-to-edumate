from datetime import datetime, timedelta

from input import input_and_req
from model import Result
from process import parse_json

# Test loop to ensure filtering by date works correctly
start_date = "2023-01-01"
end_date = "2023-12-31"
year_group = "12"
numAssessments = 0

while True:
    year_group, data = input_and_req(start_date, end_date, year_group)
    result: Result = parse_json(data)
    assessments = result.filter_by_year(year_group)
    print(f"Found {len(assessments)} assessments for {start_date} to {end_date}")

    if len(assessments) < numAssessments:
        break

    numAssessments = len(assessments)

    start_date = (
        datetime.strptime(start_date, "%Y-%m-%d") - timedelta(days=1)
    ).strftime("%Y-%m-%d")
