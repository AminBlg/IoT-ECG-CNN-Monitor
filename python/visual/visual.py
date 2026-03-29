import numpy as np
import matplotlib.pyplot as plt
from scipy.datasets import electrocardiogram
import heartpy as hp
import pandas as pd

from time import sleep

import matplotlib.pyplot as plt
import matplotlib.animation as animation


import threading

def run(ecg):

    fig = plt.figure()
    ax1 = fig.add_subplot(1,1,1)

    def animate(i,ecg):
        xs= np.arange(ecg.size)/125
        ys=ecg

        ax1.clear()
        ax1.plot(xs,ys)

    while True:
        
        ecg=electrocardiogram()
        ani = animation.FuncAnimation(fig, animate, fargs=([ecg]), interval=1000)
        plt.show()



if __name__ == '__main__':
    try:    
        drawThread = threading.Thread(target = run, args=([electrocardiogram()] ))
        drawThread.start()
        while True:
            sleep(1)


    except KeyboardInterrupt:
        print("iz dead")