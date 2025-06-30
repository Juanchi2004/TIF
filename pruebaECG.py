import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from RawSignal import RawSignal
from EEGsignal import EEGSignal
from ECGSignal import ECGSignal
from Clase_Anotaciones import Anotaciones
from pda import Info


ecg = np.load("Datasets/ECG/ecg/ecg.npy", "r")[:,np.newaxis].T

# print(ecg.shape)

x=np.arange(ecg.shape[1])
# print(x.shape)
# plt.plot(x,ecg[0])
# plt.show()
anotacion = Anotaciones()
anotacion.load("Datasets/ECG/ecg/eventos_ecg.csv")

signal = ECGSignal(data=ecg, anotaciones=anotacion, sfreq=512)

# print(signal.tiempo())
# signal.plot(duration=signal.tiempo(),show_anotaciones=False)

picos = signal.picos_R(altura_min=100, distancia_min=100)
print(picos.shape)

# plt.vlines(picos, ymax=1000, ymin=-1000)
# plt.plot(np.arange(signal.data.shape[1]),ecg[0])
# plt.show()
freq = signal.f_cardiaca()
print(freq)