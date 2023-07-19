import os
from datetime import datetime

import requests
from dotenv import load_dotenv


def input_and_req(start_date=None, end_date=None, year_group=None):
    load_dotenv()

    headers = {
        "Authorization": os.getenv("AUTH"),
        "Accept": "application/json",
        "Content-Type": "application/json",
    }

    if start_date is None or end_date is None:
        # request and validate input from user in form YYYY-MM-DD for start and end time
        valid = False
        while not valid:
            start_date = input("Enter start date in format YYYY-MM-DD: ")
            end_date = input("Enter end date in format YYYY-MM-DD: ")
            try:
                start_date = datetime.strptime(start_date, "%Y-%m-%d")
                end_date = datetime.strptime(end_date, "%Y-%m-%d")
                if start_date < end_date:
                    valid = True
                else:
                    print("Start date must be before end date")
            except ValueError:
                print("Invalid date format")
    else:
        try:
            start_date = datetime.strptime(start_date, "%Y-%m-%d")
            end_date = datetime.strptime(end_date, "%Y-%m-%d")
            if start_date >= end_date:
                raise ValueError
        except ValueError:
            print("Start date must be before end date")
            return None

    # convert to format required by API, start midnight and end 11:59pm
    start_date = start_date.strftime("%Y-%m-%dT00:00:00+11:00")
    end_date = end_date.strftime("%Y-%m-%dT23:59:59+11:00")

    if year_group is None:
        # input year group between 7 and 13
        valid = False
        while not valid:
            year_group = input("Enter year group between 7 and 13: ")
            try:
                year_group = int(year_group)
                if 7 <= year_group <= 13:
                    valid = True
                else:
                    print("Year group must be between 7 and 13")
            except ValueError:
                print("Invalid year group")
    else:
        try:
            year_group = int(year_group)
            if not 7 <= year_group <= 13:
                raise ValueError
        except ValueError:
            print("Year group must be between 7 and 13")
            return None

    # ,"yearLevel":{{"name": "{year_group}"}}
    f = f'{{"weighted":true,"workType":{{"name":"Assessment task"}},"dueDate":{{"from": "{start_date}","to": "{end_date}"}}}}'
    params = {
        "filter": f,
        "limit": 10000,  # Hopefully this is enough...
    }

    req = requests.get(
        os.getenv("HOST"),
        params=params,
        headers=headers,
    )

    return year_group, req.json(), req.status_code
