from scipy.datasets import electrocardiogram
import matplotlib.pyplot as plt
import numpy as np

ecg= electrocardiogram()
fs=360
time = np.arange(ecg.size) / fs

plt.plot(time, ecg)
plt.xlabel("time in s")
plt.ylabel("ECG in mV")
plt.show()
