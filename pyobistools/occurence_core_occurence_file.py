import dash
import numpy as np
import pandas as pd
from dash import dash_table, html

from pyobistools.table_format_analysis              import table_format_analysis
from pyobistools.validation.basisofrecord           import validate_basisofrecord
from pyobistools.validation.datasetid               import validate_datasetid
from pyobistools.validation.decimal_coordinates     import validate_decimal_coordinates
from pyobistools.validation.eventdate               import validate_eventdate
from pyobistools.validation.footprintwkt            import validate_foorprintwkt
from pyobistools.validation.locationid              import validate_LocationIDOccurrences
from pyobistools.validation.occurrenceid            import validate_occurrenceid
from pyobistools.validation.occurrencestatus        import validate_occurrencestatus
from pyobistools.validation.organism_quantity       import (
                                                        AfficheOrgnismQuantityTypeOccurrences,
                                                        AfficheSiOrganismQuantityEtTypeSontPresent,
                                                    )
from pyobistools.validation.worms_itis              import (
                                                        validation_Worms_Itis_fonction,
                                                    )

NaN = np.nan

def occurence_core_occurence_file(data, colonne_jeu_donnees, nombre_rangees):
    # filtrer les champs présent dans le jeu de données
    col_analyse = {
        "Nom du champ / Field name": [
            "basisofrecord",
            "datasetid",
            "decimallatitude",
            "decimallongitude",
            "eventdate",
            "occurrenceid",
            "occurrencestatus",
            "scientificname",
            "scientificnameid",
            "taxonid",
            "footprintwkt",
            "locationID",
            "organismquantity",
            "organismquantitytype",
        ],
        "Nécéssaire ou optionnel / Necessary or optionnal": [
            "Nécéssaire / Necessary",
            "Nécéssaire / Necessary",
            "Nécéssaire / Necessary",
            "Nécéssaire / Necessary",
            "Nécéssaire / Necessary",
            "Nécéssaire / Necessary",
            "Nécéssaire / Necessary",
            "Nécéssaire / Necessary",
            "Nécéssaire / Necessary",
            "Nécéssaire / Necessary",
            "Optionnel / Optionnal",
            "Optionnel / Optionnal",
            "Optionnel / Optionnal",
            "Optionnel / Optionnal",
        ],
        "Présence/Presence ou/or absence": [
            NaN,
            NaN,
            NaN,
            NaN,
            NaN,
            NaN,
            NaN,
            NaN,
            NaN,
            NaN,
            NaN,
            NaN,
            NaN,
            NaN,
        ],
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
    if "basisofrecord" in liste_format:
        basisofrecord = validate_basisofrecord(data)
        liste_affichage.append(basisofrecord)

    if "datasetid" in liste_format:
        datasetid = validate_datasetid(data)
        liste_affichage.append(datasetid)

    if "decimallatitude" in liste_format and "decimallongitude" in liste_format:
        latitude_longitude = validate_decimal_coordinates(data)
        liste_affichage.append(latitude_longitude)

    if "eventdate" in liste_format:
        eventdate = validate_eventdate(data)
        liste_affichage.append(eventdate)

    if "occurrenceid" in liste_format:
        occurenceid = validate_occurrenceid(data)
        liste_affichage.append(occurenceid)

    if "occurrencestatus" in liste_format:
        occurrencestatus = validate_occurrencestatus(data)
        liste_affichage.append(occurrencestatus)

    if "scientificname" in liste_format and "scientificnameid" not in liste_format:
        tableau_valid_nom_scientifique = validation_Worms_Itis_fonction(data, "names")
        liste_affichage.append(tableau_valid_nom_scientifique)

    if (
        "scientificname" in liste_format
        and "scientificnameid" in liste_format
        and "occurrenceid" in liste_format
    ):

        if "taxonrank" in colonnes_extra:
            (
                tableau_valid_nom_scientifique,
                tableau_valid_croisee,
            ) = validation_Worms_Itis_fonction(data, "names_taxons_ids")
            liste_affichage.append(tableau_valid_nom_scientifique)
            liste_affichage.append(tableau_valid_croisee)

        if "taxonrank" not in colonnes_extra:
            (
                tableau_valid_nom_scientifique,
                tableau_valid_croisee,
            ) = validation_Worms_Itis_fonction(data, "names_ids")
            liste_affichage.append(tableau_valid_nom_scientifique)
            liste_affichage.append(tableau_valid_croisee)

    if "footprintwkt" in liste_format:
        footprintwkt = validate_foorprintwkt(data)
        liste_affichage.append(footprintwkt)

    if "locationid" in liste_format:
        locationid = validate_LocationIDOccurrences(data)
        liste_affichage.append(locationid)

    # S'assure que si organismquantitytype ou organismquantity est présent, l'autre l'est aussi
    organismQuantityEtType = AfficheSiOrganismQuantityEtTypeSontPresent(liste_format)
    if organismQuantityEtType is not None:
        liste_affichage.append(organismQuantityEtType)

    if "organismquantitytype" in liste_format:
        organismquantitytype = AfficheOrgnismQuantityTypeOccurrences(data)
        liste_affichage.append(organismquantitytype)

    # section retournant le tableau d'analyse du format ainsi que les retours des fonctions des champs présents
    return table_format_analysis(
        colonne_analyse, colonnes_extra, liste_affichage, nombre_rangees
    )
