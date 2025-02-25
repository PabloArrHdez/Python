import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

import src.exploracion as exp
import src.transformación as trs
import src.visualizacion as viz

if __name__== "__main__":
    df_titanic = pd.read_csv("data/titanic.csv")

    exp.descripcion_df(df_titanic)
    trs.titanic_limpio(df_titanic)

    df_titanic_1 = df_titanic.drop(columns=['survived', 'pclass', 'sibsp', 'parch', 'fare', 'embarked', 'adult_male', 'deck', 'alone'])
    df_titanic_2 = df_titanic_1.dropna(subset=['embark_town']).fillna(df_titanic_1['age'].mean())
    viz.grafico_1(df_titanic_2)
    viz.grafico_2(df_titanic_2)