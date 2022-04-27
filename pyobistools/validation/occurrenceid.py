import numpy as np
import pandas as pd
from dash import dash_table, html

NaN = np.nan


def validate_occurrenceid(data):
    data = data.rename(columns=str.lower)

    tableau_occurrenceid = {
        "Nombre de valeur unique / Number of unique values": [
            data["occurrenceid"].nunique(dropna=False)
        ]
    }
    tableau_occurrenceid = pd.DataFrame(data=tableau_occurrenceid)
    tableau_occurrenceid

    liste_occurrenceid = [
        "Le nombre de valeurs uniques trouvées dans la colonne 'occurrenceID' est présenté dans le tableau.",
        "Lien vers référence: https://dwc.tdwg.org/terms/#dwc:occurrenceID",
    ]

    return html.Div(
        [
            html.H4("Champ/Field 'occurrenceID':"),
            dash_table.DataTable(
                data=tableau_occurrenceid.to_dict("records"),
                id={"type": "tableau_occurrenceid"},
                columns=[
                    {
                        "name": [
                            "Validation de données / Data validation: 'occurrenceid'",
                            i,
                        ],
                        "id": i,
                    }
                    for i in tableau_occurrenceid.columns
                ],
                sort_action="native",
                filter_action="native",
                editable=False,
                row_deletable=False,
                style_header={
                    "backgroundColor": "rgb(0, 173, 239)",
                    "color": "white",
                    "textAlign": "center",
                },
                style_table={"height": "375", "width": "50%", "overflowY": "auto"},
                style_cell={
                    "textAlign": "center",
                    "whiteSpace": "normal",
                    "height": "auto",
                    "lineHeight": "15px",
                },
                export_format="csv",
                merge_duplicate_headers=True,
                export_headers="display",
            ),
            html.Details(
                [
                    html.Summary("Info sur/on 'occurrenceID'"),
                    html.Ul([html.Li(x) for x in liste_occurrenceid]),
                ]
            ),
            html.P(""),
        ]
    )
