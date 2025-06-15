from pda import Info
from RawSignal import RawSignal 
import numpy as np
import matplotlib.pyplot as plt

canales=[i+1 for i in range(19)]

info = Info(ch_names=canales,
            ch_types="eeg", 
            experimenter="ETCAHRT. Juan Luis",
            subject_info={"edad": 21, "sexo": "M"})

with open("Datasets/EEG/s00.csv", "r") as f:
    eeg = [fila.split(",") for fila in f.read().split("\n")]
    del eeg[-1] #Deleteo la ultima fila porque es un caracter vacío

eeg = np.array(eeg, dtype= float)
# #Datos de eeg: eeg.shape -> (31000,19)
# #   - 19 canales (o columnas)
# #   - 3100 muestras (o filas)

eeg = eeg.T #la traspuesta invierte columnas por filas

# print(eeg.shape)
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

cambio_canales = {
    1: "c1",
    2: "Cz",
    3: "asd"
}

info.rename_channels(cambio_canales)

# print(info["ch_types"])
# print(info.items())

# print(len(info))

signal = RawSignal(eeg, info=info)

# print(signal.data.shape)



# eeg2 = eeg["",]
# eeg2.shape
# canal = "c1"
# print(signal.data[canal,:].max(axis=1))
# print(signal.data[canal,:].min(axis=1))
# print((signal.data[canal,:].max(axis=1) - signal.data[canal,:].min(axis=1)))

# signal2 , t = signal.get_data(picks=canal, times= True)

# print(signal2.shape)
# print(signal2[:10])
# print(info.ch_names[:5])
# print(signal2[0] == signal.data[0,0])
# print(signal2[0] , signal.data[0,0])
# s2, tiempo = signal.get_data(times=True)


######### Drop Chanel #########

# print(signal.data.shape)
# signal2 = signal.drop_chanel("asd")
# print(signal2.data.shape)
# print(signal2.info["ch_names"])
# print(signal.info.ch_names)
# print(signal.info["ch_types"])
# print(signal2.info.ch_types)

###############################
############ Crop ############# 

# signal30 = signal.crop(tmax=30)
# signal60 = signal.crop(tmax=60)

# print(signal30.data.shape)
# print(signal60.data.shape)

# print(signal30.tiempo())
# print(signal60.tiempo())

###############################
########### describe ##########

dataframe = signal.describe() 
print(dataframe.head())