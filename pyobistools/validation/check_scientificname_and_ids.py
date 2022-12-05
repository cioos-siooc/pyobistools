import asyncio
import time

import httpx
import numpy as np
import pandas as pd
import requests

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
    data_valid_scientific_name = data_valid_scientific_name.drop_duplicates(subset=[
                                                                            "scientificname"])
    data_valid_scientific_name.reset_index(drop=True, inplace=True)
    data_valid_scientific_name.replace(NaN, "", inplace=True)

    # get rid of sp, sp. and spp. suffix because Worms database does not support them
    liste_noms_pre_modif, liste_noms, liste_noms_sans_suffix, liste_noms_sp, liste_noms_sp_point, liste_noms_spp, liste_noms_spp_point = function_suffix_removal(
        data_valid_scientific_name)

    # fonction async
    timeout = httpx.Timeout(10)

    async def info_noms(index, nom):
        async with httpx.AsyncClient(timeout=timeout) as client:
            list_of_list = function_add_suffix(
                nom, liste_noms_sans_suffix, liste_noms_sp, liste_noms_sp_point, liste_noms_spp, liste_noms_spp_point)
            # print(list_of_list)
            # print(list_of_list.keys())

            response = await client.get(f"https://www.marinespecies.org/rest/AphiaRecordsByName/{nom}?like=false&marine_only=false&offset=1")

            # si réponse positive de Worms, fait:
            if response.status_code == 200:
                for key in list_of_list:
                    # print(list_of_list[key])
                    response2 = response.json()
                    data_valid_scientific_name.loc[data_valid_scientific_name['scientificname']
                                                   == list_of_list[key], 'TaxonID'] = response2[0]['AphiaID']
                    data_valid_scientific_name.loc[data_valid_scientific_name['scientificname']
                                                   == list_of_list[key], 'Status'] = response2[0]['status']
                    data_valid_scientific_name.loc[data_valid_scientific_name['scientificname']
                                                   == list_of_list[key], 'Unacceptreason'] = response2[0]['unacceptreason']
                    data_valid_scientific_name.loc[data_valid_scientific_name['scientificname']
                                                   == list_of_list[key], 'Taxon_Rank'] = response2[0]['rank']
                    data_valid_scientific_name.loc[data_valid_scientific_name['scientificname']
                                                   == list_of_list[key], 'Valid_TaxonID'] = response2[0]['valid_AphiaID']
                    data_valid_scientific_name.loc[data_valid_scientific_name['scientificname']
                                                   == list_of_list[key], 'Valid_Name'] = response2[0]['valid_name']
                    data_valid_scientific_name.loc[data_valid_scientific_name['scientificname']
                                                   == list_of_list[key], 'LSID'] = response2[0]['lsid']
                    data_valid_scientific_name.loc[data_valid_scientific_name['scientificname']
                                                   == list_of_list[key], 'Source'] = "Worms"
                    print(f"{index} : {response.status_code}: Worms {list_of_list[key]} ")

            # if empty answer from Worms, prepare table for Itis later on
            if response.status_code == 204:
                list_of_list = function_add_suffix(
                    nom, liste_noms_sans_suffix, liste_noms_sp, liste_noms_sp_point, liste_noms_spp, liste_noms_spp_point)
                for key in list_of_list:
                    data_valid_scientific_name.loc[data_valid_scientific_name['scientificname']
                                                   == list_of_list[key], 'Source'] = "Itis"
                    print(f"{index} : {response.status_code}: Worms {list_of_list[key]} ")

    # definition of async calls sequence

    async def main(liste_noms):
        task_list = []
        for index, nom in enumerate(liste_noms):
            task_list.append(info_noms(index, nom))
        await asyncio.gather(*task_list)

    # call and timing of the async calls
    start_time = time.monotonic()
    asyncio.run(main(liste_noms))
    end_time = time.monotonic()

    # for empty answers from WORMS, try ITIS if option is selected
    if itis_usage:
        s = requests.Session()
        for row in data_valid_scientific_name.index:
            if data_valid_scientific_name.loc[row, 'Source'] == 'Itis':
                response3 = s.get(
                    f"https://www.itis.gov/ITISWebService/jsonservice/searchByScientificName?srchKey={data_valid_scientific_name.loc[row, 'scientificname']}")
                if response3.status_code == 200:
                    response4 = response3.json()

                    # entre les valeurs du serveur dans le tableau
                    if response4['scientificNames'] != [None]:
                        #   for key in list_of_list:
                        data_valid_scientific_name.loc[row,
                                                       'TaxonID'] = response4['scientificNames'][0]['tsn']
                        data_valid_scientific_name.loc[row,
                                                       'Valid_TaxonID'] = response4['scientificNames'][0]['tsn']
                        data_valid_scientific_name.loc[row,
                                                       'Valid_Name'] = response4['scientificNames'][0]['combinedName']
                        data_valid_scientific_name.loc[row, 'LSID'] = "urn:lsid:itis.gov:itis_tsn:" + \
                            response4['scientificNames'][0]['tsn']
                        print(
                            f"{row} : {response3.status_code}: Itis {data_valid_scientific_name.loc[row, 'scientificname']}")

                    else:
                        print(
                            f"{row} : {response3.status_code}: Itis {data_valid_scientific_name.loc[row, 'scientificname']} - Empty answer")

                else:
                    print(
                        f"{row} : {response3.status_code}: Itis {data_valid_scientific_name.loc[row, 'scientificname']}")

    data_valid_scientific_name = data_valid_scientific_name.drop(['Source'], axis=1)

    # Analysis and tables preparation section
    if value == 'names':
        data_valid_scientific_name = names_analyse(data_valid_scientific_name)
        return data_valid_scientific_name

    if value == 'names_ids':
        data_valid_scientific_name, data_cross_validation = names_ids_analyse(
            data_valid_scientific_name, data)
        return data_valid_scientific_name, data_cross_validation

    if value == 'names_taxons_ids':
        data_valid_scientific_name, data_cross_validation = names_taxons_ids_analyse(
            data_valid_scientific_name, data)
        return data_valid_scientific_name, data_cross_validation

    print(f"Time Taken:{end_time - start_time}")
