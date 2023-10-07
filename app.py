import os
import atexit
from flask import Flask, render_template, Response, request, jsonify
import datetime
import data
import tensorflow as tf
from apscheduler.schedulers.background import BackgroundScheduler
import pandas as pd
import numpy as np
from tensorflow import keras
from keras.models import load_model
from transformers import TFBertModel
from scipy import signal

# Initialize Flask

app = Flask(__name__, template_folder="templetes")


@app.route('/', methods=['GET'])
def index():
    return render_template('main.html')


@app.route('/predication/<date>', methods=['GET'])
def predict(date):
    global prediction_model  # Use the global variable

    file_path = f'downloads/prediction/{date.replace("-", "")}.csv'

    output_y = []
    output_x = []
    if not os.path.exists(file_path):
        file_path = f'downloads/processed/{date.replace("-", "")}.csv'
        data.fetch_data(date)
        df = pd.read_csv(file_path)
        custom_objects = {'TFBertModel': TFBertModel}
        prediction_model = load_model(
            'models/kp_prediction.h5', custom_objects)

        output = prediction_model.predict(df)

        output_y = signal.resample(output, 500)
        output_x = np.linspace(0, len(output), len(output))
        out_df = pd.DataFrame({'x': output_x, 'y': output_y})
        out_df.to_csv(file_path.replace('processed', 'prediction'))
    else:
        df = pd.read_csv(file_path)
        output_y = df['y'].values
        output_x = np.linspace(0, 24, len(output_y))

    # data1 = np.linspace(0, 500, 500)
    return jsonify({"x": output_x.tolist(), 'y': output_y.tolist()})


@app.route('/forcast/<date>/<size>', methods=['GET'])
def forcast_api(date, size):
    date2 = f'{date[0:4]}-{date[4:6]}-{date[6:]}'
    data.fetch_data(date2)
    model = tf.keras.models.load_model('models/forecasting_model.h5')
    df = pd.read_csv(f'downloads/processed/{date}.csv')
    columns = df.columns
    output = data.forcast_data(df.values[-70:], model, int(size))
    output = df.values[-70:]
    return jsonify({"columns name": columns.to_list(), 'data': output.tolist()})

@app.route("/data/<date>", methods = ['GET'])
def return_data(date):
    date2 = f'{date[0:4]}-{date[4:6]}-{date[6:]}'
    data.fetch_data(date2)
    df = pd.read_csv(f'downloads/processed/{date}.csv')
    dict_df = df.to_dict(orient='list')
    return jsonify(dict_df)


def update_data():
    current_date = datetime.date.today()
    yesterday = current_date - datetime.timedelta(days=1)
    formatted_date = yesterday.strftime("%Y-%m-%d")
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=data.fetch_data(
        formatted_date), trigger="interval", days=1)
    scheduler.start()
    atexit.register(lambda: scheduler.shutdown())


if __name__ == '__main__':
    app.run(debug=True)
