"""
Apis for ui app
"""
import csv
from datetime import datetime

import pytz
import requests
from django.conf import settings


def fetch_mbta_times():
    """
    Takes care of fetching the data from the MBTA API and parsing the content.
    The fields expected from the CSV file are:
    TimeStamp, Origin, Trip, Destination, ScheduledTime, Lateness, Track, Status,

    Args:
        None

    Returns:
        list: A list of dictionaries representing the data coming from the MBTA API

    Raises:
        csv.Error: csv parsing errors are intentionally not handled
    """
    # fetch the data
    response = requests.get(settings.DEPARTURE_BOARD_URL)
    response.raise_for_status()
    mbta_data_list = response.text.splitlines()
    # the first row contains the fields
    fields = mbta_data_list[0].split(',')
    reader = csv.DictReader(mbta_data_list[1:], fields)
    # read the data and reformat some fields
    formatted_data = []
    for row in reader:
        formatted_row = {}
        for key, value in row.items():
            formatted_row[key] = value
            if key == 'ScheduledTime':
                parsed_time = datetime.fromtimestamp(int(value), tz=pytz.timezone('US/Eastern'))
                formatted_row['ScheduledHour'] = parsed_time.strftime('%I:%M %p')
                formatted_row['ScheduledDay'] = parsed_time.strftime('%b %d')
            elif key == 'Lateness':
                # round to the bottom integer
                formatted_row['LatenessMinutes'] = int(round(int(value)/60))
        formatted_data.append(formatted_row)
    # sort by ScheduledTime just to be sure to return all the values in the correct order
    formatted_data.sort(key=lambda x: x['ScheduledTime'])

    return formatted_data
