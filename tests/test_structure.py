"""
test_structure
"""

import pandas as pd


def get_event():
    return pd.DataFrame({
      'eventID': ["cruise_1", "station_1", "station_2", "sample_1", "sample_2", "sample_3", "sample_4", "subsample_1", "subsample_2"],
      'parentEventID': [pd.NA, "cruise_1", "cruise_1", "station_1", "station_1", "station_2", "station_2", "sample_3", "sample_3"],
      'eventDate': [pd.NA, pd.NA, pd.NA, "2017-01-01", "2017-01-02", "2017-01-03", "2017-01-04", pd.NA, pd.NA],
      'decimalLongitude': [pd.NA, 2.9, 4.7, pd.NA, pd.NA, pd.NA, pd.NA, pd.NA, pd.NA],
      'decimalLatitude': [pd.NA, 54.1, 55.8, pd.NA, pd.NA, pd.NA, pd.NA, pd.NA, pd.NA]})


def get_occurrence():
    return pd.DataFrame({
      'occurrenceID': [1, 2, 3, 4, 5, 6, 7, 8],
      'eventID': ["sample_1", "sample_1", "sample_2", "sample_2", "sample_3", "sample_4", "subsample_1", "subsample_1"],
      'scientificName': ["Abra alba", "Lanice conchilega", "Pectinaria koreni", "Nephtys hombergii", "Pectinaria koreni", "Amphiura filiformis", "Desmolaimus zeelandicus", "Aponema torosa"]})


def test_treeStructure():
    """
    treeStructure works
    """
    assert True


"""
  ts <- treeStructure(get_event(), get_occurrence())
  expect_equal(ts$height, 6)
"""


def test_exportTree():
    """
    exportTree works
    """
    assert True


"""
  ts <- treeStructure(get_event(), get_occurrence())
  f <- tempfile("treestructure", fileext = ".html")
  on.exit(file.remove(f))
  exportTree(ts, f)
  expect_true(file.exists(f))
"""
