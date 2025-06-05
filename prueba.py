from pda import Info
from RawSignal import RawSignal 
import numpy as np
import matplotlib.pyplot as plt

canales=[i+1 for i in range(3)]

info = Info(ch_names=canales,
            ch_types=["eeg"]*len(canales), 
            experimenter="ETCAHRT. Juan Luis",
            subject_info={"edad": 21, "sexo": "M"})

with open("Datasets/EEG/s00.csv/s00.csv", "r") as f:
    eeg = [fila.split(",") for fila in f.read().split("\n")]
    del eeg[-1] #Deleteo la ultima fila porque es un caracter vacío

eeg = np.array(eeg, dtype= float)
# #Datos de eeg: eeg.shape -> (31000,19)
# #   - 19 canales (o columnas)
# #   - 3100 muestras (o filas)

# eeg = eeg.T

# print(eeg[:,0].shape)
# print(eeg[0,:].shape)
# print(type(eeg[5,5]))

# x=np.arange(512)
# y=eeg[:512,0]

# plt.plot(x,y)
# plt.grid(True)
# plt.show()




# print(info.ch_names) #[1, 2, 3]
# print(info.sfreq) #512
# print(info.description) #Registro EEG para análisis de patrones ERDS

# print(info["experimenter"])

# print(info["ch_names"])

# cambio_canales = {
#     1: "c1",
#     2: "Cz",
#     3: "asd"
# }

# info.rename_channels(cambio_canales)

# print(info["ch_names"])
print(info.items())
print(len(info))

# signal = RawSignal(eeg)

# print(signal.data.shape)

# s2, tiempo = signal.get_data(times=True)



