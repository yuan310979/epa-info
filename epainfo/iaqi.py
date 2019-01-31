class IAQI:
    def __init__(self):
        # Corresponding IAQI chart
        self.O3 = [0, 0, 0.125, 0.164, 0.204, 0.404, 0.504, 0.604]
        self.O3_8hr = [0, 0.054, 0.07, 0.085, 0.105, 0.20, 0.20, 0.20]
        self.PM25 = [0, 15.4, 35.4, 54.4, 150.4, 250.4, 350.4, 500.4]
        self.PM10 = [0, 54, 125, 254, 354, 424, 504, 604]
        self.CO = [0, 4.4, 9.4, 12.4, 15.4, 30.4, 40.4, 50.4]
        self.SO2 = [0, 35, 75, 185, 304, 604, 804, 1004]
        self.NO2 = [0, 53, 100, 360, 649, 1249, 1649, 2049]

    def get_iaqi_params(self, target, _val):
        index = -1
        for idx, val in enumerate(target):
            if _val <= val:
                index = idx
                break
        return _val, target[idx-1], target[idx], 50*(idx-1), 50*idx 

    def transfer2IAQI(self, target, *args):
        if target == "O3":
            O3_hr, O3_8hr = args
            val1, val2 = 0, 0
            if O3_hr >= self.O3[2]:
                val1 = self.IAQI_formula(*self.get_iaqi_params(self.O3, O3_hr))
            if O3_8hr <= self.O3_8hr[-3]:
                val2 = self.IAQI_formula(*self.get_iaqi_params(self.O3_8hr, O3_8hr))
            return val1 if val1 > val2 else val2
        elif target == "PM2.5":
            return self.IAQI_formula(*self.get_iaqi_params(self.PM25, args[0]))
        elif target == "PM10":
            return self.IAQI_formula(*self.get_iaqi_params(self.PM10, args[0]))
        elif target == "CO":
            return self.IAQI_formula(*self.get_iaqi_params(self.CO, args[0]))
        elif target == "SO2":
            return self.IAQI_formula(*self.get_iaqi_params(self.SO2, args[0]))
        elif target == "NO2":
            return self.IAQI_formula(*self.get_iaqi_params(self.NO2, args[0]))
        else:
            print("[Error] Pollution type not found.")
            exit()

    @staticmethod
    def IAQI_formula(Cp, BPhi, BPlo, IAQIh, IAQIl):
        return (IAQIh-IAQIl) / (BPhi-BPlo) * (Cp-BPlo) + IAQIl

if __name__ == '__main__':
    m = IAQI()
    v = m.transfer2IAQI('O3', 0.52, 0.1)
    print(v)
