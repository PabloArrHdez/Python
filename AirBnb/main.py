import matplotlib.pyplot as plt

from src.exploration import cargar_datos, explorar_datos, cargar_datos_reducidos
from src.transformation import (
    eliminar_columnas_innecesarias, resumen_nulos, eliminar_filas_sin_datos_clave,
    marcar_tiene_resenas, imputar_bedrooms, calcular_limites_precio,
    eliminar_precios_atipicos, tramos_minimum_nights, limpiar_minimum_nights,
    analizar_accommodates, analizar_property_type, preparar_variables_exploratorias,
)
from src.visualization import (
    configurar_estilo, graficar_correlacion_precio, graficar_precio_por_capacidad,
    graficar_precio_por_tipo_alojamiento, graficar_relacion_valoracion_precio,
    graficar_top10_barrios_baratos, graficar_mapa_precios, graficar_ubicacion_vs_precio,
    graficar_precio_por_huesped, graficar_peso_puntuacion_valoracion,
    graficar_peso_estancias_largas, graficar_precio_largaestancia,
    graficar_pct_sin_resenas_por_tipo, graficar_pct_sin_resenas_por_precio,
)


def etl():
    listings = cargar_datos("data/Listings.csv")
    explorar_datos(listings)

    listings_reduce = eliminar_columnas_innecesarias(listings)
    resumen_nulos(listings_reduce)
    listings_reduce = eliminar_filas_sin_datos_clave(listings_reduce)
    listings_reduce = marcar_tiene_resenas(listings_reduce)
    listings_reduce = imputar_bedrooms(listings_reduce)
    listings_reduce = calcular_limites_precio(listings_reduce)
    listings_reduce = eliminar_precios_atipicos(listings_reduce)

    tramos = tramos_minimum_nights(listings_reduce)
    listings_reduce = limpiar_minimum_nights(listings_reduce)
    analizar_accommodates(listings_reduce)
    analizar_property_type(listings_reduce)
    return listings_reduce


def analisis_exploratorio():
    listings_exploratory = cargar_datos_reducidos("data/listings_reduce.csv")
    listings_exploratory = preparar_variables_exploratorias(listings_exploratory)
    ciudades = sorted(listings_exploratory["city"].unique())

    configurar_estilo()
    graficar_correlacion_precio(listings_exploratory)
    graficar_precio_por_capacidad(listings_exploratory)
    graficar_precio_por_tipo_alojamiento(listings_exploratory, ciudades)

    b, mask, _, _ = graficar_relacion_valoracion_precio(listings_exploratory)
    graficar_top10_barrios_baratos(b, mask)

    graficar_mapa_precios(listings_exploratory, ciudades)
    graficar_ubicacion_vs_precio(listings_exploratory)
    graficar_precio_por_huesped(listings_exploratory)
    graficar_peso_puntuacion_valoracion(listings_exploratory)
    graficar_peso_estancias_largas(listings_exploratory)
    graficar_precio_largaestancia(listings_exploratory)
    graficar_pct_sin_resenas_por_tipo(listings_exploratory)
    graficar_pct_sin_resenas_por_precio(listings_exploratory)

    plt.show();


if __name__ == "__main__":
    etl()
    analisis_exploratorio()