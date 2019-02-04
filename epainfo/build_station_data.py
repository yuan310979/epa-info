import pandas as pd
import pickle
import re

from pathlib import Path
from pprint import pprint as pp
from typing import Dict, Any
from datetime import datetime
from itertools import chain
# from tqdm import tqdm_notebook as tqdm
from tqdm import tqdm
from collections import defaultdict

def build_station_data_by_year(start_year:int, end_year:int):
    ret = {}
    for y in tqdm(range(start_year, end_year+1)):
        ret = build_station_data(y, ret)
    return ret

def build_station_data(year:str, ret:Dict) -> Dict[str, Dict[datetime, Dict[str, Any]]]:
    dataset_path = Path(f'../raw_data/{year}')
    target_path = sorted(dataset_path.glob('**/*.*')) 
    assert len(target_path) >= 2 

    ftype = target_path[1].suffix[1:] 

    assert ftype != 'ods'
    
    attr = ['AMB_TEMP',
            'CO',
            'NO',
            'NO2',
            'NOx',
            'O3',
            'PH_RAIN',
            'PM10',
            'PM2.5',
            'RAINFALL',
            'RAIN_COND',
            'RH',
            'SO2',
            'WD_HR',
            'WIND_DIREC',
            'WIND_SPEED',
            'WS_HR']

    record = {}
    for _attr in attr:
        record[_attr] = [-1] * 24

    _date = None
    target_path = sorted(dataset_path.glob(f'**/*.{ftype}'))
    if ftype == 'xls':
        for p in tqdm(target_path):
            station_name = re.findall(r"年(.*)站", p.name)[0] 
            if ret.get(station_name) == None:
                ret[station_name] = {}
            xls = pd.read_excel(p)
            for row in xls.iterrows():
                date = None
                if(isinstance(row[1][0], datetime)):
                    date = datetime.strptime(str(row[1][0]), "%Y-%m-%d %H:%M:%S").date()
                else:
                    date = datetime.strptime(row[1][0], "%Y/%m/%d").date() 
                if _date != date:
                    record = {}
                    for _attr in attr:
                        record[_attr] = [-1] * 24
                key = row[1][2]
                record[key] = list(row[1][3:])
                ret[station_name][date] = record
                #  if(ret.get(station_name).get(date) == None):
                    #  ret[station_name][date] = {}
                #  ret[station_name][date][key] = list(row[1][3:])
                _date = date
    elif ftype == 'csv':
        for p in tqdm(target_path):
            station_name = re.findall(r"年(.*)站", p.name)[0] 
            if ret.get(station_name) == None:
                ret[station_name] = {}
            csv = pd.read_csv(p, encoding='big5')
            for row in csv.iterrows():
                date = datetime.strptime(row[1][0], "%Y/%m/%d").date() 
                key = row[1][2]
                if _date != date:
                    record = {}
                    for _attr in attr:
                        record[_attr] = [-1] * 24
                #  if(ret.get(station_name).get(date) == None):
                    #  ret[station_name][date] = {}
                record[key] = list(row[1][3:])
                ret[station_name][date] = record
                #  ret[station_name][date][key] = list(row[1][3:])
                _date = date
    return ret

def save_pickle(path, obj):
    path = Path(path)
    if not path.parent.exists():
        path.parent.mkdir() 
    path.write_bytes(pickle.dumps(obj))

def load_pickle(path):
    path = Path(path)
    return pickle.load(path.open('rb'))

if __name__ == '__main__':
    start_year = 89 
    end_year = 106 
    d = build_station_data_by_year(start_year, end_year)
    save_pickle('../pickle_data/epa-89-106.pickle', d)
