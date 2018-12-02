import pickle
import numpy as np

from epainfo import EPAInfo
from pathlib import Path
from tqdm import tqdm
from pprint import pprint as pp
from itertools import product

start_lon = 120.00
start_lat = 21.80
lon_range = 2
lat_range = 3.5
step = 0.01

"""
start_lon = 121.50
start_lat = 25.00
lon_range = 0.1
lat_range = 0.1
step = 0.01
"""

grids = {}

EPA = EPAInfo()
EPA.load_station_data_from_pickle('../pickle_data/stations_info.pickle')
EPA.load_aqi_data_from_pickle('../pickle_data/epa-104.pickle')

keys = product(np.arange(0, lat_range,step) + start_lat, np.arange(0, lon_range, step) + start_lon)
keys = [(round(key[0], 2), round(key[1], 2)) for key in keys]

for key in tqdm(keys):
    st_name = EPA.get_nearest_station(*key)
    grids[key] = EPA.get_data_by_station_name(st_name)

feature_data_path = Path('../input_feature/aqi.pickle')

if not feature_data_path.parent.exists():
    feature_data_path.parent.mkdir()

feature_data_path.write_bytes(pickle.dumps(grids))

# d = pickle.load(feature_data_path.open('rb'))
