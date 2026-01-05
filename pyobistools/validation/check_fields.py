import numpy as np
import pandas as pd
from pyobistools.validation.validationVars import ( #There is copy and paste across scripts. If it is all the same lets put it in a common file. Need to double check. 
    event_core_fields,
    occurrence_extension_fields,
    extended_measurement_or_fact_extension_fields,
    occurrence_core_fields
)
NaN = np.nan
def check_fields(data, level='error', analysis_type='occurrence_core', accepted_name_usage_id_check=False):
    # if statements to determine the analysis to run
    if analysis_type == 'event_core':
        dataframe_column_key = pd.DataFrame(data=event_core_fields)
    elif analysis_type == 'occurrence_extension':
        dataframe_column_key = pd.DataFrame(data=occurrence_extension_fields)
    elif analysis_type == 'extended_measurement_or_fact_extension':
        dataframe_column_key = pd.DataFrame(data=extended_measurement_or_fact_extension_fields)
    elif analysis_type == 'occurrence_core':
        dataframe_column_key = pd.DataFrame(data=occurrence_core_fields)

    return check_fields_generic(data, level, dataframe_column_key, accepted_name_usage_id_check)

def get_field_presence(level, dataframe_column_key, data_columns_lower_case):
    
    analysis_fields_presence = pd.DataFrame()
    
    if level == 'warning': 
        analysis_fields_presence = dataframe_column_key.loc[dataframe_column_key['Required or recommended'] == 'Recommended field', ['field']].copy()
    elif level == 'error':
        analysis_fields_presence = dataframe_column_key.loc[dataframe_column_key['Required or recommended'] == 'Required field', ['field']].copy()
    
    if analysis_fields_presence.empty:
        return pd.DataFrame(columns=['field', 'level', 'row', 'message'])
        
    analysis_fields_presence['level'] = NaN
    analysis_fields_presence['row'] = NaN
    analysis_fields_presence['message'] = NaN 
    
    missing_mask = ~analysis_fields_presence['field'].str.lower().isin(data_columns_lower_case)
    analysis_fields_presence = analysis_fields_presence.loc[missing_mask]
    
    if analysis_fields_presence.empty:
        return pd.DataFrame(columns=['field', 'level', 'row', 'message'])

    analysis_fields_presence['level'] = level
    prefix = 'Required field ' if level == 'error' else 'Recommended field '
    analysis_fields_presence['message'] = prefix + analysis_fields_presence['field'] + ' is missing'
    analysis_fields_presence = analysis_fields_presence.fillna("NaN")
    return analysis_fields_presence 
    
def check_case(dataframe_column_key, data_columns_normal_case, data_columns_lower_case):

    df_fields = dataframe_column_key[['field']].copy()

    mask_incorrect_case = df_fields['field'].str.lower().isin(data_columns_lower_case) & \
                          ~df_fields['field'].isin(data_columns_normal_case)

    result = df_fields.loc[mask_incorrect_case].copy()

    if result.empty:
        return pd.DataFrame(columns=['field', 'level', 'row', 'message'])
    else:
        result['level'] = 'warning'
        result['row'] = NaN
        result['message'] = result['field'] + ' has incorrect case'
        result = result.fillna("NaN")
        return result

def check_na(data, level, dataframe_column_key, data_columns_lower_case, data_columns_normal_case):

    
    data_clean = data.copy()
    old_option = pd.get_option('future.no_silent_downcasting')
    pd.set_option('future.no_silent_downcasting', True)# have to temp suppress warning. following recommended pattern on next line.
    data_clean = data_clean.replace('', np.nan).infer_objects(copy=False)
    pd.set_option('future.no_silent_downcasting', old_option)
    
    if level == 'error':
        field_list = dataframe_column_key.loc[dataframe_column_key['Required or recommended'] == 'Required field', 'field'].tolist()
    elif level == 'warning':
        field_list = dataframe_column_key.loc[dataframe_column_key['Required or recommended'] == 'Recommended field', 'field'].tolist()

    if not field_list:
        return pd.DataFrame(columns=['field', 'level', 'row', 'message'])

    
    field_list_lower = [f.lower() for f in field_list]
    existing_fields_lower = [f for f in field_list_lower if f in data_columns_lower_case]

    if not existing_fields_lower:
        return pd.DataFrame(columns=['field', 'level', 'row', 'message'])
    data_lower = data_clean.copy()
    data_lower.columns = data_columns_lower_case

    df_long = data_lower[existing_fields_lower].reset_index().melt(
        id_vars='index', var_name='field_lower', value_name='value'
    )

    analysis_missing_values = df_long[df_long['value'].isna()].copy()
    if analysis_missing_values.empty:
        return pd.DataFrame(columns=['field', 'level', 'row', 'message'])

    analysis_missing_values['field'] = analysis_missing_values['field_lower'].map(dict(zip(data_columns_lower_case, data_columns_normal_case)))
    analysis_missing_values['level'] = level
    analysis_missing_values['row'] = analysis_missing_values['index']
    prefix = 'Empty value for required field ' if level == 'error' else 'Empty value for recommended field '
    analysis_missing_values['message'] = prefix + analysis_missing_values['field']

    return analysis_missing_values[['field', 'level', 'row', 'message']].reset_index(drop=True)
    
def check_fields_generic(data, level='error', dataframe_column_key=None, accepted_name_usage_id_check=False):
    #to-do: should check to make sure level is either error or warning
    data_columns_normal_case = list(data.columns)
    data_columns_lower_case = list(map(str.lower, data.columns))
    
    analysis_missing_values = pd.DataFrame()
    analysis_accepted_name_usage_id_check = pd.DataFrame()
    analysis_case_check_fields = pd.DataFrame()
    analysis_results = pd.DataFrame()
    
    
    analysis_fields_presence = get_field_presence(level, dataframe_column_key,data_columns_lower_case)

    analysis_missing_values = check_na(data, level, dataframe_column_key, data_columns_lower_case, data_columns_normal_case)


    # ACCEPTED_NAME_USAGE_ID_CHECK - IRRESPECTIVE OF CASE
    if accepted_name_usage_id_check:
        if 'acceptednameusageid' in data_columns_lower_case:

            data2 = data.replace('', NaN).copy()
            data2.rename(columns=str.lower, inplace=True)

            # previous error table filtered for scientifinameid errors
            analysis_accepted_name_usage_id_check = analysis_missing_values.copy()
            analysis_accepted_name_usage_id_check = analysis_accepted_name_usage_id_check[analysis_accepted_name_usage_id_check['field'].str.lower(
            ) == 'scientificnameid'].copy()

            # data table filtered to find index to substract from analysis_field
            index_of_filtered_data = data2[(data2['scientificnameid'].isna()) & (
                data2['acceptednameusageid'].notna())].index

            # filter analysis_accepted_name_usage_id_check to keep only rows where we
            # know scientificnameid IS EMPTY and acceptednameusageid IS NOT EMPTY
            analysis_accepted_name_usage_id_check = analysis_accepted_name_usage_id_check[analysis_accepted_name_usage_id_check["row"].isin(
                index_of_filtered_data)]

    # FIND FIELDS WITH INCORRECT CASE 
    if level == 'warning':
        analysis_case_check_fields = check_case(dataframe_column_key, data_columns_normal_case,data_columns_lower_case )
    # ANALYSIS RESULTS MERGE
    if analysis_fields_presence.empty is False:
        analysis_results = pd.concat([analysis_results, analysis_fields_presence])

    if analysis_missing_values.empty is False:
        analysis_results = pd.concat([analysis_results, analysis_missing_values])

    if accepted_name_usage_id_check:
        analysis_results = pd.concat(
            [analysis_results, analysis_accepted_name_usage_id_check]).drop_duplicates(keep=False)

    if analysis_case_check_fields.empty is False:
        analysis_results = pd.concat([analysis_results, analysis_case_check_fields])

    if len(analysis_results) == 0:
        analysis_results = pd.DataFrame(columns=['field', 'level', 'row', 'message'])

    return analysis_results
