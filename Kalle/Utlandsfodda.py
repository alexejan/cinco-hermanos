import numpy as np
import pandas as pd
import os
import sys
import pickle
sys.stdout.reconfigure(encoding='utf-8')
'''Jobbig källdatafil :( Används senare till beräkning av CNI'''
df = pd.read_csv('2018.csv', sep=';', skiprows=4)   # Läser in csvfil och hoppar över de fyra första raderna
temp=[]
df.fillna(0, inplace=True)  # Sätter NaN-värden till 0 för att kunna summera
df = (df[df.columns[[0, 2, 3, 14, 18, 22, 23]]])    # Tar bara med kolumner där utlandsfödda i förbestämda länder hittas
a = list(df)

df = df.loc[(df['Kön'] =='Båda könen') & (df['Län'].str.endswith('län'))]   # Tar endast med där raderna innehåller båda könen samt är ett län
for i in range(4):
    df[a[3+i]] = df[a[3+i]].str.replace(' ', '').astype(int)                # Sätter ihop tusentalssiffror med ett mellanslag till utan och omvandlar datatypen till int

df['Utlandsfödda'] = (df['Unnamed: 14']) + df['Unnamed: 18'] + df['Unnamed: 22'] + df['Unnamed: 23']    # Summerar alla olika landskategorier
df = (df[df.columns[[0, -1]]])  # Tar med första och sista kolumnen
df.set_index('Län', inplace=True)   # Sätter länskolumnen till index
df.to_pickle('utlandsfodda.pickle')