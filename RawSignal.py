## Trabajo integrador final.
## Realizado por Juan Etchart y Gabriel Ferrer.

#///////////// Librerias importadas /////////////
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pda import Info

class RawSignal():
    """
    # DOCUMENTAR:
    
----------------------------
    Clase para manejar señales fisiológicas en formato NumPy. \n
    Este constructor permite inicializar el objeto 'RawSignal' a partir de un array de datos,
    con información adicional de los canales y el índice de la primera muestra.
    """
    def __init__(self, data:np.ndarray, sfreq:float = 512, first_samp:int = 0, info:Info = None,  anotaciones = None):
        

        if len(data.shape) != 2:
            raise ValueError (f"El set de datos no tiene dimensiones 2D (matriz)")
        
        if first_samp not in range(len(data[0,:])):
            raise ValueError (f"La muestra: {first_samp} está fuera de rango")

        self.data = data #Matriz 2D de forma (n_canales, n_muestras)
        self.sfreq = sfreq
        self.first_samp = first_samp
        self.info = info
        self.anotaciones = anotaciones
        
    def get_data(self, picks = None, start=0, stop=0 , reject=None, times=False):
        #Si stop == 0 retorna los primeros 10 segundos
        
        new_data = self.data

        if picks == None and start == 0 and stop == 0 and reject == None and times == None:
            return RawSignal(data=new_data[:self.sfreq*10,:], sfreq= self.sfreq, first_samp= self.first_samp, info= self.info, anotaciones= self.anotaciones)

        if not isinstance(picks, None):
            new_data = new_data[picks, start: stop]
        
        if not isinstance(reject, None):
            # new_data = new_data #Consultar a Lucas que onda con esto, si es una especie de filtro por frecuencia o que onda.
            pass

        if times:
            return RawSignal(data=new_data, sfreq= self.sfreq, first_samp= self.first_samp, info= self.info, anotaciones= self.anotaciones), np.arange(len(new_data))
            


        return RawSignal(data=new_data, sfreq= self.sfreq, first_samp= self.first_samp, info= self.info, anotaciones= self.anotaciones)