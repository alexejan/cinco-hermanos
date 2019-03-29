import sys
import plotly.plotly as py # används inte för närvarande, men är inkluderad utifall online-grafer ska skapas
import plotly.offline as pyofl
import plotly.graph_objs as go
import pandas as pd

# ser till att rätt encoding sätts för stdout
sys.stdout.reconfigure(encoding='UTF-8')

# läser in data från .csv-filer och lagrar dem i variabler
skl_data = pd.read_csv(r"C:\Users\steblo\Desktop\Nackademin\Dropbox\BI-relaterade programspråk\Grupparbete\Excelbilaga till Hälso- och sjukvårdsrapporten 2018.csv", sep=';', encoding='UTF-8')
vis_data = pd.read_csv(r"C:\Users\steblo\Desktop\Nackademin\Dropbox\BI-relaterade programspråk\Grupparbete\vis_export_trunkerad.csv", sep=';', encoding='UTF-8')

# funktion för att hämta data från 'En god vård? Övergripande indikatorer för sjukvårdens kvalitet och resultat' (https://oppnadata.se/datamangd/#esc_entry=1032&esc_context=77)
""" def get_dgv_data(string_var, data, y_name):

    # instantiering av en data frame som segmenterar data från det excel-data som lästs in. mer specifikt används .loc för att dels filtrera fram data baserat på rader där ett visst villkor uppfylls, och i andra hand de kolumner som ska läsas in
    df = data.loc[data['name_short'] == string_var, ['Landsting och regioner', 'Värde', 'Källa', 'Mätperiod']]

    # ersätter kommatecken med punkt för att decimalvärden ska tolkas rätt, samt omvandlar värdena till float
    df['Värde'] = (df['Värde'].replace(',','.', regex=True).astype(float))

    # splittar årtal från eventuell följande distinktion (halvår/kvartal/månad). detta möjliggör gruppering 
    df['Mätperiod'] = (df['Mätperiod'].str.split(' ').str[0])
    
    # skapar en ny beräknad kolumn som grupperar genomsnittlig data (från kolumnen värde) efter Enhetsnamn och Mätperiod
    df['Medel'] = df.groupby(['Landsting och regioner','Mätperiod']).transform('mean')

     # instantiering av nya data frames med ett urval för de olika åren som ska undersökas
    df15 = df.loc[df['Mätperiod'] == '2015', ['Landsting och regioner', 'Medel']]
    df16 = df.loc[df['Mätperiod'] == '2016', ['Landsting och regioner', 'Medel']]
    df17 = df.loc[df['Mätperiod'] == '2017', ['Landsting och regioner', 'Medel']]
    df18 = df.loc[df['Mätperiod'] == '2018', ['Landsting och regioner', 'Medel']]

    # variabler som innehåller dataunderlag för de grafer som ska skapas  
    data15 = go.Bar(x=df15['Landsting och regioner'], y=df15['Medel'], name='2015')
    data16 = go.Bar(x=df16['Landsting och regioner'], y=df16['Medel'], name='2016')
    data17 = go.Bar(x=df17['Landsting och regioner'], y=df17['Medel'], name='2017')
    data18 = go.Bar(x=df18['Landsting och regioner'], y=df18['Medel'], name='2018')

    # definition av layout för den graf som ska skapas 
    layout = go.Layout(title = string_var, annotations = [dict(x = 1.025, y = -0.25, text = 'Källa: ' + str(df.iloc[0, 2]), showarrow = False, xref = 'paper', yref = 'paper', xanchor ='right', yanchor = 'auto', xshift = 0, yshift=0, font = dict(size=12, color="red"))], xaxis = {'title':'Regioner och landsting'}, yaxis = {'title':y_name}, barmode = 'group', margin= dict(b =100), showlegend=True)
    
    # använder funktionen go.Figure för att skapa grafer baserat på data och layout
    figure = go.Figure(data=[data15, data16, data17, data18],layout=layout)
    
    # graferna renderas med plotlys online-plot funktion
    pyofl.plot(figure, filename = string_var + ".html")

 """


# funktion för att hämta data från 'Excelbilaga till Hälso- och sjukvårdsrapporten 2018' (https://skl.se/)
def get_skl_data(string_var, data, y_name):

    # instantiering av en data frame som segmenterar data från det excel-data som lästs in. mer specifikt används .loc för att dels filtrera fram data baserat på rader där ett visst villkor uppfylls, och i andra hand de kolumner som ska läsas in
    df = data.loc[data['Indikatornamn'] == string_var, ['Landsting och regioner', 'Värde', 'Källa', 'Mätperiod']]

    # ersätter kommatecken med punkt för att decimalvärden ska tolkas rätt, samt omvandlar värdena till float
    df['Värde'] = (df['Värde'].replace(',','.', regex=True).astype(float))

    # splittar årtal från eventuell följande distinktion (halvår/kvartal/månad). detta möjliggör gruppering 
    df['Mätperiod'] = (df['Mätperiod'].str.split(' ').str[0])
    
    # skapar en ny beräknad kolumn som grupperar genomsnittlig data (från kolumnen värde) efter Enhetsnamn och Mätperiod
    df['Medel'] = df.groupby(['Landsting och regioner','Mätperiod']).transform('mean')

     # instantiering av nya data frames med ett urval för de olika åren som ska undersökas
    df15 = df.loc[df['Mätperiod'] == '2015', ['Landsting och regioner', 'Medel']]
    df16 = df.loc[df['Mätperiod'] == '2016', ['Landsting och regioner', 'Medel']]
    df17 = df.loc[df['Mätperiod'] == '2017', ['Landsting och regioner', 'Medel']]
    df18 = df.loc[df['Mätperiod'] == '2018', ['Landsting och regioner', 'Medel']]

    # variabler som innehåller dataunderlag för de grafer som ska skapas  
    data15 = go.Bar(x=df15['Landsting och regioner'], y=df15['Medel'], name='2015')
    data16 = go.Bar(x=df16['Landsting och regioner'], y=df16['Medel'], name='2016')
    data17 = go.Bar(x=df17['Landsting och regioner'], y=df17['Medel'], name='2017')
    data18 = go.Bar(x=df18['Landsting och regioner'], y=df18['Medel'], name='2018')

    # definition av layout för den graf som ska skapas 
    layout = go.Layout(title = string_var, annotations = [dict(x = 1.025, y = -0.25, text = 'Källa: ' + str(df.iloc[0, 2]), showarrow = False, xref = 'paper', yref = 'paper', xanchor ='right', yanchor = 'auto', xshift = 0, yshift=0, font = dict(size=12, color="red"))], xaxis = {'title':'Regioner och landsting'}, yaxis = {'title':y_name}, barmode = 'group', margin= dict(b =100), showlegend=True)
    
    # använder funktionen go.Figure för att skapa grafer baserat på data och layout
    figure = go.Figure(data=[data15, data16, data17, data18],layout=layout)
    
    # graferna renderas med plotlys online-plot funktion
    pyofl.plot(figure, filename = string_var + ".html")

# funktion för att hämta data från excel-underlag hämtat från Vården i siffror (https://vardenisiffror.se/)
def get_vis_data(string_var, data, y_name):
    
    # instantiering av en data frame som segmenterar data från den csv-fil som lästs in. mer specifikt används .loc för att dels filtrera fram data baserat på rader där ett visst villkor uppfylls, och i andra hand de kolumner som ska läsas in
    df = data.loc[data['Titel'] == string_var, ['Register/källa', 'Enhetsnamn', 'Mätperiod', 'Värde']]
     
    # sparar index för rader där värdet är okänt som ogiltiga rader  
    invalid_rows = df[df['Värde'] == 'UNK' ].index  
    
    # tar bort ogiltiga rader baserat på indexet ovan
    df.drop(invalid_rows , inplace=True)
 
    # ersätter kommatecken med punkt för att decimalvärden ska tolkas rätt, samt omvandlar värdena till float
    df['Värde'] = (df['Värde'].replace(',','.', regex=True).astype(float))

    # splittar årtal från eventuell följande distinktion (halvår/kvartal/månad). detta möjliggör gruppering 
    df['Mätperiod'] = (df['Mätperiod'].str.split(' ').str[0])

    # skapar en ny beräknad kolumn som grupperar genomsnittlig data (från kolumnen värde) efter Enhetsnamn och Mätperiod
    df['Medel'] = df.groupby(['Enhetsnamn','Mätperiod']).transform('mean')
    
    # instantiering av nya data frames med ett urval för de olika åren som ska undersökas
    df15 = df.loc[df['Mätperiod'] == '2015', ['Enhetsnamn', 'Medel']]
    df16 = df.loc[df['Mätperiod'] == '2016', ['Enhetsnamn', 'Medel']]
    df17 = df.loc[df['Mätperiod'] == '2017', ['Enhetsnamn', 'Medel']]
    df18 = df.loc[df['Mätperiod'] == '2018', ['Enhetsnamn', 'Medel']]

    # variabler som innehåller dataunderlag för de grafer som ska skapas
    data15 = go.Bar(x=df15['Enhetsnamn'], y=df15['Medel'], name='2015')
    data16 = go.Bar(x=df16['Enhetsnamn'], y=df16['Medel'], name='2016')
    data17 = go.Bar(x=df17['Enhetsnamn'], y=df17['Medel'], name='2017')
    data18 = go.Bar(x=df18['Enhetsnamn'], y=df18['Medel'], name='2018')

    # definition av layout för den graf som ska skapas 
    layout = go.Layout(title = string_var, annotations = [dict(x = 1.025, y = -0.25, text = 'Källa: ' + str(df.iloc[0, 0]), showarrow = False, xref = 'paper', yref = 'paper', xanchor ='right', yanchor = 'auto', xshift = 0, yshift=0, font = dict(size=12, color="red"))], xaxis = {'title':'Regioner och landsting'}, yaxis = {'title':y_name}, barmode = 'group', margin= dict(b =100))

    # använder funktionen go.Figure för att skapa graf baserat på de tre dataunderlagen samt layout
    figure = go.Figure(data = [data15, data16, data17, data18], layout=layout)

    # graf renderas med plotlys offline-plot funktion
    pyofl.plot(figure, filename = string_var + ".html")


# funktion för att hämta data från excel-underlag hämtat från Vården i siffror (https://vardenisiffror.se/)
def get_test_data(string_var, data, y_name):
    
    # instantiering av en data frame som segmenterar data från den csv-fil som lästs in. mer specifikt används .loc för att dels filtrera fram data baserat på rader där ett visst villkor uppfylls, och i andra hand de kolumner som ska läsas in
    df = data.loc[data['Titel'] == string_var, ['Register/källa', 'Enhetsnamn', 'Mätperiod', 'Värde', 'Måttenhet', 'Täljare', 'Nämnare/antal fall']]
     
    # sparar index för rader där värdet är okänt som ogiltiga rader  
    invalid_rows = df[df['Värde'] == 'UNK' ].index  

    # tar bort ogiltiga rader baserat på indexet ovan
    df.drop(invalid_rows , inplace=True)
 
    # ersätter kommatecken med punkt för att decimalvärden ska tolkas rätt, samt omvandlar värdena till float
    df['Värde'] = (df['Värde'].replace(',','.', regex=True).astype(float))

    
    # ersätter bindestreck med 0 för att decimalvärden ska tolkas rätt, samt omvandlar värdena till int
    df['Täljare'] = (df['Täljare'].replace('-',0, regex=True).astype(int))  
    df['Nämnare/antal fall'] = (df['Nämnare/antal fall'].replace('-',0, regex=True).astype(int))


    # splittar årtal från eventuell följande distinktion (halvår/kvartal/månad). detta möjliggör gruppering 
    df['Mätperiod'] = (df['Mätperiod'].str.split(' ').str[0])

    # skapar en ny beräknad kolumn som grupperar genomsnittlig data (från kolumnen värde) efter Enhetsnteamn och Mätperiod
    # df['Täljare_summa'] = df.groupby(['Enhetsnamn','Mätperiod']).Täljare.sum().reset_index()

    # test = df.groupby(['Enhetsnamn','Mätperiod'])['Täljare'].sum().reset_index()

    df['Täljare_summerat'] = df.groupby(['Enhetsnamn','Mätperiod'])['Täljare'].transform('sum')
    df['Nämnare_summerat'] = df.groupby(['Enhetsnamn','Mätperiod'])['Nämnare/antal fall'].transform('sum')
    
    df['Medel'] = df.groupby(['Enhetsnamn','Mätperiod'])['Värde'].transform('mean')

    df['Andel'] = (df['Täljare_summerat']/ df['Nämnare_summerat']) * 100

    # print(df['Täljare'])
    print(df['Nämnare/antal fall'])

    df.to_csv(r"C:\Users\steblo\Desktop\Nackademin\Dropbox\BI-relaterade programspråk\Grupparbete\test.csv")

    if (df['Täljare'] != 0):
        y_values = 'Andel'
    
    else:
        y_values = 'Medel'

    # instantiering av nya data frames med ett urval för de olika åren som ska undersökas
    df15 = df.loc[df['Mätperiod'] == '2015', ['Enhetsnamn', y_values]]
    df16 = df.loc[df['Mätperiod'] == '2016', ['Enhetsnamn', y_values]]
    df17 = df.loc[df['Mätperiod'] == '2017', ['Enhetsnamn', y_values]]
    df18 = df.loc[df['Mätperiod'] == '2018', ['Enhetsnamn', y_values]]

    # variabler som innehåller dataunderlag för de grafer som ska skapas
    data15 = go.Bar(x=df15['Enhetsnamn'], y=df15[y_values], name='2015')
    data16 = go.Bar(x=df16['Enhetsnamn'], y=df16[y_values], name='2016')
    data17 = go.Bar(x=df17['Enhetsnamn'], y=df17[y_values], name='2017')
    data18 = go.Bar(x=df18['Enhetsnamn'], y=df18[y_values], name='2018')

    # definition av layout för den graf som ska skapas 
    layout = go.Layout(title = string_var, annotations = [dict(x = 1.025, y = -0.25, text = 'Källa: ' + str(df.iloc[0, 0]), showarrow = False, xref = 'paper', yref = 'paper', xanchor ='right', yanchor = 'auto', xshift = 0, yshift=0, font = dict(size=12, color="red"))], xaxis = {'title':'Regioner och landsting'}, yaxis = {'title':y_name}, barmode = 'group', margin= dict(b =100))

    # använder funktionen go.Figure för att skapa graf baserat på de tre dataunderlagen samt layout
    figure = go.Figure(data = [data15, data16, data17, data18], layout=layout)

    # graf renderas med plotlys offline-plot funktion
    pyofl.plot(figure, filename = string_var + ".html")



# variabler som ska användas i anrop av funktion för att ge namn till y-axel
procent = 'Andel positiva svar från patienter (%)'
antal = 'Antal per 1000 invånare'


get_test_data('Tillgång till den hälso- och sjukvård man behöver', vis_data, procent)

# anrop av funktion get_skl_data för specifika frågeställningar
""" get_skl_data('Antal helårsanställda läkare i primärvården', skl_data, antal)
get_skl_data('Antal helårsanställda sjuksköterskor i primärvården ', skl_data, antal)
get_skl_data('Hyrkostnader andel av egna personalkostnader', skl_data, 'Andel (%)') """

# get_skl_data('Primärvårdens tillgänglighet per telefon', skl_data, procent)


# anrop av funktion get_vis_data för specifika frågeställningar. notera skillnad i det tredje argumentet beroende på vilken data som ska visas
""" get_vis_data('Andra besök än läkarbesök i primärvård', vis_data, antal)
get_vis_data('Förtroende för vård- eller hälsocentral', vis_data, antal) 
get_vis_data('Kostnad per vårdkontakt i primärvården', vis_data, 'Kostnad per viktad vårdkontakt (SEK)') 
get_vis_data('Läkarbesök i primärvården', vis_data, antal) 
get_vis_data('Nettokostnad för primärvård', vis_data, 'Nettokostnad per invånare (SEK)')
get_vis_data('Positiv upplevelse av delaktighet i vården hos patienter som besökt en primärvårdsmottagning', vis_data, procent)
get_vis_data('Positiv upplevelse av information och kunskap hos patienter som besökt en primärvårdsmottagning', vis_data, procent)
get_vis_data('Positiv upplevelse av kontaktvägar med primärvården', vis_data, procent)
get_vis_data('Positiv upplevelse av kontinuitet och samordning hos patienter som besökt en primärvårdsmottagning', vis_data, procent)
get_vis_data('Positiv upplevelse av känslomässigt stöd bland patienter som besökt en primärvårdsmottagning', vis_data, procent)
get_vis_data('Positiv upplevelse av tillgänglighet hos patienter som besökt en primärvårdsmottagning', vis_data, procent)
get_vis_data('Positiv upplevelse av respekt och bemötande hos patienter som besökt en primärvårdsmottagning', vis_data, procent)
get_vis_data('Positivt helhetsintryck hos patienter som besökt en primärvårdsmottagning.', vis_data, procent)
get_vis_data('Rimlig väntetid till vårdcentral', vis_data, procent)
get_vis_data('Stort förtroende för vårdcentraler', vis_data, antal) 
get_vis_data('Upplevd rimlig väntetid till vårdcentral', vis_data, procent) """

# get_vis_data('Primärvårdens tillgänglighet per telefon', vis_data, procent)
