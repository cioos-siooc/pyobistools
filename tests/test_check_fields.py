
import numpy as np
import pandas as pd

from pyobistools.validation.check_fields import check_fields

NaN = np.nan


def test_check_fields_default():
    """
    test_check_fields_default detects missing or empty required and recommended fields (if any)
    for the occurrence_core format. It also checks for empty values and case sensitivity.
    """
    field_data = pd.DataFrame({
        'occurrenceID': ["1", "2", "3"],
        'scientificName': ["Abra alba", NaN, ""],
        'locality': ["North Sea", "English Channel", "Flemish Banks"],
        'minimumDepthInMeters': ["10", "", "5"]})
    # required terms
    correct_data = pd.DataFrame(data={
        'field': ["basisOfRecord", "scientificNameID", "eventDate", "decimalLatitude", "decimalLongitude", "occurrenceStatus", "countryCode", "kingdom", "geodeticDatum", "scientificName", "scientificName"],
        'level': ["error", "error", "error", "error", "error", "error", "error", "error", "error", "error", "error"],
        'row': ['NaN', 'NaN', 'NaN', 'NaN', 'NaN', 'NaN', 'NaN', 'NaN', 'NaN', '1', '2'],
        'message': ["Required field basisOfRecord is missing", "Required field scientificNameID is missing", "Required field eventDate is missing", "Required field decimalLatitude is missing", "Required field decimalLongitude is missing", "Required field occurrenceStatus is missing", "Required field countryCode is missing", "Required field kingdom is missing", "Required field geodeticDatum is missing", 'Empty value for required field scientificName', 'Empty value for required field scientificName']
    })

    # required terms & empty values
    error = check_fields(field_data)

    assert correct_data.astype(str).reset_index(drop=True).equals(
        error.astype(str).reset_index(drop=True))

    # recommended terms if any, empty values & case sensitivity check
    error = check_fields(field_data, level="warning")
    assert len(error.index) == 11


def test_check_fields_event_core():
    """
    test_check_fields_event_core detects missing or empty required and recommended fields (if any)
    for the event_core format. It also checks for empty values and case sensitivity.

    """
    field_data = pd.DataFrame({
        'eventID': ["1", "2", "3"],
        'decimalLatitude': [46.0, 48, ''],
        'countryCode': ["CA", "CA", "US"],
    })

    # required terms & empty values
    error = check_fields(field_data, analysis_type="event_core")
    assert len(error.index) == 4

    # recommended terms if any, empty values & case sensitivity check
    error = check_fields(field_data, analysis_type="event_core", level="warning")
    assert error.empty


def test_check_fields_occurrence_extension():
    """
    test_check_fields_occurrence_extension detects missing or empty required and recommended fields (if any)
    for the occurrence_extension fromat. It also checks for empty values and case sensitivity.
    """
    field_data = pd.DataFrame({
        'eventid': ["1", "1", "2"],
        'occurrenceID': ["1", "2", "3"],
        'scientificName': ["Abra alba", NaN, ""],
        'occurrencestatus': ["North Sea", "English Channel", "Flemish Banks"]
    })

    # required terms & empty values
    error = check_fields(field_data, analysis_type="occurrence_extension")
    assert len(error.index) == 5

    # recommended terms if any, empty values & case sensitivity check
    error = check_fields(field_data, analysis_type="occurrence_extension", level="warning")
    assert len(error.index) == 2


def test_check_fields_extended_measurement_or_fact_extension():
    """
    test_check_fields_extended_measurement_or_fact_extension detects missing or empty required and recommended fields (if any)
    for the extended_measurement_or_fact_extension fromat. It also checks for empty values and case sensitivity.
    """
    field_data = pd.DataFrame({
        'eventID': ["1", "1", "1"],
        'occurrenceID': ["1", "1", "2"],
        'measurementID': ["1", "2", "3"],
        'measurementType': ["temperature", "tail length", "temperature"],
        'measurementValue': [12, 12.7, 15.873],
        'measurementUnit': ["C", "cm", "C"],
        'measurementremarks': ["", NaN, "not calibrated"]
    })

    # required terms & empty values
    error = check_fields(field_data, analysis_type="extended_measurement_or_fact_extension")
    assert len(error.index) == 9

    # recommended terms if any, empty values & case sensitivity check
    error = check_fields(
        field_data, analysis_type="extended_measurement_or_fact_extension", level="warning")
    assert len(error.index) == 1
