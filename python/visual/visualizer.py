import matplotlib.pyplot as plt
import matplotlib.animation as animation
from pandas import read_csv
import numpy as np
import pandas as pd
import heartpy as hp
import os
import csv
from sklearn import preprocessing

fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)

def animate(i):
    try:
        data=read_csv('ecgLive.csv',sep=r'\s*,\s*', engine='python')
        ecg=(data['ecg'])
        #ecg=(preprocessing.normalize((data['ecg'].to_numpy()).reshape(1, -1)))*10
        #ecg=(ecg.apply(lambda x: (x-x.mean())/ x.std())).to_numpy()
        temp=(data['temp'].to_numpy())
        humidity=(data['humidity'].to_numpy())
        xs= np.arange(ecg.size)/125
        ys=ecg

        ax1.clear()
        ax1.plot(xs,ys, label='ecg')
        ax1.plot(xs,temp, label='temp')
        ax1.plot(xs,humidity, label='humidity')
        ax1.legend()

    except pd.errors.ParserError:
        pass
    """
        os.remove('ecgLive.csv')
        data=open("ecgLive.csv","x")
        (csv.writer(data)).writerow(["temp", "humidity", "ecg"])#index names
        data.close()
    """

while True:
    try:
        ani = animation.FuncAnimation(fig, animate, interval=1000)
        plt.show()

    except pd.errors.ParserError:
        pass
    """
        os.remove('ecgLive.csv')
        data=open("ecgLive.csv","x")
        (csv.writer(data)).writerow(["temp", "humidity", "ecg"])#index names
        data.close()
    """
#print("how to kill a mockingbird")
