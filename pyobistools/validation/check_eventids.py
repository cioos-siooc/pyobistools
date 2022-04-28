import numpy as np
import pandas as pd
NaN = np.nan


def check_eventids(data):
    data = pd.DataFrame(data=data)
    data.rename(columns=str.lower, inplace=True)
    column_names = list(data.columns)

    list_fields_to_check_presence = ['eventid', 'parenteventid']
    field_analysis = pd.DataFrame(columns=['level', 'field', 'row', 'message'])

    # check field presence in the dataset
    for item in list_fields_to_check_presence:
        if item not in column_names:
            row = {'level': 'error', 'field': item, 'row': NaN, 'message': 'Field ' + item + ' is missing'}
            field_analysis = field_analysis.append(row, ignore_index = True)

    if len(field_analysis) != 0:
        return field_analysis


def check_extension_eventids():
    return
