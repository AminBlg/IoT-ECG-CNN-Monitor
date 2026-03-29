# IoT ECG Monitor with CNN Classification

1st place winner at the national Inetech v3 hackathon (72 hours). A real-time ECG monitoring system combining embedded hardware (ESP32 + AD8232) with deep learning-based arrhythmia classification.

## Architecture

```
+-------------+       TCP/WiFi        +------------------+      +----------------+
|   ESP32     | --------------------> |  Python Backend  | ---> |  CNN Model     |
|  + AD8232   |   raw ECG samples     |  (TCP Server)    |      |  (Keras .h5)   |
|  + DHT22    |   temp/humidity       |                  |      |  MIT-BIH based |
+-------------+                       +------------------+      +----------------+
                                             |                         |
                                             v                         v
                                      +-------------+          +----------------+
                                      | data.csv    |          | Classification |
                                      | ecgLive.csv |          | Results        |
                                      +-------------+          +----------------+
                                             |
                                             v
                                      +----------------+
                                      | Visualization  |
                                      | (matplotlib)   |
                                      +----------------+
```

**Data flow:**
1. The ESP32 reads analog ECG from the AD8232 sensor (pin 34) at ~125 Hz, plus temperature/humidity from a DHT22.
2. Samples are sent over WiFi via TCP to the Python backend.
3. The TCP server buffers incoming data into CSV files.
4. The CNN model segments the signal into 186-sample windows, normalizes them, and classifies each window.
5. Results are averaged and written to `modelResult.csv` for downstream use.

## CNN Classification

The model (`best_model.h5`) is a 1D Convolutional Neural Network trained on the [MIT-BIH Arrhythmia Database](https://physionet.org/content/mitdb/1.0.0/). It classifies ECG beats into the following AAMI standard categories:

| Class | Description                |
|-------|----------------------------|
| N     | Normal beat                |
| S     | Supraventricular ectopic   |
| V     | Ventricular ectopic        |
| F     | Fusion beat                |
| Q     | Unknown / unclassifiable   |

Each 186-sample window is normalized and fed through the CNN. The output is a probability distribution across the five classes.

## Hardware Setup

### Components
- **ESP32** development board (any variant with WiFi)
- **AD8232** single-lead ECG sensor module
- **DHT22** temperature and humidity sensor
- Electrode pads and cables (3-lead)

### Wiring

| AD8232 Pin | ESP32 Pin | Description          |
|------------|-----------|----------------------|
| OUTPUT     | GPIO 34   | Analog ECG signal    |
| LO+        | GPIO 15   | Leads-off detection  |
| LO-        | GPIO 4    | Leads-off detection  |
| 3.3V       | 3V3       | Power supply         |
| GND        | GND       | Ground               |

Connect the DHT22 data pin to an available GPIO (configured in the ESP32 firmware).

### Electrode Placement
Place the three electrodes in the standard Einthoven Lead I configuration:
- **RA (Right Arm):** Right wrist or right collarbone area
- **LA (Left Arm):** Left wrist or left collarbone area
- **RL (Right Leg / Reference):** Right ankle or lower right abdomen

## Software Setup

### 1. Flash the ESP32

1. Open `ECGFINAL.ino` (or the appropriate sketch in `Esp32/`) in the Arduino IDE.
2. Install the ESP32 board package via Arduino Board Manager.
3. Set the board to your ESP32 variant and the correct COM port.
4. Update the WiFi credentials and the server IP address in the firmware to match your setup.
5. Upload the sketch.

### 2. Install Python Dependencies

```bash
cd python/
pip install -r requirements.txt
```

Requires Python 3.10 or later.

### 3. Run the Backend

```bash
cd python/
python main.py
```

This starts the TCP server (default: `127.0.0.1:8888`), listens for ESP32 data, runs CNN inference on incoming ECG segments, and logs results.

### 4. Visualization

The `python/visual/` directory contains matplotlib-based scripts for real-time ECG plotting. Run them separately while the main backend is active:

```bash
python visual/visual.py
```

## Repository Structure

```
.
├── ECGFINAL.ino              # Main Arduino firmware for ESP32 + AD8232
├── Esp32/                    # Additional Arduino sketches and experiments
├── python/
│   ├── main.py               # Orchestrator: server + model + data management
│   ├── requirements.txt      # Python dependencies
│   ├── process/
│   │   └── model.py          # CNN inference (TensorFlow/Keras)
│   ├── network/
│   │   └── server.py         # TCP server for receiving ESP32 data
│   ├── visual/
│   │   ├── visual.py         # Real-time ECG visualization
│   │   └── visualizer.py     # Alternative visualization script
│   ├── best_model.h5         # Pre-trained CNN weights
│   ├── data.csv              # Live data buffer
│   ├── ecgLive.csv           # Current session ECG data
│   └── modelResult.csv       # Latest classification output
└── README.md
```

## Known Considerations

- **Noise:** Real ECG signals contain baseline wander (from respiration, ~0.15-0.7 Hz), 50/60 Hz power-line interference, and motion artifacts. The AD8232 provides hardware filtering, but additional digital filtering may improve results.
- **Sampling rate:** The ESP32 ADC samples at approximately 125 Hz (8 ms delay). The CNN expects 186-sample windows at this rate.
- **Model retraining:** To retrain on your own data, segment beats into 186-sample windows following the MIT-BIH AAMI standard and train a 1D CNN with the same input shape.

## License

This project was built during the Inetech v3 hackathon. See the repository for license details.
