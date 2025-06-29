import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from RawSignal import RawSignal
from EEGsignal import EEGSignal
from ClaseAnotaciones import Anotaciones
from pda import Info

canales=[i+1 for i in range(62)]

info = Info(ch_names=canales,
            ch_types="eeg", 
            experimenter="ETCAHRT. Juan Luis",
            subject_info={"edad": 21, "sexo": "M"})

# with open("Datasets/EEG/s00.csv", "r") as f:
#     eeg = [fila.split(",") for fila in f.read().split("\n")]
#     del eeg[-1] #Deleteo la ultima fila porque es un caracter vacío

# eeg = np.array(eeg, dtype= float).T


eeg = np.load("Datasets/EEG/eeg_signal.np", "r")
print(eeg.shape)

anotacion = Anotaciones()
anotacion.load("Datasets/EEG/eventos_ejemplo.csv")


signal = RawSignal(data= eeg, info= info)

