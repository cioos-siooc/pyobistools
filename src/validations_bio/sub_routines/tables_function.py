import numpy as np
import pandas as pd
NaN = np.nan
import numpy as np
import pandas as pd
NaN = np.nan
from dash import dash_table, dcc, html


def names_table(data_valid_scientific_name):
    liste_names = ["Les valeurs trouvées dans la colonne 'scientificName' sont présentées dans le tableau.",
    "L'algorithme garde les valeurs uniques des noms scientifique du jeu de données de départ (et supprime les suffixes sp et sp.) et vérifie auprès de base de données WORMS si ceux-ci y sont répertorié. Des champs sont retournées lors d'une recherche fructueuse. Dans le cas d'une recherche sans résultat auprès de WORMS, une recherche est effectuée auprès de la base de données ITIS. Le premier tableau est donc constitué des noms scientifiques du jeu de données, des valeurs retournés par WORMS ou ITIS et d'une colonne dite de validation qui indique si un nom scientifique se trouve ou non dans les bases de données.",
    "Lien vers référence: https://dwc.tdwg.org/terms/#dwc:scientificName"]
    
    data_valid_scientific_name.sort_values(by='Exact_Match', ascending=True, inplace=True)

   
    return html.Div([

        html.H4("Champ/Field 'scientificName':"),

        dash_table.DataTable(data=data_valid_scientific_name.to_dict('records'),
            columns=[
            {"name": ["Valeurs / Values", data_valid_scientific_name.columns[0]], "id": data_valid_scientific_name.columns[0]},
            {"name": ["Validation", data_valid_scientific_name.columns[1]], "id": data_valid_scientific_name.columns[1]},
            {"name": ["Valeurs base de données / Database values", data_valid_scientific_name.columns[2]], "id": data_valid_scientific_name.columns[2]},
            {"name": ["Valeurs base de données / Database values", data_valid_scientific_name.columns[3]], "id": data_valid_scientific_name.columns[3]},
            {"name": ["Valeurs base de données / Database values", data_valid_scientific_name.columns[4]], "id": data_valid_scientific_name.columns[4]},
            {"name": ["Valeurs base de données / Database values", data_valid_scientific_name.columns[5]], "id": data_valid_scientific_name.columns[5]},
            {"name": ["Valeurs base de données / Database values", data_valid_scientific_name.columns[6]], "id": data_valid_scientific_name.columns[6]},
            {"name": ["Valeurs base de données / Database values", data_valid_scientific_name.columns[7]], "id": data_valid_scientific_name.columns[7]},
            {"name": ["Valeurs base de données / Database values", data_valid_scientific_name.columns[8]], "id": data_valid_scientific_name.columns[8]}],
            merge_duplicate_headers=True,       
            #columns=[{'name': i, 'id': i} for i in data_valid_scientific_name.columns],
            page_size=9, sort_action='native', filter_action='native', editable=False, row_deletable=False,
            style_header={'backgroundColor': 'rgb(0, 173, 239)','color': 'white','textAlign': 'center',},
            style_cell={'textAlign': 'left','whiteSpace': 'normal','height': 'auto','lineHeight': '15px',},
            style_table={'height': '375', 'overflowY': 'auto'},
            export_format="csv",
            export_headers='display'),

            dcc.Store(id= 'stored_data_valid_scientific_name' , data=data_valid_scientific_name.to_dict('records')),
            
            html.Details([
            html.Summary("Info sur/on 'scientificName'"),
            html.Ul([html.Li(x) for x in liste_names]),
            ]),
            
            html.P(""),])
             
            

def names_ids_tables(data_valid_scientific_name, data_cross_validation):
    liste_names = ["Les valeurs trouvées dans la colonne 'scientificName' sont présentées dans le tableau.",
    "L'algorithme garde les valeurs uniques des noms scientifique du jeu de données de départ (et supprime les suffixes sp et sp.) et vérifie auprès de base de données WORMS si ceux-ci y sont répertorié. Des champs sont retournées lors d'une recherche fructueuse. Dans le cas d'une recherche sans résultat auprès de WORMS, une recherche est effectuée auprès de la base de données ITIS. Le premier tableau est donc constitué des noms scientifiques du jeu de données, des valeurs retournés par WORMS ou ITIS et d'une colonne dite de validation qui indique si un nom scientifique se trouve ou non dans les bases de données.",
    "Lien vers référence: https://dwc.tdwg.org/terms/#dwc:scientificName"]

    liste_ids = ["Les valeurs trouvées dans la colonne 'scientificNameID' sont présentées dans le tableau.",
    "Le deuxième tableau se sert des extrants des appels aux bases de données afin de faire la validation des noms scientifiques et des LSID et ce, par rapport à chaque observation ('occurence').",
    "Lien vers référence: https://dwc.tdwg.org/terms/#dwc:scientificNameID"]

    return html.Div([

        html.H4("Champs/Fields 'scientificName' et/and 'scientificNameID':"),

        dash_table.DataTable(data=data_valid_scientific_name.to_dict('records'),
            columns=[
            {"name": ["Valeurs / Values", data_valid_scientific_name.columns[0]], "id": data_valid_scientific_name.columns[0]},
            {"name": ["Validation", data_valid_scientific_name.columns[1]], "id": data_valid_scientific_name.columns[1]},
            {"name": ["Valeurs base de données / Database values", data_valid_scientific_name.columns[2]], "id": data_valid_scientific_name.columns[2]},
            {"name": ["Valeurs base de données / Database values", data_valid_scientific_name.columns[3]], "id": data_valid_scientific_name.columns[3]},
            {"name": ["Valeurs base de données / Database values", data_valid_scientific_name.columns[4]], "id": data_valid_scientific_name.columns[4]},
            {"name": ["Valeurs base de données / Database values", data_valid_scientific_name.columns[5]], "id": data_valid_scientific_name.columns[5]},
            {"name": ["Valeurs base de données / Database values", data_valid_scientific_name.columns[6]], "id": data_valid_scientific_name.columns[6]},
            {"name": ["Valeurs base de données / Database values", data_valid_scientific_name.columns[7]], "id": data_valid_scientific_name.columns[7]},
            {"name": ["Valeurs base de données / Database values", data_valid_scientific_name.columns[8]], "id": data_valid_scientific_name.columns[8]}],
            merge_duplicate_headers=True,       
            #columns=[{'name': i, 'id': i} for i in data_valid_scientific_name.columns],
            page_size=9, sort_action='native', filter_action='native', editable=False, row_deletable=False,
            style_header={'backgroundColor': 'rgb(0, 173, 239)','color': 'white','textAlign': 'center',},
            style_cell={'textAlign': 'left','whiteSpace': 'normal','height': 'auto','lineHeight': '15px',},
            style_table={'height': '375', 'overflowY': 'auto'},
            export_format="csv",
            export_headers='display'),

            dcc.Store(id= 'stored_data_valid_scientific_name' , data=data_valid_scientific_name.to_dict('records')),
            dcc.Store(id= 'stored_data_cross_validation' , data=data_cross_validation.to_dict('records')),
            
            html.Details([
            html.Summary("Info sur/on 'scientificName'"),
            html.Ul([html.Li(x) for x in liste_names]),
            ]),
            
            html.P(""),
            
            ]), html.Div([
            dash_table.DataTable(data=data_cross_validation.to_dict('records'),
            columns=[
            {"name": ["ID référence / Ref. ID", data_cross_validation.columns[0]], "id": data_cross_validation.columns[0]},
            {"name": ["Validation", data_cross_validation.columns[1]], "id": data_cross_validation.columns[1]},
            {"name": ["Validation", data_cross_validation.columns[2]], "id": data_cross_validation.columns[2]},
            {"name": ["Valeurs / Values", data_cross_validation.columns[3]], "id": data_cross_validation.columns[3]},
            {"name": ["Valeurs / Values", data_cross_validation.columns[4]], "id": data_cross_validation.columns[4]},
            {"name": ["Valeurs base de données / Database values", data_cross_validation.columns[5]], "id": data_cross_validation.columns[5]},
            {"name": ["Valeurs base de données / Database values", data_cross_validation.columns[6]], "id": data_cross_validation.columns[6]},
            ],
            merge_duplicate_headers=True, 
            page_size=9, sort_action='native', filter_action='native', editable=False, row_deletable=False,
            style_header={'backgroundColor': 'rgb(0, 173, 239)','color': 'white','textAlign': 'center',
                'whiteSpace': 'normal','height': 'auto','lineHeight': '15px', 'font_size': '12px',},
            style_cell={'textAlign': 'left','whiteSpace': 'normal','height': 'auto','lineHeight': '15px','overflow': 'hidden','textOverflow': 'ellipsis','maxWidth': 0},
            style_table={'height': '375', 'overflowY': 'auto'}, 
            tooltip_data=[{column: {'value': str(value), 'type': 'markdown'} for column, value in row.items()} for row in data_cross_validation.to_dict('records')], 
            tooltip_duration=None,
            export_format="csv", 
            export_headers='display'),
            
            html.Details([
            html.Summary("Info sur/on 'scientificNameID'"),
            html.Ul([html.Li(x) for x in liste_ids]),
            ]),
            
            html.P(""),
            
            ])

def names_taxons_ids_tables(data_valid_scientific_name, data_cross_validation):
    liste_names = ["Les valeurs trouvées dans la colonne 'scientificName' sont présentées dans le tableau.",
    "L'algorithme garde les valeurs uniques des noms scientifique du jeu de données de départ (et supprime les suffixes sp et sp.) et vérifie auprès de base de données WORMS si ceux-ci y sont répertorié. Des champs sont retournées lors d'une recherche fructueuse. Dans le cas d'une recherche sans résultat auprès de WORMS, une recherche est effectuée auprès de la base de données ITIS. Le premier tableau est donc constitué des noms scientifiques du jeu de données, des valeurs retournés par WORMS ou ITIS et d'une colonne dite de validation qui indique si un nom scientifique se trouve ou non dans les bases de données.",
    "Lien vers référence: https://dwc.tdwg.org/terms/#dwc:scientificName"]

    liste_taxons_ids = ["Les valeurs trouvées dans les colonnes 'taxonRank' et 'scientificNameID' sont présentées dans le tableau.",
    "Le deuxième tableau se sert des extrants des appels aux bases de données afin de faire la validation des noms scientifiques mais aussi des rangs taxonomiques et des LSID et ce, par rapport à chaque observation ('occurence').",
    "Liens vers référence: https://dwc.tdwg.org/terms/#dwc:taxonRank et https://dwc.tdwg.org/terms/#dwc:scientificNameID"]

    return html.Div([

        html.H4("Champs/Fields 'scientificName', 'taxonRank' et/and 'scientificNameID':"),

        dash_table.DataTable(data=data_valid_scientific_name.to_dict('records'),
            columns=[
            {"name": ["Valeurs / Values", data_valid_scientific_name.columns[0]], "id": data_valid_scientific_name.columns[0]},
            {"name": ["Validation", data_valid_scientific_name.columns[1]], "id": data_valid_scientific_name.columns[1]},
            {"name": ["Valeurs base de données / Database values", data_valid_scientific_name.columns[2]], "id": data_valid_scientific_name.columns[2]},
            {"name": ["Valeurs base de données / Database values", data_valid_scientific_name.columns[3]], "id": data_valid_scientific_name.columns[3]},
            {"name": ["Valeurs base de données / Database values", data_valid_scientific_name.columns[4]], "id": data_valid_scientific_name.columns[4]},
            {"name": ["Valeurs base de données / Database values", data_valid_scientific_name.columns[5]], "id": data_valid_scientific_name.columns[5]},
            {"name": ["Valeurs base de données / Database values", data_valid_scientific_name.columns[6]], "id": data_valid_scientific_name.columns[6]},
            {"name": ["Valeurs base de données / Database values", data_valid_scientific_name.columns[7]], "id": data_valid_scientific_name.columns[7]},
            {"name": ["Valeurs base de données / Database values", data_valid_scientific_name.columns[8]], "id": data_valid_scientific_name.columns[8]}],
            merge_duplicate_headers=True,       
            #columns=[{'name': i, 'id': i} for i in data_valid_scientific_name.columns],
            page_size=9, sort_action='native', filter_action='native', editable=False, row_deletable=False,
            style_header={'backgroundColor': 'rgb(0, 173, 239)','color': 'white','textAlign': 'center',},
            style_cell={'textAlign': 'left','whiteSpace': 'normal','height': 'auto','lineHeight': '15px',},
            style_table={'height': '375', 'overflowY': 'auto'},
            export_format="csv",
            export_headers='display'),

            dcc.Store(id= 'stored_data_valid_scientific_name' , data=data_valid_scientific_name.to_dict('records')),
            dcc.Store(id= 'stored_data_cross_validation' , data=data_cross_validation.to_dict('records')),
            
            html.Details([
            html.Summary("Info sur/on 'scientificName'"),
            html.Ul([html.Li(x) for x in liste_names]),
            ]),
            
            html.P(""),
            
            ]), html.Div([
            dash_table.DataTable(data=data_cross_validation.to_dict('records'),
            columns=[
            {"name": ["ID référence / Ref. ID", data_cross_validation.columns[0]], "id": data_cross_validation.columns[0]},
            {"name": ["Validation", data_cross_validation.columns[1]], "id": data_cross_validation.columns[1]},
            {"name": ["Validation", data_cross_validation.columns[2]], "id": data_cross_validation.columns[2]},
            {"name": ["Validation", data_cross_validation.columns[3]], "id": data_cross_validation.columns[3]},
            {"name": ["Valeurs / Values", data_cross_validation.columns[4]], "id": data_cross_validation.columns[4]},
            {"name": ["Valeurs / Values", data_cross_validation.columns[5]], "id": data_cross_validation.columns[5]},
            {"name": ["Valeurs / Values", data_cross_validation.columns[6]], "id": data_cross_validation.columns[6]},
            {"name": ["Valeurs base de données / Database values", data_cross_validation.columns[7]], "id": data_cross_validation.columns[7]},
            {"name": ["Valeurs base de données / Database values", data_cross_validation.columns[8]], "id": data_cross_validation.columns[8]},
            {"name": ["Valeurs base de données / Database values", data_cross_validation.columns[9]], "id": data_cross_validation.columns[9]}],
            merge_duplicate_headers=True, 
            page_size=9, sort_action='native', filter_action='native', editable=False, row_deletable=False,
            style_header={'backgroundColor': 'rgb(0, 173, 239)','color': 'white','textAlign': 'center',
                'whiteSpace': 'normal','height': 'auto','lineHeight': '15px', 'font_size': '12px',},
            style_cell={'textAlign': 'left','whiteSpace': 'normal','height': 'auto','lineHeight': '15px','overflow': 'hidden','textOverflow': 'ellipsis','maxWidth': 0},
            style_table={'height': '375', 'overflowY': 'auto'}, 
            tooltip_data=[{column: {'value': str(value), 'type': 'markdown'} for column, value in row.items()} for row in data_cross_validation.to_dict('records')], 
            tooltip_duration=None,
            export_format="csv", 
            export_headers='display'),
            
            html.Details([
            html.Summary("Info sur/on 'taxonRank' et 'scientificNameID'"),
            html.Ul([html.Li(x) for x in liste_taxons_ids]),
            ]),
            
            html.P(""),
            
            ])
            


