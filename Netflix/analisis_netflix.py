import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
###################################
datos_netflix = pd.read_csv("datos_netflix.csv")
datos_netflix["show_id"] = datos_netflix["show_id"].str.replace('[s]', ' ', regex=True) #eliminamos la 's' en todos los 'show_id'
datos_netflix["title"] = datos_netflix["title"].str.replace('[#]','',regex=True ) #eliminamos la '#' en todos los 'title'
###################################
datos_netflix_limpio = datos_netflix.dropna() #elinamos los NA o documentos en blanco
datos_netflix_limpio = datos_netflix_limpio.drop('description', axis=1) #eliminamos la columna 'description' del dataframe
datos_netflix_limpio = datos_netflix_limpio.drop('show_id', axis=1) #eliminamos la columna 'show_id' del dataframe
datos_netflix_limpio['show_id'] = datos_netflix_limpio.index #creamos una columna indice nueva 'show_id
print(datos_netflix_limpio)
################################### (1º pregunta)
datos_netflix_limpio_90s = datos_netflix_limpio[(datos_netflix_limpio['release_year']>=1990)&(datos_netflix_limpio['release_year']<=1999)] #Filtra las filas donde los años están entre 1990 y 1999
duration_90s =datos_netflix_limpio_90s['duration'].mode()[0] #Calcula la moda (duración más frecuente) de la columna duración.
print("La duración más frecuente de las películas entre 1990 y 1999 es:", duration_90s)
################################### (2º pregunta)
datos_netflix_limpio_90s = datos_netflix_limpio[(datos_netflix_limpio['release_year']>=1990)&(datos_netflix_limpio['release_year']<=1999)]
peliculas_accion_menos90 = datos_netflix_limpio_90s[(datos_netflix_limpio_90s['genre'].str.contains('Action', case=False)) & (datos_netflix_limpio_90s['duration'] < 90)] #Filtra las películas cuyo género contenga la palabra "action". El argumento case=False hace que la búsqueda no sea sensible a mayúsculas/minúsculas y Filtra las películas que duran menos de 90 minutos.
total_peliculas_accion_menos90= peliculas_accion_menos90.shape[0] #Cuenta el número de filas (películas) que cumplen con las condiciones.
print("El número total de películas de acción que duran menos de 90 minutos entre 1990 y 1999 es:", total_peliculas_accion_menos90)
################################### (grafico de barras 1)
cantidad_total = datos_netflix_limpio['genre'].value_counts() #calculamos el nº total de peliculas por genero
plt.figure(figsize=(9, 4)) # dimensiones del grafico de barras. 
cantidad_total.plot(kind='bar')
plt.xlabel('Genero')
plt.xticks(rotation=45, ha="right")
plt.ylabel('Cantidad')
plt.show()
################################### (grafico de queso*)
cantidad_total = datos_netflix_limpio['type'].value_counts()
plt.figure(figsize=(9, 4)) # dimensiones del grafico de barras. 
cantidad_total.plot(kind='bar')
plt.xlabel('Tipo')
plt.xticks(rotation=45, ha="right")
plt.ylabel('Cantidad')
plt.show()
################################### (grafico lineal)
datos_filtrados = datos_netflix_limpio[datos_netflix_limpio['release_year'] >= 1990] #filtramos datos a partir de 1990
cantidad_estrenos = datos_filtrados['dated_added'].value_counts().sort_index() #codigo para calcular el numero de estrenos por año
plt.plot(cantidad_estrenos.index, cantidad_estrenos.values) #codigo para grafico lineal
plt.xlabel('Año')
plt.ylabel('Estrenos')
plt.show()