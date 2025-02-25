import seaborn as sns
import matplotlib.pyplot as plt

## 1º grafico ##
def grafico_1(df_titanic_2):
    muertos = df_titanic_2[df_titanic_2["alive"]=="no"]
    plt.figure(figsize=(8, 6))
    grafico = sns.histplot(data=muertos, x="sex", hue="who", multiple="stack", shrink=0.8, discrete=True)
    plt.xlabel("Género", fontsize=12)
    plt.ylabel("Cantidad", fontsize=12)
    plt.title("Cantidad de fallecidos", fontsize=14)
    plt.savefig("imagenes/fallecidos_sexo.png")
    plt.show();

## 2º grafico ##
def grafico_2(df_titanic_2):
    vivos = df_titanic_2[df_titanic_2["alive"]=="yes"]
    categoria = vivos['class'].value_counts()
    sns.set(style="whitegrid")
    plt.figure(figsize=(7, 7))
    plt.pie(categoria, labels=categoria.index, autopct='%1.1f%%',startangle=90, colors=sns.color_palette("Set2", len(categoria)))
    plt.title('Distribución de clases entre los sobrevivientes')
    plt.axis('equal')  
    plt.savefig("imagenes/categoria_vivos.png")
    plt.show();