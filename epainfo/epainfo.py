import pickle
import re

from math import sin, cos, sqrt, atan2, radians
from pathlib import Path
from tqdm import tqdm
from datetime import datetime, timedelta, date
from pprint import pprint as pp

class EPAInfo:

    def __init__(self):
        self.station_data = None
        self.aqi_data = None

    def load_station_data_from_pickle(self, path):
        path = Path(path)
        self.station_data = pickle.load(Path(path).open('rb'))
    
    def load_aqi_data_from_pickle(self, path):
        path = Path(path)
        self.aqi_data = pickle.load(Path(path).open('rb'))

    def get_nearest_station(self, lat, lon):
        ret = None
        min_dis = 10 ** 10
        for k, v in self.station_data.items():
            dis = self.latlon_distance(lat, lon, v['lat'], v['lon'])
            if dis < min_dis:
                min_dis = dis
                ret = k
        return ret

    def get_aqi_data_in_period(self, st_name, aqi_type, st_time, ed_time):
        aqi = ['CO', 'SO2', 'NO', 'NO2', 'NOx', 'O3', 'PM2.5', 'PM10']
        ret = [] 
        d = self.get_data_by_station_name(st_name)
        if aqi_type in aqi:
            with tqdm(total=(ed_time-st_time)/timedelta(days=1)) as pbar:
                while st_time != ed_time:
                    pp(st_time)
                    try:
                        for i in d[st_time][aqi_type]:
                            if isinstance(i, int) or isinstance(i, float):
                                ret.append(i)
                            elif(isinstance(i, str)):
                                i = re.findall('[0-9]+[\.]{0,1}[0-9]*', i)[0]
                                ret.append(i)
                            else:
                                print('[Error]\t(get_aqi_data_in_period) value error!')
                    except Exception as ex:
                        print(ex)
                    finally:
                        st_time += timedelta(days=1)
                        pbar.update(1)
            return ret
        else:
            print('[Error]\t(get_aqi_data_in_period) type not found!')

    def get_stations(self):
        return self.station_data

    def get_data_by_station_name(self, s_name):
        try:
            return self.aqi_data[s_name] 
        except:
            print(f"[Error]\t{s_name} is not exist!")
            return None

    @staticmethod
    def latlon_distance(lat1:float, lon1:float, lat2:float, lon2:float) -> float:
        # Ref: https://www.movable-type.co.uk/scripts/latlong.html 
        R = 6371.0
        phi1 = radians(lat1)
        phi2 = radians(lat2)
        phi = radians(lat2-lat1)
        sigma = radians(lon2-lon1)

        a = sin(phi/2)**2 + cos(phi1) * cos(phi2) * sin(sigma/2)**2
        c = 2 * atan2(sqrt(a), sqrt(1-a))

        return R * c

if __name__ == "__main__":
    EPA = EPAInfo() 
    EPA.load_station_data_from_pickle('../pickle_data/stations_info.pickle')
    EPA.load_aqi_data_from_pickle('../pickle_data/epa-104.pickle')

    st = EPA.get_nearest_station(24.32323, 121.456465)
    #  print(EPA.get_data_by_station_name(st))
    #  print(st)
    d = EPA.get_aqi_data_in_period(st, 'SO2', datetime(2015, 1, 1), datetime(2015, 2, 1))
    pp(d)
