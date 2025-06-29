import pandas as pd

class Anotaciones:
    """
    Clase Anotaciones:
    Permite agregar, eliminar, buscar, guardar y cargar anotaciones de eventos.

    Atributos:
    self.df : pd.DataFrame
    Contiene las anotaciones en formato de columnas como 'onset', 'duration' y 'event_id'.

    Métodos:
    - add(): Agrega una nueva anotación validando estructura y tipo de datos.
    - remove(): Elimina eventos por event_id o cualquier columna.
    - find(): Busca eventos por un valor dado.
    - get_annotations(): Devuelve todas las anotaciones.
    - save(): Guarda las anotaciones como archivo CSV.
    - load(): Carga anotaciones desde un CSV y valida las columnas.
    """

    def __init__(self, onset=None, duration=None, event_id=None):
        """
        Constructor de la clase Anotaciones. Si se reciben listas, se crea un DataFrame con ellas.
        Si no se pasa nada, se inicializa con columnas vacías.

        Parametros:
        onset : list of float
            Tiempos de inicio de cada evento.
        duration : list of float
            Duraciones de cada evento.
        event_id : list of str
            Descripción de cada evento.
        """
        if onset is not None and duration is not None and event_id is not None:

            #Validación del tipo
            if not (isinstance(onset, list) and isinstance(duration, list) and isinstance(event_id, list)):
                raise TypeError("onset, duration y event_id deben ser listas.")
            
            #Validación de la longitud
            if not (len(onset) == len(duration) == len(event_id)):
                raise ValueError("Las listas onset, duration y event_id deben tener la misma longitud.")

            # Se crea el DataFrame con las columnas correspondientes
            self.df = pd.DataFrame({
                'onset': onset,
                'duration': duration,
                'event_id': event_id
            })

        else:
            #Se inicializa un DataFrame vacío con las columnas esperadas
            self.df = pd.DataFrame(columns=['onset', 'duration', 'event_id'])

    def add(self, **datosnuevos):
        """
        Agrega una nueva anotación al DataFrame.

        Parametros:
        datosnuevos : dict
            Debe incluir claves que coincidan exactamente con las columnas del DataFrame.
            Ejemplo: onset, duration, event_id

        Ejemplo de uso:
            x.add(onset=555.35, duration=6.2, event_id="IZQUIERDA")
        """
        if set(datosnuevos.keys()) != set(self.df.columns):
            raise ValueError(f"Las claves deben coincidir con las columnas: {list(self.df.columns)}")
        
        #Se verifican los tipos por columna
        if not isinstance(datosnuevos['onset'], (int, float)):
            raise TypeError("El valor de 'onset' debe ser numérico (int o float).")
        if not isinstance(datosnuevos['duration'], (int, float)):
            raise TypeError("El valor de 'duration' debe ser numérico (int o float).")
        if not isinstance(datosnuevos['event_id'], str):
            raise TypeError("El valor de 'event_id' debe ser una cadena (str).")

        #Se convierte el dict a DataFrame de una sola fila
        nueva_fila = pd.DataFrame([datosnuevos])

        #Se agrega al final del DataFrame existente
        self.df = pd.concat([self.df, nueva_fila], ignore_index=True)

    def remove(self, valor, columna="event_id", por_indice=False):
        """
        Elimina una anotación del DataFrame por valor o por índice.

        Parametros:
        valor : any
            Valor a buscar o índice de fila a eliminar.
        columna : str
            Columna en la que buscar el valor (si por_indice es False).
        por_indice : bool
            Si es True, 'valor' se interpreta como índice de fila a eliminar.

        Ejemplo de uso:
            x.remove(valor=40, por_indice=True)
        """
        if por_indice:

            #Se verifica si el índice está dentro del rango
            if not (0 <= valor < len(self.df)):
                raise IndexError(f"El índice {valor} está fuera del rango válido (0 a {len(self.df)-1}).")
            
            #Se elimina la fila por índice
            self.df = self.df.drop(index=valor).reset_index(drop=True)
        else:

            #Se elimina por valor en columna
            if columna not in self.df.columns:
                raise ValueError(f"La columna '{columna}' no existe en la tabla.")
            self.df = self.df[self.df[columna] != valor].reset_index(drop=True)

    def find(self, valor, columna="event_id", por_indice=False):
        """
        Busca y devuelve una o más filas del DataFrame por valor en una columna,
        o por índice si se especifica.

        Parametros:
        valor : any
            Valor a buscar, o índice si 'por_indice=True'.
        columna : str
            Nombre de la columna en la que buscar el valor (si por_indice=False).
        por_indice : bool
            Si es True, se busca por índice de fila.

        Returns:
        pd.DataFrame con la(s) fila(s) encontrada(s).

        Ejemplo de uso:
            x.find(valor=39, por_indice=True)
        """
        if por_indice:
            if not (0 <= valor < len(self.df)):
                raise IndexError(f"El índice {valor} está fuera del rango (0 a {len(self.df)-1}).")
            
            #Se devuelve la fila como DataFrame con .iloc
            resultado = self.df.iloc[[valor]]
            print(f"Fila encontrada en el índice {valor}:")
            return resultado
        else:
            if columna not in self.df.columns:
                raise ValueError(f"La columna '{columna}' no existe en la tabla.")
            resultado = self.df[self.df[columna] == valor]
            if resultado.empty:
                print(f"No se encontró ninguna fila con {columna} == '{valor}'.")
            else:
                print(f"Coincidencias encontradas con {columna} == '{valor}':")
            return resultado

    def get_annotations(self):
        """
        Devuelve el DataFrame con todas las anotaciones actuales.

        Returns:
        pd.DataFrame con las columnas ['onset', 'duration', 'event_id'].
        """
        return self.df

    def save(self, ruta):
        """
        Guarda las anotaciones en un archivo CSV.

        Parametros:
        ruta : str
            Ruta completa donde se desea guardar el archivo.
        """
        if self.df.empty:
            print("El DataFrame está vacío. Nada fue guardado.")
            return
        self.df.to_csv(ruta, index=False)
        print(f"Archivo guardado en: {ruta}")

    def load(self, ruta):
        """
        Carga anotaciones desde un archivo CSV.

        Parametros:
        ruta : str
            Ruta del archivo CSV.

        Error:
        ValueError si las columnas del CSV no coinciden con ['onset', 'duration', 'event_id']
        """
        self.df = pd.read_csv(ruta)
        # Si se carga una columna extra (como índice), se elimina
        if 'Unnamed: 0' in self.df.columns:
            self.df.drop(columns=['Unnamed: 0'], inplace=True)

        columnas_esperadas = {'onset', 'duration', 'event_id'}
        if set(self.df.columns) != columnas_esperadas:
            raise ValueError(f"El archivo debe tener las columnas: {columnas_esperadas}")
