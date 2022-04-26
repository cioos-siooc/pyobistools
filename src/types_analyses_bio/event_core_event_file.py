import numpy as np
import pandas as pd
from dash import dash_table, html
NaN = np.nan

from validations_bio.datasetid_fonction            import datasetid_fonction
from validations_bio.eventid_fonction              import eventid_fonction
from validations_bio.eventdate_fonction            import eventdate_fonction
from validations_bio.decimal_coordinates_fonction  import decimal_coordinates_fonction
from validations_bio.footprintwkt_fonction         import footprintwkt_fonction
from validations_bio.locationid_function           import AfficheLocationIDOccurrences
from types_analyses_bio.table_format_analysis      import table_format_analysis

def event_core_event_file(data, colonne_jeu_donnees, nombre_rangees):
    #filtrer les champs présent dans le jeu de données et créer un tableau
    #filters the fields present in the dataset and creates a table
    col_analyse = {
        'Nom du champ / Field name': ["datasetid","decimallatitude","decimallongitude","eventdate","eventid","footprintwkt","locationid"],
        'Nécéssaire ou optionnel / Necessary or optionnal': ["Nécéssaire / Necessary","Nécéssaire / Necessary","Nécéssaire / Necessary","Nécéssaire / Necessary","Nécéssaire / Necessary","Nécéssaire / Necessary","Optionnel / Optionnal"],
        'Présence/Presence ou/or absence':[NaN,NaN,NaN,NaN,NaN,NaN,NaN]}

    colonne_analyse = pd.DataFrame(data=col_analyse)
    colonne_analyse['Présence/Presence ou/or absence'] = colonne_analyse['Nom du champ / Field name'].isin(colonne_jeu_donnees)
    colonne_analyse['Présence/Presence ou/or absence'].replace(False,"Absent", inplace=True)
    colonne_analyse['Présence/Presence ou/or absence'].replace(True,"Présent/Present", inplace=True)
    colonne_analyse.sort_values(by='Présence/Presence ou/or absence', ascending=True, inplace=True)

    # liste de champs présents dans le jeu de données
    #lists the fields present in the dataset
    liste_format = colonne_analyse[colonne_analyse['Présence/Presence ou/or absence']=='Présent/Present']['Nom du champ / Field name']
    liste_format = list(liste_format)
    
    # liste des différences entre le tableau des champs nécessaires/optionnels présents et tous les champs présents dans le jeu de données
    # lists the differences between the table of required/optional fields AND the fields give in the dataset
    colonnes_extra = list(set(colonne_jeu_donnees) - set(liste_format))
    colonnes_extra = sorted(colonnes_extra)
    if len(colonnes_extra) == 0:
        colonnes_extra = ['aucune colonne / no column']

    #section servant à rouler les fonctions de validation pour les colonnes présentes dans le jeu de données
    #this section tests the validation functions for the columns given in the dataset
    liste_affichage = []
    if 'datasetid' in liste_format:
        datasetid = datasetid_fonction(data)
        liste_affichage.append(datasetid)
    
    if 'decimallatitude' in liste_format and 'decimallongitude' in liste_format:
        latitude_longitude = decimal_coordinates_fonction(data)
        liste_affichage.append(latitude_longitude)

    if 'eventdate' in liste_format:
        eventdate = eventdate_fonction(data)
        liste_affichage.append(eventdate)

    if 'eventid' in liste_format:
        eventid  = eventid_fonction(data)
        liste_affichage.append(eventid)
    
    if 'footprintwkt' in liste_format:
        footprintwkt = footprintwkt_fonction(data)
        liste_affichage.append(footprintwkt)

    if 'locationid' in liste_format:
        locationid = AfficheLocationIDOccurrences(data)
        liste_affichage.append(locationid) 
    

    # section retournant le tableau d'analyse du format ainsi que les retours des fonctions des champs présents
    # section returns the format analysis table as well as the outputs from the field presence functions
    return table_format_analysis(colonne_analyse, colonnes_extra, liste_affichage, nombre_rangees)

