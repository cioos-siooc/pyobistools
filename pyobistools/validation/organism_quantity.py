import numpy as np
from dash import html
from pyobistools.validation.sub_routines.analyse_colonne import (
    AfficheOccurrenceParValeur,
)

NaN = np.nan


def AfficheOrgnismQuantityTypeOccurrences(data):

    list_quantityType = [
        "Les valeurs trouvées dans la colonne 'organismQuantityType' sont présentées dans le tableau.",
        "Lien vers référence: https://dwc.tdwg.org/terms/#dwc:organismQuantityType",
    ]

    # append le tableau fait via analyse_colonne
    ret = html.Div(
        [
            html.H4("Champ/Field 'organismQuantityType':"),
            AfficheOccurrenceParValeur(data, "organismquantitytype"),
            html.Details(
                [
                    html.Summary("Info sur/on 'organismQuantityType'"),
                    html.Ul([html.Li(x) for x in list_quantityType]),
                ]
            ),
            html.P(""),
        ]
    )

    return ret


def AfficheSiOrganismQuantityEtTypeSontPresent(listecolonnes):
    ret = None
    if "organismquantitytype" in listecolonnes:
        # s'assure que la colonne organismquantity existe
        if "organismquantity" not in listecolonnes:
            ret = html.Div(
                [
                    html.H4("Champ/Field 'organismquantity' manquant/missing:"),
                    html.P(""),
                    html.H6(
                        "Il est nécessaire d'avoir la colonne 'organismquantity' en tandem de la colonne 'organismquantitytype'."
                    ),
                    html.H6(
                        "It is necessary to have column 'organismquantity' in tandem with column 'organismquantitytype'."
                    ),
                    html.P(""),
                ]
            )
    elif "organismquantity" in listecolonnes:
        # manque organismquantitytype
        ret = html.Div(
            [
                html.H4("Champ/Field 'organismquantitytype' manquant/missing:"),
                html.P(""),
                html.H6(
                    "Il est nécessaire d'avoir la colonne 'organismquantitytype' en tandem de la colonne 'organismquantity.'"
                ),
                html.H6(
                    "It is necessary to have column 'organismquantitytype' in tandem with column 'organismquantity.'"
                ),
                html.P(""),
            ]
        )

    return ret
