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
df = pd.read_csv('C:\Grupparbete\Dataset\KLARA DATASET\CSV\medarbetarengagemangmotivation.csv', sep = ';')

#Visar alla rubriker och rader i csvfilen
df.head(64)

# Variabel trace skapas med funktionen go.Bar tillsammans med efterfrågade kolumner i X resp Y.
trace = go.Bar(
     x= list(df['Enhetsnamn']),
     y= list(df['Värde']))

# Variabel data skapas för att användas i funktionen go.Figure längre ner.
data = [trace]

# definition av layout för den graf som ska skapas
layout = go.Layout(
    title='Siffrorna visar andelen medarbetare som är motiverade',
)

# använder funktionen go.Figure för att skapa grafer baserat på data och layout
fig = go.Figure(data=data, layout=layout)

# graferna renderas med plotlys offline-plot funktion
py.offline.plot(fig)




