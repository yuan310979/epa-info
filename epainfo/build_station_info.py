import pandas as pd
import pickle

from pathlib import Path
from pprint import pprint as pp

def build_station_info():
    dataset_path = Path('../raw_data/')
    stations_info_path = dataset_path / '空氣品質測站基本資料.csv'
    stations_info_csv = pd.read_csv(stations_info_path, encoding='big5')

    ret = {}
    for row in stations_info_csv.dropna(how='all', subset=['經度', '緯度']).iterrows():
        # '新竹': {'lat': 24.805619, 'lon': 120.972075}
        station_name = row[1][3]
        ret[station_name]= {'lon': row[1][6], 'lat': row[1][7]}

    return ret 

def save_pickle(path, obj):
    path = Path(path)
    if not path.exists():
        path.parent.mkdir() 
    path.write_bytes(pickle.dumps(obj))

def load_pickle(path):
    path = Path(path)
    return pickle.load(path.open('rb'))

if __name__ == '__main__':
    # store stations info to pickle
    stations_info = build_station_info() 
    save_pickle('../pickle_data/stations_info.pickle', stations_info)

    # load pickle
    st = load_pickle('../pickle_data/stations_info.pickle')
    pp(st)
