import numpy as np
import pandas as pd
NaN = np.nan


def check_fields(data, level = 'error', analysis_type = 'occurrence_core'):
    NaN = np.nan
    data = pd.DataFrame(data=data)
    data.rename(columns=str.lower, inplace=True)
    column_names = list(data.columns)

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

    # function that do the analysis
    def analysis_level_error(analysis):
        analysis = analysis.loc[analysis['Required or recommended'] == 'Required field']

        analysis.loc[:, 'level'] = 'error'
        analysis.loc[:, 'row'] = NaN
        analysis.loc[:, 'message'] = NaN

        analysis = analysis.reindex(columns=['level', 'field', 'row', 'message']).copy()

        analysis.loc[:, 'message'] = analysis["field"].isin(column_names)
        analysis = analysis.loc[~analysis.message].copy()
        analysis.loc[:, 'message'] = 'Required field ' + analysis['field'] + " is missing"

        if analysis.empty:
            return print('No errors')
        else:
            return analysis

    def analysis_level_warning(analysis):
        if len(analysis.loc[analysis['Required or recommended'] == 'Recommended field']) == 0:
            print('No recommended fields for this analysis type, therefore no warnings')
            return
        else:
            analysis = analysis.loc[analysis['Required or recommended'] == 'Recommended field']

            analysis.loc[:, 'level'] = 'warning'
            analysis.loc[:, 'row'] = NaN
            analysis.loc[:, 'message'] = NaN

            analysis = analysis.reindex(columns=['level', 'field', 'row', 'message']).copy()

            analysis.loc[:, 'message'] = analysis["field"].isin(column_names)
            analysis = analysis.loc[~analysis.message].copy()
            analysis.loc[:, 'message'] = 'Recommended field ' + analysis['field'] + " is missing"

            return analysis

    # if statements to determine the analysis to run
    if level == 'error':
        if analysis_type == 'event_core':
            analysis = pd.DataFrame(data=event_core)
        elif analysis_type == 'occurrence_extension':
            analysis = pd.DataFrame(data=occurrence_extension)
        elif analysis_type == 'extended_measurement_or_fact_extension':
            analysis = pd.DataFrame(data=extended_measurement_or_fact_extension)
        elif analysis_type == 'occurrence_core':
            analysis = pd.DataFrame(data=occurrence_core)

        return analysis_level_error(analysis)

    if level == 'warning':
        if analysis_type == 'event_core':
            analysis = pd.DataFrame(data=event_core)
        elif analysis_type == 'occurrence_extension':
            analysis = pd.DataFrame(data=occurrence_extension)
        elif analysis_type == 'extended_measurement_or_fact_extension':
            analysis = pd.DataFrame(data=extended_measurement_or_fact_extension)
        elif analysis_type == 'occurrence_core':
            analysis = pd.DataFrame(data=occurrence_core)

        return analysis_level_warning(analysis)
