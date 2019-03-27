import sys
import plotly.plotly as py
import plotly.offline as pyof
import plotly.graph_objs as go
import pandas as pd

sys.stdout.reconfigure(encoding='UTF-8')

# sparar filnamn som en variabel
healthreport_2018 = r"C:\Users\steblo\Desktop\Nackademin\Dropbox\BI-relaterade programspråk\Grupparbete\Excelbilaga till Hälso- och sjukvårdsrapporten 2018.xlsx"
healthcare_in_numbers = r"C:\Users\steblo\Desktop\Nackademin\Dropbox\BI-relaterade programspråk\Grupparbete\HC_in_numbers.csv"

# använder funktionen ExcelFile för att läsa in en excel-fil och lagrar det i en variabel
xl = pd.ExcelFile(healthreport_2018)

# läser in en CSV-fil och lagrar det i en variabel
vis = pd.read_csv(healthcare_in_numbers, sep=";", encoding='UTF-8', decimal=",")

# använder funktionen parse för at läsa in en specifik flik från den excel.fil som ska läsas in
data = xl.parse('Data samtliga områden')


def get_health_data(string_var, data, y_name):
    # instantiering av en data frame som segmenterar data från det excel-data som lästs in. mer specifikt används .loc för att dels filtrera fram data baserat på rader där ett visst villkor uppfylls, och i andra hand de kolumner som ska läsas in
    df = data.loc[data['Indikatornamn'] == string_var, ['Landsting och regioner', 'Värde']]
    
    # variabel som innehåller dataunderlag för den graf som ska skapas
    data = go.Bar(x=df['Landsting och regioner'], y=df['Värde'], name= string_var)
    
    # definition av layout för den graf som ska skapas 
    layout = go.Layout(title=string_var, xaxis={'title':'Regioner'}, yaxis={'title':y_name})
    
    # använder funktionen go.Figure för att skapa grafer baserat på data och layout
    figure = go.Figure(data=[data],layout=layout)
    
    # graferna renderas med plotlys online-plot funktion
    pyof.plot(figure, filename = string_var + ".html")


def get_vis_data(string_var, data, y_name):
    # instantiering av en data frame som segmenterar data från den csv-fil som lästs in. mer specifikt används .loc för att dels filtrera fram data baserat på rader där ett visst villkor uppfylls, och i andra hand de kolumner som ska läsas in
    df = data.loc[data['Titel'] == string_var, ['Enhetsnamn', 'Mätperiod', 'Värde']]
    
    # ersätter komma-tecken med punkt för att värden ska tolkas rätt, samt omvandlar värdena till float
    df['Värde'] = (df['Värde'].replace(',','.', regex=True).astype(float))
    
    # instantiering av tre st nya data frames med ett urval för de olika åren som ska undersökas
    df15 = df.loc[df['Mätperiod'] == '2015', ['Enhetsnamn', 'Värde']]
    df16 = df.loc[df['Mätperiod'] == '2016', ['Enhetsnamn', 'Värde']]
    df17 = df.loc[df['Mätperiod'] == '2017', ['Enhetsnamn', 'Värde']]

    # variabler som innehåller dataunderlag för de grafer som ska skapas
    data15 = go.Bar(x=df15['Enhetsnamn'], y=df15['Värde'], name='2015')
    data16 = go.Bar(x=df16['Enhetsnamn'], y=df16['Värde'], name='2016')
    data17 = go.Bar(x=df17['Enhetsnamn'], y=df17['Värde'], name='2017')

    # definition av layout för den graf som ska skapas 
    layout = go.Layout(title=string_var, xaxis={'title':'Regioner och landsting'}, yaxis={'title':y_name}, barmode='group')

    # använder funktionen go.Figure för att skapa graf baserat på data och layout
    figure = go.Figure(data = [data15, data16, data17], layout=layout)

    # grafen renderas med plotlys online-plot funktion
    pyof.plot(figure, filename = string_var  + ".html")

# variabler som ska användas i anrop av funktion för att ge namn till y-axel
procent = 'Andel positiva svar från patienter (%)'
antal = 'Antal per 1000 invånare'


# anrop av funktion get_health_data för specifika frågeställningar
get_health_data('Positivt helhetsintryck hos patienter som besökt en primärvårdsmottagning', data, procent)
get_health_data('Förtroende för vård- eller hälsocentral', data, procent)
get_health_data('Positiv upplevelse av tillgänglighet hos patienter som besökt en primärvårdsmottagning', data, procent)
get_health_data('Rimlig väntetid till vård- eller hälsocentral', data, procent)
get_health_data('Primärvårdens tillgänglighet per telefon', data, procent)
get_health_data('Antal helårsanställda läkare i primärvården', data, antal)
get_health_data('Antal helårsanställda sjuksköterskor i primärvården ', data, antal)
get_health_data('Hyrkostnader andel av egna personalkostnader', data, 'Andel (%)')


# anrop av funktion get_vis_data för specifika frågeställningar
get_vis_data('Positiv upplevelse av respekt och bemötande hos patienter som besökt en primärvårdsmottagning', vis, procent)
get_vis_data('Positiv upplevelse av delaktighet i vården hos patienter som besökt en primärvårdsmottagning', vis, procent)
get_vis_data('Positiv upplevelse av information och kunskap hos patienter som besökt en primärvårdsmottagning', vis, procent)
get_vis_data('Positiv upplevelse av kontaktvägar med primärvården', vis, procent)
get_vis_data('Positiv upplevelse av kontinuitet och samordning hos patienter som besökt en primärvårdsmottagning', vis, procent)
get_vis_data('Positiv upplevelse av känslomässigt stöd bland patienter som besökt en primärvårdsmottagning', vis, procent)
get_vis_data('Positiv upplevelse av respekt och bemötande hos patienter som besökt en primärvårdsmottagning', vis, procent)
get_vis_data('Positiv upplevelse av tillgänglighet hos patienter som besökt en primärvårdsmottagning', vis, procent)
get_vis_data('Positiv upplevelse av respekt och bemötande hos patienter som besökt en primärvårdsmottagning', vis, procent)
get_vis_data('Positivt helhetsintryck hos patienter som besökt en primärvårdsmottagning.', vis, procent)

get_vis_data('Nettokostnad för primärvård', vis, 'Nettokostnad per invånare (SEK)')
get_vis_data('Kostnad per vårdkontakt i primärvården', vis, 'Kostnad per viktad vårdkontakt (SEK)')


