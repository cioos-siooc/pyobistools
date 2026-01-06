import numpy as np
import pandas as pd
import warnings
NaN = np.nan


def check_eventids(data):
    NaN = np.nan
    data = pd.DataFrame(data=data)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", FutureWarning)
        data = data.replace('', np.nan).infer_objects() #This line will throw a warning, but we are following the recommended pattern 
    
    
    data.rename(columns=str.lower, inplace=True)
    column_names = list(data.columns)

    field_analysis = pd.DataFrame(columns=['field', 'level', 'row', 'message'])

    # check field presence in the dataset
    list_fields_to_check_presence = ['eventid', 'parenteventid']

    for item in list_fields_to_check_presence:
        if item not in column_names:
            # row = {'field': item, 'level': 'error', 'row': 'NaN', 'message': 'Field ' + item + ' is missing'}
            row = pd.DataFrame(np.array(
                [[item, 'error', 'NaN', 'Field ' + item + ' is missing']]), columns=['field', 'level', 'row', 'message'])
            # row = pd.DataFrame.from_dict(row, orient='index').T
            field_analysis = pd.concat([field_analysis, row])

    # check duplicate eventIDs
    field_analysis2 = pd.DataFrame(columns=['field', 'level', 'row', 'message'])
    if 'eventid' in column_names:
        duplicates_eventid = data[data.duplicated('eventid', keep=False)]
        if len(duplicates_eventid) != 0:

            field_analysis2['field'] = duplicates_eventid['eventid']
            field_analysis2['level'] = 'error'
            field_analysis2['row'] = duplicates_eventid.index
            field_analysis2['message'] = field_analysis2.agg(
                'eventid {0[field]} is duplicated'.format, axis=1)
            field_analysis2['field'] = 'eventid'

    # check if all parentEventIDs have corresponding eventID
    field_analysis3 = pd.DataFrame(columns=['field', 'level', 'row', 'message'])
    if 'eventid' in column_names:
        if 'parenteventid' in column_names:
            event_eventids = data["eventid"][(data["eventid"].notnull()) & (data["eventid"] != '')]
            event_parenteventids = data["parenteventid"][(
                data["parenteventid"].notna()) & (data["parenteventid"] != '')]
            event_parenteventids = pd.DataFrame(data=event_parenteventids)
            event_parenteventids.loc[:, 'message'] = event_parenteventids['parenteventid'].isin(
                event_eventids)
            event_parenteventids = event_parenteventids[~event_parenteventids["message"]]

            if len(event_parenteventids[~event_parenteventids["message"]]) != 0:

                field_analysis3['field'] = event_parenteventids['parenteventid']
                field_analysis3['level'] = 'error'
                field_analysis3['row'] = event_parenteventids.index
                field_analysis3['message'] = field_analysis3.agg(
                    'parenteventid {0[field]} has no corresponding eventID'.format, axis=1)
                field_analysis3['field'] = 'parenteventid'

    # append error tables together
    if len(field_analysis2) != 0:
        field_analysis = pd.concat([field_analysis, field_analysis2])

    if len(field_analysis3) != 0:
        field_analysis = pd.concat([field_analysis, field_analysis3])

    return field_analysis


def check_extension_eventids(core, extension_or_emof, field='eventID'):

    core = pd.DataFrame(data=core)
    core = core.replace('', NaN)
    core.rename(columns=str.lower, inplace=True)

    extension_or_emof = pd.DataFrame(data=extension_or_emof)
    extension_or_emof = extension_or_emof.replace('', NaN)
    extension_or_emof.rename(columns=str.lower, inplace=True)

    # check if all eventIDs (or occurrenceIDs) in an extension or emof file
    # have corresponding eventIDs (or occurrenceIDs) in the core file
    field_analysis = pd.DataFrame(columns=['field', 'level', 'row', 'message'])
    field_lower = field.lower()

    if field_lower in core.columns and field_lower in extension_or_emof.columns:
        missing_values = extension_or_emof[~extension_or_emof[field_lower].isin(
            core[field_lower])][field_lower]
        if not missing_values.empty:
            field_analysis['row'] = missing_values.index
            field_analysis['message'] = [
                f"Field {v} has no corresponding {field} in the core" for v in missing_values]
            field_analysis['field'] = field_lower
            field_analysis['level'] = 'error'

    return field_analysis
