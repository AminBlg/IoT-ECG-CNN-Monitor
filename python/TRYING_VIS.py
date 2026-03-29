import threading 
from network.server import TCPServer
from visual.visual import Visual
from process.model import Proc
import csv
import os
from time import sleep


HOST = "192.168.154.27"
#HOST = "127.0.0.1"
PORT = 8888
count = 0
filecount=0
class Proc:
    def __init__(self, visual):
        self.visual = visual
        
    def run(self):
        while True:
            # Read ECG values from the TCP server
            ecg_values = read_ecg_values()

            # Update the visual object with the new ECG values
            self.visual.data = ecg_values

if __name__ == '__main__':
    #init thread classes
    tcp=TCPServer(HOST ,PORT)
    visual = Visual()
    proc=Proc(visual)  # Pass visual object to proc thread
    try:
        #init thread and start em 
        tcpThread = threading.Thread(target=tcp.run)
        tcpThread.start()

        procThread = threading.Thread(target=proc.run)
        procThread.start()

        #run main loop
        while(True):
            # Do not call visual.run() inside the main loop
            if(tcp.done==0):
                count+=1
                print("finished sending")
                tcp.done=1
                if( count >=5):
                    print("reached here")
                    os.rename("data.csv",f"archive/{filecount}.csv")
                    count=0
                    filecount+=1
                    data=open("data.csv","x")
                    data.close()
            sleep(0.5)

    except KeyboardInterrupt:
        tcp.writer.close()
        print("main killed by you")
        tcpThread.join()
        procThread.join()
