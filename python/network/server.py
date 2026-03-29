## init, new connection, loop reading, append(data, time), close conn, save in csv, clear list, repeat

import threading
import socket
import csv
import os


# Default connection settings
DEFAULT_HOST = '127.0.0.1'
DEFAULT_PORT = 8888

DATA_CSV = 'data.csv'
LIVE_CSV = 'ecgLive.csv'
CSV_HEADER = ["temp", "humidty", "ecg"]


class TCPServer(threading.Thread):
    def __init__(self, host, port):
        super().__init__()
        self.host = host
        self.port = port

        # Create socket object
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Bind to host & port, then make server connectable
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen()

        # Init variables
        self.data = None
        self.list = []
        self.done = 1
        self.running = True

    def _init_csv(self, path):
        """Create a fresh CSV file with the standard header."""
        with open(path, 'w', newline='\n') as f:
            csv.writer(f).writerow(CSV_HEADER)

    def run(self):
        # Safely reset the live CSV file
        if os.path.exists(LIVE_CSV):
            os.remove(LIVE_CSV)
        self._init_csv(LIVE_CSV)

        while self.running:
            # Wait for new connection
            client_socket, address = self.server_socket.accept()
            print(f"Connection accepted from {address}")

            while self.running:
                self.data = client_socket.recv(2048)
                if not self.data:
                    break

                self.list.append([self.data.decode()])
                print(self.data.decode())

                try:
                    with open(LIVE_CSV, 'a', newline='') as filee:
                        writer = csv.writer(filee)
                        for item in self.list:
                            lst = [float(x) for x in item[0].split(",")]
                            writer.writerow(lst)
                except (ValueError, IOError) as e:
                    print(f"Error writing to {LIVE_CSV}: {e}")

            # Client disconnected
            client_socket.close()
            self.done = 0

            # Save buffered data to data.csv
            try:
                with open(DATA_CSV, 'a', newline='\n') as myfile:
                    writer = csv.writer(myfile)
                    for item in self.list:
                        try:
                            if item[0].strip():
                                lst = [float(x) for x in item[0].split(",")]
                                writer.writerow(lst)
                        except ValueError:
                            pass
            except IOError as e:
                print(f"Error writing to {DATA_CSV}: {e}")

            self.list.clear()

    def kill(self):
        self.running = False
        # Close the server socket to unblock accept()
        try:
            self.server_socket.close()
        except OSError:
            pass


if __name__ == '__main__':
    server = TCPServer(DEFAULT_HOST, DEFAULT_PORT)
    server.start()
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print(f"Buffered data: {server.list}")
        print("Server interrupted, closing...")
        server.kill()
