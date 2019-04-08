import sys
import os
import numpy as np
import pandas as pd
import colorlover as cl
import plotly as py
import plotly.graph_objs as go

# Funktion för att ranka länen sinsemellan till användning av färgkodning

def bins(kolumn):
    bininterval = (np.max(kolumn) - np.min(kolumn)) / len(colors)      # Delar upp intervallet i lika många delar som antalet färger i färgskalan
    bin = []
    for i in kolumn:                             # Itererar genom varje värde i kolumnen som skickas in i funktionen
        for j in range(len(colors)):             # Loopar lika många gånger som antalet färger i färgskalan "colors"
            if i <= np.min(kolumn) + bininterval * (1 + j):  # kollar om värdet är <= minsta värdet + intervallet definierat i första raden
                bin.append(j)                                # Om inte, adderar ytterligare ett intervall
                break                                        # Avslutar loop
    return bin

# Färgskala som används till att färgkoda celler efter rankning
colors = ['rgb(105, 149, 228)', 'rgb(133, 170, 233)', 'rgb(163, 191, 238)', 'rgb(193, 211, 243)', 'rgb(223, 232, 249)',
          'rgb(242, 242, 242)', 'rgb(250, 223, 223)', 'rgb(246, 195, 194)', 'rgb(242, 167, 166)', 'rgb(238, 139, 137)',
          'rgb(234, 112, 109)']



# Lägger till kolumner som är befolkningen i olika kategorier
befolkning_csv = pd.read_csv('befolkning.csv')
befolkning = befolkning_csv.iloc[:,:-1]
cni = pd.DataFrame(befolkning['Län'])

# Skapar kolumner som andelar i procent i förhållande till folkmängden eller undergrupper
cni['<5 år'] = round((befolkning['Befolkning 0-4'] / befolkning['Befolkning Total'] * 100), 2)
cni['Utlandsfödda (Urval länder)'] = round((befolkning['Utlandsfödda urval'] / befolkning['Befolkning Total'] * 100), 2)
cni['Ensamboende 65+'] = round((befolkning['Ensamboende 65+'] / befolkning['Befolkning Total'] * 100), 2)
cni['Ensamstående föräldrar'] = round((befolkning['Ensamstående föräldrar'] / befolkning['Befolkning 16-64'] * 100), 2)
cni['Nyinflyttad'] = round((befolkning['Nyinflyttad'] / befolkning['Befolkning Total'] * 100), 2)
cni['Arbetslös'] = round((befolkning['Arbetslös'] / befolkning['Befolkning 16-64'] * 100), 2)
cni['Lågutbildad'] = round((befolkning['Lågutbildad'] / befolkning['Befolkning 25-64'] * 100), 2)

# Lista för medelvärdet för respektive kolumn
columns_avg = []
for column in cni.iloc[:, 1:]:
    columns_avg.append(round(np.mean(cni[column]), 2))

# Dataframe där andelskolumnerna har beräknats i förhållande till medelvärdet, för att kunna användas till beräkningen av index
cni_norm = pd.DataFrame(cni['Län'])
counter = 0
for i in cni.iloc[:, 1:8]:      # För varje kolumn...
    cni_norm[i] = cni[i] / columns_avg[counter]    # Dela den på respektive medelvärde
    counter += 1

# Lägger till ny beräknad kolumn för sammanställningen av CNI-indexet.
cni['CNInorm'] = round(cni_norm.iloc[:, 1:].sum(axis=1) / len(list(cni)[1:]), 2)
cni.sort_values(by=['CNInorm'], inplace=True)       # Sorterar efter CNI

# Rankar alla län sinsemellan för varje kolumn
rank = []
for i in list(cni.iloc[:, 1:]):
    rank.append(bins(cni[i]))

# Lista med alla tabellrubriker
table_headers = ['','<5 år',
                 'Utlandsfödda (Urval länder)',
                 'Ensamboende 65+',
                 'Ensamstående föräldrar',
                 'Nyinflyttad',
                 'Arbetslös',
                 'Lågutbildad',
                 'CNI']
# Skapar en plotlytrace för användning till att plotta tabellen
trace = go.Table(
    columnwidth = [1.7,1,1,1,1,1,1,1],      # Ändrar första kolumnens bredd
    header = dict(
        values = table_headers,             # Sätter in värden till kolumnrubriker
        line = dict(color = 'White'),
        fill = dict(color = 'White'),
        align = ['right','center'],
        font = dict(color = 'black', size = 12),
        height = 15
    ),
    cells = dict(
        height = 25,
        font = dict(size = 13),
        values = [cni['Län'], cni['<5 år'], cni['Utlandsfödda (Urval länder)'], cni['Ensamboende 65+'],
                  cni['Ensamstående föräldrar'], cni['Nyinflyttad'], cni['Arbetslös'], cni['Lågutbildad'],
                  cni['CNInorm']],
        align = ['right', 'center'],
        fill = dict(            # Kopplar färgerna till länsdatan och färgar cellerna därefter
            color = ['White',   np.array(colors)[rank[0]], np.array(colors)[rank[1]],
                                np.array(colors)[rank[2]], np.array(colors)[rank[3]],
                                np.array(colors)[rank[4]], np.array(colors)[rank[5]],
                                np.array(colors)[rank[6]], np.array(colors)[rank[7]]]),
        line = dict(
            color = ['White',   np.array(colors)[rank[0]], np.array(colors)[rank[1]],
                                np.array(colors)[rank[2]], np.array(colors)[rank[3]],
                                np.array(colors)[rank[4]], np.array(colors)[rank[5]],
                                np.array(colors)[rank[6]], np.array(colors)[rank[7]]])
        )
    )
# Aaaand print
layout = dict(margin=dict(l=10, t=10, b=0))
fig = dict(data=[trace], layout=layout)
py.plotly.plot(fig, filename='CNI')

# Nedan användes till andra filer för lite test samt en god vård + cni = superindex :)
# cni.insert(0, column='Länskod', value=befolkning_csv['Länskod'].apply(lambda x: '{0:0>2}'.format(x)))
# cni.reset_index(inplace=True)
# cni.index.name = 'Index'
# cni.drop(cni.iloc[:, 0:1], axis=1, inplace=True)
# cni.to_csv('cni.csv')
# cni.to_pickle('cnii.pickle')