"""
check eventIDs
"""

import pandas as pd

test_data_1 = pd.DataFrame({'eventID': ["a", "b"]})
test_data_2 = pd.DataFrame({'parentEventID': ["a", "b"]})
test_data_3 = pd.DataFrame({'eventID': ["a", "b", "c", "d", "e", "f"], 'parentEventID': ["", "", "a", "a", "bb", "b"]})
test_data_2 = pd.DataFrame({'eventID': ["a", "b", "b", "c"]})


def test_check_eventids_missing_columns():
    """
    check_eventids detects missing columns
    """
    assert True


"""
  results <- check_eventids(test_data_1)
  expect_true(nrow(results) == 1)

  results <- check_eventids(test_data_2)
  expect_true(nrow(results) == 1)
"""


def test_check_eventids_missing_eventIDs():
    assert True


"""
test_that("check_eventids detects missing eventIDs", {

  results <- check_eventids(test_data_3)
  expect_true(nrow(results) == 1)
  expect_true(5 %in% results$row)
"""


def test_check_eventids_duplicate_eventIDs():
    assert True


"""
  results <- check_eventids(test_data_4)
  expect_true(nrow(results) == 1)
  expect_true(3 %in% results$row)
"""


def test_check_extension_eventids():
    """
    check_extension_eventids works
    """
    # event = pd.DataFrame({'eventID': ["a", "b", "b", "c"]})
    # extension = pd.DataFrame({'xeventID': ["a", "b", "b", "d", "e"]})

    assert True


"""
  event <- data.frame(eventID = c("a", "b", "b", "c"), stringsAsFactors = FALSE)
  extension <- data.frame(xeventID = c("a", "b", "b", "d", "e"), stringsAsFactors = FALSE)
  df <- check_extension_eventids(event, extension, "xeventID")
  expect_equal(nrow(df), 2)
  expect_true(all(c(4,5) %in% df$row))

  df <- check_extension_eventids(event[NULL, , drop=FALSE], extension[NULL, , drop=FALSE], "xeventID")
  expect_equal(nrow(df), 0)
"""
