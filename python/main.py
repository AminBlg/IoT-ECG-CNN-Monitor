import threading 
from network.server import TCPServer
#from visual.visual import Visual
from process.model import Proc
import csv
import os
from time import sleep
from pandas import read_csv
import pandas as pd
from scipy.datasets import electrocardiogram
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.animation as animation

fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)

#HOST = "192.168.154.27"
HOST = "127.0.0.1"
PORT = 8888
count = 0
filecount=0


"""
def animate(i,ecg):
    xs= np.arange(ecg.size)/125
    ys=ecg

    ax1.clear()
    ax1.plot(xs,ys)
"""



if __name__ == '__main__':
    #init thread classes
    tcp=TCPServer(HOST ,PORT)
    proc=Proc()
    #init thread and start em
    #tcpThread = threading.Thread(target = tcp.run, args=())
    tcpThread = tcp
    tcpThread.start()


    #run main loop
    try:
        while(True):
            try:
                #visual.run()
                data=read_csv('data.csv',sep=r'\s*,\s*', engine='python')
                print(data['ecg'].to_numpy())
                result=proc.run((data['ecg'].to_numpy()))
                with open('modelResult.csv','w') as filee:
                    csv.writer(filee).writerow(result)

                if(tcp.done==0):
                    count+=1
                    #print("finished sending")
                    data=read_csv('data.csv')
                    tcp.done=1
                    if( count >=5):
                        #print("reached here")
                        #mv data somewhere else
                        os.popen('cp data.csv ecgLive.csv')
                        os.rename("data.csv",f"archive/{filecount}.csv")

                        count=0
                        data=open("data.csv","x")
                        (csv.writer(data)).writerow(["temp", "humidty", "ecg"])#index names
                        data.close()
                sleep(0.5)

            except (pd.errors.ParserError ,FileNotFoundError):
                if os.path.exists('data.csv'):
                    os.remove('data.csv')
                data=open("data.csv","x")
                (csv.writer(data)).writerow(["temp", "humidty", "ecg"])#index names
                data.close()


    except KeyboardInterrupt:
        print("main killed by you")
        tcp.kill()
        print(tcp.running)
        #tcpThread.join()

        #threading.join()
