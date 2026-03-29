## init, new connection, loop reading, append(data, time), close conn, save in csv, clear list, repeat

import threading
import socket
import csv
import os
#from datetime import datetime

# Define connection ip and port
host ='127.0.0.1'
port = 8888

class TCPServer(threading.Thread):
    def __init__(self, host, port):
        super().__init__()
        self.host = host
        self.port = port

        #create socket object
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Binds to host & port, then make server connectable
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen()
        #print(f"Listening on {self.host}:{self.port}")

        # Init variables
        self.data = None
        self.list = []
        #self.writer = None#csv.writer(open('data.csv', 'a', newline='\n'))
        self.done=1
        self.running= True

    def run(self):
        os.remove('ecgLive.csv')
        data=open("ecgLive.csv","x")
        (csv.writer(data)).writerow(["temp", "humidty", "ecg"])#index names
        data.close()
        while self.running: 
            # Waits for new connection
            client_socket, address = self.server_socket.accept()  #waits for new connnection
            #print(f"Accepted connection from {address}")
            print("outside loop")

            while self.running:  #loops for messages, breaks when disconnected 
                self.data = client_socket.recv(2048)
                if not self.data:
                    # Break if disconnected
                    break

                self.list.append([self.data.decode()])
                print(self.data.decode())
                with open('ecgLive.csv','a') as filee:
                    for item in self.list: #loop through the words and add a word for each row
                        lst = [float(x) for x in item[0].split(",")]
                        csv.writer(filee).writerow(lst)

                    #csv.writer(filee).writerow([self.data.decode()])


                # message = self.data.decode()
                # print(f"Received message from {address}: {message}")
            
            # When losing connection with client
            client_socket.close()
            self.done=0
            #print(f"Closed connection to {address}")

            # after sending ends, save to csv, clear list 
            myfile=open('data.csv', 'a', newline='\n')
            self.writer= csv.writer(myfile)
            for item in self.list: #loop through the words and add a word for each row
                try:
                    if item[0] !=' ':
                        lst = [float(x) for x in item[0].split(",")]
                        self.writer.writerow(lst)
                except ValueError:
                    pass
            self.list.clear()
            myfile.close()

    def kill(self):
        self.running = False



if __name__ == '__main__':
    server = TCPServer(host,port)#'127.0.0.1', 8888)
    server.start()
    try:
        while True:
            print("jf:")

    except KeyboardInterrupt:
        print(f"Here's your junk: {server.list}")
        print("Server interrupted, closing...")
        server.server_socket.close()
