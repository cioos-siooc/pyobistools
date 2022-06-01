
import pandas as pd
from pyobistools.validation.check_fields import check_fields
import numpy as np
NaN = np.nan

def test_check_fields_default():
    """
    check_fields_default detects missing or empty required and recommended fields
    for the occurrence_core format. This is the default behaviour for check_fields
    """
    field_data = pd.DataFrame({
      'occurrenceID': ["1", "2", "3"],
      'scientificName': ["Abra alba", NaN, ""],
      'locality': ["North Sea", "English Channel", "Flemish Banks"],
      'minimumDepthInMeters': ["10", "", "5"]})
    # required terms
    correct_data = pd.DataFrame(data={
      'field': ["basisofrecord", "scientificnameid", "eventdate", "decimallatitude", "decimallongitude", "occurrencestatus", "countrycode", "kingdom", "geodeticdatum", "scientificname", "scientificname"], 
      'level': ["error", "error", "error", "error", "error", "error", "error", "error", "error", "error", "error"], 
      'message': ["Required field basisofrecord is missing", "Required field scientificnameid is missing", "Required field eventdate is missing", "Required field decimallatitude is missing", "Required field decimallongitude is missing", "Required field occurrencestatus is missing", "Required field countrycode is missing", "Required field kingdom is missing", "Required field geodeticdatum is missing", 'Empty value for required field scientificname', 'Empty value for required field scientificname'], 
      'row': [NaN, NaN, NaN, NaN, NaN, NaN, NaN, NaN, NaN, 1, 2] })
    error = check_fields(field_data)

    # reset index of both dataframe or the compare won't work
    assert correct_data.reset_index(drop=True).equals(error.reset_index(drop=True)) == True

    # recommended terms
    error = check_fields(field_data, level="warning")
    assert len(error.index) == 11


def test_check_fields_eventcore():
    """
    check_fields_eventcore detects missing or empty required and recommended fields
    for the event_core format.

    """
    field_data = pd.DataFrame({
      'eventid': ["1", "2", "3"],
      'decimallatitude': [46.0, 48, ''],
      'countrycode': ["CA", "CA", "US"],
      })

    # required terms
    error = check_fields(field_data, analysis_type="event_core")
    assert len(error.index) == 4

    # recommended terms
    error = check_fields(field_data, analysis_type="event_core", level="warning")
    assert error is None


def test_check_fields_occurrence_extension():
    """
    check_fields_default detects missing or empty required and recommended fields
    for the occurrence_core fromat. This is the default behaviour for check_fields
    """
    field_data = pd.DataFrame({
      'eventid': ["1", "1", "2"],
      'occurrenceID': ["1", "2", "3"],
      'scientificName': ["Abra alba", NaN, ""],
      'occurrencestatus': ["North Sea", "English Channel", "Flemish Banks"]
      })
    # required terms
    error = check_fields(field_data, analysis_type="occurrence_extension")
    assert len(error.index) == 5

    # recommended terms
    error = check_fields(field_data, analysis_type="occurrence_extension", level="warning")
    assert error is None


def test_check_fields_extended_measurement_or_fact():
    """
    check_fields_default detects missing or empty required and recommended fields
    for the occurrence_core fromat. This is the default behaviour for check_fields
    """
    field_data = pd.DataFrame({
      'eventid': ["1", "1", "1"],
      'occurrenceID': ["1", "1", "2"],
      'measurementid': ["1", "2", "3"],
      'measurementtype': ["temperature", "tail length", "temperature"],
      'measurementvalue': [12, 12.7, 15.873],
      'measurementunit': ["C", "cm", "C"],
      'measurementremarks': ["", NaN, "not calibrated"]
      })
    # required terms
    error = check_fields(field_data, analysis_type="extended_measurement_or_fact_extension")
    assert len(error.index) == 9

    # recommended terms
    error = check_fields(field_data, analysis_type="extended_measurement_or_fact_extension", level="warning")
    assert error is None
