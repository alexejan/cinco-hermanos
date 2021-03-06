# -*- coding: utf-8 -*-
"""
Created on Fri Mar 29 14:06:03 2019

@author: Anders Rönnbäck
"""
# Läser in lämpliga bibliotek i Python och döper om dessa till förkortningar.
import plotly as py
import plotly.graph_objs as go

import pandas as pd
import numpy as np

# Läser in csv-filen och skapar en variabel df
df = pd.read_csv('C:\Grupparbete\Dataset\KLARA DATASET\CSV\Sammanstallning modeller.csv', sep = ';')

#Visar alla rubriker och rader i csvfilen
df.head(70)

# Variabel trace skapas med funktionen go.Bar tillsammans med efterfrågade kolumner i X resp Y.
trace1 = go.Bar(
     x= list(df['Landsting/Region']),
     y= list(df['Kostnad för läkarbesök på annan vc'])

,
    name='Kostnad för läkarbesök på annan vc'
     )

trace2 = go.Bar(
     x= list(df['Landsting/Region']),
     y= list(df['Kostnad läkarbesök på nationell taxa'])
,
    name='Kostnad läkarbesök på nationell taxa'
     )


# Variabel data skapas för att användas i funktionen go.Figure längre ner.
data = [trace1,trace2]

# definition av layout för den graf som ska skapas
layout = go.Layout(
    title='Sammanställning av kostnader',
)

# använder funktionen go.Figure för att skapa grafer baserat på data och layout
fig = go.Figure(data=data, layout=layout)

# graferna renderas med plotlys offline-plot funktion
py.offline.plot(fig)