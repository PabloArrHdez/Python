import pandas as pd
import matplotlib.pyplot as plt

import src.exploracion as exp
import src.transformacion as trs
import src.visualizacion as viz

if __name__== "__main__":
    df_netflix = pd.read_csv("data/datos_netflix.csv")
    df_netflix_1 = df_netflix.drop(columns=['description','show_id'])
    df_netflix_2 = df_netflix_1.replace('[#]','',regex=True)
    df_netflix_2_90s = df_netflix_2[(df_netflix_2['release_year']>=1990)&(df_netflix_2['release_year']<=1999)]

    exp.descripcion(df_netflix)

    trs.columnas_delete(df_netflix)
    trs.remplazo_title(df_netflix_1)
    trs.columna_fecha(df_netflix_2)
    trs.duracion_90_99(df_netflix_2)
    trs.accion_menos90(df_netflix_2_90s)

    viz.peliculas_genero(df_netflix_2)
    viz.filmografia_tipo(df_netflix_2)
    viz.filmografia_año(df_netflix_2)