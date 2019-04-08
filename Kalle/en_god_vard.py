import numpy as np
import pandas as pd
import sys
import os
import time
import plotly as py
import plotly.graph_objs as go
import collections

# Funktion för att returnera hur mycket ett läns värde skiljer sig från medelvärdet.
# Beräknas olika beroende på om ett högt eller lågt värde eftersöks.
def diff_from_mean(df, period):
    # Kollar om ett högt värde är bra eller dåligt (aim_direction)
    return np.where(df['aim_direction'] == 1 ,df['value'].loc[(df['period_order'] == period)] / (df['value'].loc[(df['period_order'] == period) & (
        df['geo_cat'] == 'RIKET')].mean()), 2 - (df['value'].loc[(df['period_order'] == period)] / (df['value'].loc[(df['period_order'] == period) & (
        df['geo_cat'] == 'RIKET')].mean())))

# Färgkodning för de fem sämsta länen
colors = {'Skåne': 'maroon',
          'Gävleborg': 'gold',
          'Jämtland': 'purple',
          'Västernorrland': 'orange',
          'Norrbotten': 'seagreen'}

'''
Reducerar storleken på källdatan för att slippa processa all data vid varje test

Läser in csvfilen till en dataframe
df = pd.read_csv('en_god_vard.csv', sep=';', encoding='latin1')
# Tar bort onödiga kolumner
df.drop(df.columns[[0,4,8,14,16,17,18]], axis=1, inplace=True)

df.to_pickle('en_god_vard.pickle')
'''

# Läser in reducerade datakällan
df = pd.read_pickle('en_god_vard.pickle')
# Ersätter kommatecken med punkt
df['value'] = df['value'].str.replace(',','.').astype(float)

# Ersätter diverse tecken som inte avkodats ordentligt
df['name_short'] = df['name_short'].str.replace('\x96', '-')
df['question'] = df['question'].str.replace('"', '').str.replace('\x94', '')

# Skapar en lista med alla län och filtrerar sen Dataframen så att bara län kommer med
lan = list(df['geo_cat'].loc[(df['nr_rapp'] == 1)].drop_duplicates())
df = df.loc[(df['geo_cat'].isin(lan))]
lan_kod = pd.DataFrame(df[['geo_cat','cat_code']].drop_duplicates())
lan_kod.to_pickle('lan_kod.pickle')
# Tar bort de sista 10 raderna
df.drop(df.iloc[-10:,:].index, inplace=True, axis=0)

# Sparar de frågor där "totalt" inte finns med i könkolumnen till en egen dataframe
dfspecial = df.loc[(df['nr_rapp'] == 17) & (df['period_order'] == 0)]
dfspecial = dfspecial.append(df.loc[(df['nr_rapp'] == 30) & (df['period_order'] == 0)])
dfspecial = dfspecial.append(df.loc[(df['nr_rapp'] == 46) & (df['period_order'] == 0)])

# Tar bort de rader där könkolumnen inte är "totalt"
df.drop(df[df['sex_all'] != 'Totalt'].index, inplace=True)

# lägger in "specialfallen" i en lista och loopar igenom dem och summerar deras värden till ett totalvärde per län
dflists = []
for i in [17,30,46]:
    dflists.append(dfspecial.loc[(dfspecial['nr_rapp'] == i) & (dfspecial['period_order'] == 0)]) # senaste undersökningen (period_order = 0)
dflists = [dflists[i].groupby(['geo_cat', 'question', 'aim_direction', 'nr_rapp', 'period',
                               'period_order', 'type', 'name_short'], as_index=False)['value'].mean()
           for i in range(len(dflists))]

# Filtrerar df per fråga samt endast den senaste undersökningen (period_order = 0)
dflist = []
for i in df['nr_rapp'].drop_duplicates():
    dflist.append(df[['geo_cat',  'question', 'aim_direction', 'nr_rapp', 'period', 'period_order', 'type',
                             'name_short', 'value']].loc[(df['nr_rapp'] == i) & (df['period_order'] == 0)])

# Grupperar på kategorier
dflist = [dflist[i].groupby(['geo_cat',  'question', 'aim_direction', 'nr_rapp', 'period', 'period_order', 'type',
                             'name_short'], as_index=False)['value'].mean() for i in range(len(dflist))]

# Lägger tillbaka in "specialfallen" på rätt position
dflist.insert(16, dflists[0])
dflist.insert(29, dflists[1])
dflist.insert(45, dflists[2])

# Skepar en ny kolumn som visar hur mycket varje läns resultat skiljer sig från medelvärdet
for i in dflist:
    i.loc[(i['period_order'] == 0), 'diff_from_mean'] = diff_from_mean(i, 0)
    i['diff_from_mean'].replace(0,1, inplace=True)      # Ersätter 0-värden med medelvärdet 1
    i.fillna(1, inplace=True)                           # Ersätter NaN-värden med medelvärdet 1

# Variabel för frågekategorierna
questions_categorized = []
questions = ['Hur mycket betalar vi för hälso- och sjukvården?',
             'Har vi tillgång till hälso- och sjukvård när vi behöver?',
             'Hur väl bidrar hälso- och sjukvården till att hålla oss friska?',
             'Hur är kvaliteten i hälso- och sjukvården vi får?',
             'Blir vi friskare och lever längre?',
             'Hur bidrar hälso- och sjukvården till hållbart god vård?']

# Räknar hur många underfrågor det finns per frågekategori
d = collections.defaultdict(int)
for i in dflist:
    d[i.iloc[1,1]] += 1

# Lägger in dataframes i respektive frågekategori-lista
counter = 0
for i in d.values():
    temp = []
    for j in range(counter, i+counter):                         # Loopar igenom antalet underfrågor per frågekategori
        temp.append(dflist[j][['nr_rapp','diff_from_mean']])    # Lägger till en kolumn med namnet frågenumret samt värdena i "diff_from_mean"
    questions_categorized.append(temp)
    counter += i

# Skapar en ihopslagen dataframe per frågekategori
df_per_question = []
for i in range(len(questions_categorized)):
    tempdf = pd.DataFrame()
    for j in questions_categorized[i]:
        tempdf[j.iloc[1,0]] = j['diff_from_mean']       # Lägger till en kolumn med namnet frågenumret samt värdena i "diff_from_mean"
    df_per_question.append(tempdf)

# Skapar ett index för varje frågekategori som är en summering av hur alla län skiljer sig från medelvärdet i underfrågorna
for dff in df_per_question:
    dff['index'] = (round(dff.sum(axis=1) / len(list(dff)), 3) * 1000).astype(int)
    dff['Län'] = lan
    dff['Color'] = dff['Län'].map(colors).fillna('#1f77b4')
    dff.sort_values(['index'], inplace=True)

# Skapar ett sammanlagt index för alla frågekategorier, ett så kallat mega super index ;)
mega_super_total_index = pd.Series(df_per_question[0]['index'])
for i in range(1, len(df_per_question)):
    mega_super_total_index += df_per_question[i]['index']
mega_super_total_index /= (len(df_per_question))
mega_super_total_indexdf = pd.DataFrame(mega_super_total_index)
mega_super_total_indexdf['Län'] = df_per_question[0]['Län']
mega_super_total_indexdf.sort_values('index', inplace=True)

# Färgar de fem sämst placerade länen
mega_super_total_indexdf['Color'] = mega_super_total_indexdf['Län'].map(colors).fillna('#1f77b4')


dataplots = [go.Bar(x=df['Län'], y=df['index'], marker={'color': df['Color']}) for df in df_per_question]
layout_mega_super_index = dict(xaxis=dict(title='Län'),
                               yaxis=dict(title='Superindex'))
# Printar en graf per frågekategori
for i in range(len(dataplots)):
    fig = go.Figure(data=dataplots[i:1+i], layout=dict(xaxis=dict(title='Län'),
                                                       yaxis=dict(title='Index')))
    py.plotly.plot(fig, filename=questions[i])
fig2 = go.Figure(data=[go.Bar(x=mega_super_total_indexdf['Län'],
                              y=mega_super_total_indexdf['index'],
                              marker={'color': mega_super_total_indexdf['Color']})],
                 layout=layout_mega_super_index)

# Och en för det sammanställda
py.plotly.plot(fig2, filename='en_god_vard_sammanställt')
mega_super_total_indexdf.reset_index(inplace=True)
mega_super_total_indexdf.to_pickle('msti.pickle')