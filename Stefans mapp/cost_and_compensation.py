# import av moduler
import plotly.plotly as py
import plotly.graph_objs as go
import pandas as pd
import plotly.offline

# läser in data från .csv-fil och lagrar dem i variabel
df = pd.read_csv(r'C:\Users\steblo\Desktop\Nackademin\Dropbox\BI-relaterade programspråk\Grupparbete\Kod\cinco-hermanos\Sammanstallning modeller.csv', sep=';', encoding='UTF-8')

# ersätter strängen 'faktisk kostnad' med '0' för att strängen inte ska orsaka datatypsfel senare i skriptet
df["Kostnad läkarbesök på nationell taxa"] = df["Kostnad läkarbesök på nationell taxa"].str.replace('faktisk kostnad', '0')

# fyller alla tomma fält med värdet 0
df.fillna(0, inplace=True)

# gör om allt innehåll i data frameen till numeriska värden
df[["Kostnad för läkarbesök på annan vc", "Kostnad läkarbesök på nationell taxa",'Patientavgift Läkarbesök', 'Ersättning läkarbesök egenlistad', 'Ersättning läkarbesök listad annan vc', 'Ersättning läkarbesök utomlänspatient']] = df[["Kostnad för läkarbesök på annan vc", "Kostnad läkarbesök på nationell taxa", 'Patientavgift Läkarbesök', 'Ersättning läkarbesök egenlistad', 'Ersättning läkarbesök listad annan vc', 'Ersättning läkarbesök utomlänspatient']].apply(pd.to_numeric)

# nya beräknade kolumner definieras som ska representera kostnader som negativa värden i den slutgiltiga grafen
df['Kostnad annan vc'] = df['Kostnad för läkarbesök på annan vc']-(df['Kostnad för läkarbesök på annan vc']*2)
df['Kostnad nationell vc'] = df['Kostnad läkarbesök på nationell taxa']-(df['Kostnad läkarbesök på nationell taxa']*2)

# trace för diagrammet som ska ritas upp använder metoden 'Bar' från plotly.graph_objs för att definiera  ett stapeldiagram. metoden i fråga anropas sex st gånger för att alla uppsättningar med värden ska få en egen stapel
trace = [
    go.Bar(
        x = df['Landsting/Region'],
        y = df['Patientavgift Läkarbesök'],
        base = 0,
        marker = dict(
          color = 'blue'
        ),
        name = 'Patientavgift Läkarbesök'
    ),

    go.Bar(
        x = df['Landsting/Region'],
        y = df['Ersättning läkarbesök egenlistad'],
        base = 0,
        marker = dict(
          color = 'lawngreen'
        ),
        name = 'Ersättning läkarbesök egenlistad'
    ),

    go.Bar(
        x = df['Landsting/Region'],
        y = df['Ersättning läkarbesök listad annan vc'],
        base = 0,
        marker = dict(
          color = 'lightgreen'
        ),
        name = 'Ersättning läkarbesök listad annan vc'
    ),

    go.Bar(
        x = df['Landsting/Region'],
        y = df['Ersättning läkarbesök utomlänspatient'],
        base = 0,
        marker = dict(
          color = 'darkgreen'
        ),
        name = 'Ersättning läkarbesök utomlänspatient'
    ),

    go.Bar(
        x = df['Landsting/Region'],
        y = df['Kostnad för läkarbesök på annan vc'],
        base = df['Kostnad annan vc'],
        marker = dict(
          color = 'red'
        ),
        name = 'Kostnad för läkarbesök på annan vc'
    ),

     go.Bar(
        x = df['Landsting/Region'],
        y = df['Kostnad läkarbesök på nationell taxa'],
        base = df['Kostnad nationell vc'],
        marker = dict(
          color = 'darkred'
        ),
        name = 'Kostnad läkarbesök på nationell taxa'
    )
]

# definition av layout för den graf som ska skapas 
layout = go.Layout(xaxis = {'title':'Regioner och landsting'}, yaxis = {'title': 'Kronor'}, barmode = 'group', margin= dict(b = 100), showlegend = True)

# använder funktionen go.Figure för att skapa graf baserat på  dataunderlaget ovan samt layout
figure = go.Figure(data=trace, layout=layout)

# graf renderas med plotlys offline-plot funktion (används i testsyfte)
# plotly.offline.plot(fig, filename='Ersättningsmodell.html')

# graf renderas med plotlys onine-plot funktion
py.plot (figure, filename='Ersättningsmodell.html')
