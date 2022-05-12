
import pandas as pd
from pyobistools.validation import check_fields


def test_check_fields_default():
    """
    check_fields_default detects missing or empty required and recommended fields
    for the occurrence_core format. This is the default behaviour for check_fields
    """
    field_data = pd.DataFrame({
      'occurrenceID': ["1", "2", "3"],
      'scientificName': ["Abra alba", pd.NA, ""],
      'locality': ["North Sea", "English Channel", "Flemish Banks"],
      'minimumDepthInMeters': ["10", "", "5"]})
    # required terms
    error = check_fields.check_fields(field_data)
    # print(error)
    assert len(error.index) == 9

    # recommended terms
    error = check_fields.check_fields(field_data, level="warning")
    assert len(error.index) == 10


def test_check_fields_eventcore():
    """
    check_fields_eventcore detects missing or empty required and recommended fields
    for the event_core format.

    """
    field_data = pd.DataFrame({
      'eventid': ["1", "2", "3"],
      'decimallatitude': [46.0, 48, 31.43563],
      'countrycode': ["CA", "CA", "US"],
      })

    # required terms
    error = check_fields.check_fields(field_data, analysis_type="event_core")
    assert len(error.index) == 3

    # recommended terms
    error = check_fields.check_fields(field_data, analysis_type="event_core", level="warning")
    assert error is None


def test_check_fields_occurrence_extension():
    """
    check_fields_default detects missing or empty required and recommended fields
    for the occurrence_core fromat. This is the default behaviour for check_fields
    """
    field_data = pd.DataFrame({
      'eventid': ["1", "1", "2"],
      'occurrenceID': ["1", "2", "3"],
      'scientificName': ["Abra alba", pd.NA, ""],
      'occurrencestatus': ["North Sea", "English Channel", "Flemish Banks"]
      })
    # required terms
    error = check_fields.check_fields(field_data, analysis_type="occurrence_extension")
    print(error)
    assert len(error.index) == 3

    # recommended terms
    error = check_fields.check_fields(field_data, analysis_type="occurrence_extension", level="warning")
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
      'measurementremarks': ["", pd.NA, "not calibrated"]
      })
    # required terms
    error = check_fields.check_fields(field_data, analysis_type="extended_measurement_or_fact_extension")
    print(error)
    assert len(error.index) == 7

    # recommended terms
    error = check_fields.check_fields(field_data, analysis_type="extended_measurement_or_fact_extension", level="warning")
    assert error is None
