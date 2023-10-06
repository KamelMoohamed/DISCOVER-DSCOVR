import os
import atexit
from flask import Flask, render_template, Response, request, jsonify
import datetime
import data
# import tensorflow as tf
from apscheduler.schedulers.background import BackgroundScheduler
import pandas as pd
import numpy as np
from tensorflow.keras.models import load_model
from transformers import TFBertModel
from scipy import signal


app = Flask(__name__, template_folder="templetes")


@app.route('/', methods=['GET'])
def index():
    return render_template('main.html')


@app.route('/predication/<date>', methods=['GET'])
def predict(date):
    data.fetch_data(date)
    file_path = f'downloads/processed/{date.replace("-", "")}'
    df = pd.read_csv(file_path)

    custom_objects = {'TFBertModel': TFBertModel}

    model = load_model('models/kp_prediction.h5', custom_objects)
    output = model(df.values)

    output_y = signal.resample(output, 500)
    output_x = np.linspace(0, len(output), len(output))

    data1 = np.linspace(0,500,500)    
    return jsonify({"x":output_x.tolist(), 'y':output_y.tolist()})


@app.route('/forcast/<date>/<size>', methods=['GET'])
def forcast_api(date,size):
    date2 = f'{date[0:4]}-{date[4:6]}-{date[6:]}'
    data.fetch_data(date2)
    # model = tf.keras.models.load_model('models\forecasting_model.h5')
    df = pd.read_csv(f'downloads/processed/{date}.csv')
    df.drop(columns='dsc_time', axis = 1, inplace = True)
    columns = df.columns
    # output = data.forcast_data(df.values[-70:],size)
    output = df.values[-70:]
    return jsonify({"columns name": columns.to_list(),'data' :output.tolist()})


def update_data():
    current_date = datetime.date.today()
    yesterday = current_date - datetime.timedelta(days=1)
    formatted_date = yesterday.strftime("%Y-%m-%d")
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=data.fetch_data(formatted_date), trigger="interval", days=1)
    scheduler.start()
    atexit.register(lambda: scheduler.shutdown())


if __name__ == '__main__':
    app.run(debug=True)
