import numpy as np
import pandas as pd

COLUMNAS_ELIMINAR = [
    "name", "host_id", "host_location", "host_response_time", "district",
    "host_response_rate", "host_acceptance_rate", "host_is_superhost", "host_has_profile_pic",
    "host_identity_verified", "amenities", "maximum_nights", "review_scores_accuracy",
    "review_scores_checkin", "review_scores_communication", "instant_bookable",
]


def eliminar_columnas_innecesarias(listings):
    listings_reduce = listings.drop(columns=COLUMNAS_ELIMINAR, errors="ignore")
    print("columnas restantes:", listings_reduce.shape[1])
    return listings_reduce


def resumen_nulos(listings_reduce):
    return listings_reduce.isna().sum()


def eliminar_filas_sin_datos_clave(listings_reduce):
    return listings_reduce.dropna(subset=["host_since", "host_total_listings_count"])


def marcar_tiene_resenas(listings_reduce):
    listings_reduce["has_reviews"] = listings_reduce["review_scores_rating"].notna()
    print(listings_reduce.shape)
    return listings_reduce


def nulos_bedrooms_por_ciudad(listings_reduce):
    return (
        listings_reduce.groupby("city")["bedrooms"]
        .agg(nulos=lambda s: s.isna().sum(), pct=lambda s: s.isna().mean().round(3), total="size")
        .sort_values("pct", ascending=False)
    )


def comparar_accommodates_segun_bedrooms_nulo(listings_reduce):
    return listings_reduce.groupby(listings_reduce["bedrooms"].isna())["accommodates"].describe()


def distribucion_bedrooms(listings_reduce):
    return listings_reduce["bedrooms"].value_counts().sort_index().head(8)


def imputar_bedrooms(listings_reduce):
    listings_reduce["bedrooms_imputed"] = listings_reduce["bedrooms"].isna()

    med = listings_reduce.groupby(["city", "room_type", "accommodates"])["bedrooms"].transform("median")
    listings_reduce["bedrooms"] = listings_reduce["bedrooms"].fillna(med)

    med2 = listings_reduce.groupby(["city", "accommodates"])["bedrooms"].transform("median")
    listings_reduce["bedrooms"] = listings_reduce["bedrooms"].fillna(med2)

    listings_reduce["bedrooms"] = listings_reduce["bedrooms"].fillna(listings_reduce["bedrooms"].median())
    listings_reduce["bedrooms"] = listings_reduce["bedrooms"].round().astype(int)

    print(listings_reduce["bedrooms"].isna().sum(), "nulos restantes")
    print(listings_reduce["bedrooms_imputed"].sum(), "filas imputadas")
    return listings_reduce


def calcular_limites_precio(listings_reduce):
    listings_reduce = listings_reduce[listings_reduce["price"] > 0].copy()

    log_p = np.log10(listings_reduce["price"])
    q = log_p.groupby(listings_reduce["city"]).quantile([.25, .75]).unstack()
    iqr = q[0.75] - q[0.25]

    lim = pd.DataFrame({
        "lim_inf": 10 ** (q[0.25] - 3 * iqr),
        "lim_sup": 10 ** (q[0.75] + 3 * iqr),
    })

    aux = listings_reduce.join(lim, on="city")
    listings_reduce["price_outlier"] = (aux["price"] > aux["lim_sup"]) | (aux["price"] < aux["lim_inf"])

    print(lim.round(0))
    print(listings_reduce.groupby("city")["price_outlier"].agg(["sum", "mean"]).round(4))
    return listings_reduce


def eliminar_precios_atipicos(listings_reduce):
    listings_reduce = listings_reduce[~listings_reduce["price_outlier"]].copy()
    listings_reduce = listings_reduce.drop(columns="price_outlier")
    print(listings_reduce.shape)
    return listings_reduce


def estadisticos_minimum_nights(listings_reduce):
    return listings_reduce.groupby("city")["minimum_nights"].describe(percentiles=[.5, .75, .95, .99])


def tramos_minimum_nights(listings_reduce):
    return pd.cut(
        listings_reduce["minimum_nights"],
        bins=[0, 1, 3, 7, 29, 364, float("inf")],
        labels=["1 noche", "2-3", "4-7", "8-29", "30-364 (larga estancia)", "365+"],
    )


def reparto_tramos_por_ciudad(listings_reduce, tramos):
    return (pd.crosstab(listings_reduce["city"], tramos, normalize="index") * 100).round(1)


def valores_mas_frecuentes_minimum_nights(listings_reduce):
    return listings_reduce["minimum_nights"].value_counts().head(15)


def precio_por_tramo_y_ciudad(listings_reduce, tramos):
    return (
        listings_reduce.groupby(["city", tramos], observed=True)["price"]
        .median().unstack().round(0)
    )


def limpiar_minimum_nights(listings_reduce):
    print((listings_reduce["minimum_nights"] > 365).sum(), "anuncios con mínimo > 365 noches")

    listings_reduce = listings_reduce[listings_reduce["minimum_nights"] <= 365].copy()
    listings_reduce["long_stay"] = listings_reduce["minimum_nights"] >= 30

    print(listings_reduce.shape)
    print((listings_reduce.groupby("city")["long_stay"].mean() * 100).round(1).sort_values(ascending=False))
    return listings_reduce


def analizar_accommodates(listings_reduce):
    print(listings_reduce["accommodates"].describe(percentiles=[.5, .9, .99]))
    print(listings_reduce["accommodates"].value_counts().sort_index())
    print(listings_reduce.groupby("city")["accommodates"].agg(["min", "median", "max"]))

    incoherentes = listings_reduce[
        (listings_reduce["accommodates"] >= 10) & (listings_reduce["bedrooms"] <= 1)
    ]
    print(len(incoherentes), "anuncios con 10+ huéspedes y 1 dormitorio o menos")
    return incoherentes[["city", "room_type", "accommodates", "bedrooms", "price"]].head(10)


def analizar_property_type(listings_reduce):
    print(listings_reduce["property_type"].nunique(), "categorías")
    return listings_reduce["property_type"].value_counts()


def preparar_variables_exploratorias(listings_exploratory):
    """Variables derivadas usadas en el análisis exploratorio (price_idx, acc_bucket...)."""
    listings_exploratory["price_idx"] = (
        listings_exploratory["price"]
        / listings_exploratory.groupby("city")["price"].transform("median")
    )
    listings_exploratory["acc_bucket"] = pd.cut(
        listings_exploratory["accommodates"], [0, 1, 2, 4, 6, np.inf],
        labels=["1", "2", "3-4", "5-6", "7+"],
    )
    listings_exploratory["precio_pers"] = (
        listings_exploratory["price"] / listings_exploratory["accommodates"]
    )
    listings_exploratory["pp_idx"] = (
        listings_exploratory["precio_pers"]
        / listings_exploratory.groupby("city")["precio_pers"].transform("median")
    )
    listings_exploratory["tramo_precio"] = pd.cut(
        listings_exploratory["price_idx"], [0, .5, .75, 1, 1.5, 2, np.inf],
        labels=["<0,5×", "0,5-0,75×", "0,75-1×", "1-1,5×", "1,5-2×", "2×+"],
    )
    listings_exploratory["sin_resenas"] = listings_exploratory["review_scores_rating"].isna()
    return listings_exploratory