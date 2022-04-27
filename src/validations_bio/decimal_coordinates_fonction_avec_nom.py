import numpy as np
import pandas as pd
from dash import dash_table, dcc, html
import plotly.graph_objects as go
from dash import dcc, html
NaN = np.nan


def decimal_coordinates_fonction_avec_nom(data, colonne1, colonne2, colonne3):
    data1 = data.rename(columns=str.lower)

    colonne1 = colonne1.lower()
    colonne2 = colonne2.lower()
    colonne3 = colonne3.lower()

    
    data1.astype({colonne1: 'float64'}).dtypes
    print(data1[colonne1].dtypes)
    
    # obtenir les valeurs qui ne sont pas dans les limites données des latitudes et longitudes
    # get the values that are not within the given bounds for latitude and longitude
    latitudes_non_valides = data1.loc[(data1[colonne1].gt(90)) | (data1[colonne1].lt(-90)) ]
    longitudes_non_valides = (data1.loc[(data1[colonne2].gt(180)) | (data1[colonne2].lt(-180))]) 
    frames = [latitudes_non_valides, longitudes_non_valides]
    coordonees_non_valides = pd.concat(frames)

        # on garde les colonnes de coordonnées et la colonne d'id et on se débarasse des duplicata
        # keep the coordiante columns and the id column and remove the duplicates
    latitude_colonne  =  coordonees_non_valides.columns.get_loc(colonne1)
    longitude_colonne =  coordonees_non_valides.columns.get_loc(colonne2)
    coordonees_non_valides = coordonees_non_valides.iloc[:,[0,latitude_colonne, longitude_colonne]]
    coordonees_non_valides.drop_duplicates(inplace=True)

    # obtenir les valeurs de latitudes et de longitudes entre -90 et 90 degrés et -180 et 180 degrés
    # get the latitude and longitude values between -90 and 90 / -180 and 180 degrees
    coordonnees_valides = data1[data1[colonne1].between(-90,90) & data1[colonne2].between(-180,180)]

    def afficher_tableau_coordo_non_valides(coordonees_non_valides):
       
        return html.Div([
            dash_table.DataTable(
                data=coordonees_non_valides.to_dict('records'),id={'type': 'coordonees_non_valides'},
                columns=[{'name': ["Coordonnées non valides / Invalid coordinates", i], 'id': i} for i in coordonees_non_valides.columns],
                sort_action='native', filter_action='native', editable=False, row_deletable=False,
                style_header={'backgroundColor': 'rgb(0, 173, 239)','color': 'white', 'textAlign': 'center'},
                style_table={'height': '375','width':'50%', 'overflowY': 'auto'},
                style_cell={'textAlign': 'center','whiteSpace': 'normal','height': 'auto','lineHeight': '15px'},
                export_format="csv",
                merge_duplicate_headers=True,
                export_headers='display'),

            html.P(''),

            ])
    
    def afficher_phrase_coordo_valides(coordonees_non_valides):
        un = "Toutes les latitudes sont entre -90 et 90 degrés et toutes les longitudes sont entre -180 et 180 degrés."
        deux = "All latitudes are betweeen -90 et 90 degrees and all longitudes are between -180 and 180 degrees."
        liste_item = [un, deux]

        return html.Div([
            html.Ul([html.Li(x) for x in liste_item]),

        ])

    liste_affichage1 = []
    if len(coordonees_non_valides) != 0:
        liste_affichage1.append(afficher_tableau_coordo_non_valides(coordonees_non_valides))

    if len(coordonees_non_valides) == 0:
        liste_affichage1.append(afficher_phrase_coordo_valides(coordonees_non_valides))

    # affichage de la carte
    # print the map
    centre_long =.5*(max(np.asarray(np.float64(coordonnees_valides[colonne2]).tolist())) + min(np.asarray(np.float64(coordonnees_valides[colonne2]).tolist())))
    centre_lat = .5*(max(np.asarray(np.float64(coordonnees_valides[colonne1]).tolist())) + min(np.asarray(np.float64(coordonnees_valides[colonne1]).tolist())))
    height = max(np.asarray(np.float64(coordonnees_valides[colonne1]).tolist())) - min(np.asarray(np.float64(coordonnees_valides[colonne1]).tolist()))
    width = max(np.asarray(np.float64(coordonnees_valides[colonne2]).tolist())) -  min(np.asarray(np.float64(coordonnees_valides[colonne2]).tolist()))
    area = height * width

    zoom = np.interp(x=area,
                    xp=[0.0005,   .02,   .05,  30,  350,   3500],
                    fp=[12,        9.5,    6,     4,   2,     1])
    print('centre lat: ', centre_lat) 
    print('centre lon: ', centre_long) 
    print('aire / area: ', area)
    print('zoom : ', zoom)

    fig = go.Figure(go.Scattermapbox(
        lon = np.asarray(np.float64(coordonnees_valides[colonne2]).tolist()), lat = np.asarray(np.float64(coordonnees_valides[colonne1]).tolist()),
            mode='markers', 
            marker = { 'size': 7, 'color': "rgb(16, 40, 54)", 'opacity': 0.8 },
            text=coordonnees_valides[colonne3]))
    
    fig.update_layout(
                mapbox = {'style': "open-street-map", 
                    'center': {'lon': centre_long, 'lat': centre_lat},
                    'zoom': zoom
                },
                showlegend = False,
                margin = {'l':0, 'r':0, 'b':0, 't':0}, 
                )

         
    return html.Div([

        
        html.Div(children=[liste_affichage1[i] for i in range(len(liste_affichage1))]),
        html.H6("Coordonnées géographiques / Geographic coordinates:"),
        dcc.Graph(figure=fig),
    
        ])
        
        

         
     
        