import numpy as np
import pandas as pd

NaN = np.nan


def check_fields(data, level='error', analysis_type='occurrence_core', accepted_name_usage_id_check=False):
    NaN = np.nan
    data = pd.DataFrame(data=data)
    data.rename(columns=str.lower, inplace=True)

    event_core = {
        'field': [
            "eventid",
            "eventdate",
            "decimallatitude",
            "decimallongitude",
            "countrycode",
            "geodeticdatum"],
        'Required or recommended': [
            "Required field",
            "Required field",
            "Required field",
            "Required field",
            "Required field",
            "Required field"],
    }

    occurrence_extension = {
        'field': [
            "eventid",
            "occurrenceid",
            "basisofrecord",
            "scientificname",
            "scientificnameid",
            "kingdom",
            "occurrencestatus"],
        'Required or recommended': [
            "Required field",
            "Required field",
            "Required field",
            "Required field",
            "Required field",
            "Required field",
            "Required field"],
    }

    extended_measurement_or_fact_extension = {
        "field": [
            "measurementid",
            "eventid",
            "occurrenceid",
            "measurementtype",
            "measurementtypeid",
            "measurementvalue",
            "measurementvalueid",
            "measurementaccuracy",
            "measurementunit",
            "measurementunitid",
            "measurementdetermineddate",
            "measurementdeterminedby",
            "measurementmethod",
            "measurementremarks"
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

    occurrence_core = {
        'field': [
            "occurrenceid",
            "basisofrecord",
            "scientificname",
            "scientificnameid",
            "eventdate",
            "decimallatitude",
            "decimallongitude",
            "occurrencestatus",
            "countrycode",
            "kingdom",
            "geodeticdatum",
            "minimumdepthinmeters",
            "maximumdepthinmeters",
            "coordinateuncertaintyinmeters",
            "samplingprotocol",
            "taxonrank",
            "organismquantity",
            "organismquantityType",
            "datasetname",
            "datageneralizations",
            "informationwithheld",
            "institutioncode",
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
    # if statements to determine the analysis to run
    if analysis_type == 'event_core':
        dataframe_column_key = pd.DataFrame(data=event_core)
    elif analysis_type == 'occurrence_extension':
        dataframe_column_key = pd.DataFrame(data=occurrence_extension)
    elif analysis_type == 'extended_measurement_or_fact_extension':
        dataframe_column_key = pd.DataFrame(data=extended_measurement_or_fact_extension)
    elif analysis_type == 'occurrence_core':
        dataframe_column_key = pd.DataFrame(data=occurrence_core)

    # list of columns in dataset
    dataset_column_names = list(data.columns)

    # list of required or recommended columns and error dataframe creation
    if level == "error":
        column_type_based_level = dataframe_column_key['field'].loc[dataframe_column_key['Required or recommended'] == 'Required field'].tolist(
        )
        analysis_field = dataframe_column_key.loc[dataframe_column_key['Required or recommended'] == 'Required field']
    if level == "warning":
        column_type_based_level = dataframe_column_key['field'].loc[dataframe_column_key['Required or recommended'] == 'Recommended field'].tolist(
        )
        analysis_field = dataframe_column_key.loc[dataframe_column_key['Required or recommended']
                                                  == 'Recommended field']

    # # SECTION FOR FORMAT ANALYSIS
    if analysis_field.empty:
        print('This combination of level and analysis type has no field presence to analyze')

    else:
        # dataframe filling for column analysis
        analysis_field = analysis_field.drop(columns=['Required or recommended'])
        analysis_field.loc[:, 'level'] = 'NaN'
        analysis_field.loc[:, 'row'] = 'NaN'
        analysis_field.loc[:, 'message'] = analysis_field["field"].isin(dataset_column_names)
        analysis_field = analysis_field.loc[~analysis_field.message].copy()

        if level == "error":
            analysis_field.loc[:, 'level'] = 'error'
            analysis_field.loc[:, 'message'] = 'Required field ' + \
                analysis_field['field'] + " is missing"
        if level == "warning":
            analysis_field.loc[:, 'level'] = 'warning'
            analysis_field.loc[:, 'message'] = 'Recommended field ' + \
                analysis_field['field'] + " is missing"

        # FIND EMPLTY VALUES FOR REQUIRED OR RECOMMENDED FIELDS
        # subset of dataset using required or recommended columns and keeping na values
        data = data.replace('', NaN)
        table_na_values = data[data.columns[data.columns.isin(column_type_based_level)]].isna()

        for column in table_na_values:
            field_analysis2 = pd.DataFrame(columns=['field', 'level', 'row', 'message'])
            if len(table_na_values[table_na_values[column]]) != 0:
                field_analysis2.loc[:,
                                    'row'] = table_na_values[column][table_na_values[column]].index
                field_analysis2.loc[:, 'field'] = column
                field_analysis2.loc[:, 'level'] = 'error'
                field_analysis2.loc[:, 'message'] = field_analysis2.agg(
                    'Empty value for required field {0[field]}'.format, axis=1)

                analysis_field = pd.concat([analysis_field, field_analysis2])

    if accepted_name_usage_id_check:
        if 'acceptednameusageid' in dataset_column_names:

            # previous error table filtered for scientifinameid errors
            field_analysis3 = analysis_field[analysis_field['field'] == 'scientificnameid']

            # data table filtered to find index to substract from analysis_field
            index_of_filtered_data = data[(data['scientificnameid'].isna()) & (
                data['acceptednameusageid'].str.len() > 6)].index

            # filter field_analysis3 to keep only rows where we know scientificnameid IS EMPTY and acceptednameusageid IS NOT EMPTY
            field_analysis3 = field_analysis3[field_analysis3["row"].isin(index_of_filtered_data)]

            # concat field_analysis3 and analysis_field and get rid of values of all duplicates which in this case are lines where acceptednameusageid IS NOT EMPTY
            field_analysis3 = pd.concat([analysis_field, field_analysis3]
                                        ).drop_duplicates(keep=False)
            analysis_field = field_analysis3

        else:
            pass

    return analysis_field
