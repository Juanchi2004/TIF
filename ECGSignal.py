from RawSignal import RawSignal
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import spectrogram, hilbert, find_peaks
# from neurokit2 import ecg_clean, ecg_peaks #AVISAR EN ALGÚN LADO QUE SE IMPORTA ESTA LIBRERÍA

class ECGSignal(RawSignal):
    def __init__(self, data, sfreq = 512, first_samp = 0, info = None, anotaciones=None):
        super().__init__(data, sfreq, first_samp, info, anotaciones)
        
        
        self.picos_r = self.picos_R()
        self.freq_cardiaca = self.f_cardiaca()
    
    def picos_R(self, canales = None, altura_min = 100, distancia_min = 100):
        """
        documentar
        """

        # if distancia_min < 1:
        #     raise ValueError ("La distancia minima entre pico y pico tiene que ser 1 o mayor", distancia_min)
        data = self.get_data(picks=canales, stop=self.data.shape[1])

        r_peaks =[]
        for i in range(data.shape[0]):
            peaks, _ = find_peaks(data[i,:], height=altura_min, distance=distancia_min)
            r_peaks.append(peaks)
        
        return np.array(r_peaks)

    def f_cardiaca(self, canales = None):
        """
        documentar
        
        """

        lista_picos = self.picos_R(canales=canales)

        lista_picos = lista_picos/self.sfreq
        
        freq = []
        for i in range(lista_picos.shape[1]):
            resta = lista_picos[:,i] - lista_picos[:,i-1]
            freq.append(resta)
        del freq[0]
        freq = 60/np.mean(freq)

        return round(freq, 2)

        

