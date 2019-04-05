# -*- coding: utf-8 -*-
"""
Created on Fri Mar 29 09:32:48 2019

@author: Anders Rönnbäck
"""
# Läser in lämpliga bibliotek i Python och döper om dessa till förkortningar.
import plotly as py
import plotly.graph_objs as go

import pandas as pd
import numpy as np

# Läser in csv-filen och skapar en variabel df
df = pd.read_csv('C:\Grupparbete\Dataset\KLARA DATASET\CSV\medarbetarengagemangsammanslagning.csv', sep = ';')

#Visar alla rubriker och rader i csvfilen
df.head(65)
df.sort_values("Ledarskapsindex",ascending=False,inplace=True)

# Variabel trace skapas med funktionen go.Bar tillsammans med efterfrågade kolumner i X resp Y.
trace1 = go.Bar(
     x= list(df['Enhetsnamn']),
     y= list(df['Ledarskapsindex'])

,
    name='Ledarskapsindex'
     )

trace2 = go.Bar(
     x= list(df['Enhetsnamn']),
     y= list(df['Motivationsindex'])

,
    name='Motivationsindex'
     )

trace3 = go.Bar(
     x= list(df['Enhetsnamn']),
     y= list(df['Styrningsindex'])

,
    name='Styrningsindex'
     )

# Variabel data skapas för att användas i funktionen go.Figure längre ner.
data = [trace1,trace2,trace3]

# definition av layout för den graf som ska skapas
layout = go.Layout(
    title='Siffrorna visar hur medarbetarna ser på engagemanget',
)

# använder funktionen go.Figure för att skapa grafer baserat på data och layout
fig = go.Figure(data=data, layout=layout)


# graferna renderas med plotlys offline-plot funktion
py.offline.plot(fig)


