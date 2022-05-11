
import pandas as pd
from pyobistools.validation import check_fields

field_data = pd.DataFrame({
  'occurrenceID': ["1", "2", "3"],
  'scientificName': ["Abra alba", pd.NA, ""],
  'locality': ["North Sea", "English Channel", "Flemish Banks"],
  'minimumDepthInMeters': ["10", "", "5"]})

# require more test date for other analysis type


def test_check_fields_default():
    """
    check_fields_default detects missing or empty required and recommended fields
    for the occurrence_core fromat. This is the default behaviour for check_fields
    """
    # required terms
    error = check_fields.check_fields(field_data)
    # print(error)
    assert len(error.index) == 9

    # recommended terms
    error = check_fields.check_fields(field_data, level="warning")
    print(error)
    assert len(error.index) == 10


def test_check_fields_eventcore():
    """
    check_fields_default detects missing or empty required and recommended fields
    for the occurrence_core fromat. This is the default behaviour for check_fields
    """
    # required terms
    error = check_fields.check_fields(field_data, analysis_type="event_core")
    # print(error)
    assert len(error.index) == 9

    # recommended terms
    error = check_fields.check_fields(field_data, analysis_type="event_core", level="warning")
    print(error)
    assert len(error.index) == 10


def test_check_fields_occurrence_extension():
    """
    check_fields_default detects missing or empty required and recommended fields
    for the occurrence_core fromat. This is the default behaviour for check_fields
    """
    # required terms
    error = check_fields.check_fields(field_data, analysis_type="occurrence_extension")
    print(error)
    assert len(error.index) == 9

    # recommended terms
    error = check_fields.check_fields(field_data, analysis_type="occurrence_extension", level="warning")
    print(error)
    assert len(error.index) == 10


def test_check_fields_extended_measurement_or_fact():
    """
    check_fields_default detects missing or empty required and recommended fields
    for the occurrence_core fromat. This is the default behaviour for check_fields
    """
    # required terms
    error = check_fields.check_fields(field_data, analysis_type="extended_measurement_or_fact")
    print(error)
    assert len(error.index) == 9

    # recommended terms
    error = check_fields.check_fields(field_data, analysis_type="extended_measurement_or_fact", level="warning")
    print(error)
    assert len(error.index) == 10
