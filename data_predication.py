import os
import glob
import numpy as np
import pandas as pd
from keras.models import load_model


class DataPredication:
    def __init__(self):
        self.path = self.get_last_path()
        self.fullPath = os.path.join(os.path.dirname(os.path.realpath(__file__)), self.path)
        print(self.fullPath)
        df = pd.read_csv(self.fullPath)
        self.X = df[['BGSM1', 'BGSM2', 'BGSM3', 'BGSE1', 'BGSE2', 'BGSE3']]
        self.X = np.array(self.X).reshape((self.X.shape[0], self.X.shape[1], 1))
        self.prediction_model = load_model("predication_model.h5")



    def get_last_path(self):
        path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "uploads/CSV/*.csv")
        my_list = []
        for fName in glob.glob(path):
            my_list.append(os.path.basename(fName)[10:18])
        lastDate = max(my_list)
        for i in range(0, len(my_list)):
            if my_list[i] == lastDate:
                return glob.glob(path)[i]
        return ""

    def predict(self):
        self.y = self.prediction_model.predict(self.X)
        output = np.array(np.argmax(self.y, axis=1)).max()
        return [self.convertToString(output), np.argmax(self.y)]

    def convertToString(self, modelOutput):
        if modelOutput == 0:
            out = "Normal State."
        elif modelOutput == 1:
            out = 'Moderate Storm.'
        else:
            out = "Strong Storm."
        return out
