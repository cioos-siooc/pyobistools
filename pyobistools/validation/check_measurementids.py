import numpy as np
import pandas as pd
import warnings

NaN = np.nan


def check_measurementids(data):
    NaN = np.nan
    data = pd.DataFrame(data=data)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", FutureWarning)
        data = data.replace('', NaN).infer_objects()
    data.rename(columns=str.lower, inplace=True)
    column_names = list(data.columns)

    # check duplicate measurementIDs
    field_analysis = pd.DataFrame(columns=['field', 'level', 'row', 'message'])

    if 'measurementid' in column_names:
        duplicates_measurementid = data[data.duplicated(
            'measurementid', keep=False)]['measurementid']
        if not duplicates_measurementid.empty:

            field_analysis['row'] = duplicates_measurementid.index
            field_analysis['message'] = [
                f"measurementid {v} is duplicated" for v in duplicates_measurementid]
            field_analysis['field'] = 'measurementid'
            field_analysis['level'] = 'error'

    return field_analysis
