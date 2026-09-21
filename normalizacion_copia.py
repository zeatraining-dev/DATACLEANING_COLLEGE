# Author: Gabriel Martínez Vazquez
# Date: 14-08-2026

# ------------------------------------------------------------
# NORMALIZACIÓN DE NOMBRES Y APELLIDOS
# ------------------------------------------------------------

# Importamos la librería pandas para trabajar con
# estructuras de datos y archivos de Excel.
import pandas as pd


# ------------------------------------------------------------
# CARGA DE LOS DATOS
# ------------------------------------------------------------

# Leemos el archivo de Excel y almacenamos la información
# en un DataFrame llamado "docente".
docente = pd.read_excel("dataset_original.xlsx")


# ------------------------------------------------------------
# FUNCIÓN PARA NORMALIZAR EL TEXTO
# ------------------------------------------------------------

# Esta función recibe una col   umna del DataFrame y
# convierte el contenido de cada celda a minúsculas.
def normalizar(nombre_docente):

    # Convertimos cada valor de la columna a minúsculas.
    minuscula = (
        nombre_docente.str.lower()
    )

    # Retornamos la columna ya normalizada.
    return minuscula


# ------------------------------------------------------------
# COLUMNAS A PROCESAR
# ------------------------------------------------------------

# Definimos las columnas que contienen los nombres
# y apellidos que serán procesados.
columnas = ["nombre", "ape_paterno", "ape_materno"]


# ------------------------------------------------------------
# PALABRAS QUE DEBEN CONSERVARSE EN MINÚSCULAS
# ------------------------------------------------------------

# Estas palabras son excepciones al formato generado
# por .str.title(), por lo que posteriormente serán
# convertidas nuevamente a minúsculas.
excepciones = ["De", "Y", "La", "El", "Del", "Los", "Las"]


# ------------------------------------------------------------
# NORMALIZACIÓN DE NOMBRES Y APELLIDOS
# ------------------------------------------------------------

# Recorremos cada una de las columnas definidas anteriormente.
for columna in columnas:

    # Primero convertimos todo el contenido a minúsculas
    # mediante la función "normalizar".
    # Después utilizamos .str.title() para colocar en mayúscula
    # la primera letra de cada palabra.
    docente[columna] = normalizar(docente[columna]).str.title()

    # Separamos cada celda en una lista de palabras.
    # Ejemplo:
    # "Juan Garcia Lopez" -> ["Juan", "Garcia", "Lopez"]
    docente[columna] = docente[columna].str.split()

    # Recorremos cada fila por cada columna.
    for fila in docente[columna]:

        # Recorremos cada palabra utilizando su posición
        # dentro de la lista.
        for i in range(len(fila)):

            # Comparamos la palabra actual con la lista
            # de excepciones.
            if fila[i] in excepciones:

                # Si la palabra pertenece a las excepciones,
                # la convertimos a minúsculas.
                fila[i] = fila[i].lower()

    # Unimos nuevamente las palabras de cada fila utilizando
    # un espacio para recuperar el formato de texto original.
    # Ejemplo:
    # ["Juan", "de", "Garcia"] -> "Juan de Garcia"
    docente[columna] = docente[columna].apply(" ".join)


# ------------------------------------------------------------
# CREACIÓN DE UNA COPIA CON LAS COLUMNAS NECESARIAS
# ------------------------------------------------------------

# Creamos una copia que contiene únicamente las columnas
# de nombres y apellidos que serán utilizadas para obtener
# una lista de palabras únicas.
lista_columnas = docente[["nombre", "ape_paterno", "ape_materno"]].copy()


# ------------------------------------------------------------
# FUNCIÓN PARA OBTENER PALABRAS INDIVIDUALES
# ------------------------------------------------------------

# Esta función recibe una columna y separa cada nombre o
# apellido en palabras individuales.
def nombres_unicos(columna):

    # .str.split() separa cada celda en palabras y
    # .explode() convierte cada palabra en una fila independiente.
    lista_unicos = (
        columna.str.split().explode()
    )

    # Retornamos la lista de palabras individuales.
    return lista_unicos


# ------------------------------------------------------------
# UNIFICACIÓN DE TODAS LAS PALABRAS
# ------------------------------------------------------------

# Creamos una lista vacía donde almacenaremos todas las
# palabras obtenidas de nombres y apellidos.
lista_unidos = []


# Recorremos cada una de las columnas de nombres y apellidos.
for columna in columnas:

    # Obtenemos las palabras individuales de la columna actual.
    lista_separados = nombres_unicos(lista_columnas[columna])

    # Recorremos cada palabra obtenida y la agregamos
    # a la lista general.
    for palabra in lista_separados:
        lista_unidos.append(palabra)


# ------------------------------------------------------------
# ELIMINACIÓN DE PALABRAS NO NECESARIAS
# ------------------------------------------------------------

# Lista de palabras que no se desean conservar en el
# resultado de palabras únicas.
eliminar = ["de", "y", "la", "el", "del", "los", "las"]


# Convertimos la lista de palabras en un DataFrame para
# facilitar su limpieza y manipulación con pandas.
lista_unidos = pd.DataFrame(lista_unidos, columns=["separados"])


# Elimina los valores duplicados de la columna "separados",
# conservando únicamente la primera aparición de cada valor.
lista_unidos = lista_unidos.loc[~lista_unidos["separados"].duplicated()]


# Eliminamos las palabras que se encuentran dentro de
# la lista "eliminar".
lista_unidos = lista_unidos.loc[~lista_unidos["separados"].isin(eliminar)]


# Exporta los nombres y apellidos únicos a un archivo CSV que servirá
# como referencia para detectar la incorporación de acentos faltantes, 
# mediante un diccionario de correcciones.
lista_unidos.to_csv("dataset_diccionario.csv", index=False)



# ------------------------------------------------------------
# DICCIONARIO DE CORRECCIONES
# ------------------------------------------------------------

# Diccionario utilizado para corregir palabras que necesitan acentos ortográficos.
# La clave representa la palabra encontrada en los datos
# y el valor representa su forma corregida.
correcciones = {
    "Maria": "María",
    "Rocio": "Rocío",
    "Angel": "Ángel",
    "Cesar": "César",
    "Julian": "Julián",
    "Jose": "José",
    "Concepcion": "Concepción",
    "Jesus": "Jesús",
    "Anais": "Anaís",
    "Ramon": "Ramón",
    "Alvaro": "Álvaro",
    "Oscar": "Óscar",
    "Diogenes": "Diógenes",
    "Alvarez": "Álvarez",
    "Chavez": "Chávez",
    "Dominguez": "Domínguez",
    "Garcia": "García",
    "Gonzalez": "González",
    "Guzman": "Guzmán",
    "Hernandez": "Hernández",
    "Jimenez": "Jiménez",
    "Leon": "León",
    "Lopez": "López",
    "Ordoñez": "Ordóñez",
    "Perez": "Pérez",
    "Ramirez": "Ramírez",
    "Sanchez": "Sánchez",
    "Cordova": "Córdova",
    "Frias": "Frías",
    "Gomez": "Gómez",
    "Calderon": "Calderón",
    "Diaz": "Díaz",
    "Martinez": "Martínez",
    "Elias": "Elías",
    "Silvan": "Silván"
}


# ------------------------------------------------------------
# APLICACIÓN DE LAS CORRECCIONES
# ------------------------------------------------------------

# Recorremos nuevamente las columnas que contienen
# nombres y apellidos.
for columna in columnas:

    # Separamos nuevamente cada celda en palabras
    # individuales para poder revisar cada una.
    docente[columna] = docente[columna].str.split()

    # Recorremos cada fila de la columna.
    for fila in docente[columna]:

        # Recorremos cada palabra mediante su posición.
        for i in range(len(fila)):

            # Verificamos si la palabra actual existe
            # dentro del diccionario de correcciones.
            if fila[i] in correcciones:

                # Si existe, reemplazamos la palabra por
                # su versión corregida con acento.
                fila[i] = correcciones[fila[i]]

    # Unimos nuevamente las palabras para recuperar
    # el formato de texto.
    docente[columna] = docente[columna].apply(" ".join)


# ------------------------------------------------------------
# EXPORTACIÓN DE LOS RESULTADOS
# ------------------------------------------------------------

# Guardar el DataFrame ya normalizado en un nuevo archivo de Excel.
docente.to_excel("dataset_normalizado.xlsx", index=False)


# Mostramos en pantalla el resultado final.
#print(docente)