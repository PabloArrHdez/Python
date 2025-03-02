import pandas as pd

df_netflix = pd.read_csv("data/datos_netflix.csv")

def descripcion (df_netflix):
    print(f"Esto tiene: {df_netflix.shape[0]} filas y {df_netflix.shape[1]} columnas")
    print (f"Tiene un total de: {df_netflix.isna().sum().values.sum()} valores nulos")