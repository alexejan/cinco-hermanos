# -*- coding: utf-8 -*-
"""
Created on Fri Mar 29 14:06:03 2019

@author: Anders Rönnbäck
"""

import plotly as py
import plotly.graph_objs as go

import pandas as pd
import numpy as np

df = pd.read_csv('C:\Grupparbete\Dataset\KLARA DATASET\CSV\Sammanstallning modeller.csv', sep = ';')
df.head(70)

trace = go.Bar(
     x= list(df['Landsting/Region']),
     y= list(df['Ersättning läkarbesök listad annan vc']))


data = [trace]
layout = go.Layout(
    title='Sammanställning av ersättning till VC inom samma län',
)

fig = go.Figure(data=data, layout=layout)

py.offline.plot(fig)