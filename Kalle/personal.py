import numpy as np
import pandas as pd
import plotly as py
import plotly.graph_objs as go

# Läser in källfilen och hoppar aver första raden samt den sista (iloc[:-1,:]
df = pd.read_csv('socialstyrelsen_personal.csv', sep=';', skiprows=1).iloc[:-1,:]

# Byter namn på kolumn
df.rename(columns={'2016': 'Antal'}, inplace=True)

# Skapar en lista med alla yrkeskategorier
yrken = list(df['Grupp'].drop_duplicates())

# Summerar all antal personal per län för användning i sortering
sort = np.array(df.groupby(['Region'], sort=False, as_index=False).sum()['Antal'])

# Skapar en lista som ska få grafdata
trace = []
for i in yrken:         # För varje yrke...
    temp = pd.DataFrame.copy(df[df['Grupp'] == i]) # Filtrerar på yrke
    temp['Summa'] = sort                                       # Lägger till sorteringskolumnen
    temp.sort_values(['Summa'], inplace=True)                  # Samt sorterar efter totala antalet personal per län
    trace.append(go.Bar(x=temp['Region'],                      # Och lägger till det i tidigare skapad lista
                        y=temp['Antal'],
                        name=i))
df.to_csv('personaltathet.csv')

# Aaand print
layout=go.Layout(barmode='stack',
                 xaxis=dict(title='Län'), yaxis=dict(title='Per 100 000 invånare'))
fig=go.Figure(data=trace, layout=layout)
py.plotly.plot(fig, filename='Personal')