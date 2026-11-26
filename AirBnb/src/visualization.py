import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.ticker import NullFormatter

AZUL, GRIS, TXT, TXT2, GRID, SUP, MUTED = (
    "#2a78d6", "#b9b8b0", "#0b0b0b", "#52514e", "#e1e0d9", "#fcfcfb", "#898781"
)
SEQ = LinearSegmentedColormap.from_list("seq", ["#cde2fb", "#86b6ef", "#3987e5", "#1c5cab", "#0d366b"])
DIV = LinearSegmentedColormap.from_list("div", ["#e34948", "#f0efec", "#2a78d6"])


def configurar_estilo():
    plt.rcParams.update({
        "figure.facecolor": SUP, "axes.facecolor": SUP, "savefig.facecolor": SUP,
        "axes.edgecolor": GRID, "axes.labelcolor": TXT2, "text.color": TXT,
        "xtick.color": TXT2, "ytick.color": TXT2,
        "axes.spines.top": False, "axes.spines.right": False,
        "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.6, "axes.axisbelow": True,
        "axes.titlesize": 13, "axes.titleweight": "bold", "axes.titlelocation": "left",
    })


def heatmap(ax, tabla, cmap, vmin=None, vmax=None, fmt="{:.2f}"):
    im = ax.imshow(tabla.values, cmap=cmap, vmin=vmin, vmax=vmax, aspect="auto")
    ax.set_xticks(range(tabla.shape[1])); ax.set_xticklabels([str(c) for c in tabla.columns])
    ax.set_yticks(range(tabla.shape[0])); ax.set_yticklabels(list(tabla.index))
    ax.grid(False)
    for s in ax.spines.values():
        s.set_visible(False)
    for i in range(tabla.shape[0]):
        for j in range(tabla.shape[1]):
            v = tabla.iat[i, j]
            if pd.notna(v):
                r, g, b, _ = cmap(im.norm(v))
                ax.text(j, i, fmt.format(v), ha="center", va="center", fontsize=9,
                        color="white" if 0.299*r + 0.587*g + 0.114*b < 0.5 else TXT)
    return im
plt.show();


def graficar_correlacion_precio(listings_exploratory, ciudades):
    ciudades = sorted(listings_exploratory["city"].unique())
    num = {
        "accommodates": "Huéspedes", "bedrooms": "Dormitorios", "minimum_nights": "Noches\nmínimas",
        "review_scores_rating": "Valoración\nglobal", "review_scores_location": "Ubicación",
        "review_scores_value": "Calidad-\nprecio",
    }
    corr = listings_exploratory.groupby("city")[list(num) + ["price"]].apply(
        lambda g: g.corr(method="spearman")["price"].drop("price")
    )
    corr = corr[list(num)].rename(columns=num)

    fig, ax = plt.subplots(figsize=(9, 5.5))
    im = heatmap(ax, corr, DIV, -1, 1)
    ax.set_title("¿Qué variables se asocian al precio?")
    fig.colorbar(im, ax=ax, label="Correlación de Spearman con el precio", shrink=.8)
    return fig, ax
plt.show();


def graficar_precio_por_capacidad(listings_exploratory):
    idx = listings_exploratory.pivot_table(
        index="city", columns="acc_bucket", values="price_idx", aggfunc="median", observed=True
    )
    fig, ax = plt.subplots(figsize=(8, 5.5))
    im = heatmap(ax, idx, SEQ)
    ax.set_title("Precio según capacidad (1,00 = mediana de la ciudad)")
    ax.set_xlabel("Huéspedes")
    fig.colorbar(im, ax=ax, shrink=.8)
    return fig, ax
plt.show();


def graficar_precio_por_tipo_alojamiento(listings_exploratory, ciudades):
    fig, axes = plt.subplots(2, 5, figsize=(16, 6), constrained_layout=True)
    for ax, c in zip(axes.flat, ciudades):
        s = listings_exploratory[listings_exploratory["city"] == c].groupby("room_type")["price"].median().sort_values()
        ax.barh(s.index, s.values, color=AZUL, height=0.55)
        for y, v in enumerate(s.values):
            ax.text(v, y, f" {v:,.0f}", va="center", fontsize=8, color=TXT2)
        ax.set_title(c, fontsize=11)
        ax.set_xlim(0, s.max() * 1.3)
        ax.grid(axis="y", visible=False)
        ax.tick_params(labelsize=8)
    fig.suptitle(
        "Precio mediano por tipo de alojamiento (moneda local de cada ciudad)",
        x=0.01, ha="left", fontsize=14, fontweight="bold",
    )
    return fig, axes
plt.show();


def graficar_relacion_valoracion_precio(listings_exploratory):
    b = (
        listings_exploratory.dropna(subset=["review_scores_value"]).groupby(["city", "neighbourhood"])
        .agg(n=("price", "size"), precio_idx=("price_idx", "median"), valor=("review_scores_value", "mean"))
        .query("n >= 50").reset_index()
    )
    mask = (b["precio_idx"] < 1) & (b["valor"] >= b["valor"].quantile(.75))

    fig, ax = plt.subplots(figsize=(9, 6))
    ax.scatter(b.loc[~mask, "precio_idx"], b.loc[~mask, "valor"], s=30, color=GRIS,
               edgecolor=SUP, linewidth=.8, label="Resto de barrios")
    ax.scatter(b.loc[mask, "precio_idx"], b.loc[mask, "valor"], s=40, color=AZUL,
               edgecolor=SUP, linewidth=.8, label="Más baratos que su ciudad y valoración en el 25 % superior")
    ax.set_xscale("log"); ax.axvline(1, color=TXT2, lw=.8, ls="--")
    lo, hi = ax.get_xlim(); t = [x for x in [.25, .5, 1, 2, 4] if lo <= x <= hi]
    ax.set_xticks(t); ax.set_xticklabels([f"{x:g}×" for x in t]); ax.xaxis.set_minor_formatter(NullFormatter())
    ax.set_xlabel("Precio del barrio relativo a la mediana de su ciudad (escala log)")
    ax.set_ylabel("Puntuación media calidad-precio")
    ax.set_title("¿Dónde está la mejor relación valoración/precio?")
    ax.legend(frameon=False, loc="lower left")
    return b, mask, fig, ax
plt.show();


def graficar_top10_barrios_baratos(b, mask):
    top = b[mask].sort_values("valor", ascending=False).head(10).iloc[::-1]
    etiq = (top["neighbourhood"] + " (" + top["city"] + ")").tolist()
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.hlines(etiq, top["valor"].min() - .05, top["valor"], color=GRID, lw=1.5)
    ax.scatter(top["valor"], etiq, color=AZUL, s=55, zorder=3)
    for v, y in zip(top["valor"], etiq):
        ax.text(v + .005, y, f"{v:.2f}", va="center", fontsize=9, color=TXT2)
    ax.set_xlim(top["valor"].min() - .05, top["valor"].max() + .05)
    ax.grid(axis="y", visible=False)
    ax.set_title("Top 10 barrios: más baratos que su ciudad y mejor calidad-precio")
    ax.set_xlabel("Puntuación media calidad-precio")
    return fig, ax
plt.show();


def graficar_mapa_precios(listings_exploratory, ciudades):
    fig, axes = plt.subplots(2, 5, figsize=(18, 7.5), constrained_layout=True)
    for ax, c in zip(axes.flat, ciudades):
        g = listings_exploratory[listings_exploratory["city"] == c]
        lo0, lo1 = g["longitude"].quantile([.005, .995]); la0, la1 = g["latitude"].quantile([.005, .995])
        hb = ax.hexbin(g["longitude"], g["latitude"], C=g["price_idx"], reduce_C_function=np.median,
                       gridsize=30, mincnt=5, cmap=SEQ, vmin=0.5, vmax=2.0,
                       extent=(lo0, lo1, la0, la1), linewidths=0.2, edgecolors=SUP)
        ax.set_xlim(lo0, lo1); ax.set_ylim(la0, la1)
        ax.set_aspect(1 / np.cos(np.radians(g["latitude"].mean())))
        ax.set_title(c, fontsize=11, loc="center")
        ax.set_xticks([]); ax.set_yticks([]); ax.grid(False)
        for s in ax.spines.values():
            s.set_visible(False)
    fig.colorbar(hb, ax=axes, shrink=.6, label="Precio relativo a la mediana de la ciudad")
    fig.suptitle("Mapa de precios por ciudad", x=0.01, ha="left", fontsize=14, fontweight="bold")
    return fig, axes
plt.show();


def graficar_ubicacion_vs_precio(listings_exploratory):
    u = (
        listings_exploratory.dropna(subset=["review_scores_location"]).groupby(["city", "neighbourhood"])
        .agg(n=("price", "size"), precio_idx=("price_idx", "median"), ubic=("review_scores_location", "mean"))
        .query("n >= 50").reset_index()
    )
    rho = u["ubic"].corr(u["precio_idx"], method="spearman")

    fig, ax = plt.subplots(figsize=(9, 6))
    ax.scatter(u["ubic"], u["precio_idx"], s=32, color=AZUL, alpha=.65, edgecolor=SUP, linewidth=.8)
    ax.set_yscale("log"); ax.axhline(1, color=TXT2, lw=.8, ls="--")
    lo, hi = ax.get_ylim(); t = [x for x in [.25, .5, 1, 2, 4] if lo <= x <= hi]
    ax.set_yticks(t); ax.set_yticklabels([f"{x:g}×" for x in t]); ax.yaxis.set_minor_formatter(NullFormatter())
    ax.set_xlabel("Puntuación media de ubicación")
    ax.set_ylabel("Precio relativo a la mediana de su ciudad (escala log)")
    ax.set_title("¿Se paga por la ubicación?")
    ax.text(.02, .96, f"Spearman = {rho:.2f}  ·  cada punto es un barrio",
            transform=ax.transAxes, va="top", color=TXT2, fontsize=10)
    return fig, ax
plt.show();


def graficar_precio_por_huesped(listings_exploratory):
    pp = listings_exploratory.pivot_table(
        index="city", columns="acc_bucket", values="pp_idx", aggfunc="median", observed=True
    )
    fig, ax = plt.subplots(figsize=(8, 5.5))
    im = heatmap(ax, pp, SEQ)
    ax.set_title("Precio por huésped (1,00 = mediana de la ciudad)")
    ax.set_xlabel("Huéspedes del alojamiento")
    fig.colorbar(im, ax=ax, shrink=.8)
    return fig, ax
plt.show();


def graficar_peso_puntuacion_valoracion(listings_exploratory):
    sub = {
        "review_scores_cleanliness": "Limpieza",
        "review_scores_location": "Ubicación",
        "review_scores_value": "Calidad-precio",
    }
    c5 = listings_exploratory.groupby("city")[["review_scores_rating"] + list(sub)].apply(
        lambda g: g.corr(method="spearman")["review_scores_rating"].drop("review_scores_rating")
    )
    c5 = c5[list(sub)].rename(columns=sub)
    c5.loc["Todas las ciudades"] = (
        listings_exploratory[["review_scores_rating"] + list(sub)]
        .corr(method="spearman")["review_scores_rating"].drop("review_scores_rating").rename(sub)
    )

    fig, ax = plt.subplots(figsize=(7.5, 5.5))
    im = heatmap(ax, c5, SEQ, 0, 1)
    ax.set_title("¿Qué puntuación pesa más en la valoración global?")
    fig.colorbar(im, ax=ax, label="Correlación de Spearman con la valoración global", shrink=.8)
    return fig, ax
plt.show();


def graficar_peso_estancias_largas(listings_exploratory):
    pct = (listings_exploratory.groupby("city")["long_stay"].mean() * 100).sort_values()
    colores = [GRIS] * (len(pct) - 2) + [AZUL] * 2
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.barh(pct.index, pct.values, color=colores, height=.6)
    for y, v in enumerate(pct.values):
        ax.text(v, y, f" {v:.1f} %", va="center", fontsize=9, color=TXT2)
    ax.set_xlim(0, pct.max() * 1.15); ax.grid(axis="y", visible=False)
    ax.set_title("Peso de las estancias de 30 noches o más")
    ax.set_xlabel("% de anuncios con mínimo de 30 noches o más")
    return fig, ax
plt.show();


def graficar_precio_largaestancia(listings_exploratory):
    ls = listings_exploratory.groupby(["city", "long_stay"])["price_idx"].median().unstack().sort_values(True)
    fig, ax = plt.subplots(figsize=(9, 5.5))
    ax.hlines(ls.index, ls[False], ls[True], color=GRID, lw=2.5)
    ax.scatter(ls[False], ls.index, color=MUTED, s=65, zorder=3, label="Corta estancia (< 30 noches)")
    ax.scatter(ls[True], ls.index, color=AZUL, s=65, zorder=3, label="Larga estancia (30+ noches)")
    ax.axvline(1, color=TXT2, lw=.8, ls="--")
    ax.grid(axis="y", visible=False)
    ax.set_xlabel("Precio mediano relativo a la mediana de la ciudad")
    ax.set_title("¿Es más barata la larga estancia?")
    ax.legend(frameon=False, loc="lower right")
    return fig, ax
plt.show();


def graficar_pct_sin_resenas_por_tipo(listings_exploratory):
    t8 = listings_exploratory.pivot_table(index="city", columns="room_type", values="sin_resenas", aggfunc="mean") * 100
    n8 = listings_exploratory.pivot_table(index="city", columns="room_type", values="sin_resenas", aggfunc="size")
    t8 = t8.where(n8 >= 30)

    fig, ax = plt.subplots(figsize=(8, 5.5))
    im = heatmap(ax, t8, SEQ, vmin=0, fmt="{:.0f} %")
    ax.set_title("% de anuncios sin reseñas")
    fig.colorbar(im, ax=ax, shrink=.8)
    return fig, ax
plt.sow();


def graficar_pct_sin_resenas_por_precio(listings_exploratory):
    t8b = listings_exploratory.groupby("tramo_precio", observed=True)["sin_resenas"].mean() * 100

    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.bar(t8b.index.astype(str), t8b.values, color=AZUL, width=.6)
    for x, v in enumerate(t8b.values):
        ax.text(x, v, f"{v:.0f} %", ha="center", va="bottom", fontsize=9, color=TXT2)
    ax.grid(axis="x", visible=False)
    ax.set_ylim(0, t8b.max() * 1.15)
    ax.set_title("¿Los anuncios más caros tienen menos reseñas?")
    ax.set_xlabel("Precio relativo a la mediana de la ciudad"); ax.set_ylabel("% sin reseñas")
    return fig, ax
plt.show;