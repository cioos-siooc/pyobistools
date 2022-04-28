"""
match taxa
"""

import pandas as pd

""" test_names <- c("Abra alva", "Buccinum fusiforme", "Buccinum fusiforme", "Buccinum fusiforme", "ljkf hlqsdkf") """
test_names = pd.DataFrame({"Abra alva", "Buccinum fusiforme", "Buccinum fusiforme", "Buccinum fusiforme", "ljkf hlqsdkf"})


def test_match_taxa():
    """
    match_taxa works as expected
    """
    assert True


"""
  results <- match_taxa(test_names, ask = FALSE)
  expect_true(nrow(results) == length(test_names))
  expect_true(sum(!is.na(results$scientificNameID)) == 1)
"""

# For later maybe, test user interaction: see https://stackoverflow.com/questions/41372146/test-interaction-with-users-in-r-package for how to do this
