import numpy as np
import pandas as pd
import time
import plotly as py
import plotly.graph_objs as go
import pickle
import geopandas as gpd
import json

def bins(kolumn):
    interval = (np.max(kolumn) - np.min(kolumn)) / len(colors)      # Delar upp intervallet i lika många delar som antalet färger i färgskalan
    bin = []
    for i in kolumn:                                                # Itererar genom varje värde i kolumnen som skickas in i funktionen
        for j in range(len(colors)):                                # Loopar lika många gånger som antalet färger i färgskalan "colors"
            if i <= np.min(kolumn) + interval * (1 + j):            # kollar om värdet är <= minsta värdet + intervallet definierat i första raden
                bin.append(j)                                       # Om inte, adderar ytterligare ett intervall
                break                                               # Avslutar loop så fort ett intervall passar in
    return bin
# Läser in CNI-data
cni = pd.read_pickle('cnii.pickle')

# Öppnar källdatan med polygoner, figurer som visar hur länen ska ritas upp
with open("karta.geojson") as geofile:
    geojson_layer = json.load(geofile)

# Öppnar samma fil igen men formatterad som en geopandas DataFrame
gdf = gpd.read_file('karta.geojson')

# Färgskala som används till att färgkoda celler efter rankning
colors = ['rgb(105, 149, 228)', 'rgb(133, 170, 233)', 'rgb(163, 191, 238)', 'rgb(193, 211, 243)', 'rgb(223, 232, 249)',
          'rgb(242, 242, 242)', 'rgb(250, 223, 223)', 'rgb(246, 195, 194)', 'rgb(242, 167, 166)', 'rgb(238, 139, 137)',
          'rgb(234, 112, 109)']

# Rankar CNI-värdet mellan länen sinsemellan
rank = bins(cni.iloc[:, 9])
lan = list(cni['Länskod'])
cni_lan = list(zip(lan, rank))
cni_lan.sort()
lan_colors = np.array(colors)[rank]

# Skapar centroider (mittpunkten i polygonerna) för varje län
gdf['centroid'] = gdf['geometry'].centroid

# Extraherar longitud samt latitud för användning som markörer till till länen
xpoint, ypoint = [], []
for i in gdf['geometry']:
    xpoint.append(i.centroid.x)
    ypoint.append(i.centroid.y)
xypoint = list(zip(xpoint,ypoint))

# Skapar en dataframe för koppla markörerna till rätt län
df = pd.DataFrame(pd.Series(xypoint))
df['Länkod'] = [l for l, k in cni_lan]
cni = cni[['Länskod', 'Län', 'CNInorm']]
map_df = pd.merge(df, cni[['Län', 'CNInorm']], left_on=[df['Länkod']], right_on=[cni['Länskod']]).iloc[:,1:]

# Använder en token för att kunna använda sig utav MapBox API.
mapbox_key = 'pk.eyJ1Ijoicmluem8iLCJhIjoiY2p0ZXJ0cW11MDZ4YjN5cnJzb2kxaTVwMyJ9.cMA0hmYnxcbPLmzPQdjb4Q'

# Text som visas över respektive län. Sammanslagning av länsnamn och CNI-värdet
hovertext = map_df['Län'].str.cat(': ' + map_df['CNInorm'].astype('str'))

# Skapar ett "lager" för varje län med respektive färgkodning
layoutlayer = []
for i in range(len(lan)):
    layoutlayer.append(dict(
        visible = True,
        sourcetype = 'geojson',
        source = geojson_layer['features'][i],
        type = 'fill',
        color = colors[cni_lan[i][1]]
))
# Lägger till länens lon och lat-mittpunkter på kartan
data = go.Scattermapbox(
    lon=xpoint,
    lat=ypoint,
    hoverinfo='text',
    hovertext=hovertext
)
layout = go.Layout(
    margin=dict(t=0,l=0,r=0,b=0),
    mapbox=dict(
        layers=layoutlayer,
        accesstoken=mapbox_key,
        zoom=3,
        center=dict(lat=62.50,lon=17
        ),
    ),
)
# Aaaaand Print!
fig = dict(data=[data], layout=layout)
py.plotly.plot(fig, filename='map')