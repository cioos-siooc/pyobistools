import numpy as np
from dash import dcc, html
NaN = np.nan
import plotly.graph_objects as go
from dash import dcc, html
import geopandas as gpd
# import dash_leaflet as dl
# import dash_leaflet.express as dlx
NaN = np.nan


def footprintwkt_fonction(data):
    data = data.rename(columns=str.lower)
    data_travail = data 

    list_features = data_travail.drop_duplicates('footprintwkt')
    list_features = list_features.reset_index()

    # Polygons list
    liste_large_polygones = list_features[list_features["footprintwkt"].str.contains('POLYGON')]
    geometries = gpd.GeoSeries.from_wkt(liste_large_polygones["footprintwkt"])
    liste_large_polygones = []
    liste_large_polygones = [gpd.GeoSeries(geometries).__geo_interface__ ]

    # Linestrings list
    liste_large_linestrings = list_features[list_features["footprintwkt"].str.contains('LINESTRING')]
    geometries = gpd.GeoSeries.from_wkt(liste_large_linestrings["footprintwkt"])
    liste_large_linestrings = []
    liste_large_linestrings = [gpd.GeoSeries(geometries).__geo_interface__ ]

    # Points list
    liste_large_points = list_features[list_features["footprintwkt"].str.contains('POINT')]
    geometries = gpd.GeoSeries.from_wkt(liste_large_points["footprintwkt"])
    liste_large_points = []
    liste_large_points = [gpd.GeoSeries(geometries).__geo_interface__ ]

    def function_show_polygons(noms, liste_de_WKT):
        fig = go.Figure(go.Scattermapbox())
        fig.update_layout(
            mapbox = {'style': 'stamen-terrain',
            'center': { 'lon': -62, 'lat': 48},'zoom': 4, 
            'layers': [{'source': layer,
                        'type': 'fill', 
                        'below': 'traces', 
                        'color': 'royalblue'} for layer in liste_de_WKT]},
                        margin = {'l':0, 'r':0, 'b':0, 't':0},)
        return html.Div([
            html.H6("Carte des objects / Objects map: "+noms+":"),
            dcc.Graph(figure=fig),
            html.P(""),
            ])
    
    def function_show_lines(noms, liste_de_WKT):
        fig = go.Figure(go.Scattermapbox(marker = {'size': 10}))
        fig.update_layout(
            mapbox = {'style': 'stamen-terrain',
            'center': { 'lon': -62, 'lat': 48},'zoom': 4, 
            'layers': [{'source': layer,
                        'type': 'line', 
                        'below': 'traces', 
                        'color': 'royalblue'} for layer in liste_de_WKT]},
                        margin = {'l':0, 'r':0, 'b':0, 't':0},)
        return html.Div([
            html.H6("Carte des objects / Objects map: "+noms+":"),
            dcc.Graph(figure=fig),
            html.P(""),
            ])

    def function_show_points(noms, liste_de_WKT):
        fig = go.Figure(go.Scattermapbox())
        fig.update_layout(
            mapbox = {'style': 'stamen-terrain',
            'center': { 'lon': -62, 'lat': 48},'zoom': 4, 
            'layers': [{'source': layer,
                        'below': 'traces', 
                        'color': 'royalblue'}  for layer in liste_de_WKT ]},
                        margin = {'l':0, 'r':0, 'b':0, 't':0},)
        return html.Div([
            html.H6("Carte des objects / Objects map: "+noms+":"),
            dcc.Graph(figure=fig),
            html.P(""),
            ])
        # return html.Div([
        #     dl.Map([
        #         dl.TileLayer(),
        #         dl.GeoJSON(data = liste_de_WKT , cluster=True),], 
        #         center=(45, -65), zoom=11, style={'width': '100%', 'height': '50vh', 'margin': "auto", "display": "block"}),
        #         ])


    list_maps = []
    if len(liste_large_polygones[0]['features']) != 0:   
        list_maps.append(function_show_polygons("'Polygon' et/and 'MultiPolygon'", liste_large_polygones))

    if len(liste_large_linestrings[0]['features']) != 0:
        list_maps.append(function_show_lines("'LineString' et/and 'MultiLineString'", liste_large_linestrings))

    if len(liste_large_points[0]['features']) != 0:
        list_maps.append(function_show_points("'Point' et/and 'MultiPoint'", liste_large_points))


    list_footprintwkt = ["Les différents objets du champ 'footprintWKT' sont représentées sur des cartes géographiques.",
    "Lien vers référence: https://dwc.tdwg.org/terms/#dwc:footprintWKT"]
    
    return html.Div([

        html.H4("Champ/Field 'footprintWKT':"),
        html.Div(children=[list_maps[i] for i in range(len(list_maps))]),

        html.Details([
        html.Summary("Info sur/on 'footprintWKT'"),
        html.Ul([html.Li(x) for x in list_footprintwkt]),

        ]),
        
        html.P(""),

        ]) 
     
        