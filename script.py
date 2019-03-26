# import json
# import requests
import sys

import plotly.plotly as py
import plotly.graph_objs as go
# import plotly.figure_factory as FF

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

sys.stdout.reconfigure(encoding='UTF-8')

# sparar filnamn som en variabel
healthreport_2018 = r"C:\Users\steblo\Desktop\Nackademin\Dropbox\BI-relaterade programspråk\Grupparbete\Excelbilaga till Hälso- och sjukvårdsrapporten 2018.xlsx"

# använder funktionen ExcelFile för att läsa in en excel-fil och lagrar det i en variabel
xl = pd.ExcelFile(healthreport_2018)

# använder funktionen parse för at läsa in en specifik flik från den excel.fil som ska läsas in
data = xl.parse('Data samtliga områden')

# instantiering av tre st data frames som segmenterar data från det excel-data som lästs in. mer specifikt används .loc för att dels filtrera fram data baserat på rader där ett visst villkor uppfylls, och i andra hand de kolumner som ska läsas in
df1 = data.loc[data['Indikatornamn'] =='Positivt helhetsintryck hos patienter som besökt en primärvårdsmottagning', ['Landsting och regioner', 'Värde']]
df2 = data.loc[data['Indikatornamn'] =='Primärvårdens tillgänglighet per telefon', ['Landsting och regioner', 'Värde']]
df3 = data.loc[data['Indikatornamn'] =='Positiv upplevelse av tillgänglighet hos patienter som besökt en primärvårdsmottagning', ['Landsting och regioner', 'Värde']]

# index för samtliga tre data frames ovan sätts till 'Landsting och regioner' för att det ska återspeglas i de tabeller som ska genereras. Mer specifikt värdena för kolumnen landsting och regioner återspeglas i x-axeln på de tabeller som ska ritas upp
df1.set_index('Landsting och regioner',inplace=True)
df2.set_index('Landsting och regioner',inplace=True)
df3.set_index('Landsting och regioner',inplace=True)

# avänder funktionen .plot för att skapa bar charts för de tre data frames som har instantierats tidigare
df1.plot(kind='bar', legend = 'Procent', alpha = 0.75, rot = 45, title = 'Positivt helhetsintryck hos patienter som besökt en primärvårdsmottagning')
df2.plot(kind='bar', legend = 'Procent', alpha = 0.75, rot = 45, title = 'Primärvårdens tillgänglighet per telefon')
df3.plot(kind='bar', legend = 'Procent', alpha = 0.75, rot = 45, title = 'Positiv upplevelse av tillgänglighet hos patienter som besökt en primärvårdsmottagning')

# ritar upp de tre graferna ovan
plt.show()

""" for i, j in df.iterrows(): 
    print(i, j) 
    print() """ 

# data_table = FF.create_table(df.head(3))

# py.plot(data_table, filename='data-table')

# läser in data från en csv-fil och sparar det i en variabel
# data = pd.read_csv('Datalista En god vard.csv',sep=";",encoding='iso8859-10')

# plottar en grafisk tabell baserat på variabeln data table
# py.plot(data_table, filename='data-table')

""" from pyscbwrapper import SCB

scb = SCB('sv')
scb.go_down('HS')
print(scb.info()) """
