import pandas as pd
import numpy as np
import plotly as py
import plotly.graph_objs as go

# Läser in källfilen till df
df = pd.read_csv('besok_per_yrke.csv', skiprows=1, sep=';')

# Sorterar bort oväsentliga värden
df = df.iloc[:,1:].loc[(df['Värden'] == 'Besök per 1000 inv, spec') &
                       (df['Område'] == 'Primärvård') &
                       (df['År'] == 2017) &
                       (df['Prestation'].str.lower().str.contains('hem') == False) &
                       (df['varav'].str.lower().str.contains('hem') == False)]
# x =list(df)[-22:]
# Tar bort onödiga kolumner
df.drop(['Värden','År', 'varav', 'Område', 'Prestationsgrupp', 'Prestation'], axis=1, inplace=True)

# Gör en "unpivot" på på DataFramen så att alla länskolumner hamnar i en kolumn
df_unpivot = pd.melt(df, id_vars=['Egen/annan produktion', 'Därav', 'Läkare/ Övrigt'],
                     var_name='Län', value_name='Antal').fillna('0')

# Fixar till 1000-talssiffror där de var formaterade som '1 000'
df_unpivot['Antal'] = df_unpivot['Antal'].str.replace(' ', '').astype(int)

# Summerar ihop Läkare samt ej läkare
df_unpivot = df_unpivot.groupby(['Egen/annan produktion', 'Därav', 'Län'], sort=False, as_index=False).sum()
mottagning = df_unpivot['Därav'].drop_duplicates()
off_privat = df_unpivot['Egen/annan produktion'].drop_duplicates()

# Skapar en kolumn där värdena för offentlig och privat har summerats
df_unpivot['Summa'] = df_unpivot.groupby(['Därav', 'Län'])['Antal'].transform(sum)

# Sorterar dataframen på föregående skapad kolumn
df_unpivot.sort_values('Summa', inplace=True)

# Skapar ett stapeldiagram per mottagningstyp
for mot in mottagning:          # För varje mottagningstyp...
    trace = []
    for op in off_privat:       # För varje mottagningstyp i antingen privat eller offentlig regi
        filter = df_unpivot[(df_unpivot['Därav'] == mot) & (df_unpivot['Egen/annan produktion'] == op)] # Skapar ett filter för att filtrera på loopinnehållet
        trace.append(go.Bar(x=filter['Län'], y=filter['Antal'], name=op))
    layout = go.Layout(barmode='stack',     # Stacked bars
                       xaxis=dict(title='Län'), yaxis=dict(title='Per 100 000 invånare'))
    fig=go.Figure(data=trace, layout=layout)
    py.offline.plot(fig, filename=f'{mot}')
df_unpivot.to_csv('verksamhetsbesok.csv')

