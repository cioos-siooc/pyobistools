import numpy as np
import pandas as pd
from dash import dash_table, html
NaN = np.nan

def validate_occurrencestatus(data):
    data = data.rename(columns=str.lower)

    valeur_exemples = ['present', 'absent']

    tableau_occurrencestatus = pd.DataFrame(data=data["occurrencestatus"].value_counts(dropna=False))
    tableau_occurrencestatus.reset_index(inplace=True)

    tableau_occurrencestatus.rename(columns={"index":"Valeurs / Values","occurrencestatus": "Nombres d'observations / Number of observations"}, inplace=True)
    tableau_occurrencestatus = tableau_occurrencestatus.reindex(columns = ['Valeurs / Values','DWC standard',"Nombres d'observations / Number of observations"])
    tableau_occurrencestatus['DWC standard'] = tableau_occurrencestatus["Valeurs / Values"].isin(valeur_exemples)
    tableau_occurrencestatus['DWC standard'].replace(False,"Absence", inplace=True)
    tableau_occurrencestatus['DWC standard'].replace(True,"Présent / Present", inplace=True)
    tableau_occurrencestatus.sort_values(by='DWC standard', ascending=True, inplace=True)


    liste_occurrencestatus = ["Les valeurs trouvées dans la colonne 'occurrenceStatus' sont présentées dans le tableau et leur présence ou non dans la documentation est analysée.",
    "Les valeurs données en exemple dans la documentation sont: 'present', 'absent'.",
    "Lien vers référence: https://dwc.tdwg.org/terms/#dwc:occurrenceStatus"]
        
    return html.Div([

        html.H4("Champ/Field 'occurrenceStatus':"),

        dash_table.DataTable(
        data=tableau_occurrencestatus.to_dict('records'),id={'type': 'tableau_occurrencestatus'},
        columns=[{'name': ["Validation de données: champ 'occurrencestatus'", i], 'id': i} for i in tableau_occurrencestatus.columns],
        sort_action='native', filter_action='native', editable=False, row_deletable=False,
        style_header={'backgroundColor': 'rgb(0, 173, 239)','color': 'white', 'textAlign': 'center'},
        style_table={'height': '375','width':'50%', 'overflowY': 'auto'},
        style_cell={'textAlign': 'center','whiteSpace': 'normal','height': 'auto','lineHeight': '15px'},
        export_format="csv",
        merge_duplicate_headers=True,
        export_headers='display'),
        
        html.Details([
        html.Summary("Info sur/on 'occurrenceStatus'"),
        html.Ul([html.Li(x) for x in liste_occurrencestatus]),
        ]),
        
        html.P(""),

        ])  
