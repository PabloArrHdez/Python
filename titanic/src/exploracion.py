import pandas as pd
df_titanic = pd.read_csv("data/titanic.csv")

def descripcion_df(df_titanic):
    print(f"Esto tiene: {df_titanic.shape[0]} filas y {df_titanic.shape[1]} columnas")
    print (f"Tiene un total de: {df_titanic.isna().sum().values.sum()} valores nulos")