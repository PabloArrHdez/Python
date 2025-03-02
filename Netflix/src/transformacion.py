import pandas as pd
df_netflix = pd.read_csv("data/datos_netflix.csv")

def columnas_delete(df_netflix):
    df_netflix_1 = df_netflix.drop(columns=['description','show_id'])
    return df_netflix_1

def remplazo_title(df_netflix_1):
    df_netflix_2 = df_netflix_1.replace('[#]','',regex=True)
    return df_netflix_2

def columna_fecha(df_netflix_2):
    df_netflix_1 = df_netflix.drop(columns=['description','show_id'])
    df_netflix_2 = df_netflix_1.replace('[#]','',regex=True)
    df_netflix_2['date_added'] = pd.to_datetime(df_netflix_2['date_added'], format='mixed', errors='coerce') 
    df_netflix_2['date_added'] = pd.to_datetime(df_netflix_2['date_added'], format='%Y-%m-%d')
    df_netflix_2['date_added_year'] = df_netflix_2['date_added'].dt.year
    return df_netflix_2['date_added_year']

def duracion_90_99 (df_netflix_2):
    df_netflix_2_90s = df_netflix_2[(df_netflix_2['release_year']>=1990)&(df_netflix_2['release_year']<=1999)]
    duration_90s = df_netflix_2_90s['duration'].mode()[0]
    print(f"La duración más frecuente de las películas entre 1990 y 1999 es: {duration_90s} minutos")

def accion_menos90 (df_netflix_2_90s):
    pel_accion_menos90 = df_netflix_2_90s[(df_netflix_2_90s['genre'].str.contains('Action', case=False)) & (df_netflix_2_90s['duration'] < 90)]
    t_pel_accion_menos90 = pel_accion_menos90.shape[0] 
    print(f"El número total de películas de acción que duran menos de 90 minutos entre 1990 y 1999 es: {t_pel_accion_menos90} peliculas")