import dash
import numpy as np
import pandas as pd
from dash import dash_table, html
NaN = np.nan



def table_format_analysis(colonne_analyse, colonnes_extra, liste_affichage, nombre_rangees):
    
    un = "Les données des champs validés comme 'Présent' dans le tableau précédent sont analysées dans cette section. / Data from fields validated as 'Present' in the previous table are analyzed in this section."
    deux = f"Pour référence, il y a {nombre_rangees} rangées  dans le jeu de données. / For reference, there are {nombre_rangees} rows in this dataset."

    liste_item = [un, deux]

    # section retournant le tableau d'analyse du format ainsi que les retours des fonctions des champs présents
    return html.Div([
        html.H3("Validation de format / Format validation:"),
        html.H6("La présence des champs attendus pour un type d'analyse et de fichier est analysé ici-bas:"),
        html.H6("The presence of the expected fields for a type of analysis and file is analyzed below:"),

        dash_table.DataTable(data=
        colonne_analyse.to_dict('records'),id={'type': 'colonne_analyse'},
        columns=[{'name': ["Validation de format / Format validation", i], 'id': i} for i in colonne_analyse.columns],
        sort_action='native', filter_action='native', editable=False, row_deletable=False,
        style_header={'backgroundColor': 'rgb(0, 173, 239)','color': 'white', 'textAlign': 'center'},
        style_table={'height': '375','width':'50%', 'overflowY': 'auto'},
        style_cell={'textAlign': 'center','whiteSpace': 'normal','height': 'auto','lineHeight': '15px'},
        export_format="csv",
        merge_duplicate_headers=True,
        export_headers='display'),

        html.P(''),
        html.H6("Les colonnes suivantes font parties du jeu de données et ne sont pas prise en compte dans le tableau précédent:"),
        html.H6("The following columns are part of the dataset and are not taken into account in the previous table:"),

        html.Ul([html.Li(x) for x in colonnes_extra]),
        html.P(''),
        
        html.H3("Validation des données / Data validation:"),
        html.Ul([html.Li(x) for x in liste_item]),
        html.P(''),         
        html.Div(children=[liste_affichage[i] for i in range(len(liste_affichage))]),
        ]),