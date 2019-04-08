# import av moduler
import sys
import plotly.offline
import plotly.graph_objs as go
import pandas as pd
import plotly.plotly as py 

# ser till att rätt encoding sätts för stdout
sys.stdout.reconfigure(encoding='UTF-8')

# läser in data från .csv-fil och lagrar den i en data frame
vis_data = pd.read_csv(r"C:\Users\steblo\Desktop\Nackademin\Dropbox\BI-relaterade programspråk\Grupparbete\Kod\cinco-hermanos\truncated_data_SS.csv", sep=';', encoding='UTF-8')

# splittar årtal från eventuell följande distinktion (halvår/kvartal/månad). detta möjliggör gruppering i nya dataframes nedan
vis_data['Mätperiod'] = (vis_data['Mätperiod'].str.split(' ').str[0])

# definition av stapelfärger för landsting/regioner som fått ett lågt värde i 'superindex' (sammanställning av resultat från https://www.socialstyrelsen.se/Lists/Artikelkatalog/Attachments/21230/2019-1-20.pdf ) 
colors = {'Skåne': 'maroon',
          'Gävleborg': 'gold',
          'Jämtland Härjedalen': 'purple',
          'Västernorrland': 'orange',
          'Norrbotten': 'seagreen'}

# funktion för att hämta data från csv-underlag hämtat från Vården i siffror (https://vardenisiffror.se/)
def get_vis_data(string_var, data):
    
    # instantiering av en data frame som segmenterar data från den csv-fil som lästs in. mer specifikt används .loc för att dels filtrera fram data baserat på rader där ett visst villkor uppfylls, och i andra hand de kolumner <som ska läsas in  
    df_first = data.loc[(data['Diagramrubrik'] == string_var) & (data['Kön/Totalt'] == 'Totalt'), ['Register/källa', 'Måttenhet', 'Titel', 'Område', 'Enhetsnamn', 'Mätperiod', 'Värde', 'Måttenhet', 'Täljare', 'Nämnare/antal fall']]

    # för att se till att endast data för det senast registrerade året lagras görs en ny dataframe där en filtrering görs på det maximala värdet i kolumnen Mätperiod, d v s det senaste året
    df = df_first.loc[df_first['Mätperiod'] == df_first['Mätperiod'].max(), ['Register/källa', 'Måttenhet', 'Titel', 'Område', 'Enhetsnamn','Mätperiod', 'Värde', 'Måttenhet', 'Täljare', 'Nämnare/antal fall']]    

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

    # ny beräknad kolumn för stapelfärger - default-färg sätts till samma default-färg som plotly använder i sina grafer ('#1f77b4')
    df['Color'] = df['Enhetsnamn'].map(colors).fillna('#1f77b4')

    # ersätter bindestreck med 0 i nedan nämnda två kolumner för att decimalvärden ska tolkas rätt, samt omvandlar värdena till int
    df['Täljare'] = (df['Täljare'].replace('-',0, regex=True).astype(int))
    df['Nämnare/antal fall'] = (df['Nämnare/antal fall'].replace('-',0, regex=True).astype(int))

    # skapar två nya calculated columns som innehåller summeringar av data från kolumnerna 'Täljare' och 'Nämnare/antal fall' grupperat efter data från kolumnerna 'Enhetnamn' och 'Mätperiod'
    df['Täljare_summerat'] = df.groupby(['Enhetsnamn'])['Täljare'].transform('sum')
    df['Nämnare_summerat'] = df.groupby(['Enhetsnamn'])['Nämnare/antal fall'].transform('sum')

    # skapar en beräknad kolumn baserat på kvoten mellan summeringar av data från täljare och nämnare (se ovan). Beräkningen görs för att få en övergripande bild för de fall där det förekommer flera poster med samma enhetsnamn och mätperiod
    df['Andel'] = (df['Täljare_summerat']/ df['Nämnare_summerat']) * 100

    # instantierar en lista dit ny kolumndata ska läggas in
    new_column = []

    # for-lopp som itererar genom hela data framen df baserat på dess index. Om någon av kolumnerna Täljare eller Nämnare visar 0 läggs värdet för kolumnen 'Värde' till i listan eftersom ingen division då kan göras. Om dock bägge kolumnerna innehåller data läggs värdet för kolumnen 'Andel' till i listan.
    for i in df.index:
        if df.loc[i]['Täljare']== 0 or df.loc[i]['Nämnare/antal fall']== 0:
            new_column.append(df.loc[i]['Värde'])
        else :
            new_column.append(df.loc[i]['Andel'])            
        
    # skapar en ny beräknad kolumn baserat på listan från for-loopen ovan
    df['Andel/Värde'] = new_column
    
    # skriver ut data frame till fil (med syfte att dumpa data i händelse att data frame kan återanvändas på annan plats) 
    df.to_csv(str(df.iloc[0, 3]) + ".csv")

    # en ny instans av data frame som enbart innehåller de tre kolumnerna nedan. dessa tre kolumner är de enda som behöver användas i grafen (med undantag av vissa titlar - se layout)
    df_trace = df[['Enhetsnamn', 'Andel/Värde', 'Color']]

    # sorterar den nya dataframen (se direkt ovan) efter värde i stigande ordning för att staplarna i grafen ska sorteras efter detta
    df_trace.sort_values('Andel/Värde', ascending=True, inplace = True)
    
    # trace för diagrammet som ska ritas upp använder metoden 'Bar' från plotly.graph_objs för att definiera  ett stapeldiagram. x-axel sätts till likvärdig med värdena i kolumnen för 'Landsting och regioner' och y-axeln sätts till att följa värdena i kolumnen 'Värde. Dessutom markeras staplar med färg baserat på kolumnen 'Color'
    trace = go.Bar(x=df_trace['Enhetsnamn'], y=df_trace['Andel/Värde'], marker={'color': df_trace['Color']})
    
    # definition av layout för den graf som ska skapas 
    layout = go.Layout(xaxis = {'title':'Regioner och landsting' + ' ('+ str(df_first['Mätperiod'].max()) + ')'}, yaxis = {'title':str(df.iloc[0, 2])}, barmode = 'group', margin= dict(b = 100), showlegend = False)

    # använder funktionen go.Figure för att skapa graf baserat på dataunderlaget (trace) samt layout
    figure = go.Figure(data = [trace], layout=layout)

    # graf renderas med plotlys offline-plot funktion (används i testsyfte)
    # plotly.offline.plot(figure, filename = str(df.iloc[0, 3]) + ".html")

    # graf renderas med plotlys onine-plot funktion
    py.plot(figure, filename = str(df.iloc[0, 3]))

# skapar en data series med unika värden från kolumnen Diagramrubrik i vis_data (den data frame till vilken källdata har lästs in) 
df_series = vis_data.Diagramrubrik.unique()

# for-loop som itererar igenom alla element i df_series (se direkt ovan) och som anropar funktionen get_vis_data för vart och ett av dessa element
for item in df_series:
    get_vis_data(item, vis_data)

# anrop av ovanstående funktion med specifika frågeställningar (för testsyfte)
# get_vis_data('Landstingens kostnader per viktad vårdkontakt inom primärvården.', vis_data)
# get_vis_data('Motivationsindex för hälso- och sjukvård totalt enligt resultat från medarbetarenkät.', vis_data)

