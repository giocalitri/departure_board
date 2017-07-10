"""
Apis for ui app
"""
import csv

import requests
from django.conf import settings


def fetch_times():
    """
    Takes care of fetching the data from the MBTA API and parsing the content

    Args:
        None

    Returns:
        list: A list of dictionaries representing the data coming from the MBTA API

    Raises:
        csv.Error: csv parsing errors are intentionally not handled
    """
    response = requests.get(settings.DEPARTURE_BOARD_URL)
    response.raise_for_status()

    mbta_data_list = response.text.splitlines()
    fields = mbta_data_list[0].split(',')
    reader = csv.DictReader(mbta_data_list[1:], fields)
    return [row for row in reader]
