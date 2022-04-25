import dash
import numpy as np
import pandas as pd
from dash import dash_table, html
NaN = np.nan

from validations_bio.basisofrecord_fonction         import basisofrecord_fonction
from validations_bio.datasetid_fonction             import datasetid_fonction
from validations_bio.occurrenceid_fonction          import occurrenceid_fonction
from validations_bio.occurrencestatus_fonction      import occurrencestatus_fonction
from validations_bio.eventdate_fonction             import eventdate_fonction
from validations_bio.decimal_coordinates_fonction   import decimal_coordinates_fonction
from validations_bio.footprintwkt_fonction          import footprintwkt_fonction
from validations_bio.validation_Worms_Itis_fonction import validation_Worms_Itis_fonction
from validations_bio.locationid_function            import AfficheLocationIDOccurrences
from validations_bio.organismQuantity_functions     import AfficheOrgnismQuantityTypeOccurrences, AfficheSiOrganismQuantityEtTypeSontPresent
from validations_bio.validation_Worms_Itis_fonction import validation_Worms_Itis_fonction
from types_analyses_bio.table_format_analysis       import table_format_analysis


def occurence_core_occurence_file(data, colonne_jeu_donnees, nombre_rangees):
    #filtrer les champs présent dans le jeu de données
    col_analyse = {
        'Nom du champ / Field name': ["basisofrecord", "datasetid","decimallatitude", "decimallongitude", "eventdate", "occurrenceid", "occurrencestatus", "scientificname","scientificnameid", "taxonid","footprintwkt","locationID", "organismquantity", "organismquantitytype"],
        'Nécéssaire ou optionnel / Necessary or optionnal': ["Nécéssaire / Necessary","Nécéssaire / Necessary","Nécéssaire / Necessary","Nécéssaire / Necessary","Nécéssaire / Necessary","Nécéssaire / Necessary","Nécéssaire / Necessary","Nécéssaire / Necessary","Nécéssaire / Necessary","Nécéssaire / Necessary","Optionnel / Optionnal","Optionnel / Optionnal","Optionnel / Optionnal","Optionnel / Optionnal"],
        'Présence/Presence ou/or absence':[NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN]}

    colonne_analyse = pd.DataFrame(data=col_analyse)
    colonne_analyse['Présence/Presence ou/or absence'] = colonne_analyse['Nom du champ / Field name'].isin(colonne_jeu_donnees)
    colonne_analyse['Présence/Presence ou/or absence'].replace(False,"Absent", inplace=True)
    colonne_analyse['Présence/Presence ou/or absence'].replace(True,"Présent/Present", inplace=True)
    colonne_analyse.sort_values(by='Présence/Presence ou/or absence', ascending=True, inplace=True)

    # liste de champs présents dans le jeu de données
    liste_format = colonne_analyse[colonne_analyse['Présence/Presence ou/or absence']=='Présent/Present']['Nom du champ / Field name']
    liste_format = list(liste_format)
    
    # liste des différences entre le tableau des champs nécessaires/optionnels présents et tous les champs présents dans le jeu de données
    colonnes_extra = list(set(colonne_jeu_donnees) - set(liste_format))
    colonnes_extra = sorted(colonnes_extra)
    if len(colonnes_extra) == 0:
        colonnes_extra = ['aucune colonne / no column']

    #section servant à rouler les fonctions de validation pour les colonnes présentes dans le jeu de données
    liste_affichage = []
    if 'basisofrecord' in liste_format:
        basisofrecord = basisofrecord_fonction(data)
        liste_affichage.append(basisofrecord)

    if 'datasetid' in liste_format:
        datasetid = datasetid_fonction(data)
        liste_affichage.append(datasetid)

    if 'decimallatitude' in liste_format and 'decimallongitude' in liste_format:
        latitude_longitude = decimal_coordinates_fonction(data)
        liste_affichage.append(latitude_longitude)

    if 'eventdate' in liste_format:
        eventdate = eventdate_fonction(data)
        liste_affichage.append(eventdate)

    if 'occurrenceid' in liste_format:
        occurenceid = occurrenceid_fonction(data)
        liste_affichage.append(occurenceid)  

    if 'occurrencestatus' in liste_format:
        occurrencestatus = occurrencestatus_fonction(data)
        liste_affichage.append(occurrencestatus)   
    
    if 'scientificname' in liste_format and 'scientificnameid' not in liste_format :
        tableau_valid_nom_scientifique  = validation_Worms_Itis_fonction(data, 'names')
        liste_affichage.append(tableau_valid_nom_scientifique)

    if 'scientificname' in liste_format and 'scientificnameid' in liste_format and 'occurrenceid' in liste_format:
        
        if 'taxonrank' in colonnes_extra:
            tableau_valid_nom_scientifique, tableau_valid_croisee = validation_Worms_Itis_fonction(data, 'names_taxons_ids')
            liste_affichage.append(tableau_valid_nom_scientifique)
            liste_affichage.append(tableau_valid_croisee)
        
        if 'taxonrank' not in colonnes_extra:
            tableau_valid_nom_scientifique, tableau_valid_croisee = validation_Worms_Itis_fonction(data, 'names_ids')
            liste_affichage.append(tableau_valid_nom_scientifique)
            liste_affichage.append(tableau_valid_croisee)
    
    if 'footprintwkt' in liste_format:
        footprintwkt = footprintwkt_fonction(data)
        liste_affichage.append(footprintwkt)

    if 'locationid' in liste_format:
        locationid = AfficheLocationIDOccurrences(data)
        liste_affichage.append(locationid) 

    # S'assure que si organismquantitytype ou organismquantity est présent, l'autre l'est aussi
    organismQuantityEtType = AfficheSiOrganismQuantityEtTypeSontPresent(liste_format)
    if organismQuantityEtType is not None:
        liste_affichage.append(organismQuantityEtType) 

    if 'organismquantitytype' in liste_format:
        organismquantitytype = AfficheOrgnismQuantityTypeOccurrences(data)
        liste_affichage.append(organismquantitytype) 


    # section retournant le tableau d'analyse du format ainsi que les retours des fonctions des champs présents
    return table_format_analysis(colonne_analyse, colonnes_extra, liste_affichage, nombre_rangees)
