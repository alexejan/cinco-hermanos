# import av moduler
import sys
import plotly.offline
import plotly.graph_objs as go
import pandas as pd
import plotly.plotly as py 

# ser till att rätt encoding sätts för stdout
sys.stdout.reconfigure(encoding='UTF-8')

# läser in data från .csv-fil och lagrar denna data i data frame
skl_data = pd.read_csv(r"C:\Users\steblo\Desktop\Nackademin\Dropbox\BI-relaterade programspråk\Grupparbete\Kod\cinco-hermanos\VC_statistik.csv", sep=';', encoding='UTF-8')

# instantiering av en data frame som segmenterar data från den csv-fil som har lästs in. mer specifikt används .loc för att dels filtrera fram data baserat på rader där ett visst villkor uppfylls (en specifik indikator), och i andra hand de kolumner som ska läsas in
df = skl_data.loc[skl_data['År'] == 2017, ['Storlek på vårdcentralerna', 'Landsting', 'Offentlig regi', 'Privat regi', 'Kombinerat']]

# ersätter tomma celler med 0
df.fillna(0, inplace=True)

# skapar en beräknad kolumn som summerar alla värden baserat på gruppering av regioner.
df['Summa per region'] = df.groupby(['Landsting'])['Kombinerat'].transform('sum')

# instantierar en lista dit ny kolumndata ska läggas in
new_column = []

# for-lopp som itererar genom hela data framen df baserat på dess index och som delar antalet vårdcentraler för en viss typ med summa per region
for i in df.index:
    new_column.append((df.loc[i]['Kombinerat']/df.loc[i]['Summa per region'])*100)

# skapar en ny beräknad kolumn baserat på listan från for-loopen ovan
df['Andel'] = new_column

# sorterar alla värden i data frame efter landsting för att grafen ska visas sorterat efter landsting
df.sort_values('Landsting', ascending=True, inplace = True)

# skriver ut data frame till fil (med syfte att dumpa data i händelse att data frame kan återanvändas på annan plats) 
# df.to_csv('Dump av ekonomistatistik.csv')

# nya data frames som innehåller dataunderlag för de grafer som ska skapas
df1 = df.loc[df['Storlek på vårdcentralerna'] == 'Vårdcentraler med 1 läkare', ['Landsting', 'Andel']]
df2 = df.loc[df['Storlek på vårdcentralerna'] == 'Vårdcentraler med 2 läkare', ['Landsting', 'Andel']]
df3 = df.loc[df['Storlek på vårdcentralerna'] == 'Vårdcentraler med 3 läkare', ['Landsting', 'Andel']]
df4 = df.loc[df['Storlek på vårdcentralerna'] == 'Vårdcentraler med 4 läkare', ['Landsting', 'Andel']]
df5 = df.loc[df['Storlek på vårdcentralerna'] == 'Vårdcentraler med 5-10 läkare', ['Landsting', 'Andel']]
df6 = df.loc[df['Storlek på vårdcentralerna'] == 'Vårdcentraler med fler än 10 läkare', ['Landsting', 'Andel']]
df7 = df.loc[df['Storlek på vårdcentralerna'] == 'Uppgift om storlek saknas', ['Landsting', 'Andel']]

# variabler som innehåller dataunderlag för de grafer som ska skapas
data1 = go.Bar(x=df1['Landsting'], y=df1['Andel'], name='Vårdcentraler med 1 läkare') 
data2 = go.Bar(x=df2['Landsting'], y=df2['Andel'], name='Vårdcentraler med 2 läkare')
data3 = go.Bar(x=df3['Landsting'], y=df3['Andel'], name='Vårdcentraler med 3 läkare')
data4 = go.Bar(x=df4['Landsting'], y=df4['Andel'], name='Vårdcentraler med 4 läkare')
data5 = go.Bar(x=df5['Landsting'], y=df5['Andel'], name='Vårdcentraler med 5-10 läkare')
data6 = go.Bar(x=df6['Landsting'], y=df6['Andel'], name='Vårdcentraler med fler än 10 läkare')
data7 = go.Bar(x=df7['Landsting'], y=df7['Andel'], name='Uppgift om storlek saknas')

# definition av layout för den graf som ska skapas 
layout = go.Layout(xaxis = {'title':'Regioner och landsting (2017)'}, yaxis = {'title': 'Andel av total'}, barmode = 'stack', margin = dict(b = 100), showlegend = True)

# använder funktionen go.Figure för att skapa graf baserat på dataunderlaget samt layout
figure = go.Figure(data = [data1, data2, data3, data4, data5, data6, data7], layout = layout)

# graf renderas med plotlys offline-plot funktion (används i testsyfte)
# plotly.offline.plot(figure, filename ='stacked_VC.html')

# graf renderas med plotlys onine-plot funktion
py.plot(figure, filename = 'Typ av vårdcentraler')