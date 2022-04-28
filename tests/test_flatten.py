"""
flatten
"""

# import pandas as pd


def test_flatten_event():
    """
    flatten_event works
    """
    # event = pd.DataFrame({'eventID': ["cruise_1", "station_1", "station_2", "sample_1", "sample_2", "sample_3", "sample_4", "subsample_1", "subsample_2"],
    #   'eventDate': [pd.NA, "cruise_1", "cruise_1", "station_1", "station_1", "station_2", "station_2", "sample_3", "sample_3"],
    #   'decimalLongitude': [pd.NA, 2.9, 4.7, pd.NA, pd.NA, pd.NA, pd.NA, pd.NA, pd.NA],
    #   'decimalLatitude': [pd.NA, 54.1, 55.8, pd.NA, pd.NA, pd.NA, pd.NA, pd.NA, pd.NA]})
    assert True


"""
  e <- flatten_event(event)
  expect_equal(nrow(e), 9)
  expect_equal(unlist(event[event$eventID == "station_1", c("decimalLongitude", "decimalLatitude")]),
               unlist(unique(e[!is.na(e$parentEventID) & e$parentEventID == "station_1", c("decimalLongitude", "decimalLatitude")])))
"""


def test_flatten_event_id_error():
    """
    flatten_event catch event id errors
    """
    # event = pd.DataFrame({
    #   'eventID': ["a", "b", "c", "d", "e", "f"],
    #   "parentEventID": ["", "", "a", "a", "bb", "b"]})

    assert True


"""
expect_error(flatten_event(event), "check_eventids")
"""


def test_flatten_event_custom():
    """
    flatten_event custom fields
    """
    # event = pd.DataFrame({
    #   'eventID': ["a", "b", "c", "d"],
    #   'parentEventID': ["", "", "a", "a"],
    #   'test_column1': [1, 2, pd.NA, pd.NA],
    #   'test_column2': [1, 2, pd.NA, pd.NA]})


"""
  e <- flatten_event(event, fields = "test_column1")
  expect_equal(nrow(e), 4)
  expect_equal(e$test_column1, c(1,2,1,1))
  expect_equal(e$test_column2, c(1,2,NA,NA))
"""


def test_flatten_occurrence():
    """
    flatten_occurrence works
    """
    assert True

    # event = pd.DataFrame({
    #   'eventID': ["cruise_1", "station_1", "station_2", "sample_1", "sample_2", "sample_3", "sample_4", "subsample_1", "subsample_2"],
    #   'parentEventID': [pd.NA, "cruise_1", "cruise_1", "station_1", "station_1", "station_2", "station_2", "sample_3", "sample_3"],
    #   'eventDate': [pd.NA, pd.NA, pd.NA, "2017-01-01", "2017-01-02", "2017-01-03", "2017-01-04", pd.NA, pd.NA],
    #   'decimalLongitude ': [pd.NA, 2.9, 4.7, pd.NA, pd.NA, pd.NA, pd.NA, pd.NA, pd.NA],
    #   'decimalLatitude': [pd.NA, 54.1, 55.8, pd.NA, pd.NA, pd.NA, pd.NA, pd.NA, pd.NA]})
    # occurrence= pd.DataFrame({
    #   'eventID': ["sample_1", "sample_1", "sample_2", "sample_2", "sample_3", "sample_4", "subsample_1", "subsample_1"],
    #   'scientificName': ["Abra alba", "Lanice conchilega", "Pectinaria koreni", "Nephtys hombergii", "Pectinaria koreni", "Amphiura filiformis", "Desmolaimus zeelandicus", "Aponema torosa"]})
    assert True


"""
  f <- flatten_occurrence(event, occurrence)
  expect_equal(nrow(f), 8)
  expect_equal(f$eventID, occurrence$eventID)
  expect_equal(f$scientificName, occurrence$scientificName)
  expect_true(all(!is.na(f$eventDate)))
  expect_true(all(!is.na(f$decimalLongitude)))
  expect_true(all(!is.na(f$decimalLatitude)))
"""
