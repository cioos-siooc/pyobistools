import numpy as np
import pandas as pd
from dash import dash_table
NaN = np.nan

def AfficheOccurrenceParValeur(data, nomcolonne):
    data = data.rename(columns=str.lower)
    nomcolonne = nomcolonne.lower()
    print(nomcolonne)
    tableau_valeur = pd.DataFrame(data=data[nomcolonne].value_counts(dropna=False))
    tableau_valeur.reset_index(inplace=True)

    tableau_valeur.rename(columns={"index":"Valeurs / Values",nomcolonne: "Nombre d'observations / Number of observations"}, inplace=True)

    return dash_table.DataTable(
        data=tableau_valeur.to_dict('records'),id={'type': 'tableau_valeur'},
        columns=[{'name': ["Validation de données / Data validation: '" + nomcolonne + "'", i], 'id': i} for i in tableau_valeur.columns],
        sort_action='native', filter_action='native', editable=False, row_deletable=False,
        style_header={'backgroundColor': 'rgb(0, 173, 239)','color': 'white', 'textAlign': 'center'},
        style_table={'height': '375','width':'50%', 'overflowY': 'auto'},
        style_cell={'textAlign': 'center','whiteSpace': 'normal','height': 'auto','lineHeight': '15px'},
        export_format="csv",
        merge_duplicate_headers=True,
        page_size=9,
        export_headers='display')

       
       
