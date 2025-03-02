import matplotlib.pyplot as plt

def peliculas_genero (df_netflix_2):
    total_genero = df_netflix_2['genre'].value_counts() 
    plt.figure(figsize=(9, 4))  
    total_genero.plot(kind='bar')
    plt.xlabel('Genero')
    plt.xticks(rotation=45, ha="right") 
    plt.ylabel('Cantidad')
    plt.savefig("imagenes/nº_peliculas_genero.png")
    plt.show();

def filmografia_tipo (df_netflix_2):
    total_tipo = df_netflix_2['type'].value_counts()
    plt.figure(figsize=(9, 4))
    total_tipo.plot(kind='bar')
    plt.xlabel('Tipo')
    plt.xticks(rotation=45, ha="right") 
    plt.ylabel('Cantidad')
    plt.savefig("imagenes/nº_filmografia_tipo.png")
    plt.show();

def filmografia_año(df_netflix_2):
    filmografia = df_netflix_2['data_added_year'].value_counts().sort_index() 
    plt.figure(figsize=(8, 5)) 
    plt.plot(filmografia.index, filmografia.values, marker='o', linestyle='-', color='b') #
    plt.xlabel('Años') 
    plt.ylabel('Cantidad') 
    plt.grid(True)
    plt.savefig("imagenes/filmografia_año.png")
    plt.show();