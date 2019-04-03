import numpy as np
import pandas as pd
import sys
import os
import time
import plotly.offline as pyofl
import plotly.graph_objs as go

# pd.set_option('display.max_columns', 8)
# pd.set_option('display.width', 1000)

# Läser in csvfilen till en dataframe
df = pd.read_csv('en_god_vard.csv', sep=';', encoding='iso8859-1')
#  Tar bort onödiga kolumner
df.drop(df.columns[[0,1,2,4,8,9,10,11,14,17,18]], axis=1, inplace=True)

# Ersätter kommatecken med punkt
df['value'] = df['value'].str.replace(',','.').astype(float)

# Tar bort rader med data för hela riket
df.drop(df.loc[df['geo_cat'] == 'RIKET'].index, inplace=True)

# Skapar en lista med alla frågeställningar
q = list(df['name_short'].drop_duplicates())

# Används tillfälligt för att lista och numrera alla frågor för att lättare kunna välja frågor
# for count, fraga in enumerate(list(q)):
#     print(count, fraga)

# Väljer ut frågor
fragor = []
fragor.extend((q[1], q[3], q[4], q[46], q[47]))

# Skapar en dataframe per fråga samt filtrerar rader baserat på fråga, båda könen samt från 2016 och fram
dflist = []
for i in fragor:
    dflist.append(df.loc[(df['name_short'] == i) & (df['sex_all'] == 'Totalt') & (df['period'] >= '2016')])

# Grupperar dataframen per fråga, tid och län på medelvärdet (om det hade varit uppdelat i exempelvis månadsvis)
dflist = [dflist[i].groupby(['geo_cat', 'period', 'name_short'], as_index=False).mean()
          for i in range(len(dflist))]


data = []
loopcounter = []
for i in range(len(dflist)):
    counter = 0
    a = list(set(dflist[i]['period']))
    a.sort()
    for year in a:
        x = dflist[i]['geo_cat'].loc[dflist[i]['period'] == year]
        y = dflist[i]['value'].loc[dflist[i]['period'] == year]
        data.append(go.Bar(x=x, y=y, name=year))
        counter += 1
    loopcounter.append(counter)

x = 0
y = 0
for i in loopcounter:
    pyofl.plot(data[x:x+i], filename=fragor[y].replace(' ', '_') + '.html')
    x += i
    y += 1
