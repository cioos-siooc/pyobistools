import numpy as np
import pandas as pd
NaN = np.nan

# fonction qui permet de vérifier le match des colonnes de noms scientifiques mais en enlevant les suffixes d'une des colonnes
# this function verifies the comparison between the scientific name columns, but removes the suffixes from one of the columns
def exact_match_suffix(a, b):
    if a == b:
        return "Oui/Yes"
    elif a[-3:] == 'sp.':
        a = a[:-4]
        if a == b:
            return 'Oui, avec qualificatif / Yes, with qualifier'
        else:
            return 'Non/no'
    elif a[-2:] == 'sp': 
        a = a[:-3]
        if a == b:
            return 'Oui, avec qualificatif / Yes, with qualifier'
        else:
            return 'Non/no'
    elif a[-4:] == 'spp.':
        a = a[:-5]    
        if a == b:
            return 'Oui, avec qualificatif / Yes, with qualifier'
        else:
            return 'Non/no'
    else:
        return "Non/no"

# fonction qui permet de vérifier le match des colonnes
# verifying if the columns match
def exact_match(a, b):
    if a == b:
        return "Oui/Yes"
    else:
        return "Non/No"


def names_analyse(data_valid_scientific_name):
    # Comparaison des noms scientifiques du serveur vs. ceux du jeu de données initial
    # compare the scientific names from the server to the names in the initial dataset
    data_valid_scientific_name['Exact_Match'] = np.vectorize(exact_match_suffix)(data_valid_scientific_name["scientificname"], data_valid_scientific_name['Valid_Name'] )
    return data_valid_scientific_name


def names_ids_analyse(data_valid_scientific_name, data):
    data_valid_scientific_name['Exact_Match'] = np.vectorize(exact_match_suffix)(data_valid_scientific_name["scientificname"], data_valid_scientific_name['Valid_Name'] )

    # Préparation du tableau de comparaison des noms scientifiques, rangs taxonimique et LSID (si applicable)
    # preps a comparison table for the scientificnames, taxa, and LSID (if applicable)
    data_cross_validation = data.copy()
    data_cross_validation = data_cross_validation[['occurrenceid','scientificname','scientificnameid',]]
    header_list1 = ['occurrenceid', 'scientificname','scientificnameid', 'ScientificName_V', 'scientificNameID_V'] 
    data_cross_validation = data_cross_validation.reindex(columns = header_list1) 
    data_cross_validation= data_cross_validation.iloc[:, [0,3,4,1,2]]

    # création d'une colonne avec autre nom afin de pouvoir la comparer à une autre colonne
    # create a column with other name in order to compare between two values
    data_valid_scientific_name['scientificname2'] = data_valid_scientific_name['scientificname']

    # Merge du tableau des noms et du tableau des noms, rangs taxonomiques et LSID
    # merge name table with name, taxa and LSID table
    data_cross_validation = data_cross_validation.merge(data_valid_scientific_name[['Valid_Name','LSID','scientificname2']],how='left',left_on='scientificname', right_on='scientificname2' )

    # Vérification des colonnes pour fin de validation
    # verify columns for final validation
    data_cross_validation['ScientificName_V'] = np.vectorize(exact_match_suffix)(data_cross_validation["scientificname"], data_cross_validation['Valid_Name'] )
    data_cross_validation['scientificNameID_V'] = np.vectorize(exact_match)(data_cross_validation["scientificnameid"], data_cross_validation['LSID'] )

    # classer les valeurs par validité
    # classify the validation values
    data_valid_scientific_name.sort_values(by='Exact_Match', ascending=True, inplace=True)
    data_cross_validation.sort_values(by=['ScientificName_V', 'scientificNameID_V'], ascending=True, inplace=True)

    return data_valid_scientific_name, data_cross_validation



def names_taxons_ids_analyse(data_valid_scientific_name, data):
    # Comparaison des noms scientifiques du serveur vs. ceux du jeu de données initial
    # compare the scientific names from the server to those in the initial dataset
    data_valid_scientific_name['Exact_Match'] = np.vectorize(exact_match_suffix)(data_valid_scientific_name["scientificname"], data_valid_scientific_name['Valid_Name'] )

    # Préparation du tableau de comparaison des noms scientifiques, rangs taxonimique et LSID (si applicable)
    # preps a comparison table for scientific names, taxa ranges and LSID (if applicable)
    data_cross_validation = data.copy()
    data_cross_validation = data_cross_validation[['occurrenceid','scientificname','taxonrank','scientificnameid',]]
    header_list1 = ['occurrenceid', 'scientificname','taxonrank','scientificnameid', 'ScientificName_V', 'TaxonRank_V', 'scientificNameID_V'] 
    data_cross_validation = data_cross_validation.reindex(columns = header_list1) 
    data_cross_validation= data_cross_validation.iloc[:, [0,4,5,6,1,2,3]]
    
    # création d'une colonne avec autre nom afin de pouvoir la comparer à une autre colonne
    # creates a column with second name, for comparing the two values
    data_valid_scientific_name['scientificname2'] = data_valid_scientific_name['scientificname']

    # Merge du tableau des noms et du tableau des noms, rangs taxonomiques et LSID
    # merge the name table with the name, taxa range and LSID table
    data_cross_validation = data_cross_validation.merge(data_valid_scientific_name[['Valid_Name','Taxon_Rank','LSID','scientificname2']],how='left',left_on='scientificname', right_on='scientificname2' )

    # Vérification des colonnes pour fin de validation
    # Verification of columns for the final validation
    data_cross_validation['ScientificName_V'] = np.vectorize(exact_match_suffix)(data_cross_validation["scientificname"], data_cross_validation['Valid_Name'] )
    data_cross_validation['TaxonRank_V'] = np.vectorize(exact_match)(data_cross_validation["taxonrank"], data_cross_validation['Taxon_Rank'] )
    data_cross_validation['scientificNameID_V'] = np.vectorize(exact_match)(data_cross_validation["scientificnameid"], data_cross_validation['LSID'] )

    
    # classer les valeurs par validité
    # classify the values based on validation
    data_valid_scientific_name.sort_values(by='Exact_Match', ascending=True, inplace=True)
    data_cross_validation.sort_values(by=['ScientificName_V', 'TaxonRank_V','scientificNameID_V'], ascending=True, inplace=True)

    return data_valid_scientific_name, data_cross_validation



