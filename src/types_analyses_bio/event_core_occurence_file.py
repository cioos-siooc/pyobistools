import numpy as np
import pandas as pd
from dash import dash_table, html
NaN = np.nan

from validations_bio.basisofrecord_fonction         import basisofrecord_fonction
from validations_bio.occurrenceid_fonction          import occurrenceid_fonction
from validations_bio.occurrencestatus_fonction      import occurrencestatus_fonction
from validations_bio.validation_Worms_Itis_fonction import validation_Worms_Itis_fonction
from validations_bio.eventid_fonction               import eventid_fonction
from validations_bio.organismQuantity_functions     import AfficheOrgnismQuantityTypeOccurrences, AfficheSiOrganismQuantityEtTypeSontPresent
from types_analyses_bio.table_format_analysis       import table_format_analysis


def event_core_occurence_file(data, colonne_jeu_donnees, nombre_rangees):
    #filtrer les champs présent dans le jeu de données
    col_analyse = {
        'Nom du champ / Field name': ["basisofrecord", "eventid","occurrenceid","occurrencestatus", "scientificname", "scientificnameid", "taxonid", "organismquantity", "organismquantitytype"],
        'Nécéssaire ou optionnel / Necessary or optionnal': ["Nécéssaire / Necessary","Nécéssaire / Necessary","Nécéssaire / Necessary","Nécéssaire / Necessary","Nécéssaire / Necessary","Nécéssaire / Necessary","Nécéssaire / Necessary","Optionnel / Optionnal","Optionnel / Optionnal"],
        'Présence/Presence ou/or absence':[NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN]}

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

    if 'eventid' in liste_format:
        eventid = eventid_fonction(data)
        liste_affichage.append(eventid)

    if 'occurenceid' in liste_format:
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

    # S'assure que si organismquantitytype ou organismquantity est présent, l'autre l'est aussi
    # Ensure that if organismquantitytype or organismquantity is present, the other is too
    organismQuantityEtType = AfficheSiOrganismQuantityEtTypeSontPresent(liste_format)
 
    if organismQuantityEtType is not None:
        liste_affichage.append(organismQuantityEtType) 

    if 'organismquantitytype' in liste_format:
        organismquantitytype = AfficheOrgnismQuantityTypeOccurrences(data)
        liste_affichage.append(organismquantitytype) 


    # section retournant le tableau d'analyse du format ainsi que les retours des fonctions des champs présents
    # this section returns the format analysis table as well as the function outputs for field presence
    return table_format_analysis(colonne_analyse, colonnes_extra, liste_affichage, nombre_rangees)
