import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
#import tensorflow as tf
from tensorflow.keras.models import load_model
from scipy.datasets import electrocardiogram
from scipy import signal
import numpy as np
from sklearn import preprocessing
from time import sleep
import pandas
import warnings
warnings.filterwarnings("ignore")


class Proc:
    def __init__(self):
        self.ecg = 1#electrocardiogram()
        self.result=None

    def run(self,ecg):
            #try: 
                ecg1=self.ecg=ecg.copy()
                savedModel=load_model('best_model.h5')
                #print("model:")
                #print(self.ecg)

        #while True:
            #try:
                #ecg1 = self.ecg #signal.resample(self.ecg, int(len(self.ecg)*(360/125)))
                if(len(ecg1)>=186):
                    ecg1= ecg1[:186*(len(ecg1)//186)]
                else:
                    ecg1= np.resize(ecg1, 186)
                ecg1 = preprocessing.normalize([ecg1])
                ecg1 = ecg1.reshape(-1,186,1)
                #print(ecg1)

                #savedModel=tf.keras.models.load_model('best_model.h5')
                savedModel=load_model('best_model.h5')
                #savedModel.summary()
                self.result = np.mean((savedModel.predict(ecg1)),axis=0)
                print(self.result)
                sleep(0.5)
            #except (TypeError,ValueError): 
                sleep(0.1)
                return self.result

if __name__ == '__main__':
    proc=Proc()
    try:
        #while True:
        data=pandas.read_csv('data.csv',sep=r'\s*,\s*', engine='python')
        proc.run(data['ecg'].to_numpy())

    except KeyboardInterrupt:
        print("Proc interrupted, closing...")
