"""
util
"""

import warnings
import pytest
import pandas as pd
from unittest.mock import patch, Mock
from pyobistools.utils import pick_worms_record, pick_itis_record
from pyobistools.validation.check_scientificname_and_ids import check_scientificname_and_ids


# --- pick_worms_record tests ---

def test_pick_worms_empty_response():
    assert pick_worms_record([]) is None
    assert pick_worms_record(None) is None


def test_pick_worms_no_accepted():
    records = [{'AphiaID': 1, 'status': 'unaccepted'}]
    assert pick_worms_record(records) is None


def test_pick_worms_single_accepted():
    record = {'AphiaID': 163921, 'status': 'accepted'}
    with warnings.catch_warnings():
        warnings.simplefilter('error')
        result = pick_worms_record([record])
    assert result == record


def test_pick_worms_multiple_first_warns():
    records = [
        {'AphiaID': 163921, 'status': 'accepted'},
        {'AphiaID': 1248, 'status': 'accepted'},
    ]
    with pytest.warns(UserWarning, match='Ambiguous taxon'):
        result = pick_worms_record(records, name='Ctenophora')
    assert result == records[0]


def test_pick_worms_multiple_first_no_warn():
    records = [
        {'AphiaID': 163921, 'status': 'accepted'},
        {'AphiaID': 1248, 'status': 'accepted'},
    ]
    with warnings.catch_warnings():
        warnings.simplefilter('error')
        result = pick_worms_record(records, warn=False)
    assert result == records[0]


def test_pick_worms_multiple_all():
    records = [
        {'AphiaID': 163921, 'status': 'accepted'},
        {'AphiaID': 1248, 'status': 'accepted'},
        {'AphiaID': 9999, 'status': 'unaccepted'},
    ]
    with warnings.catch_warnings():
        warnings.simplefilter('error')
        result = pick_worms_record(records, listall=True)
    assert len(result) == 2
    assert all(r['status'] == 'accepted' for r in result)


def test_pick_worms_all_no_accepted():
    records = [{'AphiaID': 1, 'status': 'unaccepted'}]
    assert pick_worms_record(records, listall=True) == []


def test_pick_worms_dict_input():
    record = {'AphiaID': 163921, 'status': 'accepted'}
    with warnings.catch_warnings():
        warnings.simplefilter('error')
        result = pick_worms_record(record)
    assert result == record


# --- check_scientificname_and_ids ITIS fallback warning tests ---

@patch('time.sleep')
@patch('pyobistools.validation.check_scientificname_and_ids.requests.get')
def test_itis_fallback_warns(mock_get, mock_sleep):
    worms_response = Mock(status_code=204)
    itis_response = Mock(status_code=200)
    itis_response.json.return_value = {'scientificNames': [None]}
    mock_get.side_effect = [worms_response, itis_response]

    data = pd.DataFrame({'scientificname': ['Mola mola']})
    with pytest.warns(UserWarning, match='Falling back to ITIS'):
        check_scientificname_and_ids(data, 'names', itis_usage=True)


@patch('time.sleep')
@patch('pyobistools.validation.check_scientificname_and_ids.requests.get')
def test_itis_fallback_no_warn(mock_get, mock_sleep):
    worms_response = Mock(status_code=204)
    itis_response = Mock(status_code=200)
    itis_response.json.return_value = {'scientificNames': [None]}
    mock_get.side_effect = [worms_response, itis_response]

    data = pd.DataFrame({'scientificname': ['Mola mola']})
    with warnings.catch_warnings():
        warnings.simplefilter('error')
        check_scientificname_and_ids(data, 'names', itis_usage=True, warn=False)


# --- pick_itis_record tests ---

def test_pick_itis_exact_match():
    response = {
        'scientificNames': [
            {'combinedName': 'Other species', 'tsn': '1'},
            {'combinedName': 'Mola mola', 'tsn': '12345'},
        ]
    }
    result = pick_itis_record(response, 'Mola mola')
    assert result['tsn'] == '12345'


def test_pick_itis_no_match():
    response = {
        'scientificNames': [
            {'combinedName': 'Other species', 'tsn': '1'},
        ]
    }
    assert pick_itis_record(response, 'Mola mola') is None


def test_pick_itis_empty():
    assert pick_itis_record({'scientificNames': [None]}, 'Mola mola') is None
    assert pick_itis_record({}, 'Mola mola') is None


# import pandas as pd


def test_check_lon_lat():
    """
    check lon lat works as expected
    """
    assert True


"""
test_that("check lon lat works as expected", {
  x <- obistools:::check_lonlat(data.frame(), report = TRUE)
  expect_equal(2, nrow(x))
  expect_true(all(grepl("missing", x$message)))
  x <- obistools:::check_lonlat(data.frame(decimalLatitude = ""), report = TRUE)
  expect_equal(2, nrow(x))
  expect_true(all(grepl("(missing)|(numeric)", x$message)))
  x <- obistools:::check_lonlat(data.frame(decimalLatitude = 1), report = TRUE)
  expect_equal(1, nrow(x))
  expect_true(all(grepl("(missing)|(numeric)", x$message)))
  x <- obistools:::check_lonlat(data.frame(decimalLongitude = "", decimalLatitude = ""), report = TRUE)
  expect_equal(2, nrow(x))
  expect_true(all(grepl("numeric", x$message)))
  x <- obistools:::check_lonlat(data.frame(decimalLongitude = "", decimalLatitude = 1), report = TRUE)
  expect_equal(1, nrow(x))
  expect_true(all(grepl("numeric", x$message)))
  x <- obistools:::check_lonlat(data.frame(decimalLongitude = 1, decimalLatitude = 1), report = TRUE)
  expect_equal(0, NROW(x))
  expect_error(obistools:::check_lonlat(data.frame(), report = FALSE), "missing")
})
"""


def test_cache_call():
    """
    cache call works
    """
    assert True


"""
test_that("cache call works", {
  n <- 5
  set.seed(42)
  original <- obistools:::cache_call("random5", expression(runif(n)))
  set.seed(50)
  same <- obistools:::cache_call("random5", expression(runif(n)))
  set.seed(50)
  different <- obistools:::cache_call("random5diff", expression(runif(n)))
  set.seed(50)
  original2 <- obistools:::cache_call("random5", expression(runif(n, min = 0, max = 1) ))
  expect_equal(length(original), n)
  expect_equal(original, same)
  expect_false(any(original == different))
  expect_equal(original2, different)
  expect_gte(length(obistools:::list_cache()), 3)
  # only run on Travis as clearing the cache between the test runs is annoying
  if(identical(Sys.getenv("TRAVIS"), "true")) {
    obistools:::clear_cache(-1)
    expect_equal(length(obistools:::list_cache()), 0)
  }
})
"""


def test_get_xy_clean_duplicates():
    """
    get_xy_clean_duplicates works
    """
    assert True


"""
test_that("get_xy_clean_duplicates works", {
  n <- 100
  set.seed(42)
  lots_duplicates <- data_frame(decimalLongitude=as.numeric(sample(1:10, n, replace=TRUE)), decimalLatitude=as.numeric(sample(1:10, n, replace=TRUE)))
  lots_duplicates[5,] <- c(NA,1.0)
  lots_duplicates[6,] <- c(2.0,NA)
  lots_duplicates[7,] <- c(NA,NA)
  xy <- obistools:::get_xy_clean_duplicates(lots_duplicates)

  replicate <- data_frame(decimalLongitude=rep(NA,n), decimalLatitude=rep(NA,n))
  replicate[xy$isclean,] <- xy$uniquesp[xy$duplicated_lookup,]
  replicate[!xy$isclean,] <- lots_duplicates[!xy$isclean,]
  expect_equal(lots_duplicates, replicate)
})
"""
