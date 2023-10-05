import os
import requests
import numpy as np
import pandas as pd
import cdflib
import glob
from datetime import datetime
from pandas.core.arrays.timedeltas import timedelta


class DataGenerator:
    def string_to_date(self, x):
        my_date = datetime(int(x[:4]), int(x[4:6]), int(x[6:]))
        return my_date

    def date_to_string(self, x):
        if x.day < 10:
            day = '0' + str(x.day)
        else:
            day = str(x.day)
        if x.month < 10:
            month = '0' + str(x.month)
        else:
            month = str(x.month)
        return str(x.year) + month + day

    def to_datetime(self, date1, date2):
        delta = (date1 - date2)
        timestamp = delta / np.timedelta64(1, 's')
        return timestamp

    def data_processing(self, path):
        cdf = cdflib.cdf_to_xarray(os.path.join(self.mainPath, ("uploads/Downloads" + path + ".cdf")),
                                   to_datetime=True)
        df = pd.DataFrame({
            "BGSM1": [], "BGSM2": [], "BGSM3": [],
            "BGSE1": [], "BGSE2": [],"BGSE3": [],
            "Range": [], "Label": []})

        startIndex = 0
        lst = [0, 0, 0, 0, 0, 0, 0]
        counter = 0

        for i in range(len(cdf['Epoch'][:])):
            if (self.to_datetime(cdf['Epoch'][i], cdf['Epoch'][startIndex])) < 1200:
                lst[0] += cdf['BGSE'][i][0]
                lst[1] += cdf['BGSE'][i][1]
                lst[2] += cdf['BGSE'][i][2]
                lst[3] += cdf['BGSM'][i][0]
                lst[4] += cdf['BGSM'][i][1]
                lst[5] += cdf['BGSM'][i][2]
                lst[6] += cdf['RANGE'][i]
                counter += 1
            else:
                dic = {
                    "BGSM1": [lst[0].item(0) / counter], "BGSM2": [lst[1].item(0) / counter], "BGSM3": [lst[2].item(0) / counter],
                    "BGSE1": [lst[3].item(0) / counter], "BGSE2": [lst[4].item(0) / counter], "BGSE3": [lst[5].item(0) / counter],
                    "Range": [round(lst[6].item(0) / counter)],"Label": 0
                }
                df_dummy = pd.DataFrame(dic)
                df = pd.concat([df, df_dummy])
                startIndex = i
                lst = [0, 0, 0, 0, 0, 0, 0]
                counter = 0
        df = df.reset_index()
        df = df.drop(['index'], axis=1)
        df.to_csv(os.path.join(self.mainPath, "uploads/CSV/{path}.csv".format(path=path)))
        os.remove(os.path.join(self.mainPath, ("uploads/Downloads" + path + ".cdf")))

    def generate(self):
        self.mainPath = os.path.dirname(os.path.realpath(__file__))
        generalPath = os.path.join(self.mainPath, "uploads/CSV/*.csv")
        my_list = []
        for fname in glob.glob(generalPath):
            my_list.append(os.path.basename(fname)[10:18])
        self.lastDate = max(my_list)
        general = 'wi_h2_mfi_'
        version = '05'
        date = self.string_to_date(self.lastDate)
        response = requests.get("http://asdasd.com")
        while response.status_code == 200:
            date = date + timedelta(days=1)
            string = 'https://cdaweb.gsfc.nasa.gov/pub/data/wind/mfi/mfi_h2/{year}/wi_h2_mfi_{date}_v{version}.cdf'.format(
                year=date.year,
                date=self.date_to_string(date), version=version)
            response = requests.get(string)
            v = 4
            while (response.status_code == 404 and v != 0):
                string = 'https://cdaweb.gsfc.nasa.gov/pub/data/wind/mfi/mfi_h2/{year}/wi_h2_mfi_{date}_v0{version}.cdf'.format(
                    year=date.year,
                    date=self.date_to_string(date), version=str(v))
                response = requests.get(string)
                v -= 1
            path = "/{general}{date}_v{version}".format(
                general=general, date=self.date_to_string(date), version=version)
            if response.status_code == 200:
                string = os.path.join(self.mainPath, ("uploads/Downloads" + path + ".cdf"))

                print(string)
                open(string, "wb").write(response.content)
                print("################10")
                self.data_processing(path)
                print("################11")
