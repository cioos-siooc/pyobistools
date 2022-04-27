import numpy as np
import pandas as pd
from dash import dash_table, html

NaN = np.nan


def validate_basisofrecord(data):
    data = data.rename(columns=str.lower)

    valeur_exemples = [
        "PreservedSpecimen",
        "FossilSpecimen",
        "LivingSpecimen",
        "MaterialSample",
        "Event",
        "HumanObservation",
        "MachineObservation",
        "Taxon",
        "Occurrence",
        "MaterialCitation",
    ]

    tableau_basisofrecord = pd.DataFrame(
        data=data["basisofrecord"].value_counts(dropna=False)
    )
    tableau_basisofrecord.reset_index(inplace=True)

    tableau_basisofrecord.rename(
        columns={
            "index": "Valeur / Value",
            "basisofrecord": "Nombre d'observations / Number of observations",
        },
        inplace=True,
    )
    tableau_basisofrecord = tableau_basisofrecord.reindex(
        columns=[
            "Valeur / Value",
            "DWC standard",
            "Nombre d'observations / Number of observations",
        ]
    )
    tableau_basisofrecord["DWC standard"] = tableau_basisofrecord[
        "Valeur / Value"
    ].isin(valeur_exemples)
    tableau_basisofrecord["DWC standard"].replace(False, "Absence", inplace=True)
    tableau_basisofrecord["DWC standard"].replace(
        True, "Présent / Present", inplace=True
    )

    liste_basisofrecord = [
        "Les valeurs trouvées dans la colonne 'basisofrecord' sont présentées dans le tableau et leur présence ou non dans la documentation est analysée.",
        "Les valeurs données en exemple dans la documentation sont: 'PreservedSpecimen', 'FossilSpecimen', 'LivingSpecimen', 'MaterialSample', 'Event', 'HumanObservation', 'MachineObservation', 'Taxon', 'Occurrence', 'MaterialCitation'.",
        "Lien vers référence: https://dwc.tdwg.org/terms/#dwc:basisOfRecord",
    ]

    return html.Div(
        [
            html.H4("Champ/Field 'basisOfRecord':"),
            dash_table.DataTable(
                data=tableau_basisofrecord.to_dict("records"),
                id={"type": "tableau_basisofrecord"},
                columns=[
                    {
                        "name": [
                            "Validation de données / Data validation: 'basisofrecord'",
                            i,
                        ],
                        "id": i,
                    }
                    for i in tableau_basisofrecord.columns
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
                    html.Summary("Info sur/on 'basisOfRecord'"),
                    html.Ul([html.Li(x) for x in liste_basisofrecord]),
                ]
            ),
            html.P(""),
        ]
    )
