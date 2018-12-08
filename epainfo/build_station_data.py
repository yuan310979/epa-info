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
    
    target_path = sorted(dataset_path.glob(f'**/*.{ftype}'))
    if ftype == 'xls':
        for p in tqdm(target_path):
            station_name = re.findall(r"年(.*)站", p.name)[0] 
            if ret.get(station_name) == None:
                ret[station_name] = {}
            xls = pd.read_excel(p)
            for row in xls.iterrows():
                if(isinstance(row[1][0], datetime)):
                    date = datetime.strptime(str(row[1][0]), "%Y-%m-%d %H:%M:%S").date()
                else:
                    date = datetime.strptime(row[1][0], "%Y/%m/%d").date() 
                key = row[1][2]
                if(ret.get(station_name).get(date) == None):
                    ret[station_name][date] = {}
                ret[station_name][date][key] = list(row[1][3:])
    elif ftype == 'csv':
        for p in tqdm(target_path):
            station_name = re.findall(r"年(.*)站", p.name)[0] 
            if ret.get(station_name) == None:
                ret[station_name] = {}
            csv = pd.read_csv(p, encoding='big5')
            for row in csv.iterrows():
                date = datetime.strptime(row[1][0], "%Y/%m/%d").date() 
                key = row[1][2]
                if(ret.get(station_name).get(date) == None):
                    ret[station_name][date] = {}
                ret[station_name][date][key] = list(row[1][3:])
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
    start_year = 104 
    end_year = 104 
    d = build_station_data_by_year(start_year, end_year)
    save_pickle('../pickle_data/epa-104.pickle', d)
