from RawSignal import RawSignal
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import spectrogram, hilbert

class EMGSignal(RawSignal):
    """
    # DOCUMENTAR
    """
    def __init__(self, data, sfreq = 512, first_samp = 0, info = None, anotaciones=None, umbral_activacion = 50):
        super().__init__(data, sfreq, first_samp, info, anotaciones)

        self.umbral_activacion = umbral_activacion
        self.indices_detectados = None

    def detectando_umbrales(self, canales = None, umbral_activacion = 50):
        """
        DOCUMENTAR
        """

        data = self.get_data(picks=canales, stop=self.data.shape[1])
        
        lista_activacion = np.where(np.abs(data)>umbral_activacion)[0]

        return lista_activacion
    
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