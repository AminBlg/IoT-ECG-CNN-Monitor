import threading
import shutil
from network.server import TCPServer
from process.model import Proc
import csv
import os
from time import sleep
from pandas import read_csv
import pandas as pd
import numpy as np


HOST = "127.0.0.1"
PORT = 8888

DATA_CSV = 'data.csv'
LIVE_CSV = 'ecgLive.csv'
ARCHIVE_DIR = 'archive'
RESULT_CSV = 'modelResult.csv'
CSV_HEADER = ["temp", "humidity", "ecg"]


def init_csv(path):
    """Create a fresh CSV file with the standard header."""
    with open(path, 'w', newline='\n') as f:
        csv.writer(f).writerow(CSV_HEADER)


if __name__ == '__main__':
    # Ensure archive directory exists
    os.makedirs(ARCHIVE_DIR, exist_ok=True)

    tcp = TCPServer(HOST, PORT)
    proc = Proc()

    tcp.start()

    count = 0
    filecount = 0

    try:
        while True:
            try:
                data = read_csv(DATA_CSV, sep=r'\s*,\s*', engine='python')
                ecg_data = data['ecg'].to_numpy()
                print(ecg_data)

                result = proc.run(ecg_data)
                if result is not None:
                    with open(RESULT_CSV, 'w', newline='') as f:
                        csv.writer(f).writerow(result)

                if tcp.done == 0:
                    count += 1
                    tcp.done = 1
                    if count >= 5:
                        shutil.copy2(DATA_CSV, LIVE_CSV)
                        os.rename(DATA_CSV, os.path.join(ARCHIVE_DIR, f"{filecount}.csv"))
                        filecount += 1
                        count = 0
                        init_csv(DATA_CSV)

                sleep(0.5)

            except (pd.errors.ParserError, FileNotFoundError, KeyError) as e:
                print(f"Data read error: {e}")
                if os.path.exists(DATA_CSV):
                    os.remove(DATA_CSV)
                init_csv(DATA_CSV)
                sleep(0.5)

    except KeyboardInterrupt:
        print("Main interrupted, shutting down...")
        tcp.kill()
        print(f"Server running: {tcp.running}")
