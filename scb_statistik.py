import sys
import os
import re
import numpy as np
import pandas as pd
import pickle
import collections
import time
from pyscbwrapper import SCB

sys.stdout.reconfigure(encoding='utf-8')
os.chdir('c:/users/Kalle/documents/skola/programmering/kursprojekt/grupparbete')


def get_tables(a, b, c, d=''):
    scb = SCB('sv', a, b, c, d)
    regioner = scb.get_variables()['region']
    koder = scb.info()['variables'][0]['values'][1:]
    r = re.compile(r'.* län')
    lan = list(filter(r.match, regioner))
    orter = [x for x in regioner if x not in lan][1:]
    ortkoder = [x for x in koder if len(x) != 2]
    lanskoder = [x for x in koder if len(x) == 2]
    ort_och_koder = dict(zip(ortkoder, orter))
    lan_och_koder = dict(zip(lanskoder, lan))
    return scb, ort_och_koder, lan_och_koder

# Hämtar en variabel för hur många gånger en loop i get_data ska köras per län,
# dvs hur många datapunkter per län det finns.

def get_loops(tabell):
    cnt = collections.Counter()
    lis=[]
    for i in range(len(tabell)):
        lis.append(tabell[i]['key'][0][:2])             # lägger in de två första tecknen i läns/ort-koden i lis
    for i in lis:
        cnt[i] += 1                                     # lägger till hur många gånger ett visst län förekommer
    return cnt

def get_data(scb_data):
    tabell = scb_data.get_data()['data']
    loops = get_loops(tabell)
    sum_per_lan = []
    for i in range(21):
        temp = []
        for j in range(list(loops.values())[i]):
            temp.append(int(float(tabell[j+sum(list(loops.values())[0:i])]['values'][0])))
        sum_per_lan.append(sum(temp))
        temp = []
    return sum_per_lan


alder = [(str(x) + ' år') for x in range(65, 100)]
alder.append('100+ år')
scb, ort_koder_scb, lan_koder_scb = get_tables('BE', 'BE0101', 'BE0101S', 'HushallT08')
scb.set_query(region=list(lan_koder_scb.values()), år=['2018'], hushållsställning='antal ensamboende personer',
              ålder=alder)
scb_varden = get_data(scb)
ensamboende = pd.DataFrame(scb_varden, index=lan_koder_scb.values(), columns=['Antal Ensamboende 65+'])


scb, ort_koder_scb, lan_koder_scb = get_tables('BE', 'BE0101', 'BE0101A', 'BefolkningNy')
scb.set_query(region=lan_koder_scb.values(), år=['2018'], tabellinnehåll=['Folkmängd'],
              ålder=[str(x) + ' år' for x in range(16, 65)])
scb_varden = get_data(scb)
befolkning_16_64 = pd.DataFrame(scb_varden, index=lan_koder_scb.values(), columns=['Befolkning 16-64'])


scb, ort_koder_scb, lan_koder_scb = get_tables('BE', 'BE0101', 'BE0101A', 'BefolkningNy')
scb.set_query(region=lan_koder_scb.values(), år=['2018'], tabellinnehåll=['Folkmängd'])
scb_varden = get_data(scb)
befolkning = pd.DataFrame(scb_varden, index=lan_koder_scb.values(), columns=['Befolkning Total'])


scb, ort_koder_scb, lan_koder_scb = get_tables('BE', 'BE0101', 'BE0101A', 'BefolkningNy')
scb.set_query(region=lan_koder_scb.values(), år=['2018'], tabellinnehåll=['Folkmängd'],
              ålder=[str(x) + ' år' for x in range(0, 5)])
scb_varden = get_data(scb)
befolkning_0_4 = pd.DataFrame(scb_varden, index=lan_koder_scb.values(), columns=['Befolkning 0-4'])


scb, ort_koder_scb, lan_koder_scb = get_tables('BE', 'BE0101', 'BE0101A', 'BefolkningNy')
scb.set_query(region=lan_koder_scb.values(), år=['2017'], tabellinnehåll=['Folkmängd'],
              ålder=[str(x) + ' år' for x in range(26, 65)])
scb_varden = get_data(scb)
befolkning_25_64 = pd.DataFrame(scb_varden, index=lan_koder_scb.values(), columns=['Befolkning 25-64'])


time.sleep(15)


scb, ort_koder_scb, lan_koder_scb = get_tables('LE', 'LE0102', 'LE0102J', 'LE0102T19N')
scb.set_query(region=list(lan_koder_scb.values()), år=['2017'], barnensålder='0-17 år',
              familjetyp=['ensamstående mor', 'ensamstående far'], antalbarn='totalt ')
scb_varden = get_data(scb)
ensamstaende = pd.DataFrame(scb_varden, index=lan_koder_scb.values(), columns=['Ensamstående föräldrar'])


scb, ort_koder_scb, lan_koder_scb = get_tables('UF', 'UF0506', 'Utbildning')
scb.set_query(region=list(lan_koder_scb.values()), år=['2017'], ålder=[(str(x) + ' år')  for x in range(26, 65)],
              utbildningsnivå=['förgymnasial utbildning kortare än 9 år', 'förgymnasial utbildning, 9 (10) år'])
scb_varden = get_data(scb)
lagutbildade = pd.DataFrame(scb_varden, index=lan_koder_scb.values(), columns=['Lågutbildad'])


scb, ort_koder_scb, lan_koder_scb = get_tables('BE', 'BE0101', 'BE0101J', 'FlyttFodReg')
scb.set_query(region=list(ort_koder_scb.values()), år=['2018'], tabellinnehåll='Samtliga inflyttningar')
scb_varden = get_data(scb)
nyinflyttade = pd.DataFrame(scb_varden, index=lan_koder_scb.values(), columns=['Nyinflyttad'])


arbetslosa = pd.read_pickle('arbetslosa.pickle')
utlandsfodda = pd.read_pickle('utlandsfodda.pickle')


befolkning['Befolkning 0-4'] = befolkning_0_4['Befolkning 0-4']
befolkning['Befolkning 16-64'] = befolkning_16_64['Befolkning 16-64']
befolkning['Befolkning 25-64'] = befolkning_25_64['Befolkning 25-64']
befolkning['Utlandsfödda urval'] = utlandsfodda['Utlandsfödda']
befolkning['Ensamboende 65+'] = ensamboende['Antal Ensamboende 65+']
befolkning['Ensamstående föräldrar'] = ensamstaende['Ensamstående föräldrar']
befolkning['Nyinflyttad'] = nyinflyttade['Nyinflyttad']
befolkning['Arbetslös'] = arbetslosa['Totalt']
befolkning['Lågutbildad'] = lagutbildade['Lågutbildad']

befolkning.to_csv('befolkning.csv')