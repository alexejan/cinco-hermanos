# import av moduler
import sys
import plotly.offline as pyofl
import plotly.graph_objs as go
import pandas as pd

# ser till att rätt encoding sätts för stdout
sys.stdout.reconfigure(encoding='UTF-8')

# läser in data från .csv-filer och lagrar dem i  data frames
vis_data = pd.read_csv(r"C:\Users\steblo\Desktop\Nackademin\Dropbox\BI-relaterade programspråk\Grupparbete\Kod\cinco-hermanos\vis_export.csv", sep=';', encoding='UTF-8')
question_data = pd.read_csv(r"C:\Users\steblo\Desktop\Nackademin\Dropbox\BI-relaterade programspråk\Grupparbete\Kod\cinco-hermanos\grouped_questions_SS.csv", sep=';', encoding='UTF-8')

# merge-operation för att joina data från vis_export (källdata från vård i siffror) med egendefinierade frågegrupperingar (baserat på indikatorer från Socialstyrelsen)
combined_data = vis_data.merge(question_data, on='Diagramrubrik')

# skriver ut data frame direkt ovan till ny .csv-fil som sen kan läsas in från andra program  
combined_data.to_csv(r'C:\Users\steblo\Desktop\Nackademin\Dropbox\BI-relaterade programspråk\Grupparbete\Kod\cinco-hermanos\truncated_data_SS.csv', sep=';', encoding='utf-8-sig', index=False)