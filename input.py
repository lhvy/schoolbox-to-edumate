"""
Takes input from user and makes request to API.
"""

import concurrent.futures
import os
import time
from datetime import datetime
from typing import Dict, Tuple

import requests
from dotenv import load_dotenv
from progress.spinner import Spinner


def make_request(host: str, params: Dict[str, str | int], headers: Dict[str, str]) -> requests.Response:
    """Make a request to the API.

    Args:
        host (str): Host URL
        params (Dict[str, str | int]): Parameters for the request
        headers (Dict[str, str]): Headers for the request

    Returns:
        requests.Response: Response from the API
    """
    return requests.get(host, params=params, headers=headers)

def input_and_req(
    start_date=None, end_date=None, year_group=None
) -> Tuple[int, str, str, dict, int]:
    """Takes input from user and makes request to API.

    Args:
        start_date (str, optional): Start date to search the API. Defaults to None.
        end_date (str, optional): End date to search the API. Defaults to None.
        year_group (str, optional): Year group to filter the API results. Defaults to None.

    Raises:
        ValueError: AUTH environment variable not set
        ValueError: HOST environment variable not set

    Returns:
        Tuple[int, str, str, dict, int] | None: _description_
    """
    load_dotenv()

    auth: str | None = os.getenv("AUTH")
    if auth is None:
        raise ValueError("AUTH environment variable not set")

    headers: Dict[str, str] = {
        "Authorization": auth,
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
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.strptime(end_date, "%Y-%m-%d")
        if start_date >= end_date:
            raise ValueError("Start date must be before end date")

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
        year_group = int(year_group)
        if not 7 <= year_group <= 13:
            raise ValueError("Year group must be between 7 and 13")

    # ,"yearLevel":{{"name": "{year_group}"}}
    # convert to format required by API, start midnight and end 11:59pm
    params: Dict[
        str,
        str | int,
    ] = {
        # I love daylight savings
        # This is a greedy filter that will match 1 hour before and after the start and end dates if the timezone is incorrect.
        "filter": f'{{"weighted":true,"workType":{{"name":"Assessment task"}},"dueDate":{{"from": "{start_date.strftime("%Y-%m-%dT00:00:00+11:00")}","to": "{end_date.strftime("%Y-%m-%dT23:59:59+10:00")}"}}}}',
        "limit": 10000,  # Hopefully this is enough...
    }

    host: str | None = os.getenv("HOST")
    if host is None:
        raise ValueError("HOST environment variable not set")

    spinner = Spinner('Requesting data from API... ')
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(make_request, host, params, headers)
        
        while not future.done():
            spinner.next()
            time.sleep(0.1)
            
        req = future.result()
    spinner.finish()

    return (
        year_group,
        start_date.strftime("%Y-%m-%d"),
        end_date.strftime("%Y-%m-%d"),
        req.json(),
        req.status_code,
    )
