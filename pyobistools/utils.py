#!/usr/bin/env python
# coding=utf-8
import numpy as np
import pandas as pd

NaN = np.nan


def removesuffix(obj: str, suffix: str) -> str:
    # https://peps.python.org/pep-0616/
    if suffix and obj.endswith(suffix):
        return obj[:-len(suffix)]
    else:
        return obj[:]


def function_suffix_removal(data_valid_nom_scientifique):
    liste_noms_pre_modif = []
    liste_noms = []
    liste_noms_sans_suffix = []
    liste_noms_sp = []
    liste_noms_sp_point = []
    liste_noms_spp = []
    liste_noms_spp_point = []

    liste_noms_pre_modif = data_valid_nom_scientifique['scientificname'].to_list()

    for rows in data_valid_nom_scientifique.index:
        scientificName = data_valid_nom_scientifique['scientificname'].iloc[rows].replace(
            " ", "%20")

        if scientificName[-3:] != 'sp.':
            if scientificName[-2:] != 'sp':
                if scientificName[-3:] != 'spp':
                    if scientificName[-4:] != 'spp.':
                        liste_noms_sans_suffix.append(scientificName)

        if scientificName[-3:] == 'sp.':
            scientificName = scientificName[:-6]
            liste_noms_sp_point.append(scientificName)
        if scientificName[-2:] == 'sp':
            scientificName = scientificName[:-5]
            liste_noms_sp.append(scientificName)
        if scientificName[-4:] == 'spp.':
            scientificName = scientificName[:-7]
            liste_noms_spp_point.append(scientificName)
        if scientificName[-3:] == 'spp':
            scientificName = scientificName[:-6]
            liste_noms_spp.append(scientificName)

        liste_noms.append(scientificName)

    liste_noms = list(set(liste_noms))

    return liste_noms_pre_modif, liste_noms, liste_noms_sans_suffix, liste_noms_sp, liste_noms_sp_point, liste_noms_spp, liste_noms_spp_point


def function_add_suffix(nom, liste_noms_sans_suffix, liste_noms_sp, liste_noms_sp_point, liste_noms_spp, liste_noms_spp_point):
    list_of_list = {}
    nom_recomposed = nom
    nom_recomposed = nom_recomposed.replace("%20", " ")
    nom_recomposed_sp = NaN
    nom_recomposed_sp_point = NaN
    nom_recomposed_spp = NaN
    nom_recomposed_spp_point = NaN

    if nom in liste_noms_sp:
        nom_recomposed_sp = nom_recomposed + " sp"
        list_of_list["noms_sp"] = nom_recomposed_sp

    if nom in liste_noms_sp_point:
        nom_recomposed_sp_point = nom_recomposed + " sp."
        list_of_list["noms_sp_point"] = nom_recomposed_sp_point

    if nom in liste_noms_spp:
        nom_recomposed_spp = nom_recomposed + " spp"
        list_of_list["noms_spp"] = nom_recomposed_spp

    if nom in liste_noms_spp_point:
        nom_recomposed_spp_point = nom_recomposed + " spp."
        list_of_list["noms_spp_point"] = nom_recomposed_spp_point

    if nom in liste_noms_sans_suffix:
        list_of_list["noms_sans_suffix"] = nom_recomposed

    return list_of_list


# fonction qui permet de vérifier le match des colonnes de noms scientifiques mais en enlevant les suffixes d'une des colonnes
def exact_match_suffix(a, b):
    if a == b:
        return "Oui/Yes"
    elif a[-3:] == 'sp.':
        a = a[:-4]
        if a == b:
            return 'Oui, avec qualificatif / Yes, with qualifier'
        else:
            return 'Non/No'
    elif a[-2:] == 'sp':
        a = a[:-3]
        if a == b:
            return 'Oui, avec qualificatif / Yes, with qualifier'
        else:
            return 'Non/No'
    elif a[-4:] == 'spp.':
        a = a[:-5]
        if a == b:
            return 'Oui, avec qualificatif / Yes, with qualifier'
        else:
            return 'Non/No'
    elif a[-3:] == 'spp':
        a = a[:-4]
        if a == b:
            return 'Oui, avec qualificatif / Yes, with qualifier'
        else:
            return 'Non/No'
    else:
        return "Non/No"

# fonction qui permet de vérifier le match des colonnes


def exact_match(a, b):
    if a == b:
        return "Oui/Yes"
    else:
        return "Non/No"


def names_analyse(data_valid_scientific_name):
    # Comparaison des noms scientifiques du serveur vs. ceux du jeu de données initial
    data_valid_scientific_name['Exact_Match'] = np.vectorize(exact_match_suffix)(
        data_valid_scientific_name["scientificname"].str.lower(), data_valid_scientific_name['Valid_Name'].str.lower())

    # classer les valeurs par validité
    data_valid_scientific_name.sort_values(
        by=['Exact_Match', 'scientificname'], ascending=True, inplace=True)

    columns = [('Dataset Values', 'scientificName'), ('Validation', 'Exact_Match'), ('Database values', 'TaxonID'), ('Database values', 'Status'),
               ('Database values', 'Unacceptreason'), ('Database values',
                                                       'Taxon_Rank'), ('Database values', 'Valid_TaxonID'),
               ('Database values', 'Valid_Name'), ('Database values', 'LSID')]
    data_valid_scientific_name.columns = pd.MultiIndex.from_tuples(columns)

    return data_valid_scientific_name


def names_ids_analyse(data_valid_scientific_name, data):
    data_valid_scientific_name['Exact_Match'] = np.vectorize(exact_match_suffix)(
        data_valid_scientific_name["scientificname"].str.lower(), data_valid_scientific_name['Valid_Name'].str.lower())

    # Préparation du tableau de comparaison des noms scientifiques, rangs taxonimique et LSID (si applicable)
    data_cross_validation = data.copy()
    data_cross_validation = data_cross_validation[[
        'occurrenceid', 'scientificname', 'scientificnameid', ]]
    header_list1 = ['occurrenceid', 'scientificname',
                    'scientificnameid', 'ScientificName_V', 'scientificNameID_V']
    data_cross_validation = data_cross_validation.reindex(columns=header_list1)
    data_cross_validation = data_cross_validation.iloc[:, [0, 3, 4, 1, 2]]

    # création d'une colonne avec autre nom afin de pouvoir la comparer à une autre colonne
    data_valid_scientific_name['scientificname2'] = data_valid_scientific_name['scientificname']

    # Merge du tableau des noms et du tableau des noms, rangs taxonomiques et LSID
    data_cross_validation = data_cross_validation.merge(data_valid_scientific_name[[
                                                        'Valid_Name', 'LSID', 'scientificname2']], how='left', left_on='scientificname', right_on='scientificname2')

    # Vérification des colonnes pour fin de validation
    data_cross_validation['ScientificName_V'] = np.vectorize(exact_match_suffix)(
        data_cross_validation["scientificname"].str.lower(), data_cross_validation['Valid_Name'].str.lower())
    data_cross_validation['scientificNameID_V'] = np.vectorize(exact_match)(
        data_cross_validation["scientificnameid"].str.lower(), data_cross_validation['LSID'].str.lower())

    # classer les valeurs par validité
    data_valid_scientific_name.sort_values(
        by=['Exact_Match', 'scientificname'], ascending=True, inplace=True)

    data_cross_validation.sort_values(
        by=['ScientificName_V', 'scientificNameID_V'], ascending=True, inplace=True)

    data_valid_scientific_name = data_valid_scientific_name.drop(['scientificname2'], axis=1)
    data_cross_validation = data_cross_validation.drop(['scientificname2'], axis=1)

    columns = [('Dataset Values', 'scientificName'), ('Validation', 'Exact_Match'), ('Database values', 'TaxonID'), ('Database values', 'Status'),
               ('Database values', 'Unacceptreason'), ('Database values',
                                                       'Taxon_Rank'), ('Database values', 'Valid_TaxonID'),
               ('Database values', 'Valid_Name'), ('Database values', 'LSID')]
    data_valid_scientific_name.columns = pd.MultiIndex.from_tuples(columns)

    columns = [('Ref. ID', 'occurrenceID'), ('Validation', 'scientificName_Validation'), ('Validation', 'scientificNameID_Validation'), ('Dataset Values', 'scientificName'),
               ('Dataset Values', 'scientificNameID'), ('Database values', 'Valid_Name'), ('Database values', 'LSID')]
    data_cross_validation.columns = pd.MultiIndex.from_tuples(columns)

    return data_valid_scientific_name, data_cross_validation


def names_taxons_ids_analyse(data_valid_scientific_name, data):
    # Comparaison des noms scientifiques du serveur vs. ceux du jeu de données initial
    data_valid_scientific_name['Exact_Match'] = np.vectorize(exact_match_suffix)(
        data_valid_scientific_name["scientificname"].str.lower(), data_valid_scientific_name['Valid_Name'].str.lower())

    # Préparation du tableau de comparaison des noms scientifiques, rangs taxonimique et LSID (si applicable)
    data_cross_validation = data.copy()
    data_cross_validation = data_cross_validation[[
        'occurrenceid', 'scientificname', 'taxonrank', 'scientificnameid', ]]
    header_list1 = ['occurrenceid', 'scientificname', 'taxonrank',
                    'scientificnameid', 'ScientificName_V', 'TaxonRank_V', 'scientificNameID_V']
    data_cross_validation = data_cross_validation.reindex(columns=header_list1)
    data_cross_validation = data_cross_validation.iloc[:, [0, 4, 5, 6, 1, 2, 3]]

    # création d'une colonne avec autre nom afin de pouvoir la comparer à une autre colonne
    data_valid_scientific_name['scientificname2'] = data_valid_scientific_name['scientificname']

    # Merge du tableau des noms et du tableau des noms, rangs taxonomiques et LSID
    data_cross_validation = data_cross_validation.merge(data_valid_scientific_name[[
                                                        'Valid_Name', 'Taxon_Rank', 'LSID', 'scientificname2']], how='left', left_on='scientificname', right_on='scientificname2')

    # Vérification des colonnes pour fin de validation
    data_cross_validation['ScientificName_V'] = np.vectorize(exact_match_suffix)(
        data_cross_validation["scientificname"].str.lower(), data_cross_validation['Valid_Name'].str.lower())
    data_cross_validation['TaxonRank_V'] = np.vectorize(exact_match)(
        data_cross_validation["taxonrank"].str.lower(), data_cross_validation['Taxon_Rank'].str.lower())
    data_cross_validation['scientificNameID_V'] = np.vectorize(exact_match)(
        data_cross_validation["scientificnameid"].str.lower(), data_cross_validation['LSID'].str.lower())

    # classer les valeurs par validité
    data_valid_scientific_name.sort_values(
        by=['Exact_Match', 'scientificname'], ascending=True, inplace=True)

    data_cross_validation.sort_values(
        by=['ScientificName_V', 'TaxonRank_V', 'scientificNameID_V'], ascending=True, inplace=True)

    data_valid_scientific_name = data_valid_scientific_name.drop(['scientificname2'], axis=1)
    data_cross_validation = data_cross_validation.drop(['scientificname2'], axis=1)

    columns = [('Dataset Values', 'scientificName'), ('Validation', 'Exact_Match'), ('Database values', 'TaxonID'), ('Database values', 'Status'),
               ('Database values', 'Unacceptreason'), ('Database values',
                                                       'Taxon_Rank'), ('Database values', 'Valid_TaxonID'),
               ('Database values', 'Valid_Name'), ('Database values', 'LSID')]

    data_valid_scientific_name.columns = pd.MultiIndex.from_tuples(columns)

    columns = [('Ref. ID', 'occurrenceID'), ('Validation', 'scientificName_Validation'), ('Validation', 'taxonRank_Validation'), ('Validation', 'scientificNameID_Validation'), ('Dataset Values', 'scientificName'),
               ('Dataset Values', 'taxonRank'), ('Dataset Values', 'scientificNameID'), ('Database values', 'Valid_Name'), ('Database values', 'Taxon_Rank'), ('Database values', 'LSID')]

    data_cross_validation.columns = pd.MultiIndex.from_tuples(columns)

    return data_valid_scientific_name, data_cross_validation
