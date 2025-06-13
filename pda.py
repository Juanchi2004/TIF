## Trabajo integrador final.
## Realizado por Juan Etchart y Gabriel Ferrer.


class Info():
    """
    Clase para almacenar información acerca del registro de datos.

    Esta clase se comporta como un diccionario.
            Genera un objeto Info().
        
        Parameters
    ---------
            ch_names : list of str, optional
                Lista con los nombres de los canales.

            ch_types : str or list of str, optional
                Tipo de cada canal (ej: 'eeg', 'ecg', etc.) o un único tipo para todos.

            bads : list of str, optional
                Lista de canales marcados como "malos".

            sfreq : float, optional
                Frecuencia de muestreo en Hz (por defecto 512).

            description: str, optional
                Descripción del registro de datos.
            
            experimenter : str, optional
                Nombre del experimentador.

            subject_info: dict, optional
                Información adicional del sujeto.

        ---------
        Raises
        
            ValueError. 
                Si **ch_names** y **ch_types** no tienen la misma longitud.
    """
    
    
    def __init__(self, ch_names:list = None, ch_types:list | str ="unknown", bads=None, sfreq=512, description=None, experimenter="No data", subject_info=None):
        """
        Genera un objeto Info().
        
        Parameters
        ---------
            ch_names : list of str, optional
                Lista con los nombres de los canales.

            ch_types : str or list of str, optional
                Tipo de cada canal (ej: 'eeg', 'ecg', etc.) o un único tipo para todos.

            bads : list of str, optional
                Lista de canales marcados como "malos".

            sfreq : float, optional
                Frecuencia de muestreo en Hz (por defecto 512).

            description: str, optional
                Descripción del registro de datos.
            
            experimenter : str, optional
                Nombre del experimentador.

            subject_info: dict, optional
                Información adicional del sujeto.

        ---------
        Raises
        
            ValueError. 
                Si **ch_names** y **ch_types** no tienen la misma longitud.
        
        """
        if isinstance(ch_types, str):
            ch_types = [ch_types]*len(ch_names)
        try:
            if len(ch_names) == len(ch_types):
                
                self.ch_names:list = ch_names #lista de nombres de los canales -> list[str,...]
                self.ch_types:list = ch_types #lista de los tipos de canales -> list[str,...]
                self.bads:list = bads #lista de canales malos -> list[str,...] 
                self.sfreq:int = sfreq #entero con la frecuencia de muestreo
                self.description:str = description #Texto de descripción
                self.experimenter:str = experimenter #Texto del autor del experimento
                self.subject_info:dict = subject_info #diccionario con datos del autor del experimento (edad, sexo, etc)

                
        except ValueError as vErr:
            raise (f"Las longitudes de las listas *ch_names* y *ch_types* es distitno", vErr)
       
    def  __contains__(self, item):
        # Permite verificar si una clave está en el objeto.
        return hasattr(self, item)
    
    def __getitem__(self, key):
        # Permite acceder a elementos como un diccionario.
        return getattr(self, key)

    def __len__(self):
        # Preguntar a Lucas que es lo que quiera implementar.
        # Devuelve la cantidad de elementos almacenados.

        return len(self.__dict__.keys())

    def get(self, key):
        """
        Retorna los valores asociado al atributo que desea acceder.
        """
        # Obtiene el valor de una clave específica.
        return getattr(self, key)

    def keys(self):
        """
        Retorna los nombres de los atributos del objeto.
        """
        # Devuelve las claves del objeto.
        return self.__dict__.keys()

    def items(self):
        """
        Retorna una lista con los atributos del objeto y el valor asociado a dicho atriburo.\n
        
        Forma:
        - [("atributo", valor), (...), ...]
        """
        # Devuelve los elementos como pares clave-valor.
        return list(self.__dict__.items())

    def rename_channels(self, rename:dict):
        # Permite renombrar canales de forma segura.
        for key, value in rename.items():
            if key in self.ch_names:
                self.ch_names[self.ch_names.index(key)] = value
            else:
                raise ValueError (f"El canal ({key}) no se encuentra dentro de los canales") 
        return True

    def copy(self):
        """Retorna un objeto distinto con las mismas caracteristicas que el original"""

        return Info(self.ch_names, self.ch_types, self.bads, self.sfreq, self.description, self.experimenter, self.subject_info)