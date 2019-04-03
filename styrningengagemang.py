# -*- coding: utf-8 -*-
"""
Created on Fri Mar 29 09:32:48 2019

@author: Anders Rönnbäck
"""

import plotly as py
import plotly.graph_objs as go

import pandas as pd
import numpy as np

df = pd.read_csv('C:\Grupparbete\Dataset\KLARA DATASET\CSV\medarbetarengagemangstyrning.csv', sep = ';')
df.head(64)

trace = go.Bar(
     x= list(df['Enhetsnamn']),
     y= list(df['Värde']))

data = [trace]
layout = go.Layout(
    title='Siffrorna visar andelen medarbetare som tycker att styrningen är bra',
)

fig = go.Figure(data=data, layout=layout)

py.offline.plot(fig)


