import numpy as np
import pandas as pd
from dash import dash_table, html
NaN = np.nan
import iso8601


def eventdate_fonction(data):
  
    tableau_eventdate = pd.DataFrame(data=data["eventdate"])
    tableau_eventdate = tableau_eventdate.rename(columns=str.lower)

    tableau_eventdate.reset_index(inplace=True)

    tableau_eventdate.rename(columns={"index":"Validité / Validity","eventdate": "Valeurs / Values"}, inplace=True)
    tableau_eventdate = tableau_eventdate.reindex(columns = ['Valeurs / Values','Validité / Validity'])


    def iso8601_check(a):
        try:
            iso8601.parse_date(a)
        except:
            return "Non valide / Invalid"
        return "Valide / Valid"

    tableau_eventdate['Validité / Validity'] = np.vectorize(iso8601_check)(tableau_eventdate['Valeurs / Values'])
    tableau_eventdate.sort_values(by='Validité / Validity', ascending=True, inplace=True)
    tableau_eventdate.drop_duplicates(inplace=True)


    liste_eventdate_fonction = ["Les valeurs uniques trouvées dans la colonne 'eventDate' sont présentées dans le tableau et leur validité par rapport au standard ISO8601 est analysée.",
    "Lien vers référence: https://dwc.tdwg.org/terms/#dwc:eventDate"]
    
    return html.Div([
        
        html.H4("Champ/Field 'eventDate':"),

        dash_table.DataTable(
        data=tableau_eventdate.to_dict('records'),id={'type': 'tableau_eventdate'},
        columns=[{'name': ["Validation de données / Data validation: 'eventdate'", i], 'id': i} for i in tableau_eventdate.columns],
        sort_action='native', filter_action='native', editable=False, row_deletable=False,
        style_header={'backgroundColor': 'rgb(0, 173, 239)','color': 'white', 'textAlign': 'center'},
        style_table={'height': '375','width':'50%', 'overflowY': 'auto'},
        style_cell={'textAlign': 'center','whiteSpace': 'normal','height': 'auto','lineHeight': '15px'},
        export_format="csv",
        merge_duplicate_headers=True,
        page_size=9,
        export_headers='display'),

        html.Details([
        html.Summary("Info sur 'eventDate'"),
        html.Ul([html.Li(x) for x in liste_eventdate_fonction]),
        ]),
        
        html.P('')])  

