# import av moduler
import sys
import plotly.offline
import plotly.graph_objs as go
import pandas as pd
import plotly.plotly as py 

# ser till att rätt encoding sätts för stdout
sys.stdout.reconfigure(encoding='UTF-8')

# läser in data från .csv-fil och lagrar denna data i data frame
skl_data = pd.read_csv(r"C:\Users\steblo\Desktop\Nackademin\Dropbox\BI-relaterade programspråk\Grupparbete\Kod\cinco-hermanos\Kostnad per invånare per specialitet.csv", sep=';', encoding='UTF-8')

# instantiering av en data frame som segmenterar data från den csv-fil som har lästs in. mer specifikt används .loc för att dels filtrera fram data baserat på rader där ett visst villkor uppfylls (en specifik indikator), och i andra hand de kolumner som ska läsas in
df = skl_data.loc[(skl_data['Huvudområde'] == 'Hälso- och sjukvård') & (skl_data['Område'] == 'Primärvård') & (skl_data['År'] == 2017) & (skl_data['Underkonto'] == 'Nettokostnad exkl läkemedel') & (skl_data['Delområde'] != 'Sluten primärvård') & (skl_data['Delområde'] != 'Primärvårdsansluten hemsjukvård') & (skl_data['Delområde'] != 'Övrig primärvård') , ['Delområde', 'Region', 'Värde']]

# ersätter kommatecken med punkt för att decimalvärden ska tolkas rätt, samt omvandlar värdena till float
df['Värde'] = (df['Värde'].replace(',','.', regex=True).astype(float))

# skapar en beräknad kolumn som summerar alla värden baserat på gruppering av regioner.
df['Summa per region'] = df.groupby(['Region'])['Värde'].transform('sum')

# sorterar värden efter ovanstående beräkning
df.sort_values('Summa per region', ascending=True, inplace = True)

# skriver ut data frame till fil (med syfte att dumpa data i händelse att data frame kan återanvändas på annan plats) 
df.to_csv('Dump av ekonomistatistik.csv')

# nya data frames som innehåller dataunderlag för de grafer som ska skapas
df1 = df.loc[df['Delområde'] == 'Allmänläkarvård inkl. jourverksamhet', ['Region', 'Värde']]
df2 = df.loc[df['Delområde'] == 'Barnhälsovård', ['Region', 'Värde']]
df3 = df.loc[df['Delområde'] == 'Mödrahälsovård', ['Region', 'Värde']]
df4 = df.loc[df['Delområde'] == 'Sjukgymnastik och Arbetsterapi', ['Region', 'Värde']]
df5 = df.loc[df['Delområde'] == 'Sjuksköterskevård inkl. jourverksamhet', ['Region', 'Värde']]

# variabler som innehåller dataunderlag för de grafer som ska skapas
data1 = go.Bar(x=df1['Region'], y=df1['Värde'], name='Allmänläkarvård inkl. jourverksamhet') 
data2 = go.Bar(x=df1['Region'], y=df2['Värde'], name='Barnhälsovård')
data3 = go.Bar(x=df1['Region'], y=df3['Värde'], name='Mödrahälsovård')
data4 = go.Bar(x=df1['Region'], y=df4['Värde'], name='Sjukgymnastik och Arbetsterapi')
data5 = go.Bar(x=df1['Region'], y=df5['Värde'], name='Sjuksköterskevård inkl. jourverksamhet')

# definition av layout för den graf som ska skapas 
layout = go.Layout(xaxis = {'title':'Regioner och landsting (2017)'}, yaxis = {'title': 'Nettokostnad per invånare exkl. läkemedel (kronor)'}, barmode = 'stack', margin= dict(b = 100), showlegend = True)

# använder funktionen go.Figure för att skapa graf baserat på dataunderlaget samt layout
figure = go.Figure(data = [data1, data2, data3, data4, data5], layout=layout)

# graf renderas med plotlys offline-plot funktion (används i testsyfte)
plotly.offline.plot(figure, filename ='stacked.html')

# graf renderas med plotlys onine-plot funktion
# py.plot(figure, filename = 'Ekonomistatistik')

