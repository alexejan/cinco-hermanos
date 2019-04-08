import sys
import numpy as np
import pandas as pd
import sys
import os

sys.stdout.reconfigure(encoding='utf-8')


arbetslosa = pd.read_csv('arbet.csv', sep=';')  # Läser in källdatan
arbetslosa = arbetslosa.iloc[1:]                 # Hoppar över första raden
arbetslosa.set_index('Län', inplace=True)       # Sätter länkolumnen som index
arbetslosa['Totalt'] = arbetslosa['Öppet arbetslösa'] + arbetslosa['Progr med akt.stöd']    # Summerar ihop två kolumner till en
arbetslosa.to_pickle('arbetslosa.pickle')     # Sparar det till en picklefil för användning till beräkning av CNI