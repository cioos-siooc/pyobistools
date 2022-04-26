"""
map_fields
"""

import pandas as pd

def test_map_fields():
    assert 4 == 5

"""
  df <- map_fields(data.frame(x=1:3, y=4:6),
                   list(decimalLongitude="x", decimalLatitude="y"))
  expect_true(all(c("decimalLongitude", "decimalLatitude") %in% names(df)))
  expect_equal(ncol(df), 2)
"""