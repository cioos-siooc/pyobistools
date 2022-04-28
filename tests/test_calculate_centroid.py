"""
calculate_centroid
"""

# import pandas as pd


def get_test_wkt():
    """
    generate wkt
    """
    return None


"""
get_test_wkt <- function(bbox=NULL) {
  skip_if_not_installed("randgeo")
  set.seed(42)
  list(wkt_point = randgeo::wkt_point(),
       wkt_multipoint = randgeo::wkt_point(2, as_multi = TRUE), # currently only on the iobis fork iobis/randgeo
       wkt_line = randgeo::wkt_linestring(),
       wkt_multiline = randgeo::wkt_linestring(2, as_multi = TRUE),
       wkt_polygon = randgeo::wkt_polygon(),
       wkt_multipolygon = randgeo::wkt_polygon(2, as_multi = TRUE),
       multiple_wkt_point = randgeo::wkt_point(5),
       multiple_wkt_polygon = randgeo::wkt_polygon(5))
}
"""


def test_calculate_centroid_multiple():
    """
    calculate_centroid for multiple common WKT formats works
    """
    assert True


"""
test_that("calculate_centroid for multiple common WKT formats works", {
  d <- get_test_wkt()
  for (n in names(d)) {
    centr <- calculate_centroid(d[[n]])
    expect_equal(nrow(centr), length(d[[n]]))
    expect_equal(colnames(centr), c("decimalLongitude", "decimalLatitude", "coordinateUncertaintyInMeters"))
  }
})
"""


def test_calculate_centroid_missing():
    """
    calculate_centroid missing wkt works
    """
    assert True


"""
test_that("calculate_centroid missing wkt works", {
  expect_equal(NROW(calculate_centroid(NULL)), 0)
})
"""


def test_calculate_centroid_simple_point():
    """
    calculate_centroid simple wkt point works
    """
    assert True


"""
test_that("calculate_centroid simple wkt point works", {
  centr <- calculate_centroid("POINT (0 0)")
  expect_equal(centr[1,1], 0)
  expect_equal(centr[1,2], 0)
})
"""


def test_calculate_centroid_simple_linestring():
    """
    calculate_centroid simple wkt linestring works
    """
    assert True


"""
test_that("calculate_centroid simple wkt linestring works", {
  centr <- calculate_centroid("LINESTRING (0 -1, 0 0, 0 1)")
  expect_equal(centr[1,1], 0)
  expect_equal(centr[1,2], 0)
})
"""


def test_calculate_centroid_simple_linestring2():
    """
    calculate_centroid simple wkt linestring works2
    """
    assert True


"""
test_that("calculate_centroid simple wkt linestring works", {
  centr <- calculate_centroid("LINESTRING (-1 -1, 0 -1, 0 1, 1 1)")
  expect_equal(centr[1,1], 0)
  expect_equal(centr[1,2], 0)
})
"""


def test_calculate_centroid_simple_point2():
    """
    calculate_centroid simple wkt point works
    """
    assert True


"""
test_that("calculate_centroid simple wkt polygon works", {
  centr <- calculate_centroid("POLYGON ((-1 -1, -1 1, 1 1, 1 -1, -1 -1))")
  expect_equal(centr[1,1], 0)
  expect_equal(centr[1,2], 0)
})
"""


def test_calculate_centroid_accross_dateline():
    """
    calculate_centroid accross dateline works
    """
    assert True


"""
test_that("calculate_centroid accross dateline works", {
  centr <- calculate_centroid("POLYGON ((179 -1, 179 1, -179 1, -179 -1, 179 -1))")
  expect_equal(abs(centr[1,1]), 180)
  expect_equal(centr[1,2], 0)
})
"""
