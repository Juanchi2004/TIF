## Trabajo integrador final.
## Realizado por Juan Etchart y Gabriel Ferrer.

#///////////// Librerias importadas /////////////
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import butter, sosfiltfilt, welch
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
            raise ValueError (f"El set de datos no tiene dimensiones 2D (matriz)", data.shape)
        
        if first_samp not in range(len(data[0,:])):
            raise ValueError (f"La muestra: {first_samp} está fuera de rango")

        self.data = data #Matriz 2D de forma (n_canales, n_muestras)
        self.sfreq = sfreq
        self.first_samp = first_samp
        self.info = info
        self.anotaciones = anotaciones
        
    def get_data(self, picks:list | tuple | int | str = None, start=0, stop=0 , reject=None, times=False):
        """
        # Este método sirve para obtener una cantidad de muestras de la señal.
        
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
            picks = list(range(len(self.info.ch_names))) 
        elif isinstance(picks, (int, str)) and picks in self.info.ch_names:
            picks = self.info.ch_names.index(picks)
        elif isinstance(picks, (tuple, list)):
            picks = [self.info.ch_names.index(canal) for canal in picks if canal in self.info.ch_names]
        else:
            raise ValueError ("Ocurrió algo al realizar el ajuste de 'picks'", picks)
        # Finalmente la variable **picks** tiene los indices de los canales seleccionados.

        if isinstance(start, int) and start < 0:
            raise ValueError (f"El inicio de la señal no puede ser negativo. start = {start}")
        

        start = 0 if start == None else start
        stop = new_data.shape[1] if stop == None else stop
        
        if stop <= 0:
            stop = self.sfreq * 10
        elif stop > new_data.shape[1]:
            raise ValueError (f"El valor **stop** está por fuera del rango de la señal. stop = {stop} - N° muestras: {new_data.shape[1]}")
        
        if reject != None:
            picks = [canal for canal in picks if (abs(new_data[canal,:].max() - new_data[canal,:].min())) < reject]

        new_data = new_data[picks,start:stop]

        if len(new_data.shape) == 1:
            new_data = new_data[:,np.newaxis].T

        if times:
            return new_data, np.arange((stop-start))[:,np.newaxis].T
            
        return new_data

    def drop_chanel(self, ch_names) -> "RawSignal":
        """
        Elimina uno o más canales a partir de *ch_names*.

        Parameters
        ----------
            ch_names : array like
                - Nombre de los canales a eliminar.
        
        Returns
        ----------
            - RawSignal        
        """
        #para hacerlo un poquito mas corto creo la variable.
        if isinstance(ch_names, (tuple, list)):
            ch_names = [self.info.ch_names.index(canal) for canal in self.info.ch_names if canal not in ch_names]
        elif isinstance(ch_names, (int, str)) and ch_names in self.info.ch_names:
            ch_names = [indice for indice, canal in enumerate(self.info.ch_names) if ch_names != canal]
        else:
            raise TypeError ("Los datos ingresados son erroneos.", ch_names)
        # info2 = self.info
        info2 = self.info.copy()
        info2.ch_names = [info2.ch_names[indice] for indice in ch_names]
        info2.ch_types = [info2.ch_types[0]] * len(info2.ch_names)
        return RawSignal(data=np.squeeze(self.data[[ch_names]], axis=0), #no entiendo por qeu razón me agrega un eje mas a la matriz
                         sfreq=self.sfreq,
                         first_samp=self.first_samp,
                         info=info2,
                         anotaciones=self.anotaciones)

    def tiempo(self) -> float:
        """Retorna la duración en **segundos** de la muestra
           desde *first_samp* hasta la ultima muestra"""
        return (self.data.shape[1] - self.data[:,:self.first_samp].shape[1])/self.sfreq

    def crop(self, tmin:float=None, tmax:float = None) -> "RawSignal":
        """
        Obtiene un trozo (Crop) de RawSignal. Limita los datos dentro de RawSignal
        para obtener un nuevo objeto RawSignal pero con una cantidad de muestras recortadas.
        El parámetro 'first_samp' se configura adecuadamente.

        Parameters
        ----------
        tmin : float, optional
            - Tiempo inicial, en segundos para iniciar el recorte (por defecto es 0.0)
        tmax : float or None, opcional
            - Tiempo final, en segundos, para finalizar el recorte (por defecto es None)
        
        Returns
        -------
        RawSignal
            - Nueva instancia de 'RawSignal' que contiene el segmento temporal recortado.

        Raises
        ------
        ValueError
            - Si los tiempos 'tmin' o 'tmax' están fuera del rango de la señal
        """
        if tmin == None:
            tmin = self.first_samp
        if tmax >= self.data.shape[1] * self.sfreq or tmax < 0:
            raise ValueError (f"El tiempo maximo elegido se encuentra fuera de rango: ({tmax})")
        elif tmin >= self.data.shape[1] * self.sfreq or tmin < 0:
            raise ValueError (f"El tiempo minimo elegido se encuentra fuera de rango: ({tmin}) ")
        
        info = self.info.copy()

         #Se supone que la primera muestra no tiene el valor temporal, sino el indice de la primera muestra
        tmin = tmin * self.sfreq
        tmax = tmax * self.sfreq
        data = self.get_data(start=tmin, stop=tmax)


        # anotaciones_nuevas = self.anotaciones
        # anotaciones_nuevas #modificar

        return RawSignal(data, self.sfreq, self.first_samp, info, self.anotaciones)

    def describe(self) -> "pd.DataFrame":
        """
        Crea un ***DataFrame*** con todos los canales dentro del objeto RawSignal.
        --------
        Info contenida dentro del *DataFrame*
        - Name    : Nombre del canal
        - Type    : Tipo de canal (eeg, ecg, emg)
        - Min     : Valor mínimo del canal
        - Q1      : Primer cuartil (percentil 25%)
        - Mediana : Mediana (percentil 50%)
        - Q3      : Tercer cuartil (percentil 75%)
        - Max     : Valor máximo del canal

        Returns
        -------
        DataFrame de todos los datos de todos los canales.   
        """
        try:
            dataframe = {
                "Name": self.info.ch_names,
                "Type": self.info.ch_types,
                "Min": self.data.min(axis=1),
                "Q1": np.percentile(self.data, q=25, axis=1),
                "Mediana": np.percentile(self.data, q=50, axis=1),
                "Q3": np.percentile(self.data, q=75, axis=1),
                "Max": self.data.max(axis=1)
            }
            return pd.DataFrame(data=dataframe) #Para que el indice comience en 1: index= range(1, len(self.info.ch_names)+1)
        except ValueError as vErr:
            raise ("Ocurrió un error al realizar la acción")

    def filter(self, l_freq, h_freq, notch_freq=50., order=4)->"RawSignal":
        """
        Aplica un filtro pasabanda y un filtro notch.\n
        Retorna una nueva instancia de *RawSignal* con los datos filtrados
        
        ***Parameters***
        ----------------
        l_freq : float
            -  Frecuencia de corte baja (Hz) para el filtro pasabanda.
        h_freq : float
            -  Frecuencia de corte alta (Hz) para el filtro pasabanda.
        notch_freq : float, optional
            -  Frecuencia del filtro notch para eliminar ruido (por defecto 50 Hz).
        order : int, optional
            - Orden del filtro (por defecto 4).
        fir_window : str, optional
            -  Tipo de ventana para el diseño del filtro FIR (por defecto "hamming").
        
        ***Returns***
        -------------
        RawSignal
            Nueva instancia de 'RawSignal' con los datos filtrados.

        ***Raises***
        ------------
        ValueError
            - Si los valores de 'l_freq' o 'h_freq' no son válidos.
        ValueError
            - Si el valor de 'notch_freq' no es positivo.
        """
        
        if not (isinstance(l_freq, (float, int)) or isinstance(h_freq, (float, int))):
            raise TypeError ("Los tipos de variable de *l_freq* o *h_freq* no son los correctos")
        elif l_freq < 0 | h_freq < 0:
            raise ValueError ("Las frecuencias de corte de los pasa banda no pueden ser menores a cero")
        if not isinstance(notch_freq, (float, int)):
            raise TypeError ("El tipo de variable de *notch_freq* no es el correcto")
        elif notch_freq < 0:
            raise ValueError ("El valor del *notch_freq* no puede ser menor a cero")

        f_nyq = self.sfreq / 2
        l_freq = l_freq / f_nyq #Se normaliza la frecuencia de corte
        h_freq = h_freq / f_nyq #Se normaliza la frecuencia de corte
        notch_freq = [(notch_freq-1) / f_nyq, (notch_freq+1) / f_nyq] #Se normaliza la frecuencia de corte 
        
        new_data = self.data.copy()

        sos_pasa_bajos = butter(order, h_freq, btype='low', output='sos')
        sos_pasa_altos = butter(order, l_freq, btype='high', output='sos')
        sos_notch = butter(order, notch_freq, btype='bandstop', output='sos')

        new_data = sosfiltfilt(sos_pasa_bajos, new_data, axis=1)
        new_data = sosfiltfilt(sos_pasa_altos, new_data, axis=1)
        new_data = sosfiltfilt(sos_notch, new_data, axis=1)
        
        return RawSignal(data=new_data, sfreq=self.sfreq, first_samp=self.first_samp, info=self.info, anotaciones=self.anotaciones)


    def pick(self, picks)->"RawSignal":
        """
        Retorna un subset de los canales seleccionados.

        Parameters
        ----------

        picks : str | array_like | slice
            Canales a seleccionar. Puede ser:
            - str : Nombre de un solo canal.
            - list[str] : Lista de nombres de canales.
            - list[int] : Lista de nombres de canales.
        
        Retunrs
        -------
        RawSignal
            Nueva instancia de ***RawSignal*** con el subset de canales elegidos.

        Raises
        ------
        ValueError
            Si el canal especificado no existe.
        ValueError
            Si el índice está afuera del rango
        """
        info= self.info.copy()
        #implementar:
        #nueva_anotacion = self.anotaciones.copy()
        
        if isinstance(picks, (str, int)):
            info.ch_names = [picks] if picks in info.ch_names else ValueError ("El canal no se encontró", picks)
            info.ch_types = info.ch_types[info.ch_names.index(picks)]
            return RawSignal(data=self.get_data(picks, start=0, stop=self.data.shape[1]), sfreq=self.sfreq, first_samp=self.first_samp, info=info, anotaciones=self.anotaciones)
        elif isinstance(picks, (list, tuple, np.ndarray)):
            info.ch_names = [canal for canal in picks if canal in info.ch_names]
            info.ch_types = [info.ch_types[0]] * len(info.ch_names)
            return RawSignal(data=self.get_data(picks, start=0, stop=self.data.shape[1]), sfreq=self.sfreq, first_samp=self.first_samp, info=info, anotaciones=self.anotaciones)

    def plot(self, picks=None, start=0.0, duration=10.0, show_anotaciones=True, color = None):
        """
        Grafica un segmento de la señal fisiológica.

        Parameters
        ----------
        picks : str | list of str | list of int, opcional
            Canal(es) a visualizar. Puede ser:
            - str: Nombre de un canal.
            - list[str]: Lista de nombres de canales.
            - list[int]: Índices de canales.
            \n  Si es **None**, se grafica todos los canales.

        start : float, opcional
            Tiempo inicial en segundos desde donde comenzar la visualización
            (por defecto es **0.0**).
        
        duration : float, optional
            Duración del segmento de la señal a mostrar en segundos.
            (por defecto es **10.0**).
        
        show_anotaciones : bool, optional
            Si es **True**, se muestran las anotacioens sobre la señal
            (por defecto es **True**)
        
        color : str | list of str
            Se le asignará el o los colores a los distintos canales.
            (por defecto **None**, se asignarán colores aleatoriamente).
        """
        from collections.abc import Iterable
        
        start = int(start * self.sfreq)
        duration = int(duration * self.sfreq)

        y, x = self[picks, start: duration]

        if picks == None:
            picks = self.info.ch_names

        if color == None and isinstance(picks, (tuple, list)):
            color = [self._color_random_hex() for i in range(len(picks))]
        elif isinstance(color, str) and isinstance(picks, (tuple, list)):
            color = [color]*len(picks)

        x = x[0,:]/self.sfreq
        fig, axes = plt.subplots(nrows=y.shape[0], figsize = (25,25))
        if isinstance(axes, Iterable):
            for i,canal in enumerate(y):
                axes[i].plot(x, canal, color = color[i%len(color)], label = picks[i])
                axes[i].grid(visible=True, alpha = 0.35)                
        else:
            axes.plot(x, y[0,:], color = self._color_random_hex(), label = picks)
            axes.grid(visible=True, alpha = 0.35)

        fig.tight_layout()
        fig.legend()
        plt.show()

    def _color_random_hex(self):
        rgb = np.random.randint(0, 255, 3)  # Valores R, G, B
        return '#{:02x}{:02x}{:02x}'.format(*rgb)

    def __getitem__(self, key):
        if isinstance(key, tuple) and len(key) == 2:
            canales, tiempo = key
            if isinstance(tiempo, slice):
                return self.get_data(picks=canales, start=tiempo.start, stop=tiempo.stop, times=True)
            else:
                raise TypeError ("No se pudo realizar la acción de slice", tiempo)
        elif isinstance(key, (str, int, list)):
            return self.get_data(picks=key, times=True)

    def espectro_potencias(self, metodo='welch', nperseg : int = 256, plot = False):
        """
        Calcula el espectro de potencias de la señal.
        
        Parámetros:
        - metodo: str, 'welch' (método de Welch) o 'fft' (FFT directa).
        - duracion: int, longitud de cada segmento para el método de Welch (default: 256).
        - plot: bool, si es *True* plotea los espectros de potencia.
        
        Retorna:
        - frecuencias: ndarray, frecuencias correspondientes al espectro.
        - psd: ndarray, forma [canales, frecuencias], espectro de potencias.
        """
        n_canales, n_muestras = self.data.shape

        if metodo == 'welch':
            # Usar el método de Welch
            frecuencias, psd = welch(self.data, fs=self.sfreq, nperseg=nperseg, axis=1, return_onesided=True)

            if plot:
                plt.figure(figsize=(10, 6))
                for i in range(n_canales):
                    plt.semilogy(frecuencias, psd[i], label=f'Canal {i+1}')
                plt.xlabel('Frecuencia (Hz)')
                plt.ylabel('Densidad Espectral de Potencia (V²/Hz)')
                plt.title('Espectro de Potencias (Método de Welch)')
                plt.grid(True)
                plt.legend()
                plt.show()

            return frecuencias, psd
        
        elif metodo == 'fft':
            # Calcular FFT directa
            
            frecuencias = np.fft.rfftfreq(n_muestras, d=1/self.sfreq)  # Frecuencias positivas
            fft_result = np.fft.rfft(self.data, axis=1)   # FFT de cada canal
            psd = np.abs(fft_result)**2 / n_muestras           # Espectro de potencias (normalizado)
            
            if plot:
                plt.figure(figsize=(10, 6))
                for i in range(n_canales):
                    plt.plot(frecuencias, 10 * np.log10(psd[i]), label=f'Canal {i+1}')
                plt.xlabel('Frecuencia (Hz)')
                plt.ylabel('Potencia (dB/Hz)')
                plt.title('Espectro de Potencias (dB)')
                plt.grid(True)
                plt.legend()
                plt.show()
            
            return frecuencias, psd
        
        else:
            raise ValueError("Método debe ser 'welch' o 'fft'")
