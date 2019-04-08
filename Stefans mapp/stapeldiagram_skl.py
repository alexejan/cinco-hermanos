# import av moduler
import sys
import plotly.offline
import plotly.graph_objs as go
import pandas as pd
import plotly.plotly as py 

# ser till att rätt encoding sätts för stdout
sys.stdout.reconfigure(encoding='UTF-8')

# läser in data från .csv-fil och lagrar denna data i data frame
skl_data = pd.read_csv(r"C:\Users\steblo\Desktop\Nackademin\Dropbox\BI-relaterade programspråk\Grupparbete\Excelbilaga till Hälso- och sjukvårdsrapporten 2018.csv", sep=';', encoding='UTF-8')

# splittar årtal från eventuell följande distinktion (halvår/kvartal/månad). detta möjliggör gruppering i nya dataframes nedan
skl_data['Mätperiod'] = (skl_data['Mätperiod'].str.split(' ').str[0])


# definition av stapelfärger för landsting/regioner som fått ett lågt värde i 'superindex' (sammanställning av resultat från https://www.socialstyrelsen.se/Lists/Artikelkatalog/Attachments/21230/2019-1-20.pdf ) 
colors = {'Skåne': 'maroon',
          'Gävleborg': 'gold',
          'Jämtland Härjedalen': 'purple',
          'Västernorrland': 'orange',
          'Norrbotten': 'seagreen'}

# funktion för att hämta data från 'Excelbilaga till Hälso- och sjukvårdsrapporten 2018' (https://skl.se/)
def get_skl_data(string_var, data):
 
    # instantiering av en data frame som segmenterar data från den csv-fil som har lästs in. mer specifikt används .loc för att dels filtrera fram data baserat på rader där ett visst villkor uppfylls (en specifik indikator), och i andra hand de kolumner som ska läsas in
    df = data.loc[(data['Indikatornamn'] == string_var) & (data['Mätperiod'] == data['Mätperiod'].max()), ['Landsting och regioner', 'Värde', 'Källa', 'Mätperiod', 'Måttenhet ', 'Täljare', 'Nämnare', 'Indikatornamn']]

    # ersätter kommatecken med punkt för att decimalvärden ska tolkas rätt, samt omvandlar värdena till float
    df['Värde'] = (df['Värde'].replace(',','.', regex=True).astype(float))
   
    # ny beräknad kolumn för stapelfärger - default-färg sätts till samma default-färg som plotly använder i sina grafer ('#1f77b4')
    df['Color'] = df['Landsting och regioner'].map(colors).fillna('#1f77b4')
    
    # sparar index för rader där värdet är okänt/ej numeriskt som ogiltiga rader  
    invalid_rows1 = df[df['Värde'] == 'UNK'].index  
    invalid_rows2 = df[df['Värde'] == 'MSK'].index
    invalid_rows3 = df[df['Värde'] == 'INV'].index    

    # tar bort ogiltiga rader baserat på indexet ovan
    df.drop(invalid_rows1, inplace=True)
    df.drop(invalid_rows2, inplace=True)
    df.drop(invalid_rows3, inplace=True)

    # en ny instans av data frame som enbart innehåller de tre kolumnerna nedan. dessa tre kolumner är de enda som behöver användas i grafen (med undantag av vissa titlar - se layout)
    df_trace = df[['Landsting och regioner', 'Värde', 'Color']]

    # sorterar den nya dataframen (se direkt ovan) efter värde i stigande ordning för att staplarna i grafen ska sorteras efter detta
    df_trace.sort_values('Värde', ascending=True, inplace = True)

    # skriver ut data frame till fil (med syfte att dumpa data i händelse att data frame kan återanvändas på annan plats) 
    df.to_csv('Dump av SKL-data.csv')
    
    # trace för diagrammet som ska ritas upp använder metoden 'Bar' från plotly.graph_objs för att definiera  ett stapeldiagram. x-axel sätts till likvärdig med värdena i kolumnen för 'Landsting och regioner' och y-axeln sätts till att följa värdena i kolumnen 'Värde. Dessutom markeras staplar med färg baserat på kolumnen 'Color'
    trace = go.Bar(x=df_trace['Landsting och regioner'], y=df_trace['Värde'], marker={'color': df_trace['Color']})
    
    # definition av layout för den graf som ska skapas 
    layout = go.Layout(xaxis = {'title':'Regioner och landsting' + ' ('+ str(df.iloc[0, 3]) + ')'}, yaxis = {'title':str(df.iloc[0, 4])}, barmode = 'group', margin= dict(b = 100), showlegend = False)

    # använder funktionen go.Figure för att skapa graf baserat på dataunderlaget samt layout
    figure = go.Figure(data = [trace], layout=layout)

    # graf renderas med plotlys offline-plot funktion (används i testsyfte)
    # plotly.offline.plot(figure, filename = str(df.iloc[0, 7]))

    # graf renderas med plotlys onine-plot funktion
    py.plot(figure, filename = str(df.iloc[0, 7]))

# anrop av funktion get_skl_data för specifika frågeställningar
get_skl_data('Antal helårsanställda läkare i primärvården', skl_data)
get_skl_data('Antal helårsanställda sjuksköterskor i primärvården ', skl_data)
get_skl_data('Hyrkostnader andel av egna personalkostnader', skl_data)