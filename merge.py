# import av moduler
import sys
import plotly.offline as pyofl
import plotly.graph_objs as go
import pandas as pd
import re

sys.stdout.reconfigure(encoding='UTF-8')

vis_data = pd.read_csv(r"C:\Users\steblo\Desktop\Nackademin\Dropbox\BI-relaterade programspråk\Grupparbete\vis_export.csv", sep=';', encoding='UTF-8')

question_data = pd.read_csv(r"C:\Users\steblo\Desktop\Nackademin\Dropbox\BI-relaterade programspråk\Grupparbete\questions_truncated.csv", sep=';', encoding='UTF-8')

combined_data = vis_data.merge(question_data, on='Diagramrubrik')

# print(combined_data.head(5))

# skriver ut data frame till fil (delvis för test-syfte) 
combined_data.to_csv(r'C:\Users\steblo\Desktop\Nackademin\Dropbox\BI-relaterade programspråk\Grupparbete\truncated_data.csv', sep=';', encoding='utf-8-sig', index=False)

# vis_data = pd.read_csv(r"C:\Users\steblo\Desktop\combined_data.csv", sep=',', encoding='UTF-8')


    