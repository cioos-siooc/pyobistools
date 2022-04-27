import numpy as np
import pandas as pd


from pyobistools.validation.datasetid import validate_datasetid
from pyobistools.validation.eventid import validate_eventid
from pyobistools.validation.eventdate import validate_eventdate
from pyobistools.validation.decimal_coordinates import validate_decimal_coordinates
from pyobistools.validation.footprintwkt import validate_foorprintwkt
from pyobistools.validation.locationid import validate_LocationIDOccurrences
from pyobistools.table_format_analysis import table_format_analysis

NaN = np.nan


def event_core_event_file(data, colonne_jeu_donnees, nombre_rangees):
    # filtrer les champs présent dans le jeu de données et créer un tableau
    col_analyse = {
        "Nom du champ / Field name": [
            "datasetid",
            "decimallatitude",
            "decimallongitude",
            "eventdate",
            "eventid",
            "footprintwkt",
            "locationid",
        ],
        "Nécéssaire ou optionnel / Necessary or optionnal": [
            "Nécéssaire / Necessary",
            "Nécéssaire / Necessary",
            "Nécéssaire / Necessary",
            "Nécéssaire / Necessary",
            "Nécéssaire / Necessary",
            "Nécéssaire / Necessary",
            "Optionnel / Optionnal",
        ],
        "Présence/Presence ou/or absence": [NaN, NaN, NaN, NaN, NaN, NaN, NaN],
    }

    colonne_analyse = pd.DataFrame(data=col_analyse)
    colonne_analyse["Présence/Presence ou/or absence"] = colonne_analyse[
        "Nom du champ / Field name"
    ].isin(colonne_jeu_donnees)
    colonne_analyse["Présence/Presence ou/or absence"].replace(
        False, "Absent", inplace=True
    )
    colonne_analyse["Présence/Presence ou/or absence"].replace(
        True, "Présent/Present", inplace=True
    )
    colonne_analyse.sort_values(
        by="Présence/Presence ou/or absence", ascending=True, inplace=True
    )

    # liste de champs présents dans le jeu de données
    liste_format = colonne_analyse[
        colonne_analyse["Présence/Presence ou/or absence"] == "Présent/Present"
    ]["Nom du champ / Field name"]
    liste_format = list(liste_format)

    # liste des différences entre le tableau des champs nécessaires/optionnels présents et tous les champs présents dans le jeu de données
    colonnes_extra = list(set(colonne_jeu_donnees) - set(liste_format))
    colonnes_extra = sorted(colonnes_extra)
    if len(colonnes_extra) == 0:
        colonnes_extra = ["aucune colonne / no column"]

    # section servant à rouler les fonctions de validation pour les colonnes présentes dans le jeu de données
    liste_affichage = []
    if "datasetid" in liste_format:
        datasetid = validate_datasetid(data)
        liste_affichage.append(datasetid)

    if "decimallatitude" in liste_format and "decimallongitude" in liste_format:
        latitude_longitude = validate_decimal_coordinates(data)
        liste_affichage.append(latitude_longitude)

    if "eventdate" in liste_format:
        eventdate = validate_eventdate(data)
        liste_affichage.append(eventdate)

    if "eventid" in liste_format:
        eventid = validate_eventid(data)
        liste_affichage.append(eventid)

    if "footprintwkt" in liste_format:
        footprintwkt = validate_foorprintwkt(data)
        liste_affichage.append(footprintwkt)

    if "locationid" in liste_format:
        locationid = validate_LocationIDOccurrences(data)
        liste_affichage.append(locationid)

    # section retournant le tableau d'analyse du format ainsi que les retours des fonctions des champs présents
    return table_format_analysis(
        colonne_analyse, colonnes_extra, liste_affichage, nombre_rangees
    )
