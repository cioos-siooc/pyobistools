import numpy as np
import pandas as pd
from dash import dash_table, html
NaN = np.nan
#
def validate_datasetid(data):
    data = data.rename(columns=str.lower)

    tableau_datasetid = pd.DataFrame(data=data["datasetid"].value_counts(dropna=False))
    tableau_datasetid.reset_index(inplace=True)
    tableau_datasetid.rename(columns={"index":"Valeurs / Values","datasetid": "Nombre d'observations / Number of observations"}, inplace=True)
    

    liste_datasetid = ["Les valeurs trouvées dans la colonne 'datasetID' sont présentées dans le tableau.",
    "Lien vers référence: https://dwc.tdwg.org/terms/#dwc:datasetID"]

    return html.Div([
        html.H4("Champ/Field 'datasetID':"),
        
        dash_table.DataTable(
        data=tableau_datasetid.to_dict('records'),id={'type': 'tableau_datasetid'},
        columns=[{'name': ["Validation de données / Data validation: 'datasetID'", i], 'id': i} for i in tableau_datasetid.columns],
        sort_action='native', filter_action='native', editable=False, row_deletable=False,
        style_header={'backgroundColor': 'rgb(0, 173, 239)','color': 'white', 'textAlign': 'center'},
        style_table={'height': '375','width':'50%', 'overflowY': 'auto'},
        style_cell={'textAlign': 'center','whiteSpace': 'normal','height': 'auto','lineHeight': '15px'},
        export_format="csv",
        merge_duplicate_headers=True,
        export_headers='display'),
        
        html.Details([
        html.Summary("Info sur/on 'datasetID'"),
        html.Ul([html.Li(x) for x in liste_datasetid]),
        ]),
        
        html.P(""),
        
        ])  
