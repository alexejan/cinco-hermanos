# import av moduler
import sys
import plotly.offline as pyofl
import plotly.graph_objs as go
import pandas as pd
import re

# används inte för närvarande, men är inkluderad utifall online-grafer ska skapas
import plotly.plotly as py 

# ser till att rätt encoding sätts för stdout
sys.stdout.reconfigure(encoding='UTF-8')

# läser in data från .csv-filer och lagrar dem i variabler
# skl_data = pd.read_csv(r"C:\Users\steblo\Desktop\Nackademin\Dropbox\BI-relaterade programspråk\Grupparbete\Excelbilaga till Hälso- och sjukvårdsrapporten 2018.csv", sep=';', encoding='UTF-8')

vis_data = pd.read_csv(r"C:\Users\steblo\Desktop\Nackademin\Dropbox\BI-relaterade programspråk\Grupparbete\truncated_data.csv", sep=';', encoding='UTF-8')

# vis_data = pd.read_csv(r"C:\Users\steblo\Desktop\Nackademin\Dropbox\BI-relaterade programspråk\Grupparbete\vis_export.csv", sep=';', encoding='UTF-8')

def get_vis_data_procent(string_var, data):
    
    # instantiering av en data frame som segmenterar data från den csv-fil som lästs in. mer specifikt används .loc för att dels filtrera fram data baserat på rader där ett visst villkor uppfylls, och i andra hand de kolumner som ska läsas in
    df = data.loc[(data['Socialstyrelsen'] == string_var) & (data['Måttenhet'] == '%'), ['Register/källa', 'Måttenhet', 'Enhetsnamn', 'Mätperiod', 'Värde', 'Måttenhet', 'Täljare', 'Nämnare/antal fall']]

    # sparar index för rader där värdet är okänt som ogiltiga rader  
    invalid_rows1 = df[df['Värde'] == 'UNK'].index  
    invalid_rows2 = df[df['Värde'] == 'MSK'].index
    invalid_rows3 = df[df['Värde'] == 'INV'].index    

    # tar bort ogiltiga rader baserat på indexet ovan
    df.drop(invalid_rows1, inplace=True)
    df.drop(invalid_rows2, inplace=True)
    df.drop(invalid_rows3, inplace=True)

    # ersätter kommatecken med punkt för att decimalvärden ska tolkas rätt, samt omvandlar värdena till float
    df['Värde'] = (df['Värde'].replace(',','.', regex=True).astype(float))

    # splittar årtal från eventuell följande distinktion (halvår/kvartal/månad). detta möjliggör gruppering i nya dataframes nedan
    df['Mätperiod'] = (df['Mätperiod'].str.split(' ').str[0])
    
    # ersätter bindestreck med 0 i nedan nämnda två kolumner för att decimalvärden ska tolkas rätt, samt omvandlar värdena till int
    df['Täljare'] = (df['Täljare'].replace('-',0, regex=True).astype(int))  
    df['Nämnare/antal fall'] = (df['Nämnare/antal fall'].replace('-',0, regex=True).astype(int))

    # skapar en ny beräknad kolumn som grupperar genomsnittlig data (från kolumnen värde) efter Enhetsnamn och Mätperiod
    
    # df['Medel'] = df.groupby(['Enhetsnamn','Mätperiod'])['Värde'].transform('mean')

    # skapar två nya calculated columns som innehåller summeringar av data från kolumnerna 'Täljare' och 'Nämnare/antal fall' grupperat efter data från kolumnerna 'Enhetnamn' och 'Mätperiod'
    df['Täljare_summerat'] = df.groupby(['Enhetsnamn','Mätperiod'])['Täljare'].transform('sum')
    df['Nämnare_summerat'] = df.groupby(['Enhetsnamn','Mätperiod'])['Nämnare/antal fall'].transform('sum')

    # skapar en beräknad kolumn baserat på kvoten mellan summeringar av data från täljare och nämnare (se ovan). Beräkningen görs för att få en övergripande bild för de fall där det förekommer flera poster med samma enhetsnamn och mätperiod
    df['Andel'] = (df['Täljare_summerat'] / df['Nämnare_summerat']) * 100
    
    # instantierar en lista dit ny kolumndata ska läggas in
    new_column = []

    # for-lopp som itererar genom hela data framen df baserat på dess index. Om någon av kolumnerna Täljare eller Nämnare visar 0 läggs värdet för kolumnen 'Värde' till i listan eftersom ingen division då kan göras. Om dock bägge kolumnerna innehåller data läggs värdet för kolumnen 'Andel' till i listan.
    for i in df.index:
        if df.loc[i]['Täljare']== 0 or df.loc[i]['Nämnare/antal fall']== 0:
            # print('hej')
            new_column.append(df.loc[i]['Värde'])
        else :
            new_column.append(df.loc[i]['Andel'])            
            # print('nej')
        
    # skapar en ny beräknad kolumn baserat på listan från for-loopen ovan
    df['Andel/Värde'] = new_column

    # diagram_title = string_var.split('.')
    diagram_title = string_var.replace('?','')

    # skriver ut data frame till fil (delvis för test-syfte) 
    # df.to_csv(string_var + ".csv")
    
    # instantiering av nya data frames med ett urval för de olika åren som ska undersökas
    df15 = df.loc[df['Mätperiod'] == '2015', ['Enhetsnamn', 'Andel/Värde']]
    df16 = df.loc[df['Mätperiod'] == '2016', ['Enhetsnamn', 'Andel/Värde']]
    df17 = df.loc[df['Mätperiod'] == '2017', ['Enhetsnamn', 'Andel/Värde']]
    df18 = df.loc[df['Mätperiod'] == '2018', ['Enhetsnamn', 'Andel/Värde']]

    # variabler som innehåller dataunderlag för de grafer som ska skapas
    data15 = go.Bar(x=df15['Enhetsnamn'], y=df15['Andel/Värde'], name='2015')
    data16 = go.Bar(x=df16['Enhetsnamn'], y=df16['Andel/Värde'], name='2016')
    data17 = go.Bar(x=df17['Enhetsnamn'], y=df17['Andel/Värde'], name='2017')
    data18 = go.Bar(x=df18['Enhetsnamn'], y=df18['Andel/Värde'], name='2018')

    # definition av layout för den graf som ska skapas 
    layout = go.Layout(title = diagram_title + '?', annotations = [dict(x = 1.025, y = -0.25, text = 'Källa: ' + str(df.iloc[0, 0]), showarrow = False, xref = 'paper', yref = 'paper', xanchor ='right', yanchor = 'auto', xshift = 0, yshift=0, font = dict(size=12, color="red"))], xaxis = {'title':'Regioner och landsting'}, yaxis = {'title':str(df.iloc[0, 1])}, barmode = 'group', margin= dict(b =100), showlegend=True)

    # använder funktionen go.Figure för att skapa graf baserat på de tre dataunderlagen samt layout
    figure = go.Figure(data = [data15, data16, data17, data18], layout=layout)

    # graf renderas med plotlys offline-plot funktion
    pyofl.plot(figure, filename = diagram_title + ".html")


# anrop av funktion get_skl_data för specifika frågeställningar
""" get_skl_data('Antal helårsanställda läkare i primärvården', skl_data, antal)
get_skl_data('Antal helårsanställda sjuksköterskor i primärvården ', skl_data, antal)
get_skl_data('Hyrkostnader andel av egna personalkostnader', skl_data, 'Andel (%)') """
# get_skl_data('Primärvårdens tillgänglighet per telefon', skl_data, procent)
""" 
titles = []

df = vis_data.Diagramrubrik.unique()

pattern = re.compile(r"primärvård|central|hälso-|lika villkor|tillgång till|personer som anser|medellivslängd|vårddagar per|vårdtillfällen per|antal självmord|antal utlarmningar", re.IGNORECASE)

for item in df:
    if re.search(pattern, item):
        titles.append(item)

titles.sort()

# for item in titles:
#     get_vis_data(item, vis_data) 

# test för att se vilka rader som hämtas
for x in range(len(titles)):
    print(titles[x])

print(len(titles))

 """

df_frame = vis_data.Socialstyrelsen.unique()

for item in df_frame:
    print(item)

# get_vis_data_test('Hur mycket betalar vi för hälso- och sjukvården?', vis_data)

# for item in df_frame:
    # get_vis_data_procent(item, vis_data)

""" 
for item in titles:
#     get_vis_data(item, vis_data) 

# test för att se vilka rader som hämtas
for x in range(len(titles)):
    print(titles[x])

print(len(titles))

 """