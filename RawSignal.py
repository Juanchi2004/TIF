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
        
    def get_data(self, picks:list | tuple | int | str = None, start=0, stop=0 , reject=None, times=False):
        """
        Argumentos:
        ----
        - picks: Se seleccionan los canales existentes dentro del objeto RawSignal.data
        - start: comienzo de la muestra
        - stop: fin de la muestra 
            - Si stop <= 0 retorna los primeros 10 segundos
        - reject: elimina los canales los cuales superen el umbral propuesto
        - times: habilita que adicionalmente se retorne un vector que contiene un enumerado del largo [start : stop]
        Return:
        ----
        - Si times = True:
            - np.ndarray
            - Un vector con el largo de [start : stop]
        - Si times = False:
            - np.ndarray
        """
        
        new_data = self.data.copy()
        
        if picks == None:
            picks = self.info.ch_names
        elif isinstance(picks, (int, str)) and picks in self.info.ch_names:
            picks = self.info.ch_names.index(picks)
        elif isinstance(picks, (tuple, list)):
            picks = [self.info.ch_names.index(canal) for canal in picks if canal in self.info.ch_names]
        else:
            raise ValueError ("Ocurrió algo al realizar el ajuste de 'picks'", picks)
        
        if start < 0:
            raise ValueError (f"El inicio de la señal no puede ser negativo. start = {start}")
        
        if stop <= 0:
            stop = self.sfreq * 10
        elif stop > new_data.shape[1]:
            raise ValueError (f"El valor **stop** está por fuera del rango de la señal. stop = {stop} - N° muestras: {new_data.shape[1]}")
        
        if reject != None:
            picks = [canal for canal in picks if (abs(new_data[canal,:].max() - new_data[canal,:].min())) < reject]

        if times:
            return new_data[picks,start:stop], np.arange(new_data.shape[1])
            
        return new_data[picks,start:stop]