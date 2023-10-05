from datetime import datetime
import requests
import os
import gzip
import netCDF4
import numpy as np
import pandas as pd

def ftech_data(start_date_string): 
    #date as "2021-10-05"
    if not os.path.exists("downloads/processed/"+modified_string+".csv"):
        modified_string = start_date_string.replace("-", "")
        start_date_obj = datetime.strptime(start_date_string, '%Y-%m-%d')
        start_timestamp = int(start_date_obj.timsestamp())
        end_timestamp = int(start_timestamp+172799999)
        api_url = "https://www.ngdc.noaa.gov/dscovr-data-access/files?start_date="+str(start_timestamp)+"&end_date="+str(end_timestamp)
        try:
            response = requests.get(api_url)

            if response.status_code == 200:
                data = response.json()
                # print(data[str(modified_string)]["mg1"])
            else:
                print(f"Error: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}")
        except ValueError as e:
            print(f"JSON decoding error: {e}")
        

        response = requests.get(data[str(modified_string)]["mg1"])
        input_path = os.path.join("downloads/raw_data", (str(modified_string) + ".nc.gz"))
        output_path = os.path.join("downloads/raw_data", (str(modified_string) + ".nc"))

        open(input_path, "wb").write(response.content)
        with gzip.open(input_path, 'rb') as compressed_file:
            with open(output_path, 'wb') as extracted_file:
                extracted_file.write(compressed_file.read())

        data_nc = netCDF4.Dataset(output_path)
        dsc_cols = ['time', 'bx_gse','by_gse', 'bz_gse', 'bx_gsm', 'by_gsm', 'bz_gsm']
        arrays = {}
        for col in dsc_cols:
            var = data_nc.variables[col]
            arrays[f'dsc_{col}'] = np.array(var[::92])
        data_df= pd.DataFrame(arrays)
        data_df.to_csv("downloads/processed/"+modified_string+".csv", index=False)
        os.remove(input_path)
        os.remove(output_path)



