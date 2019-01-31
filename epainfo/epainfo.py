import pickle
import re

from math import sin, cos, sqrt, atan2, radians, degrees, isnan
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

    def get_direction_and_direction_to_station(self, st_name, lat, lon):
        ret = []
        st = self.station_data[st_name]
        ret.append(self.bearing_direction(lat, lon, st['lat'], st['lon']))
        ret.append(self.latlon_distance(lat, lon, st['lat'], st['lon']))
        return ret

    def get_aqi_data_in_period(self, st_name, aqi_types, st_time, ed_time):
        aqi = ['CO', 'SO2', 'NO', 'NO2', 'NOx', 'O3', 'PM2.5', 'PM10']
        st_date = st_time.date()
        ed_date = ed_time.date()
        st_hour = st_time.hour
        ed_hour = ed_time.hour
        ret = [] 
        d = self.get_data_by_station_name(st_name)
        prev_val = [0 for _ in range(len(aqi_types))] 
        #  with tqdm(total=(ed_date-st_date)/timedelta(days=1)) as pbar:
        while st_date != ed_date + timedelta(days=1):
            try:
                st_hour = 0
                ed_hour = 24
                if st_date == st_time.date():
                    st_hour = st_time.hour+1
                if st_date == ed_time.date():
                    ed_hour = ed_time.hour+1
                for t in range(st_hour, ed_hour):
                    tmp = []
                    for aqi_index, aqi_type in enumerate(aqi_types):
                        i = d[st_date][aqi_type][t]
                        if isinstance(i, int) or isinstance(i, float):
                            if isnan(i):
                                i = prev_val[aqi_index]
                            tmp.append(i)
                        elif isinstance(i, str):
                            i = float(re.findall('[0-9]+[\.]{0,1}[0-9]*', i)[0])
                            tmp.append(i)
                        else:
                            print('[Error]\t(get_aqi_data_in_period) value error!')
                        prev_val[aqi_index] = i
                    ret.append(tmp)
            except Exception as ex:
                raise Exception
            finally:
                st_date += timedelta(days=1)
                    #  pbar.update(1)
        return ret

    def get_stations(self):
        return self.station_data

    def get_data_by_station_name(self, s_name):
        try:
            return self.aqi_data[s_name] 
        except:
            print(f"[Error]\t{s_name} is not exist!")
            return None

    @staticmethod
    def bearing_direction(lat1:float, lon1:float, lat2:float, lon2:float):
        lat1, lon1, lat2, lon2 = radians(lat1), radians(lon1), radians(lat2), radians(lon2)
        delta_lon = lon2 - lon1
        X = cos(lat2) * sin(delta_lon)
        Y = cos(lat1) * sin(lat2) - sin(lat1)*cos(lat2)*cos(delta_lon)
        return degrees(atan2(X, Y))

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
    b = EPA.bearing_direction(39.099912, -94.581213, 38.627089, -90.200203)
    EPA.load_station_data_from_pickle('../pickle_data/stations_info.pickle')
    EPA.load_aqi_data_from_pickle('../pickle_data/epa-104.pickle')

    st = EPA.get_nearest_station(24.32323, 121.456465)
    #  print(EPA.get_data_by_station_name(st))
    print(st)
    d = EPA.get_aqi_data_in_period(st, ['PM2.5', 'SO2', 'PM10'], datetime(2015, 10, 1, 1, 0), datetime(2015, 10, 26, 2, 0))
    pp(d)
    pp(len(d))
