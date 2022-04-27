import numpy as np
import pandas as pd
from dash import dash_table, html

NaN = np.nan


def validate_eventid(data):
    data = data.rename(columns=str.lower)

    tableau_eventid = pd.DataFrame(data=data["eventid"].value_counts(dropna=False))
    tableau_eventid.reset_index(inplace=True)

    tableau_eventid.rename(
        columns={
            "index": "Valeurs / Values",
            "eventid": "Nombre d'observations / Number of observations",
        },
        inplace=True,
    )

    liste_eventid = [
        "Les valeurs trouvées dans la colonne 'eventID' sont présentées dans le tableau.",
        "Lien vers référence: https://dwc.tdwg.org/terms/#dwc:eventID",
    ]

    return html.Div(
        [
            html.H4("Champ/Field 'eventID':"),
            dash_table.DataTable(
                data=tableau_eventid.to_dict("records"),
                id={"type": "tableau_eventid"},
                columns=[
                    {
                        "name": [
                            "Validation de données / Data validation: 'eventid'",
                            i,
                        ],
                        "id": i,
                    }
                    for i in tableau_eventid.columns
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
                page_size=9,
                export_headers="display",
            ),
            html.Details(
                [
                    html.Summary("Info sur/on 'eventID'"),
                    html.Ul([html.Li(x) for x in liste_eventid]),
                ]
            ),
            html.P(""),
        ]
    )
