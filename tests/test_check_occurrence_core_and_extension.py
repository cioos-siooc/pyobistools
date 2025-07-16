'''
check check_occurrence_core_and_extension
'''

import numpy as np
import pandas as pd

from pyobistools.validation.check_occurrence_core_and_extension import check_occurrence_core_and_extension

NaN = np.nan


def test_check_occurrence_core_and_extension():
    field_data = pd.DataFrame({
        'occurrenceID': ['test', 'test', 'ABCD'],
        'basisOfRecord': ['HumanObservation', 'human observation', 'HumanObservation'],
        'occurrenceStatus': ['present', 'test', 'present'],
    })
    correct_data = pd.DataFrame(data={
        'field': ['occurrenceid', 'occurrenceid', 'occurrencestatus', 'basisofrecord'],
        'level': ['error','error','error','error'],
        'row':  ['0', '1','1','1'],
        'message': ['occurrenceid test is duplicated','occurrenceid test is duplicated','occurrencestatus test is not permitted','basisofrecord human observation is not permitted']})

    error = check_occurrence_core_and_extension(field_data)

        # reset index of both dataframe or the compare won't work
    assert correct_data.astype(str).reset_index(drop=True).equals(
        error.astype(str).reset_index(drop=True))