import pandas as pd

class Anotaciones:
    """
    Clase para gestionar anotaciones de eventos en un DataFrame.
    Soporta la carga, manipulación y guardado de anotaciones en formato CSV
    con columnas 'onset', 'duration' y 'event_id', como en eventos_ejemplo.csv.
    """
    
    def __init__(self, onset=None, duration=None, event_id=None):
        """
        Inicializa un objeto Anotaciones con un DataFrame vacío o con datos proporcionados.

        Args:
            onset (list of float, optional): Tiempos de inicio de los eventos en segundos.
            duration (list of float, optional): Duraciones de los eventos en segundos.
            event_id (list of str, optional): Identificadores de los eventos (ej. 'IZQUIERDA', 'DERECHA').

        Raises:
            TypeError: Si onset, duration o event_id no son listas.
            ValueError: Si las listas no tienen la misma longitud.
        """
        # Verificar si se proporcionaron datos para inicializar
        if onset is not None and duration is not None and event_id is not None:
            # Validar que los parámetros sean listas
            if not (isinstance(onset, list) and isinstance(duration, list) and isinstance(event_id, list)):
                raise TypeError("onset, duration y event_id deben ser listas.")
            # Validar que las listas tengan la misma longitud
            if not (len(onset) == len(duration) == len(event_id)):
                raise ValueError("Las listas onset, duration y event_id deben tener la misma longitud.")
            # Crear DataFrame con los datos proporcionados
            self.df = pd.DataFrame({
                'onset': onset,
                'duration': duration,
                'event_id': event_id
            })
        else:
            # Inicializar un DataFrame vacío con las columnas esperadas
            self.df = pd.DataFrame(columns=['onset', 'duration', 'event_id'])

    def add(self, **datosnuevos):
        """
        Agrega una nueva anotación al DataFrame.

        Args:
            datosnuevos (dict): Diccionario con claves 'onset', 'duration', 'event_id'.
                               Ejemplo: {'onset': 555.35, 'duration': 6.2, 'event_id': 'IZQUIERDA'}.

        Raises:
            ValueError: Si las claves no coinciden con las columnas del DataFrame.
            TypeError: Si los tipos de datos no son correctos (onset y duration deben ser numéricos,
                       event_id debe ser str).

        Ejemplo:
            anot.add(onset=555.35, duration=6.2, event_id="IZQUIERDA")
        """
        # Validar que las claves del diccionario coincidan con las columnas
        if set(datosnuevos.keys()) != set(self.df.columns):
            raise ValueError(f"Las claves deben coincidir con las columnas: {list(self.df.columns)}")
        
        # Validar tipos de datos
        if not isinstance(datosnuevos['onset'], (int, float)):
            raise TypeError("El valor de 'onset' debe ser numérico (int o float).")
        if not isinstance(datosnuevos['duration'], (int, float)):
            raise TypeError("El valor de 'duration' debe ser numérico (int o float).")
        if not isinstance(datosnuevos['event_id'], str):
            raise TypeError("El valor de 'event_id' debe ser una cadena (str).")

        # Convertir el diccionario en un DataFrame de una sola fila
        nueva_fila = pd.DataFrame([datosnuevos])
        # Concatenar la nueva fila al DataFrame existente
        self.df = pd.concat([self.df, nueva_fila], ignore_index=True)

    def remove(self, valor, columna="event_id", por_indice=False):
        """
        Elimina anotaciones del DataFrame por valor o índice.

        Args:
            valor: Valor a buscar o índice de la fila a eliminar.
            columna (str, optional): Columna en la que buscar el valor (default: 'event_id').
            por_indice (bool, optional): Si True, elimina por índice en lugar de valor (default: False).

        Raises:
            ValueError: Si la columna especificada no existe.
            IndexError: Si el índice está fuera de rango.

        Ejemplo:
            anot.remove("IZQUIERDA")  # Elimina filas donde event_id == 'IZQUIERDA'
            anot.remove(0, por_indice=True)  # Elimina la fila en el índice 0
        """
        if por_indice:
            # Validar que el índice esté dentro del rango
            if not (0 <= valor < len(self.df)):
                raise IndexError(f"El índice {valor} está fuera del rango válido (0 a {len(self.df)-1}).")
            # Eliminar la fila por índice y reindexar
            self.df = self.df.drop(index=valor).reset_index(drop=True)
        else:
            # Validar que la columna exista
            if columna not in self.df.columns:
                raise ValueError(f"La columna '{columna}' no existe en la tabla.")
            # Eliminar filas donde el valor coincida en la columna especificada
            self.df = self.df[self.df[columna] != valor].reset_index(drop=True)

    def find(self, valor, columna="event_id", por_indice=False):
        """
        Busca anotaciones por valor en una columna o por índice.

        Args:
            valor: Valor a buscar o índice de la fila.
            columna (str, optional): Columna en la que buscar (default: 'event_id').
            por_indice (bool, optional): Si True, busca por índice (default: False).

        Returns:
            pd.DataFrame: DataFrame con las filas encontradas.

        Ejemplo:
            anot.find("DERECHA")  # Busca filas donde event_id == 'DERECHA'
            anot.find(0, por_indice=True)  # Devuelve la fila en el índice 0
        """
        if por_indice:
            # Validar que el índice esté dentro del rango
            if not (0 <= valor < len(self.df)):
                raise IndexError(f"El índice {valor} está fuera del rango (0 a {len(self.df)-1}).")
            # Devolver la fila en el índice especificado
            resultado = self.df.iloc[[valor]]
            print(f"Fila encontrada en el índice {valor}:")
            return resultado
        else:
            # Validar que la columna exista
            if columna not in self.df.columns:
                raise ValueError(f"La columna '{columna}' no existe en la tabla.")
            # Buscar filas donde el valor coincida en la columna
            resultado = self.df[self.df[columna] == valor]
            if resultado.empty:
                print(f"No se encontró ninguna fila con {columna} == '{valor}'.")
            else:
                print(f"Coincidencias encontradas con {columna} == '{valor}':")
            return resultado

    def get_annotations(self):
        """
        Devuelve todas las anotaciones actuales.

        Returns:
            pd.DataFrame: DataFrame con las columnas 'onset', 'duration', 'event_id'.
        """
        return self.df

    def save(self, ruta):
        """
        Guarda las anotaciones en un archivo CSV con formato de tabulaciones.

        Args:
            ruta (str): Ruta donde guardar el archivo CSV.

        Ejemplo:
            anot.save("anotaciones.csv")
        """
        # Verificar si el DataFrame está vacío
        if self.df.empty:
            print("El DataFrame está vacío. Nada fue guardado.")
            return
        # Guardar el DataFrame como CSV con tabulaciones
        self.df.to_csv(ruta, sep='\t', index=False)
        print(f"Archivo guardado en: {ruta}")

    def load(self, ruta):
        """
        Carga anotaciones desde un archivo CSV con formato de tabulaciones.

        Args:
            ruta (str): Ruta del archivo CSV.

        Raises:
            ValueError: Si el archivo no tiene las columnas esperadas o no se puede cargar.

        Ejemplo:
            anot.load("eventos_ejemplo.csv")
        """
        # Columnas esperadas en el archivo CSV
        columnas_esperadas = {'onset', 'duration', 'event_id'}
        
        try:
            # Cargar el archivo CSV con delimitador de tabulaciones
            self.df = pd.read_csv(ruta, sep='\t', engine='python')
            
            # Eliminar columna de índice si existe
            if 'Unnamed: 0' in self.df.columns:
                self.df.drop(columns=['Unnamed: 0'], inplace=True)
            
            # Validar que las columnas sean las esperadas
            if set(self.df.columns) != columnas_esperadas:
                raise ValueError(f"El archivo debe tener exactamente las columnas: {columnas_esperadas}")
            
            # Convertir tipos de datos
            self.df['onset'] = pd.to_numeric(self.df['onset'], errors='raise')
            self.df['duration'] = pd.to_numeric(self.df['duration'], errors='raise')
            self.df['event_id'] = self.df['event_id'].astype(str)
            
            print(f"Archivo cargado correctamente desde: {ruta}")
        
        except pd.errors.ParserError:
            raise ValueError(f"No se pudo cargar el archivo '{ruta}'. Verifica que esté separado por tabulaciones.")
        except ValueError as e:
            raise ValueError(f"Error al cargar el archivo: {str(e)}")
