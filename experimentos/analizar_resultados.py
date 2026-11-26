"""
analizar_resultados.py - Analisis estadistico del experimento formal (Clase 5, issue #4 y #12).

Responsable: Andres (R4). Lee resultados/resultados.csv (NO lo modifica) y genera:
    resultados/resumen_estadistico.csv
    resultados/grafico_1_tiempo_vs_n_loglog.png
    resultados/grafico_2_comparacion_n1M.png
e imprime la evaluacion de H1, H2 y H3 (docs/hipotesis.md).

Origen de los datos:
    - Datos de entrada SIMULADOS (src/generar_datos.py, semilla 4).
    - Tiempos (s) y picos de memoria (MiB) MEDIDOS en el PC del Integrante A (docs/entorno.md).
    - Ciclos N = f * t ESTIMADOS (f = 2.2 GHz reportada por psutil; no ve el turbo).

Reglas del analisis (D-001):
    - Tiempo: SOLO filas medicion_memoria == "no" (10 repeticiones por estrategia y n).
      La corrida de memoria tiene el tiempo inflado por tracemalloc.
    - Memoria: SOLO filas medicion_memoria == "si" (1 corrida por estrategia y n).
      Con k = 1 no hay desviacion ni IC95 %: el pico salio identico en 3 corridas previas
      (117.5 MiB, Clase 3), por eso una corrida basta.

Requiere pandas, numpy y matplotlib (dependencias opcionales de requirements.txt).
Uso (desde la raiz del repositorio):
    python -m experimentos.analizar_resultados
"""

from pathlib import Path
import math

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

CSV_PATH = Path("resultados/resultados.csv")
OUT_DIR = Path("resultados")
ESTRATEGIAS = ["A_linea_base", "B_acumuladores", "C_array_d"]
ETIQUETAS = {"A_linea_base": "A (linea base)", "B_acumuladores": "B (acumuladores)", "C_array_d": "C (array d)"}
COLORES = {"A_linea_base": "#d62728", "B_acumuladores": "#1f77b4", "C_array_d": "#2ca02c"}
N_MAYOR, N_MENOR = 1_000_000, 200_000
FRECUENCIA_HZ = 2.2e9  # reportada por psutil (estimacion: no incluye turbo)
ALFA = 0.05


# --------------------------- distribucion t de Student (sin scipy) ---------------------------
def _beta_incompleta(a: float, b: float, x: float) -> float:
    """Beta incompleta regularizada I_x(a, b) por fraccion continua (Numerical Recipes)."""
    if x <= 0.0:
        return 0.0
    if x >= 1.0:
        return 1.0
    ln_bt = math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b) + a * math.log(x) + b * math.log(1 - x)
    if x > (a + 1) / (a + b + 2):
        return 1.0 - _beta_incompleta(b, a, 1 - x)
    qab, qap, qam = a + b, a + 1, a - 1
    c, d = 1.0, 1.0 - qab * x / qap
    d = 1.0 / (d if abs(d) > 1e-300 else 1e-300)
    h = d
    for m in range(1, 300):
        m2 = 2 * m
        aa = m * (b - m) * x / ((qam + m2) * (a + m2))
        d = 1.0 + aa * d
        d = 1.0 / (d if abs(d) > 1e-300 else 1e-300)
        c = 1.0 + aa / c if abs(1.0 + aa / c) > 1e-300 else 1e-300
        h *= d * c
        aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
        d = 1.0 + aa * d
        d = 1.0 / (d if abs(d) > 1e-300 else 1e-300)
        c = 1.0 + aa / c if abs(1.0 + aa / c) > 1e-300 else 1e-300
        delta = d * c
        h *= delta
        if abs(delta - 1.0) < 1e-14:
            break
    return math.exp(ln_bt) * h / a


def t_cdf(t: float, gl: float) -> float:
    """P(T <= t) para T ~ t de Student con gl grados de libertad (gl puede no ser entero)."""
    x = gl / (gl + t * t)
    cola = 0.5 * _beta_incompleta(gl / 2, 0.5, x)
    return 1.0 - cola if t >= 0 else cola


def t_critico(gl: float, confianza: float = 0.95) -> float:
    """Valor t tal que P(-t < T < t) = confianza (busqueda por biseccion)."""
    objetivo = 1 - (1 - confianza) / 2
    lo, hi = 0.0, 100.0
    for _ in range(200):
        mid = (lo + hi) / 2
        if t_cdf(mid, gl) < objetivo:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


# --------------------------------------- carga y control ---------------------------------------
def cargar() -> pd.DataFrame:
    df = pd.read_csv(CSV_PATH)
    df["medicion_memoria"] = df["medicion_memoria"].astype(str).str.strip().str.lower()
    for col in ("n", "repeticion", "tiempo_s", "pico_mem_mib", "frecuencia_mhz"):
        df[col] = pd.to_numeric(df[col], errors="coerce")
    tiempo = df[df["medicion_memoria"] == "no"]
    memoria = df[df["medicion_memoria"] == "si"]
    assert len(df) == 99, f"Se esperaban 99 filas y hay {len(df)} (protocolo, seccion 4)"
    assert len(tiempo) == 90 and len(memoria) == 9, "Se esperaban 90 filas de tiempo y 9 de memoria"
    assert tiempo.groupby(["estrategia", "n"]).size().eq(10).all(), "Cada combinacion debe tener 10 repeticiones"
    assert tiempo["pico_mem_mib"].isna().all(), "pico_mem_mib solo debe tener valor en filas de memoria"
    return df


def resumir(df: pd.DataFrame) -> pd.DataFrame:
    tiempo = df[df["medicion_memoria"] == "no"]
    memoria = df[df["medicion_memoria"] == "si"].set_index(["estrategia", "n"])["pico_mem_mib"]
    filas = []
    for (est, n), g in tiempo.groupby(["estrategia", "n"]):
        t = g["tiempo_s"].to_numpy()
        k = len(t)
        media = float(t.mean())
        sd = float(t.std(ddof=1))  # desviacion estandar muestral
        tc = t_critico(k - 1)  # k = 10 -> gl = 9 -> 2.262
        margen = tc * sd / math.sqrt(k)
        filas.append(
            {
                "estrategia": est,
                "n": int(n),
                "k_tiempo": k,
                "media_tiempo_s": media,
                "sd_tiempo_s": sd,
                "cv_pct": 100 * sd / media,
                "t_critico": tc,
                "ic95_inf_s": media - margen,
                "ic95_sup_s": media + margen,
                "min_tiempo_s": float(t.min()),
                "max_tiempo_s": float(t.max()),
                "k_memoria": 1,
                "pico_mem_mib": float(memoria.loc[(est, n)]),
                "bytes_por_registro": float(memoria.loc[(est, n)]) * 1_048_576 / n,
                "ciclos_por_registro_estimados": FRECUENCIA_HZ * media / n,
            }
        )
    res = pd.DataFrame(filas)
    res["estrategia"] = pd.Categorical(res["estrategia"], ESTRATEGIAS, ordered=True)
    return res.sort_values(["estrategia", "n"]).reset_index(drop=True)


def pendientes(res: pd.DataFrame, columna: str) -> dict:
    """Pendiente del ajuste lineal log10(y) = b * log10(n) + a para cada estrategia."""
    out = {}
    for est in ESTRATEGIAS:
        g = res[res["estrategia"] == est]
        b, _a = np.polyfit(np.log10(g["n"]), np.log10(g[columna]), 1)
        out[est] = float(b)
    return out


# --------------------------------------------- graficos ---------------------------------------------
def grafico_loglog(res: pd.DataFrame, pend: dict) -> Path:
    fig, ax = plt.subplots(figsize=(8, 5.5))
    for est in ESTRATEGIAS:
        g = res[res["estrategia"] == est]
        err = [g["media_tiempo_s"] - g["ic95_inf_s"], g["ic95_sup_s"] - g["media_tiempo_s"]]
        ax.errorbar(
            g["n"], g["media_tiempo_s"], yerr=err, marker="o", capsize=5, color=COLORES[est],
            label=f"{ETIQUETAS[est]} - pendiente = {pend[est]:.3f}",
        )
        # recta del ajuste log-log
        b, a = np.polyfit(np.log10(g["n"]), np.log10(g["media_tiempo_s"]), 1)
        xs = np.array([g["n"].min(), g["n"].max()])
        ax.plot(xs, 10 ** (a + b * np.log10(xs)), linestyle=":", color=COLORES[est], alpha=0.7)
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("n (registros) - escala logaritmica")
    ax.set_ylabel("Tiempo medio de ejecucion t (s) - escala logaritmica")
    ax.set_title("Tiempo vs. n (log-log), media de 10 corridas con IC95 %\n"
                 "Pendiente ~ 1 = crecimiento lineal (t proporcional a n)")
    ax.grid(True, which="both", linestyle="--", alpha=0.4)
    ax.legend(title="Estrategia (pendiente del ajuste)")
    fig.text(0.01, 0.01, "Tiempos MEDIDOS en el PC del Integrante A; datos de entrada SIMULADOS (semilla 4).",
             fontsize=8, alpha=0.8)
    fig.tight_layout(rect=(0, 0.03, 1, 1))
    ruta = OUT_DIR / "grafico_1_tiempo_vs_n_loglog.png"
    fig.savefig(ruta, dpi=150)
    plt.close(fig)
    return ruta


def grafico_comparacion(res: pd.DataFrame) -> Path:
    g = res[res["n"] == N_MAYOR].set_index("estrategia").loc[ESTRATEGIAS]
    etiquetas = [ETIQUETAS[e] for e in ESTRATEGIAS]
    colores = [COLORES[e] for e in ESTRATEGIAS]
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 5))

    err = [g["media_tiempo_s"] - g["ic95_inf_s"], g["ic95_sup_s"] - g["media_tiempo_s"]]
    barras = ax1.bar(etiquetas, g["media_tiempo_s"], yerr=err, capsize=8, color=colores)
    for b, v in zip(barras, g["media_tiempo_s"]):
        ax1.text(b.get_x() + b.get_width() / 2, v * 1.04, f"{v:.3f} s", ha="center", va="bottom")
    ax1.set_ylabel("Tiempo medio t (s)")
    ax1.set_title("Tiempo (media de 10 corridas, IC95 %)")
    ax1.set_ylim(0, g["ic95_sup_s"].max() * 1.2)
    ax1.grid(True, axis="y", linestyle="--", alpha=0.4)

    barras = ax2.bar(etiquetas, g["pico_mem_mib"], color=colores)
    for b, v in zip(barras, g["pico_mem_mib"]):
        ax2.text(b.get_x() + b.get_width() / 2, v + 5, f"{v:.3f} MiB" if v < 1 else f"{v:.2f} MiB",
                 ha="center", va="bottom")
    ax2.set_ylabel("Pico de memoria M (MiB)")
    ax2.set_title("Pico de memoria (1 corrida con tracemalloc)")
    ax2.set_ylim(0, g["pico_mem_mib"].max() * 1.15)
    ax2.grid(True, axis="y", linestyle="--", alpha=0.4)

    fig.suptitle("Comparacion de estrategias con n = 1 000 000 registros")
    fig.text(0.01, 0.01, "MEDIDO en el PC del Integrante A; datos de entrada SIMULADOS (semilla 4). "
             "La memoria no tiene barras de error: k = 1 (D-001).", fontsize=8, alpha=0.8)
    fig.tight_layout(rect=(0, 0.03, 1, 0.95))
    ruta = OUT_DIR / "grafico_2_comparacion_n1M.png"
    fig.savefig(ruta, dpi=150)
    plt.close(fig)
    return ruta


# --------------------------------------------- hipotesis ---------------------------------------------
def welch(x: np.ndarray, y: np.ndarray) -> dict:
    """Prueba t de Welch (varianzas distintas) para la diferencia de medias x - y."""
    nx, ny = len(x), len(y)
    vx, vy = x.var(ddof=1), y.var(ddof=1)
    se = math.sqrt(vx / nx + vy / ny)
    t = (x.mean() - y.mean()) / se
    gl = (vx / nx + vy / ny) ** 2 / ((vx / nx) ** 2 / (nx - 1) + (vy / ny) ** 2 / (ny - 1))
    p = 2 * (1 - t_cdf(abs(t), gl))
    tc = t_critico(gl)
    dif = x.mean() - y.mean()
    s_comb = math.sqrt(((nx - 1) * vx + (ny - 1) * vy) / (nx + ny - 2))
    d = dif / s_comb  # d de Cohen
    g = d * (1 - 3 / (4 * (nx + ny) - 9))  # correccion de Hedges para muestras pequenas
    return {"t": t, "gl": gl, "p": p, "dif": dif, "ic_inf": dif - tc * se, "ic_sup": dif + tc * se,
            "d_cohen": d, "g_hedges": g}


def evaluar_hipotesis(df: pd.DataFrame, res: pd.DataFrame) -> None:
    mem = res.set_index(["estrategia", "n"])["pico_mem_mib"]
    t_ = res.set_index(["estrategia", "n"])
    print("\n=== H1: M_B < 0.10 * M_A con n = 1 000 000 (memoria, k = 1) ===")
    ma, mb = mem[("A_linea_base", N_MAYOR)], mem[("B_acumuladores", N_MAYOR)]
    print(f"M_A = {ma:.4f} MiB, M_B = {mb:.4f} MiB, 0.10*M_A = {0.10 * ma:.4f} MiB, "
          f"M_B/M_A = {mb / ma:.6f} ({100 * mb / ma:.3f} %)")
    print("Decision:", "se confirma" if mb < 0.10 * ma else "se refuta")

    print("\n=== H2: M(1 000 000) / M(200 000) ===")
    for est, (lo, hi) in {"A_linea_base": (4, 6), "B_acumuladores": (0.8, 1.2), "C_array_d": (4, 6)}.items():
        r = mem[(est, N_MAYOR)] / mem[(est, N_MENOR)]
        print(f"{est}: {mem[(est, N_MAYOR)]:.4f} / {mem[(est, N_MENOR)]:.4f} = {r:.4f}  "
              f"(rango {lo}-{hi}) -> {'dentro' if lo <= r <= hi else 'FUERA'}")
    pm = pendientes(res, "pico_mem_mib")
    print("Pendientes log-log de memoria:", {k: round(v, 4) for k, v in pm.items()})

    print("\n=== H3: t_B <= 0.80 * t_A con n = 1 000 000 (tiempo, k = 10 por estrategia) ===")
    tiempo = df[(df["medicion_memoria"] == "no") & (df["n"] == N_MAYOR)]
    xa = tiempo[tiempo["estrategia"] == "A_linea_base"]["tiempo_s"].to_numpy()
    xb = tiempo[tiempo["estrategia"] == "B_acumuladores"]["tiempo_s"].to_numpy()
    a, b = t_.loc[("A_linea_base", N_MAYOR)], t_.loc[("B_acumuladores", N_MAYOR)]
    print(f"t_A = {a.media_tiempo_s:.6f} s  IC95 [{a.ic95_inf_s:.6f}, {a.ic95_sup_s:.6f}]")
    print(f"t_B = {b.media_tiempo_s:.6f} s  IC95 [{b.ic95_inf_s:.6f}, {b.ic95_sup_s:.6f}]")
    print(f"0.80 * t_A = {0.80 * a.media_tiempo_s:.6f} s; t_B / t_A = {b.media_tiempo_s / a.media_tiempo_s:.4f}")
    peor = b.ic95_sup_s / a.ic95_inf_s
    print(f"Cociente en el peor caso (IC95 sup de B / IC95 inf de A) = {peor:.4f}")
    w = welch(xa, xb)
    texto_p = "< 1e-15" if w["p"] < 1e-15 else f"= {w['p']:.3e}"  # por debajo de 1e-15 el float no distingue
    print(f"Welch A - B: dif = {w['dif']:.6f} s, IC95 [{w['ic_inf']:.6f}, {w['ic_sup']:.6f}] s, "
          f"t = {w['t']:.3f}, gl = {w['gl']:.2f}, p {texto_p} (dos colas)")
    print(f"Tamano de efecto: d de Cohen = {w['d_cohen']:.2f}, g de Hedges = {w['g_hedges']:.2f}")
    ok = w["p"] < ALFA and peor <= 0.80
    print("Criterio: p < 0.05 en Welch Y cociente en el peor caso <= 0.80 ->",
          "se confirma" if ok else "no concluyente / se refuta")


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    df = cargar()
    res = resumir(df)
    pend_t = pendientes(res, "media_tiempo_s")
    res["pendiente_loglog_tiempo"] = res["estrategia"].map(pend_t).astype(float)
    res["pendiente_loglog_memoria"] = res["estrategia"].map(pendientes(res, "pico_mem_mib")).astype(float)
    ruta_csv = OUT_DIR / "resumen_estadistico.csv"
    res.to_csv(ruta_csv, index=False, float_format="%.6f")

    pd.set_option("display.width", 200)
    print(f"t critico (gl = 9, 95 %) = {t_critico(9):.4f}")
    cols = ["estrategia", "n", "media_tiempo_s", "sd_tiempo_s", "cv_pct", "ic95_inf_s", "ic95_sup_s", "pico_mem_mib"]
    print(res[cols].to_string(index=False, float_format=lambda v: f"{v:.6f}"))
    print("Rango de CV (%):", f"{res['cv_pct'].min():.2f} - {res['cv_pct'].max():.2f}")
    print("Pendientes log-log del tiempo:", {k: round(v, 4) for k, v in pend_t.items()})
    print("Ciclos por registro (ESTIMADOS, n = 1 000 000):",
          {e: round(v) for e, v in res[res["n"] == N_MAYOR].set_index("estrategia")
           ["ciclos_por_registro_estimados"].items()})

    evaluar_hipotesis(df, res)
    print("\nArchivos generados:", ruta_csv, grafico_loglog(res, pend_t), grafico_comparacion(res), sep="\n  ")


if __name__ == "__main__":
    main()
