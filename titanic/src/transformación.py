import pandas as pd

def titanic_limpio (df_titanic):
    df_titanic_1 = df_titanic.drop(columns=['survived', 'pclass', 'sibsp', 'parch', 'fare', 'embarked', 'adult_male', 'deck', 'alone'])
    df_titanic_2 = df_titanic_1.dropna(subset=['embark_town']).fillna(df_titanic_1['age'].mean())
    return df_titanic_2