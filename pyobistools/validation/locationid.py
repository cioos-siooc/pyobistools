import numpy as np
import pandas as pd
from dash import dash_table, dcc, html
from pyobistools.validation.sub_routines.analyse_colonne import AfficheOccurrenceParValeur

NaN = np.nan

def validate_locationIDOccurrences(data):

    liste_quantityType = ["Les valeurs trouvées dans la colonne 'locationID' sont présentées dans le tableau.",
    "Lien vers référence: https://dwc.tdwg.org/terms/#dwc:locationID"]

    # append le tableau fait via analyse_colonne
    ret = html.Div([html.H4("Champ/Field 'locationID':"),
        AfficheOccurrenceParValeur(data, 'locationID'),
        html.Details([
        html.Summary("Info sur/on 'locationID'"),
        html.Ul([html.Li(x) for x in liste_quantityType]),
        ]),
        html.P("")]) 
    return ret
