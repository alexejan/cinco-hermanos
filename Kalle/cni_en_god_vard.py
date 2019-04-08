import pickle
import pandas as pd
import numpy as np
import plotly as py
import plotly.graph_objs as go
import colorlover as cl

# Läser in CNI-datan samt MegaSuperTotalIndex (Sammanställning av "En god vård" :) )
cni = pd.read_pickle('cnii.pickle')
msti = pd.read_pickle('msti.pickle')

# Läser in län och länskoder
lan_kod = pd.read_pickle('lan_kod.pickle')

# Joinar msti med län och länskoder för att kunna joina dataframen med cni-indexdataframen eftersom samma region skrivs på olika sätt
msti_lan = msti.merge(lan_kod['cat_code'], left_on='Län', right_on=lan_kod['geo_cat'], how='inner')
msti_lan['cat_code'] = msti_lan['cat_code'].apply(lambda x: '{0:0>2}'.format(x))
super_index = cni.merge(msti_lan['index'], left_on='Länskod', right_on=msti_lan['cat_code'])

# Beräkningar för att se hur länen skiljer sig från medelvärdet
super_index['index'] = super_index['index'] / 1000
super_index['mega_index'] = (2 - super_index['index'] + super_index['CNInorm']) / 2

# Sorterar efter det nyskapade värdet mega index. Summering av "En god vård" samt CNI-index
super_index.sort_values('mega_index', inplace=True)
super_index.reset_index(inplace=True)
super_index.drop('level_0', axis=1)
super_index.index.name = 'Index'
super_index.to_csv('super_index_cni.csv')
# a = super_index[['mega_index', 'Län']]
super_index['mega_index'] = (super_index['mega_index'] -1) * 100   # Visar index som procent över/under 0
super_index['color'] = np.where(super_index['mega_index'] > 0, '#2ca02c', '#d62728')    # Grön färg om värdet är över 0, annars röd färg

# Aaaaaand print!
trace = go.Bar(x=super_index['Län'], y=super_index['mega_index'], marker=dict(color=super_index['color']))
fig = go.Figure(data=[trace], layout=dict(width=900, height=600))
py.plotly.plot(fig, filename = 'CNI_samt_en_god_vard')

# trace1 = go.Bar(x=a['Län'], y=a['mega_index'])
# fig1 = go.Figure(data=[trace1], layout=dict(width=900, height=600))
# py.offline.offline.plot(fig)
