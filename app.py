import os
import atexit
from flask import Flask, render_template, Response, request
import datetime
import data

from apscheduler.schedulers.background import BackgroundScheduler


app = Flask(__name__, template_folder="templetes")


@app.route('/', methods=['GET'])
def index():
    return render_template('homeclass.html')


@app.route('/predication', methods=['POST', 'GET'])
def predict():
    print("z")
    # d = DataPredication()
    # data = d.predict()
    # return data[0]



def update_data():
    current_date = datetime.date.today()
    formatted_date = current_date.strftime("%Y-%m-%d")
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=data.ftech_data(formatted_date), trigger="interval", days=1)
    scheduler.start()
    atexit.register(lambda: scheduler.shutdown())


if __name__ == '__main__':
    update_data()
    app.run(debug=True)
