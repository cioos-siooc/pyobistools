import numpy as np
import pandas as pd

NaN = np.nan

permitted_values_occurrencestatus = ['absent', 'present']
permitted_values_basisofrecord = [
    'PreservedSpecimen',
    'FossilSpecimen',
    'LivingSpecimen',
    'HumanObservation',
    'MachineObservation',
    'MaterialSample',
    'MaterialCitation',
    'MaterialEntity',
    'Occurrence',
    'Taxon',
    'Event']


def check_occurrence_core_and_extension(data):
    NaN = np.nan
    data = pd.DataFrame(data=data)
    data = data.replace('', NaN)
    data.rename(columns=str.lower, inplace=True)
    column_names = list(data.columns)

    # check duplicate occurrenceIDs
    field_analysis = pd.DataFrame(columns=['field', 'level', 'row', 'message'])

    if 'occurrenceid' in column_names:
        duplicates_occurrenceid = data[data.duplicated('occurrenceid', keep=False)]['occurrenceid']
        if not duplicates_occurrenceid.empty:

            field_analysis['row'] = duplicates_occurrenceid.index
            field_analysis['message'] = [
                f"occurrenceid {v} is duplicated" for v in duplicates_occurrenceid]
            field_analysis['field'] = 'occurrenceid'
            field_analysis['level'] = 'error'

    # check values of column occurrenceStatus are either 'present' or 'absent'
    field_analysis2 = pd.DataFrame(columns=['field', 'level', 'row', 'message'])
    invalid_occ_status = data[~data['occurrencestatus'].isin(
        permitted_values_occurrencestatus)]['occurrencestatus']

    field_analysis2 = pd.DataFrame(columns=['field', 'level', 'row', 'message'])
    if not invalid_occ_status.empty:

        field_analysis2['row'] = invalid_occ_status.index
        field_analysis2['message'] = [
            f"occurrencestatus {v} is not permitted" for v in invalid_occ_status]
        field_analysis2['field'] = 'occurrencestatus'
        field_analysis2['level'] = 'error'

    # check values of column basisOfRecord  are correspond to permitted values
    field_analysis3 = pd.DataFrame(columns=['field', 'level', 'row', 'message'])

    invalid_bor = data[~data['basisofrecord'].isin(permitted_values_basisofrecord)]['basisofrecord']

    field_analysis3 = pd.DataFrame(columns=['field', 'level', 'row', 'message'])
    if not invalid_bor.empty:

        field_analysis3['row'] = invalid_bor.index
        field_analysis3['message'] = [
            f"basisofrecord {v} is not permitted" for v in invalid_bor]
        field_analysis3['field'] = 'basisofrecord'
        field_analysis3['level'] = 'error'

    # append error tables together
    if not field_analysis2.empty:
        field_analysis = pd.concat([field_analysis, field_analysis2])

    if not field_analysis3.empty:
        field_analysis = pd.concat([field_analysis, field_analysis3])

    return field_analysis
