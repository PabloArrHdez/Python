import matplotlib.pyplot as plt

def grafico_barras_1 (df_netflix_2):
    total_genero = df_netflix_2['genre'].value_counts() 
    plt.figure(figsize=(9, 4))  
    total_genero.plot(kind='bar')
    plt.xlabel('Genero')
    plt.xticks(rotation=45, ha="right") 
    plt.ylabel('Cantidad')
    plt.savefig("imagenes/nº_peliculas_genero.png")
    plt.show();