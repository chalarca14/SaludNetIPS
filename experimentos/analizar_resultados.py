from pathlib import Path
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

CSV_PATH = Path("resultados/resultados.csv")
OUT_DIR = Path("resultados")
OUT_DIR.mkdir(parents=True, exist_ok=True)


def resumen_metrica(serie: pd.Series) -> dict:
    s = pd.to_numeric(serie, errors="coerce").dropna()
    k = len(s)
    if k == 0:
        return {
            "k": 0,
            "media": np.nan,
            "desviacion": np.nan,
            "cv": np.nan,
            "ic95_low": np.nan,
            "ic95_high": np.nan,
        }
    media = float(s.mean())
    if k == 1:
        return {
            "k": 1,
            "media": media,
            "desviacion": 0.0,
            "cv": 0.0 if media != 0 else np.nan,
            "ic95_low": media,
            "ic95_high": media,
        }
    desv = float(s.std(ddof=1))
    cv = float(desv / media) if media != 0 else np.nan
    error_est = desv / math.sqrt(k)
    margen = 1.96 * error_est
    return {
        "k": k,
        "media": media,
        "desviacion": desv,
        "cv": cv,
        "ic95_low": media - margen,
        "ic95_high": media + margen,
    }


df = pd.read_csv(CSV_PATH)
df["n"] = pd.to_numeric(df["n"], errors="coerce")
df["tiempo_s"] = pd.to_numeric(df["tiempo_s"], errors="coerce")
df["pico_mem_mib"] = pd.to_numeric(df["pico_mem_mib"], errors="coerce")

filas = []
for (estrategia, n), grupo in df.groupby(["estrategia", "n"], dropna=True):
    # Tiempo: usa todas las repeticiones válidas
    t_stats = resumen_metrica(grupo["tiempo_s"])
    # Memoria: prioriza filas con medicion_memoria == "si" si existen; si no, toma valores no nulos
    mem_sub = grupo[
        grupo["medicion_memoria"].astype(str).str.lower().str.strip() == "si"
    ]["pico_mem_mib"]
    if mem_sub.dropna().empty:
        mem_sub = grupo["pico_mem_mib"]
    m_stats = resumen_metrica(mem_sub)

    filas.append(
        {
            "estrategia": estrategia,
            "n": int(n),
            "k_tiempo": t_stats["k"],
            "tiempo_media_s": t_stats["media"],
            "tiempo_desv_s": t_stats["desviacion"],
            "tiempo_cv": t_stats["cv"],
            "tiempo_ic95_low_s": t_stats["ic95_low"],
            "tiempo_ic95_high_s": t_stats["ic95_high"],
            "k_mem": m_stats["k"],
            "mem_media_mib": m_stats["media"],
            "mem_desv_mib": m_stats["desviacion"],
            "mem_cv": m_stats["cv"],
            "mem_ic95_low_mib": m_stats["ic95_low"],
            "mem_ic95_high_mib": m_stats["ic95_high"],
        }
    )

resumen_df = pd.DataFrame(filas).sort_values(["n", "estrategia"])
resumen_csv = OUT_DIR / "resumen_estadistico_r4.csv"
resumen_df.to_csv(resumen_csv, index=False)
print(resumen_df.to_string(index=False))

# Gráfico 1: Pico de memoria (MiB) vs. n para A, B y C
plt.figure(figsize=(8, 5))
for estrategia, g in resumen_df.groupby("estrategia"):
    g_ord = g.sort_values("n")
    plt.plot(g_ord["n"], g_ord["mem_media_mib"], marker="o", label=estrategia)
plt.title("Pico de memoria (MiB) vs. n por estrategia")
plt.xlabel("n (registros)")
plt.ylabel("Pico de memoria (MiB)")
plt.legend()
plt.grid(True, linestyle="--", alpha=0.5)
plt.tight_layout()
plt.savefig(OUT_DIR / "grafico_1_memoria_vs_n.png", dpi=150)
plt.close()

# Gráfico 2: Tiempo (s) vs. n con barras de error
plt.figure(figsize=(8, 5))
for estrategia, g in resumen_df.groupby("estrategia"):
    g_ord = g.sort_values("n")
    plt.errorbar(
        g_ord["n"],
        g_ord["tiempo_media_s"],
        yerr=g_ord["tiempo_desv_s"],
        marker="o",
        capsize=4,
        label=estrategia,
    )
plt.title("Tiempo de ejecución (s) vs. n con barras de error")
plt.xlabel("n (registros)")
plt.ylabel("Tiempo (s)")
plt.legend()
plt.grid(True, linestyle="--", alpha=0.5)
plt.tight_layout()
plt.savefig(OUT_DIR / "grafico_2_tiempo_vs_n.png", dpi=150)
plt.close()
