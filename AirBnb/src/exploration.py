import pandas as pd

def cargar_datos(listings):
    listings = pd.read_csv(
    "data/Listings.csv", encoding = "ISO-8859-1", 
    low_memory=False,
    parse_dates =["host_since"]
    )
    return listings

def explorar_datos(listings):
    print(listings.head())
    listings.info()


def cargar_datos_reducidos(listings_exploratory):
    listings_exploratory = pd.read_csv(
    "data/listings_reduce.csv", encoding = "ISO-8859-1", 
    low_memory=False
    )
    return pd.read_csv(listings_exploratory)