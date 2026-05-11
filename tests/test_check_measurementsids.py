"""
check check_measurementids
"""

import numpy as np
import pandas as pd

from pyobistools.validation.check_measurementids import (check_measurementids)

NaN = np.nan


def test_check_measurementids():
    field_data = pd.DataFrame({
        'eventID': ["1", "2", "3"],
        'measurementID': ["1", "2", "2"],
        'measurementtype': ["temperature", "tail length", "temperature"],
        'measurementvalue': [12, 12.7, 15.873],
        'measurementunit': ["C", "cm", "C"],
    })
    correct_data = pd.DataFrame(data={
        'field': ["measurementid", "measurementid"],
        'level': ["error", "error"],
        'row': ['1', '2'],
        'message': ["measurementid 2 is duplicated", "measurementid 2 is duplicated"]})

    error = check_measurementids(field_data)

    # reset index of both dataframe or the compare won't work
    assert correct_data.astype(str).reset_index(drop=True).equals(
        error.astype(str).reset_index(drop=True))
