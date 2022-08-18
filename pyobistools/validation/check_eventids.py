import numpy as np
import pandas as pd
NaN = np.nan


def check_eventids(data):
    NaN = np.nan
    data = pd.DataFrame(data=data)
    data = data.replace('', NaN)
    data.rename(columns=str.lower, inplace=True)
    column_names = list(data.columns)

    field_analysis = pd.DataFrame(columns=['field', 'level', 'row', 'message'])

    # check field presence in the dataset
    list_fields_to_check_presence = ['eventid', 'parenteventid']

    for item in list_fields_to_check_presence:
        if item not in column_names:
            row = {'field': item, 'level': 'error', 'row': 'NaN', 'message': 'Field ' + item + ' is missing'}
            field_analysis = field_analysis.append(row, ignore_index = True)

    # check duplicate eventIDs
    field_analysis2 = pd.DataFrame(columns=['field', 'level', 'row', 'message'])
    if 'eventid' in column_names:
        duplicates_eventid = data[data.duplicated('eventid', keep=False)]
        if len(duplicates_eventid) != 0:
           
            field_analysis2['field'] = duplicates_eventid['eventid']
            field_analysis2['level'] = 'error'
            field_analysis2['row'] = duplicates_eventid.index
            field_analysis2['message'] = field_analysis2.agg('eventid {0[field]} is duplicated'.format, axis=1)
            field_analysis2['field'] = 'eventid'


    # check if all parentEventIDs have corresponding eventID
    field_analysis3 = pd.DataFrame(columns=['field', 'level', 'row', 'message'])
    if 'eventid' in column_names:
        if 'parenteventid' in column_names:
            event_eventids       = data["eventid"][ (data["eventid"].notnull())  & (data["eventid"] != '') ]
            event_parenteventids = data["parenteventid"][ (data["parenteventid"].notna()) & (data["parenteventid"] != '')]
            event_parenteventids = pd.DataFrame(data = event_parenteventids)

            event_parenteventids.loc[:, 'message'] = event_parenteventids['parenteventid'].isin(event_eventids)
            event_parenteventids = event_parenteventids[~event_parenteventids["message"]]
            #print(event_parenteventids)
            if len(event_parenteventids[~event_parenteventids["message"] ] ) != 0:
                
                field_analysis3['field'] = event_parenteventids['parenteventid']
                field_analysis3['level'] = 'error'
                field_analysis3['row'] = event_parenteventids.index
                field_analysis3['message'] = field_analysis3.agg('parenteventid {0[field]} has no corresponding eventID'.format, axis=1)
                field_analysis3['field'] = 'parenteventid'

    # append error tables together
    if len(field_analysis2) != 0:
        #field_analysis = field_analysis.append(field_analysis2, ignore_index=True)
        field_analysis = pd.concat([field_analysis, field_analysis2])

    if len(field_analysis3) != 0:
       # field_analysis = field_analysis.append(field_analysis3, ignore_index=True)
        field_analysis = pd.concat([field_analysis, field_analysis3])

    # error table output
    if field_analysis.empty:
        return print('No errors')
    else:
        return field_analysis

#Check if all eventIDs in an extension have corresponding eventIDs in the core.
# event - The event records.
# extension - The extension records.
# field - The eventID field name in the extension records.


def check_extension_eventids(event, extension, field = 'eventID'):
    event = pd.DataFrame(data=event)
    event = event.replace('', NaN)
    event.rename(columns=str.lower, inplace=True)
    column_names = list(event.columns)

    extension = pd.DataFrame(data=extension)
    extension = extension.replace('', NaN)
    extension.rename(columns=str.lower, inplace=True)

    if 'eventid' in column_names:
        field = field.lower()
        event.rename(columns=str.lower, inplace=True)
        extension.rename(columns=str.lower, inplace=True)

        extension_eventids = extension[field]
        event_eventids = event['eventid']

        field_analysis = pd.DataFrame(columns=['field', 'level', 'row', 'message'])

        extension_eventids = pd.DataFrame(data = extension_eventids)
        extension_eventids.loc[:, 'message'] = extension_eventids[field].isin(event_eventids)

        extension_eventids = extension_eventids[~extension_eventids['message']]

        if len(extension_eventids) != 0:
            field_analysis['field'] = extension_eventids[field]
            field_analysis['level'] = 'error'
            field_analysis['row'] = extension_eventids.index
            field_analysis['message'] = field_analysis.agg('Field {0[field]} has no corresponding eventID in the core'.format, axis=1)
            field_analysis['field'] = field

        # error table output
        if field_analysis.empty:
            return print('No errors')
        else:
            return field_analysis