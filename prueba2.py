import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from RawSignal import RawSignal
from pda import Info

data = np.load("Datasets/EEG/eeg_signal.np", "r")

# print(len(data[0,:])) #Columnas
# print(len(data[:,0])) #Filas

with open("C:/Users/juanc/Downloads/ecg.csv/ecg.csv") as f:
    ekg = [fila.split(",") for fila in f.read().split("\n")]
    del ekg[-1]
ekg = np.array(ekg, dtype= float).T
print(ekg.shape)
# print(ekg.shape)
# plt.figure(figsize = (50,50))
# plt.plot(np.arange(ekg.shape[0]), ekg[:,0:3])
# plt.show()

canales=list(range(ekg.shape[0]))

info = Info(
    ch_names=canales,
    ch_types="ECG",
    sfreq=125
)

signal_ecg = RawSignal(ekg, sfreq=125, info=info)
df=signal_ecg.describe()
print(signal_ecg.tiempo())
# print(df)
signal_ecg.plot(picks=list(range(120, 141, 2)), duration=5)
