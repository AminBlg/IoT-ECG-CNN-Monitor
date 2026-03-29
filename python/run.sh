#!/bin/bash

python main.py &
sleep 2 
python visual/visualizer.py &
python ecg.py &
python archiver.py &
sleep 7 
python network/tests/client2.py &
python daVisual.py
