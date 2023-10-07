from datetime import datetime
import requests
import os
import gzip
import netCDF4
import numpy as np
import pandas as pd
import tensorflow as tf

def fetch_data(start_date_string):
    # date as "2021-10-05"
    print(start_date_string)
    modified_string = start_date_string.replace("-", "")
    if not os.path.exists("downloads/processed/"+modified_string+".csv"):
        print("downloads/processed/"+modified_string+".csv")
        start_date_obj = datetime.strptime(start_date_string, '%Y-%m-%d')
        start_timestamp = int(start_date_obj.timestamp()) * 1000
        end_timestamp = int(start_timestamp+172799999000)
        api_url = "https://www.ngdc.noaa.gov/dscovr-data-access/files?start_date=" + \
            str(start_timestamp)+"&end_date="+str(end_timestamp)
        try:
            response = requests.get(api_url)

            if response.status_code == 200:
                data = response.json()
            else:
                print(f"Error: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}")
        except ValueError as e:
            print(f"JSON decoding error: {e}")

        response = requests.get(data[str(modified_string)]["mg1"])

        input_path = os.path.join(
            "downloads", "raw_data", (str(modified_string) + ".nc.gz"))
        output_path = os.path.join(
            "downloads", "raw_data", (str(modified_string) + ".nc"))

        open(input_path, "wb").write(response.content)
        with gzip.open(input_path, 'rb') as compressed_file:
            with open(output_path, 'wb') as extracted_file:
                extracted_file.write(compressed_file.read())

        data_nc = netCDF4.Dataset(output_path)
        dsc_cols = ['bx_gse', 'by_gse', 'bz_gse', 'bx_gsm', 'by_gsm', 'bz_gsm']
        arrays = {}
        for col in dsc_cols:
            var = data_nc.variables[col]
            arrays[f'dsc_{col}'] = np.array(var[::92])
        data_df = pd.DataFrame(arrays)
        processed_data = sequence_creation(data_df.values)
        model = tf.keras.models.load_model("models/mapping_mag.h5")
        mapped_data = model.predict(processed_data)


        mapped_data.to_csv("downloads/processed/" +
                       modified_string+".csv", index=False)
        # os.remove(input_path)
        # os.remove(output_path)


def forcast_data(data, model, size=100):
    n_features = data.shape[1]
    output = np.zeros((size, data.shape[1]))
    for i in range(size):
        point = model(np.array([data]))[0]
        output[i] = point
        data = np.append(data[1:], point).reshape(-1, n_features)

    return output




def sequence_creation(data, num_features=6, sequence_length=10):
  sequences = []
  for i in range(len(data) - sequence_length + 1):
    sequence = data[i:i + sequence_length]
    sequences.append(sequence)

  sequences = np.array(sequences)
  output = sequences.reshape(-1, sequence_length, num_features)

  return output

