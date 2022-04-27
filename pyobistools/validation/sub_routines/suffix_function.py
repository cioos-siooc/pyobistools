import numpy as np

NaN = np.nan


def function_suffix_removal(data_valid_nom_scientifique):
    liste_noms_pre_modif = []
    liste_noms = []
    liste_noms_sans_suffix = []
    liste_noms_sp = []
    liste_noms_sp_point = []
    liste_noms_spp_point = []

    liste_noms_pre_modif = data_valid_nom_scientifique["scientificname"].to_list()

    for rows in range(len(data_valid_nom_scientifique)):

        scientificName = (
            data_valid_nom_scientifique["scientificname"].iloc[rows].replace(" ", "%20")
        )

        if scientificName[-3:] != "sp.":
            if scientificName[-2:] != "sp":
                if scientificName[-4:] != "spp.":
                    liste_noms_sans_suffix.append(scientificName)

        if scientificName[-3:] == "sp.":
            scientificName = scientificName[:-6]
            liste_noms_sp_point.append(scientificName)
        if scientificName[-2:] == "sp":
            scientificName = scientificName[:-5]
            liste_noms_sp.append(scientificName)
        if scientificName[-4:] == "spp.":
            scientificName = scientificName[:-7]
            liste_noms_spp_point.append(scientificName)

        liste_noms.append(scientificName)

    liste_noms = list(set(liste_noms))

    return (
        liste_noms_pre_modif,
        liste_noms,
        liste_noms_sans_suffix,
        liste_noms_sp,
        liste_noms_sp_point,
        liste_noms_spp_point,
    )


def function_add_suffix(
    nom,
    liste_noms_sans_suffix,
    liste_noms_sp,
    liste_noms_sp_point,
    liste_noms_spp_point,
):
    list_of_list = {}
    nom_recomposed = nom
    nom_recomposed = nom_recomposed.replace("%20", " ")
    nom_recomposed_sp = NaN
    nom_recomposed_sp_point = NaN
    nom_recomposed_spp_point = NaN

    if nom in liste_noms_sp:
        nom_recomposed_sp = nom_recomposed + " sp"
        list_of_list["noms_sp"] = nom_recomposed_sp

    if nom in liste_noms_sp_point:
        nom_recomposed_sp_point = nom_recomposed + " sp."
        list_of_list["noms_sp_point"] = nom_recomposed_sp_point

    if nom in liste_noms_spp_point:
        nom_recomposed_spp_point = nom_recomposed + " spp."
        list_of_list["noms_spp_point"] = nom_recomposed_spp_point

    if nom in liste_noms_sans_suffix:
        list_of_list["noms_sans_suffix"] = nom_recomposed

    return list_of_list
