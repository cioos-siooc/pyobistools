import time
import numpy as np
import pandas as pd
import requests
from numpy import random
from pyobistools.utils import (function_add_suffix, function_suffix_removal,
                               names_analyse, names_ids_analyse,
                               names_taxons_ids_analyse)

NaN = np.nan


def check_scientificname_and_ids(data, value, itis_usage=False):
    data = pd.DataFrame(data=data)
    data = data.rename(columns=str.lower)
    data_valid_scientific_name = data

    data_valid_scientific_name = data_valid_scientific_name[["scientificname"]]
    header_list = ["scientificname", 'Exact_Match', 'TaxonID', 'Status',
                    'Unacceptreason', 'Taxon_Rank', 'Valid_TaxonID', 'Valid_Name', 'LSID']
    data_valid_scientific_name = data_valid_scientific_name.reindex(columns=header_list)
    data_valid_scientific_name = data_valid_scientific_name.drop_duplicates(subset=["scientificname"])
    data_valid_scientific_name.reset_index(drop=True, inplace=True)
    data_valid_scientific_name.replace(NaN, "", inplace=True)

    # get rid of sp, sp. and spp. suffix because Worms database does not support them
    liste_noms_pre_modif, liste_noms, liste_noms_sans_suffix, liste_noms_sp, liste_noms_sp_point, liste_noms_spp, liste_noms_spp_point = function_suffix_removal(data_valid_scientific_name)

    for index, nom in enumerate(liste_noms):
    #  print(nom)
        list_of_list = function_add_suffix(nom, liste_noms_sans_suffix, liste_noms_sp, liste_noms_sp_point, liste_noms_spp, liste_noms_spp_point)

        response = requests.get(f"https://www.marinespecies.org/rest/AphiaRecordsByName/{nom}?like=false&marine_only=false&offset=1")

        if response.status_code == 200:
            try:
                response2 = response.json()
                for key in list_of_list:
                    if response2:
                        data_valid_scientific_name.loc[data_valid_scientific_name['scientificname'] == list_of_list[key], 'TaxonID'] = response2[0].get('AphiaID', '')
                        data_valid_scientific_name.loc[data_valid_scientific_name['scientificname'] == list_of_list[key], 'Status'] = response2[0].get('status', '')
                        data_valid_scientific_name.loc[data_valid_scientific_name['scientificname'] == list_of_list[key], 'Unacceptreason'] = response2[0].get('unacceptreason', '')
                        data_valid_scientific_name.loc[data_valid_scientific_name['scientificname'] == list_of_list[key], 'Taxon_Rank'] = response2[0].get('rank', '')
                        data_valid_scientific_name.loc[data_valid_scientific_name['scientificname'] == list_of_list[key], 'Valid_TaxonID'] = response2[0].get('valid_AphiaID', '')
                        data_valid_scientific_name.loc[data_valid_scientific_name['scientificname'] == list_of_list[key], 'Valid_Name'] = response2[0].get('valid_name', '')
                        data_valid_scientific_name.loc[data_valid_scientific_name['scientificname'] == list_of_list[key], 'LSID'] = response2[0].get('lsid', '')
                        data_valid_scientific_name.loc[data_valid_scientific_name['scientificname'] == list_of_list[key], 'Source'] = "Worms"
                        print(f"{index} : {response.status_code}: Worms {list_of_list[key]} ")
                    else:
                        print(f"{index} : {response.status_code}: Worms {list_of_list[key]} - Empty response")

            except ValueError:
                print(f"JSON decode error for {nom}")

            except Exception as e:
                print(f"Error processing response for {nom}: {e}")

        # if empty answer from Worms, prepare table for Itis later on
        elif response.status_code == 204:
            for key in list_of_list:
                print(f"{index} : {response.status_code}: Worms {list_of_list[key]} - No content")

                if itis_usage:
                    data_valid_scientific_name.loc[data_valid_scientific_name['scientificname'] == list_of_list[key], 'Source'] = "Itis"

                    try: 
                        response3 = requests.get(f"https://www.itis.gov/ITISWebService/jsonservice/searchByScientificName?srchKey={list_of_list[key]}")
                        if response3.status_code == 200:
                            response4 = response3.json()

                            # entre les valeurs du serveur dans le tableau
                            if response4['scientificNames'] != [None]:
                                data_valid_scientific_name.loc[data_valid_scientific_name['scientificname'] == list_of_list[key], 'TaxonID'] = response4['scientificNames'][0]['tsn']
                                data_valid_scientific_name.loc[data_valid_scientific_name['scientificname'] == list_of_list[key], 'Valid_TaxonID'] = response4['scientificNames'][0]['tsn']
                                data_valid_scientific_name.loc[data_valid_scientific_name['scientificname'] == list_of_list[key], 'Valid_Name'] = response4['scientificNames'][0]['combinedName']
                                data_valid_scientific_name.loc[data_valid_scientific_name['scientificname'] == list_of_list[key], 'LSID'] = "urn:lsid:itis.gov:itis_tsn:" + response4['scientificNames'][0]['tsn']
                                print(f"{index} : {response3.status_code}: Itis  {list_of_list[key]}")
                            else:
                                print(f"{index} : {response3.status_code}: Itis  {list_of_list[key]} - Empty answer")
                        else:
                            print(f"{index} : {response3.status_code}: Itis  {list_of_list[key]}")

                    except ValueError:
                        print(f"JSON decode error for ITIS request for {list_of_list[key]}")

                    except Exception as e:
                        print(f"Error processing ITIS response for {list_of_list[key]}: {e}")

        else:
            print(f"{index} : {response.status_code}: Worms {nom} - Error response")

        # delay bwt requests
        time.sleep(round(random.uniform(.5,1.5), 1))

    #if itis_usage:
    try:
        data_valid_scientific_name = data_valid_scientific_name.drop(['Source'], axis=1)

    except:
        pass

    # Analysis and tables preparation section
    if value == 'names':
        data_valid_scientific_name = names_analyse(data_valid_scientific_name)
        return data_valid_scientific_name

    if value == 'names_ids':
        data_valid_scientific_name, data_cross_validation = names_ids_analyse(data_valid_scientific_name, data)
        return data_valid_scientific_name, data_cross_validation

    if value == 'names_taxons_ids':
        data_valid_scientific_name, data_cross_validation = names_taxons_ids_analyse(data_valid_scientific_name, data)
        return data_valid_scientific_name, data_cross_validation