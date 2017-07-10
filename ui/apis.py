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
    Takes care of fetching the data from the MBTA API.
    The fields expected from the CSV file are:
    TimeStamp, Origin, Trip, Destination, ScheduledTime, Lateness, Track, Status

    Args:
        None

    Returns:
        csv.DictReader: a cvs reader for the data coming from the MBTA API

    Raises:
        csv.Error: csv parsing errors are intentionally not handled
    """
    # fetch the data
    response = requests.get(settings.DEPARTURE_BOARD_URL)
    response.raise_for_status()
    mbta_data_list = response.text.splitlines()
    # the first row contains the fields
    fields = mbta_data_list[0].split(',')
    return csv.DictReader(mbta_data_list[1:], fields)


def get_mbta_stations_boards():
    """
    Retrieves and formats the data coming from the MBTA API.
    Args:
        None

    Returns:
        dict: A dictionary representing the formatted data coming from the MBTA API
    """
    reader = fetch_mbta_times()
    # read the data and reformat some fields
    now = datetime.now(tz=pytz.timezone('US/Eastern'))
    formatted_data = {
        'CurrentTime': now.strftime('%I:%M %p'),
        'CurrentDate': now.strftime('%m-%d-%Y'),
        'CurrentWeekDay': now.strftime('%A'),
    }
    for row in reader:
        formatted_row = {}
        station = ''
        for key, value in row.items():
            if key == "Origin":
                station = value
                continue
            elif key == 'TimeStamp':
                continue
            elif key == 'ScheduledTime':
                parsed_time = datetime.fromtimestamp(int(value), tz=pytz.timezone('US/Eastern'))
                formatted_row['ScheduledHour'] = parsed_time.strftime('%I:%M %p')
                formatted_row['ScheduledDay'] = parsed_time.strftime('%b %d')
            elif key == 'Lateness':
                # round to the bottom integer
                formatted_row['LatenessMinutes'] = int(round(int(value)/60))
                continue
            formatted_row[key] = value

        formatted_data.setdefault(station, []).append(formatted_row)
    # sort by ScheduledTime just to be sure to return all the values in the correct order
    formatted_data['North Station'].sort(key=lambda x: x['ScheduledTime'])
    formatted_data['South Station'].sort(key=lambda x: x['ScheduledTime'])
    return formatted_data
