import numpy as np
import pandas as pd
import sys
import os
import time
import plotly.offline as pyofl
import plotly.graph_objs as go
import collections

def diff_from_mean(df, period):
    return np.where(df['aim_direction'] == 1 ,df['value'].loc[(df['period_order'] == period)] / (df['value'].loc[(df['period_order'] == period) & (
        df['geo_cat'] == 'RIKET')].mean()), 2 - (df['value'].loc[(df['period_order'] == period)] / (df['value'].loc[(df['period_order'] == period) & (
        df['geo_cat'] == 'RIKET')].mean())))

# pd.set_option('display.max_columns', 22)
# pd.set_option('display.width', 2500)

# Läser in csvfilen till en dataframe
# df = pd.read_csv('en_god_vard.csv', sep=';', encoding='latin1')
# # Tar bort onödiga kolumner
# df.drop(df.columns[[0,4,8,14,16,17,18]], axis=1, inplace=True)
#
# df.to_pickle('en_god_vard.pickle')
t1 = time.time()
df = pd.read_pickle('en_god_vard.pickle')
# Ersätter kommatecken med punkt
df['value'] = df['value'].str.replace(',','.').astype(float)

# Ersätter diverse tecken som inte avkodats ordentligt
df['name_short'] = df['name_short'].str.replace('\x96', '-')
df['question'] = df['question'].str.replace('"', '').str.replace('\x94', '')

# Skapar en lista med alla län och filtrerar sen Dataframen så att bara län kommer med
lan = list(df['geo_cat'].loc[(df['nr_rapp'] == 1)].drop_duplicates())
df = df.loc[(df['geo_cat'].isin(lan))]

# Tar bort de sista 10 raderna
df.drop(df.iloc[-10:,:].index, inplace=True, axis=0)
dfspecial = df.loc[(df['nr_rapp'] == 17) & (df['period_order'] == 0)]
dfspecial = dfspecial.append(df.loc[(df['nr_rapp'] == 30) & (df['period_order'] == 0)])
dfspecial = dfspecial.append(df.loc[(df['nr_rapp'] == 46) & (df['period_order'] == 0)])


df.drop(df[df['sex_all'] != 'Totalt'].index, inplace=True)


dflists = []
for i in [17,30,46]:
    dflists.append(dfspecial.loc[(dfspecial['nr_rapp'] == i) & (dfspecial['period_order'] == 0)])
dflists = [dflists[i].groupby(['geo_cat', 'question', 'aim_direction', 'nr_rapp', 'period', 'period_order', 'type', 'name_short'],
                            as_index=False)['value'].mean() for i in range(len(dflists))]
# Filtrerar df per fråga samt endast den senaste undersökningen (period_order = 0)
dflist = []
for i in df['nr_rapp'].drop_duplicates():
    dflist.append(df.loc[(df['nr_rapp'] == i) & (df['period_order'] == 0)])

dflist = [dflist[i].groupby(['geo_cat', 'question', 'aim_direction', 'nr_rapp', 'period', 'period_order', 'type', 'name_short'],
                            as_index=False)['value'].mean() for i in range(len(dflist))]
dflist.insert(16, dflists[0])
dflist.insert(29, dflists[1])
dflist.insert(45, dflists[2])

for i in dflist:
    i.loc[(i['period_order'] == 0), 'diff_from_mean'] = diff_from_mean(i, 0)
    i['diff_from_mean'].replace(0,1, inplace=True)
    i.fillna(1, inplace=True)
questions_categorized = []
questions = ['Hur mycket betalar vi för hälso- och sjukvården?',
             'Har vi tillgång till hälso- och sjukvård när vi behöver?',
             'Hur väl bidrar hälso- och sjukvården till att hålla oss friska?',
             'Hur är kvaliteten i hälso- och sjukvården vi får?',
             'Blir vi friskare och lever längre?',
             'Hur bidrar hälso- och sjukvården till hållbart god vård?']

d = collections.defaultdict(int)
for i in dflist:
    d[i.iloc[1,1]] += 1
counter = 0
for i in d.values():
    temp = []
    for j in range(counter, i+counter):
        temp.append(dflist[j][['nr_rapp','diff_from_mean']])
    questions_categorized.append(temp)
    counter += i

df_per_question = []
for i in range(len(questions_categorized)):
    tempdf = pd.DataFrame()
    for j in questions_categorized[i]:
        tempdf[j.iloc[1,0]] = j['diff_from_mean']
    df_per_question.append(tempdf)

for dff in df_per_question:
    dff['index'] = (round(dff.sum(axis=1) / len(list(dff)), 3) * 1000).astype(int)
    dff['Län'] = lan

mega_super_total_index = pd.Series(df_per_question[0]['index'])
for i in range(1, len(df_per_question)):
    mega_super_total_index += df_per_question[i]['index']
mega_super_total_index /= (len(df_per_question))
mega_super_total_indexdf = pd.DataFrame(mega_super_total_index)
mega_super_total_indexdf['Län'] = lan
mega_super_total_indexdf.sort_values('index', inplace=True)
dataplots = [go.Bar(x=df['Län'], y=df['index']) for df in df_per_question]
layout = dict(width=1250, height=850, title='Mega Super Index')
for i in range(len(dataplots)):
    fig = go.Figure(data=dataplots[i:1+i], layout=dict(width=1250, height=850, title=questions[i]))
    pyofl.plot(fig, filename='q'+str(i) + '.html')
fig2 = go.Figure(data=[go.Bar(x=mega_super_total_indexdf['Län'], y=mega_super_total_indexdf['index'])], layout=layout)
pyofl.plot(fig2, layout)
t2=time.time()
print(t2-t1)



# # x = 0
# # y = 0
# # for i in len(df_per_question):
# #     pyofl.plot(data[x:x+i], filename=fragor[y].replace(' ', '_') + '.html')
# #     x += i
# #     y += 1
#
