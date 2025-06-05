import pandas as pd
###Clase Anotaciones###
class Anotaciones():
    """
    Esta es una clase que podrá (decir lo que hace cada función). Recibirá un diccionario de argumentos 
    nombrados (**datos), lo cual permitirá que se reciban nombres de parámetros de una manera flexible
    sin necesidad de saber de antemano cuántos argumentos con nombre va a recibir.
    """
    def __init__(self, **datos):
        longitud_datos = [len(columna) for columna in datos.values()]                                                                   #Verificar que todas las listas tengan la misma longitud
        if len(set(longitud_datos)) != 1:                                                                                               #set(longitud_datos) elimina los valores repetidos, si todas las columnas tienen la misma longitud, el set tendrá un solo valor, de lo contrario se genera un error
            raise ValueError("Todas las columnas deben tener la misma cantidad de elementos.")
        self.df = pd.DataFrame(datos)                                                                                                   #Se crea un DataFrame con las columnas
    
    def add(self, **datosnuevos):
        if set(datosnuevos.keys()) != set(self.df.columns):                                                                             #Se comparan los nombres de los argumentos con las columnas existentes
            raise ValueError(f"Las claves deben coincidir con las columnas: {list(self.df.columns)}")
        nueva_fila = pd.DataFrame([datosnuevos])                                                                                        #Se crea un DataFrame de una sola fila con los datos recibidos
        self.df = pd.concat([self.df, nueva_fila], ignore_index=True)                                                                   #Añade la nueva fila al final del DataFrame original. ignore_index=True significa que se reasignan los índices desde 0
    
    def remove(self, valor, columna="description"):                                                                                     
        if columna not in self.df.columns:                                                                                              #Verifica si el valor columna está dentro de las columnas del DataFrame, de lo contrario salta error                                         
            raise ValueError(f"La columna '{columna}' no existe en la tabla.")
        self.df = self.df[self.df[columna] != valor].reset_index(drop=True)                                                             #Dentro del DataFrame, se busca el valor en forma de string "Evento_#", si la columna coincide con el valor, se descarta esa fila. reset_index(drop=True) reasigna los índices y drop=True significa que el índice de la fila actual no se añade como una nueva columna al DataFrame.
    
    def get_annotations(self):
        return self.df
    
    def find(self, valor, columna="description"):
        if columna not in self.df.columns:                                                                                              #Verifica si el valor columna está dentro de las columnas del DataFrame, de lo contrario salta error 
            raise ValueError(f"La columna '{columna}' no existe en la tabla.")
        resultado = self.df[self.df[columna] == valor]                                                                                  #Se genera un DataFrame con una única fila correspondiente al "Evento_#" brindado
        if resultado.empty:                                                                                                             #Se pregunta si existen coincidencias, de lo contrario se avisa que no se encontró ninguna
            print(f"No se encontró ninguna fila con {columna} == '{valor}'.")
        return resultado
    
    def save(self):
        pass
    
    def load(self):
        pass

anotaciones = Anotaciones(
onset=[5.0, 12.5, 20.0],
duration=[2.0, 3.0, 3.5],
description=['Inicio_Experimento', 'Evento_1', 'Evento_2'])

#Prueba de get_annotations()
print(anotaciones.get_annotations())

#Pueba de add()
anotaciones.add(onset=3.0, duration=1.5, description="Evento_3")
print(anotaciones.get_annotations())

#Prueba de remove()
anotaciones.remove("Evento_3")
print(anotaciones.get_annotations())

#Prueba de find()
print(anotaciones.find("Evento_1"))