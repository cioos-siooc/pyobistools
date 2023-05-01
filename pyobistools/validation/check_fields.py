import numpy as np
import pandas as pd

NaN = np.nan

event_core_fields = {
    'field': [
        "eventID",
        "eventDate",
        "decimalLatitude",
        "decimalLongitude",
        "countryCode",
        "geodeticDatum"],
    'Required or recommended': [
        "Required field",
        "Required field",
        "Required field",
        "Required field",
        "Required field",
        "Required field"],
}

occurrence_extension_fields = {
    'field': [
        "eventID",
        "occurrenceID",
        "basisOfRecord",
        "scientificName",
        "scientificNameID",
        "kingdom",
        "occurrenceStatus"],
    'Required or recommended': [
        "Required field",
        "Required field",
        "Required field",
        "Required field",
        "Required field",
        "Required field",
        "Required field"],
}

extended_measurement_or_fact_extension_fields = {
    "field": [
        "measurementID",
        "eventID",
        "occurrenceID",
        "measurementType",
        "measurementTypeID",
        "measurementValue",
        "measurementValueID",
        "measurementAccuracy",
        "measurementUnit",
        "measurementUnitID",
        "measurementDeterminedDate",
        "measurementDeterminedBy",
        "measurementMethod",
        "measurementRemarks"
    ],

    "Required or recommended": [
        "Required field",
        "Required field",
        "Required field",
        "Required field",
        "Required field",
        "Required field",
        "Required field",
        "Required field",
        "Required field",
        "Required field",
        "Required field",
        "Required field",
        "Required field",
        "Required field",
    ],
}

occurrence_core_fields = {
    'field': [
        "occurrenceID",
        "basisOfRecord",
        "scientificName",
        "scientificNameID",
        "eventDate",
        "decimalLatitude",
        "decimalLongitude",
        "occurrenceStatus",
        "countryCode",
        "kingdom",
        "geodeticDatum",
        "minimumDepthInMeters",
        "maximumDepthInMeters",
        "coordinateUncertaintyInMeters",
        "samplingProtocol",
        "taxonRank",
        "organismQuantity",
        "organismQuantityType",
        "datasetName",
        "dataGeneralizations",
        "informationWithheld",
        "institutionCode",
    ],
    'Required or recommended': [
        "Required field",
        "Required field",
        "Required field",
        "Required field",
        "Required field",
        "Required field",
        "Required field",
        "Required field",
        "Required field",
        "Required field",
        "Required field",
        "Recommended field",
        "Recommended field",
        "Recommended field",
        "Recommended field",
        "Recommended field",
        "Recommended field",
        "Recommended field",
        "Recommended field",
        "Recommended field",
        "Recommended field",
        "Recommended field",
    ],
}


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


def check_fields_generic(data, level='error', dataframe_column_key=None, accepted_name_usage_id_check=False):
    data_columns_normal_case = list(data.columns)
    data_columns_lower_case = list(map(str.lower, data.columns))

    required_fields_list_normal_case = dataframe_column_key[dataframe_column_key['Required or recommended'] == 'Required field'].copy(
    )
    required_fields_list_normal_case.loc[:, 'field'] = required_fields_list_normal_case['field']

    recommended_fields_list_normal_case = dataframe_column_key[dataframe_column_key['Required or recommended'] == 'Recommended field'].copy(
    )
    recommended_fields_list_normal_case.loc[:,
                                            'field'] = recommended_fields_list_normal_case['field']

    analysis_fields_presence = pd.DataFrame()
    analysis_missing_values = pd.DataFrame()
    analysis_accepted_name_usage_id_check = pd.DataFrame()
    analysis_case_check_fields = pd.DataFrame()
    analysis_results = pd.DataFrame()

    # FIND IF REQUIRED OR RECOMMENDED FIELDS ARE PRESENT
    if level == 'warning':
        if recommended_fields_list_normal_case.empty is False:
            analysis_fields_presence = recommended_fields_list_normal_case
            analysis_fields_presence = analysis_fields_presence.drop(
                columns=['Required or recommended'])
            analysis_fields_presence.loc[:, 'level'] = 'NaN'
            analysis_fields_presence.loc[:, 'row'] = 'NaN'
            analysis_fields_presence.loc[:, 'message'] = analysis_fields_presence["field"].str.lower().isin(
                data_columns_lower_case)
            analysis_fields_presence = analysis_fields_presence.loc[~analysis_fields_presence.message].copy(
            )
            analysis_fields_presence.loc[:, 'level'] = 'warning'
            analysis_fields_presence.loc[:, 'message'] = 'Recommended field ' + \
                analysis_fields_presence['field'] + " is missing"

    if level == 'error':
        analysis_fields_presence = required_fields_list_normal_case
        analysis_fields_presence = analysis_fields_presence.drop(
            columns=['Required or recommended'])
        analysis_fields_presence.loc[:, 'level'] = 'NaN'
        analysis_fields_presence.loc[:, 'row'] = 'NaN'
        analysis_fields_presence.loc[:, 'message'] = analysis_fields_presence["field"].str.lower().isin(
            data_columns_lower_case)
        analysis_fields_presence = analysis_fields_presence.loc[~analysis_fields_presence.message].copy(
        )
        analysis_fields_presence.loc[:, 'level'] = 'error'
        analysis_fields_presence.loc[:, 'message'] = 'Required field ' + \
            analysis_fields_presence['field'] + " is missing"

    if len(analysis_fields_presence) == 0:
        analysis_fields_presence = pd.DataFrame(columns=['field', 'level', 'row', 'message'])

    # FIND EMPLTY VALUES FOR REQUIRED OR RECOMMENDED FIELDS
    # subset of dataset using required or recommended columns and keeping na values
    data1 = data.replace('', NaN).copy()

    if level == 'error':
        column_type_based_level = dataframe_column_key['field'].loc[dataframe_column_key['Required or recommended'] == 'Required field'].tolist(
        )
        table_na_values = data1[data1.columns[data1.columns.str.lower().isin(
            list(map(str.lower, column_type_based_level)))]].isna()
    if level == 'warning':
        column_type_based_level = dataframe_column_key['field'].loc[dataframe_column_key['Required or recommended'] == 'Recommended field'].tolist(
        )
        table_na_values = data1[data1.columns[data1.columns.str.lower().isin(
            list(map(str.lower, column_type_based_level)))]].isna()

    for column in table_na_values:
        field_analysis = pd.DataFrame(columns=['field', 'level', 'row', 'message'])
        if len(table_na_values[table_na_values[column]]) != 0:
            field_analysis.loc[:, 'row'] = table_na_values[column][table_na_values[column]].index
            field_analysis.loc[:, 'field'] = column

            if level == 'error':
                field_analysis.loc[:, 'level'] = 'error'
                field_analysis.loc[:, 'message'] = field_analysis.agg(
                    'Empty value for required field {0[field]}'.format, axis=1)
            if level == 'warning':
                field_analysis.loc[:, 'level'] = 'warning'
                field_analysis.loc[:, 'message'] = field_analysis.agg(
                    'Empty value for recommended field {0[field]}'.format, axis=1)

            analysis_missing_values = pd.concat([analysis_missing_values, field_analysis])

    if len(analysis_missing_values) == 0:
        analysis_missing_values = pd.DataFrame(columns=['field', 'level', 'row', 'message'])

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

            # filter analysis_accepted_name_usage_id_check to keep only rows where we know scientificnameid IS EMPTY and acceptednameusageid IS NOT EMPTY
            analysis_accepted_name_usage_id_check = analysis_accepted_name_usage_id_check[analysis_accepted_name_usage_id_check["row"].isin(
                index_of_filtered_data)]

    # FIND FIELDS WITH INCORRECT CASE
    if level == 'warning':

        # dataframe filling for column analysis
        analysis_field_normal_case = dataframe_column_key.drop(columns=['Required or recommended'])
        analysis_field_normal_case.loc[:, 'level'] = 'NaN'
        analysis_field_normal_case.loc[:, 'row'] = 'NaN'

        # analysis to find missing field with normal case
        analysis_field_normal_case.loc[:, 'message'] = analysis_field_normal_case["field"].isin(
            data_columns_normal_case)
        analysis_field_normal_case = analysis_field_normal_case.loc[~analysis_field_normal_case.message].copy(
        )

        analysis_field_lower_case = dataframe_column_key.drop(columns=['Required or recommended'])
        analysis_field_lower_case['field'] = analysis_field_lower_case['field'].str.lower()
        analysis_field_lower_case.loc[:, 'level'] = 'NaN'
        analysis_field_lower_case.loc[:, 'row'] = 'NaN'

        # analysis to find missing field with lower case
        analysis_field_lower_case.loc[:, 'message'] = analysis_field_lower_case["field"].isin(
            data_columns_lower_case)
        analysis_field_lower_case = analysis_field_lower_case.loc[~analysis_field_lower_case.message].copy(
        )

        # The difference between the two above table yields the field with incorrect case
        if len(analysis_field_lower_case) != 0:
            # find fields present in both previous analysis - means field has incorrect case
            analysis_case_check_fields = analysis_field_normal_case.loc[~analysis_field_normal_case['field'].str.lower(
            ).isin(analysis_field_lower_case['field'])]
            analysis_case_check_fields = pd.DataFrame(data=analysis_case_check_fields)
            analysis_case_check_fields.loc[:, 'level'] = 'warning'
            analysis_case_check_fields.loc[:, 'message'] = analysis_case_check_fields.agg(
                '{0[field]} has incorrect case'.format, axis=1)

        if len(analysis_case_check_fields) == 0:
            analysis_case_check_fields = pd.DataFrame(columns=['field', 'level', 'row', 'message'])

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
