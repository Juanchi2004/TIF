import numpy as np
import matplotlib.pyplot as plt

data = np.load("Datasets/EEG/eeg_signal.np", "r")

print(len(data[0,:])) #Columnas
print(len(data[:,0])) #Filas
