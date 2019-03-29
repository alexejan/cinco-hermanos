import sys
import os
import numpy as np
import pandas as pd
import colorlover as cl
import plotly as py
import plotly.graph_objs as go

def bins(kolumn):
    interval = (np.max(kolumn) - np.min(kolumn)) / 9
    bin = []
    for i in kolumn:
        for j in range(len(colors)):
            if i <= np.min(kolumn) + interval * (1 + j):
                bin.append(j)
                break
    return bin

colors = cl.scales['9']['div']['RdBu']
colors.reverse()

# Lägger till kolumner som är andelar i procent
befolkning_csv = pd.read_csv('befolkning.csv')
befolkning = befolkning_csv.iloc[:,:-1]
cni = pd.DataFrame(befolkning['Län'])

cni['<5 år'] = round((befolkning['Befolkning 0-4'] / befolkning['Befolkning Total'] * 100), 2)
cni['Utlandsfödda (Urval länder)'] = round((befolkning['Utlandsfödda urval'] / befolkning['Befolkning Total'] * 100), 2)
cni['Ensamboende 65+'] = round((befolkning['Ensamboende 65+'] / befolkning['Befolkning Total'] * 100), 2)
cni['Ensamstående föräldrar'] = round((befolkning['Ensamstående föräldrar'] / befolkning['Befolkning Total'] * 100), 2)
cni['Nyinflyttad'] = round((befolkning['Nyinflyttad'] / befolkning['Befolkning Total'] * 100), 2)
cni['Arbetslös'] = round((befolkning['Arbetslös'] / befolkning['Befolkning 16-64'] * 100), 2)
cni['Lågutbildad'] = round((befolkning['Lågutbildad'] / befolkning['Befolkning 25-64'] * 100), 2)


columns_avg = []
for column in cni.iloc[:, 1:]:
    columns_avg.append(round(np.mean(cni[column]), 2))

# cni['Cnisumma'] = cni.sum(axis=1)
# cni['CNI'] = round(cni['Cnisumma'] / cni['Cnisumma'].mean(axis=0), 2)
# cni.drop(['Cnisumma'], axis=1, inplace=True)

cni_norm = pd.DataFrame(cni['Län'])
counter = 0
for i in cni.iloc[:, 1:8]:
    cni_norm[i] = cni[i] / columns_avg[counter]
    counter += 1

cni['CNInorm'] = round(cni_norm.iloc[:, 1:].sum(axis=1) / len(list(cni)[1:]), 2)
cni.sort_values(by=['CNInorm'], inplace=True)

rank_0_9 = []
for i in list(cni.iloc[:, 1:]):
    rank_0_9.append(bins(cni[i]))


trace = go.Table(
    columnwidth = [2.8,1,1,1,1,1,1,1],
    header = dict(
        values = list(cni),
        line = dict(color = 'white'),
        fill = dict(color = 'white'),
        align = 'center',
        font = dict(color = 'black', size = 12)
    ),
    cells = dict(
        values = [cni['Län'], cni['<5 år'], cni['Utlandsfödda (Urval länder)'], cni['Ensamboende 65+'],
                  cni['Ensamstående föräldrar'], cni['Nyinflyttad'], cni['Arbetslös'], cni['Lågutbildad'],
                  cni['CNInorm']],
        align = 'center',
        fill = dict(
            color = [['white'], np.array(colors)[rank_0_9[0]], np.array(colors)[rank_0_9[1]],
                                np.array(colors)[rank_0_9[2]], np.array(colors)[rank_0_9[3]],
                                np.array(colors)[rank_0_9[4]], np.array(colors)[rank_0_9[5]],
                                np.array(colors)[rank_0_9[6]], np.array(colors)[rank_0_9[7]]]),
        line = dict(
            color = [['white'], np.array(colors)[rank_0_9[0]], np.array(colors)[rank_0_9[1]],
                                np.array(colors)[rank_0_9[2]], np.array(colors)[rank_0_9[3]],
                                np.array(colors)[rank_0_9[4]], np.array(colors)[rank_0_9[5]],
                                np.array(colors)[rank_0_9[6]], np.array(colors)[rank_0_9[7]]])
        )
    )

layout = dict(width=1250, height=1200)
fig = dict(data=[trace], layout=layout)
cni.insert(0, column='Länskod', value=befolkning_csv['Länskod'].apply(lambda x: '{0:0>2}'.format(x)))
cni.reset_index(inplace=True)
cni.index.name = 'Index'
cni.drop(cni.iloc[:, 0:1], axis=1, inplace=True)
cni.to_csv('cni.csv')
py.offline.plot(fig)