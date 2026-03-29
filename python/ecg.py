import neurokit2 as nk
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pandas import read_csv
from scipy.datasets import electrocardiogram
import warnings
warnings.filterwarnings("ignore")


#file=(read_csv('data.csv'))['ecg']
#ecg=file[pd.to_numeric(file,errors='coerce').notnull()]
#print(ecg)

#ecg=electrocardiogram()[:200]#int(len(electrocardiogram())/2)]

ecg = nk.ecg_simulate(duration=15, sampling_rate=125, heart_rate=80)
ecg=nk.ecg_clean(ecg, sampling_rate=125, method="neurokit")

signals, info  = nk.ecg_process(ecg,sampling_rate=125)
df = nk.ecg_analyze(signals, sampling_rate=125)

signal_cwt, waves_cwt = nk.ecg_delineate(ecg, 
                                         info,
                                         sampling_rate=125, 
                                         method="cwt", 
                                         show=True, 
                                         show_type='all')

#plt.subplot(2, 2, 2)
qrs_epochs = nk.ecg_segment(ecg, rpeaks=None, sampling_rate=125, show=True)

nk.ecg_plot(signals, rpeaks=info)
plt.show()
