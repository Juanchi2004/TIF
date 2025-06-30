import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from RawSignal import RawSignal
from EEGsignal import EEGSignal
from Clase_Anotaciones import Anotaciones
from pda import Info

# canales=[i+1 for i in range(62)]

# info = Info(#ch_names=canales,
#             ch_types="eeg", 
#             experimenter="ETCAHRT. Juan Luis",
#             subject_info={"edad": 21, "sexo": "M"})

# with open("Datasets/EEG/s00.csv", "r") as f:
#     eeg = [fila.split(",") for fila in f.read().split("\n")]
#     del eeg[-1] #Deleteo la ultima fila porque es un caracter vacío

# eeg = np.array(eeg, dtype= float).T


eeg = np.load("Datasets/EEG/eeg_signal.np", "r")

print(eeg.shape)

info = Info(ch_names=list(range(eeg.shape[0])),
            ch_types="eeg", 
            experimenter="ETCAHRT. Juan Luis",
            subject_info={"edad": 21, "sexo": "M"})

anotacion = Anotaciones()
anotacion.load("Datasets/EEG/eventos_ejemplo.csv")


# signal = RawSignal(data= eeg, info= info)#, anotaciones=anotacion
signal = EEGSignal(data=eeg, info=info, anotaciones=anotacion)

# signal.tiempo_frecuencia(pick=5, plot=True)
# color = ("#13e7ff", "#110ec1", "#FF0000", "#26ff00")
# signal.plot(picks=(1,2,3,4,5,6),duration=300,show_anotaciones=True, color=color)
# signal.espectro_potencias(plot=True)
c1 = signal.pick(1)
c1.espectro_potencias(plot=True)

# laplacian_signal = signal.filtro_laplaciano(1, (2,3,4,5,6))

# a, b, c = signal.hilbert(canales=(1,2), plot=True) #

# print(b.shape)
# x = np.arange(b.shape[1])
# plt.plot(x, b[0], label = "Envolvente", color = "orange")
# plt.show()
# print("fin")

