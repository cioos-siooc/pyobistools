import numpy as np
import pandas as pd
NaN = np.nan


def check_fields(data, level = 'error', analysis_type = 'occurrence_core'):
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

    # function that do the format analysis and search missing values
    def analysis(data, level, analysis):

        # list of columns in dataset
        dataset_column_names = list(data.columns)

        # list of required or recommended columns and error dataframe creation
        if level == "error":
            analysis_type_column_names = analysis['field'].loc[analysis['Required or recommended'] == 'Required field'].tolist()
            analysis_field = analysis.loc[analysis['Required or recommended'] == 'Required field']
        if level == "warning":
            analysis_type_column_names = analysis['field'].loc[analysis['Required or recommended'] == 'Recommended field'].tolist()
            analysis_field = analysis.loc[analysis['Required or recommended'] == 'Recommended field']

        # SECTION FOR FORMAT ANALYSIS
        if len(analysis_type_column_names) == 0:
            return print('This combination of level and analysis type has no field presence to analyze')

        else:
            # dataframe filling for column analysis
            analysis_field = analysis_field.drop(columns=['Required or recommended'])
            analysis_field.loc[:, 'level'] = NaN
            analysis_field.loc[:, 'message'] = analysis_field["field"].isin(dataset_column_names)
            analysis_field = analysis_field.loc[~analysis_field.message].copy()
            analysis_field.loc[:, 'row'] = NaN

            if level == "error":
                analysis_field.loc[:, 'level'] = 'error'
                analysis_field.loc[:, 'message'] = 'Required field ' + analysis_field['field'] + " is missing"
            if level == "warning":
                analysis_field.loc[:, 'level'] = 'warning'
                analysis_field.loc[:, 'message'] = 'Recommended field ' + analysis_field['field'] + " is missing"

            # FIND EMPLTY VALUES FOR REQUIRED FIELDS
            # dataframe for errors login
            field_analysis2 = pd.DataFrame(columns=['field', 'level', 'message', 'row'])

            # subset of dataset using required or recommended columns and keeping na values
            table_na_values = data[data.columns[data.columns.isin(analysis_type_column_names)]].isna()

            for column in table_na_values:
                field_analysis2 = pd.DataFrame(columns=['field', 'level', 'message', 'row'])
                if len(table_na_values[table_na_values[column]]) != 0:
                    field_analysis2.loc[:, 'row'] = table_na_values[column][table_na_values[column]].index
                    field_analysis2.loc[:, 'field'] = column
                    field_analysis2.loc[:, 'level'] = 'error'
                    field_analysis2.loc[:, 'message'] = field_analysis2.agg('Empty value for required field {0[field]} '.format, axis=1)

                    analysis_field = analysis_field.append(field_analysis2).copy()

            # error table output
            if analysis.empty:
                return print('No errors')
            else:
                return analysis_field

    # if statements to determine the analysis to run
    if analysis_type == 'event_core':
        analysis_type_df = pd.DataFrame(data=event_core)
    elif analysis_type == 'occurrence_extension':
        analysis_type_df = pd.DataFrame(data=occurrence_extension)
    elif analysis_type == 'extended_measurement_or_fact_extension':
        analysis_type_df = pd.DataFrame(data=extended_measurement_or_fact_extension)
    elif analysis_type == 'occurrence_core':
        analysis_type_df = pd.DataFrame(data=occurrence_core)

    return analysis(data, level, analysis_type_df)
