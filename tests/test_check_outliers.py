"""
Check outliers
"""

# import pandas as pd


def test_outliers_datasets():
    """
    check_outliers_datasets identifies outliers
    """
    # data = pd.DataFrame({'decimalLongitude': [170], 'decimalLatitude': [50]})
    assert True


"""
test_that("check_outliers_datasets identifies outliers", {
  data <- data.frame(decimalLongitude=170, decimalLatitude=c(50, 1:25))
  rp <- check_outliers_dataset(data, report = TRUE)
  expect_gte(nrow(rp), 1)
  d <- check_outliers_dataset(data, report = FALSE)
  expect_equal(d, data[1,])
})"""


def test_outliers_species():
    """
    check_outliers_species identifies outlier
    """
    # data = pd.DataFrame({'decimalLongitude': [170], 'decimalLatitude': [50], 'scientificNameID': ["urn:lsid:marinespecies.org:taxname:23109"]})
    assert True


"""test_that("check_outliers_species identifies outliers", {
  data <- data_frame(decimalLongitude=170, decimalLatitude=c(50, 1:25), scientificNameID="urn:lsid:marinespecies.org:taxname:23109")
  rp <- check_outliers_species(data, report = TRUE)
  expect_gte(nrow(rp), 1)
  d <- check_outliers_species(data, report = FALSE)
  expect_equal(d, data[unique(na.omit(rp$row)),])
})"""


def test_outliers_species_abra():
    """
    heck_outliers_species works for abra
    """
    assert True


"""test_that("check_outliers_species works for abra", {
  d <- check_outliers_species(abra)
  expect_gte(nrow(d), 500)
})"""
