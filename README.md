# IoT ECG Monitor with CNN Classification

1st place winner at the national Inetech v3 hackathon (72 hours). A real-time ECG monitoring system combining embedded hardware with AI-based classification.

## Architecture

- **ESP32** reads ECG signals from an AD8232 sensor + DHT22 for temperature/humidity
- Data is sent over TCP to a Python backend
- A **CNN model** (`best_model.h5`) classifies ECG segments into cardiac conditions
- Results are logged and visualized in real time

## Structure

- `Esp32/` and `ECGFINAL.ino` — Arduino firmware for ESP32 + AD8232 sensor
- `python/` — Backend: TCP server, CNN inference, data logging
  - `process/model.py` — CNN inference using TensorFlow/Keras
  - `network/server.py` — TCP server receiving ESP32 data
  - `main.py` — Main orchestrator
- `python/visual/` — Real-time ECG visualization

## Requirements

- ESP32 with AD8232 ECG sensor
- Python 3.10+, TensorFlow, scipy, scikit-learn, pandas, matplotlib
