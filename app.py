import os
import atexit
from flask import Flask, render_template, Response, request, jsonify
import datetime
import data
# import tensorflow as tf
from apscheduler.schedulers.background import BackgroundScheduler
import pandas as pd


app = Flask(__name__, template_folder="templetes")


@app.route('/', methods=['GET'])
def index():
    return render_template('main.html')


@app.route('/predication', methods=['POST', 'GET'])
def predict():
    print("z")
    # d = DataPredication()
    # data = d.predict()
    # return data[0]

@app.route('/forcast/<date>/<size>', methods=['GET'])
def forcast_api(date,size):
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
    scheduler.add_job(func=data.ftech_data(formatted_date), trigger="interval", days=1)
    scheduler.start()
    atexit.register(lambda: scheduler.shutdown())


if __name__ == '__main__':
    app.run(debug=True)
