"""
check eventIDs
"""

import numpy as np
import pandas as pd

from pyobistools.validation.check_eventids import (check_eventids,
                                                   check_extension_eventids)

NaN = np.nan


def test_check_eventids_presence_eventids_parenteventid():
    field_data = pd.DataFrame({
        'occurrenceID': ["1", "2", "3"],
        'measurementid': ["1", "2", "3"],
        'measurementtype': ["temperature", "tail length", "temperature"],
        'measurementvalue': [12, 12.7, 15.873],
        'measurementunit': ["C", "cm", "C"],
        'measurementremarks': ["", NaN, "not calibrated"]
    })
    correct_data = pd.DataFrame(data={
        'field': ["eventid", "parenteventid"],
        'level': ["error", "error"],
        'row':  ['NaN', 'NaN'],
        'message': ["Field eventid is missing", "Field parenteventid is missing"]})

    error = check_eventids(field_data)

    # reset index of both dataframe or the compare won't work
    # assert correct_data.reset_index(drop=True).equals(error.reset_index(drop=True)) == True
    assert correct_data.astype(str).reset_index(drop=True).equals(
        error.astype(str).reset_index(drop=True))


def test_check_eventids_duplicate_eventIDs():
    """
    check_fields_eventcore detects missing or empty required and recommended fields
    for the event_core format.

    """
    field_data = pd.DataFrame({
        'eventid': [1, 1, 3],
        'decimallatitude': [46.0, 48, ''],
        'parenteventid': [1, 1, 1],
        'countrycode': ["CA", "CA", "US"],
    })

    error = check_eventids(field_data)
    assert len(error.index) == 2


def test_check_eventids_parenteventids_corresponding_eventIDs():
    field_data = pd.DataFrame({
        'eventid': ["1", "2", "3"],
        'parenteventid': ["1", "2", "4"],
        'measurementid': ["1", "2", "3"],
        'measurementtype': ["temperature", "tail length", "temperature"],
        'measurementvalue': [12, 12.7, 15.873],
        'measurementunit': ["C", "cm", "C"],
        'measurementremarks': ["", NaN, "not calibrated"]
    })

    correct_data = pd.DataFrame(data={
        'field': ["parenteventid"],
        'level': ["error"],
        'row':  [2],
        'message': ["parenteventid 4 has no corresponding eventID"]})

    error = check_eventids(field_data)

    assert correct_data.astype(str).reset_index(drop=True).equals(
        error.astype(str).reset_index(drop=True))


def test_check_eventids_eventids_extension_corresponding_core():

    event = pd.DataFrame({
        'eventid': ["1", "2", "3"],
        'parenteventid': ["1", "2", "4"],
        'measurementid': ["1", "2", "3"],
        'measurementtype': ["temperature", "tail length", "temperature"],
        'measurementvalue': [12, 12.7, 15.873],
        'measurementunit': ["C", "cm", "C"],
        'measurementremarks': ["", NaN, "not calibrated"]
    })

    extension = pd.DataFrame({
        'eventid': ["1", "6", "3"],
        'parenteventid': ["1", "2", "4"],
        'measurementid': ["1", "2", "3"],
        'measurementtype': ["temperature", "tail length", "temperature"],
        'measurementvalue': [12, 12.7, 15.873],
        'measurementunit': ["C", "cm", "C"],
        'measurementremarks': ["", NaN, "not calibrated"]
    })

    error = check_extension_eventids(event=event, extension=extension)
    assert len(error.index) == 1
