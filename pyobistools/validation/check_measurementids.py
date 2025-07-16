import numpy as np
import pandas as pd

NaN = np.nan

permitted_values_occurrencestatus = ['absent', 'present']
permitted_values_basisofrecord = ['PreservedSpecimen', 'FossilSpecimen', 'LivingSpecimen', 'HumanObservation', 'MachineObservation',
                        'MaterialSample', 'MaterialCitation', 'MaterialEntity', 'Occurrence',
                        'Taxon', 'Event']

def check_measurementids(data):
    NaN = np.nan
    data = pd.DataFrame(data=data)
    data = data.replace('', NaN)
    data.rename(columns=str.lower, inplace=True)
    column_names = list(data.columns)

    # check duplicate measurementIDs
    field_analysis = pd.DataFrame(columns=['field', 'level', 'row', 'message'])

    if 'measurementid' in column_names:
        duplicates_measurementid = data[data.duplicated('measurementid', keep=False)]['measurementid']
        if not duplicates_measurementid.empty:
            
            field_analysis['row'] = duplicates_measurementid.index
            field_analysis['message'] = [
                f"measurementid {v} is duplicated" for v in duplicates_measurementid]
            field_analysis['field'] = 'measurementid'
            field_analysis['level'] = 'error'

    return field_analysis


