from RawSignal import RawSignal
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import spectrogram, hilbert
class EEGSignal(RawSignal):
    """
    # DOCUMENTAR
    """
    def __init__(self, data, sfreq = 512, first_samp = 0, info = None, anotaciones=None):
        super().__init__(data, sfreq, first_samp, info, anotaciones)

        self.promedio = None
        self.canal = self.info.ch_names[0]
        self.laplaciano = self.filtro_laplaciano(self.info.ch_names[0], self.info.ch_names[:3])


    def filtro_laplaciano(self, canal_referencia, canales_vecinos = None) -> "np.array":
        """
        Aplica un filtro laplaciano a un canal específico de datos EEG.
        
        Parameters:
        -----------
        - canal_referencia: nombre del canal de interes (ejemplo: Cz).
        - canales_vecinos: lista de los nombres de los canales vecinos.
            - Si es ***None*** toma todos los canales.
        
        Returns:
        --------
        - laplacian: señal laplaciana para el canal seleccionado [muestras].
        """
        # Extraer canal de interés
        channel_data = self.get_data(picks=canal_referencia, stop=self.data.shape[1])  
        
        # Extraer canales vecinos
        neighbor_data = self.get_data(picks=canales_vecinos, stop=self.data.shape[1]) 
        
        # Calcular promedio de los vecinos para cada muestra
        neighbor_mean = np.mean(neighbor_data, axis=0)[:,np.newaxis].T  

        # Aplicar filtro laplaciano: canal - promedio de vecinos
        laplacian = channel_data - neighbor_mean
        
        return laplacian
    
    def hilbert(self, canales = None, plot = False):
        """
        Calcula la transformada de Hilbert para uno o más canales de datos EEG y grafica los resultados.
        ------------------------
        Parameters:
        -----------
        canales : array_like | str
            - Una lista de los nombres de los canales o un simple nombre canal.
        plot : bool
            - Si esta variable toma el valor de **True** se plotea el resultado de la transformada para el primer canal enviado

        Returns:
        --------
            - analytic_signals: array de señales analíticas complejas [canales, muestras].
            - envelopes: array de envolventes [canales, muestras].
            - phases: array de fases instantáneas [canales, muestras].
        """

        signal, t= self.get_data(picks=canales, stop=self.data.shape[1], times=True)

        analytic_signal = hilbert(signal, axis = 1)
        envolvente = np.abs(analytic_signal)  
        phase = np.angle(analytic_signal)

        if plot:
            plt.plot(t[0], envolvente[0], label=f'Canal {canales[0]}', color='orange')
            plt.title('Envolvente (Amplitud instantánea)')
            plt.xlabel('Muestras')
            plt.ylabel('Amplitud (μV)')
            plt.legend()
            plt.grid(True)
            plt.show()
    
        return analytic_signal, envolvente, phase