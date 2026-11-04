"""
Línea base — Equipo 4: Gestión eficiente de memoria.

Situación inicial: el tablero de monitoreo de la empresa carga TODAS las
lecturas de sensores como diccionarios en una lista y luego calcula, para
cada sensor, temperatura media y máxima. Con archivos grandes el servidor
se queda sin memoria.

preparar(n) -> ruta del archivo de lecturas (lo genera si no existe)
ejecutar(ruta) -> {id_sensor: (media, maxima)}
Magnitud principal a medir: PICO de memoria (tracemalloc) además del tiempo.
"""
from pathlib import Path

from src.generar_datos import generar_lecturas

DATOS = Path(__file__).resolve().parents[1] / "datos"


def preparar(n: int) -> Path:
    ruta = DATOS / f"lecturas_{n}.csv"
    if not ruta.exists():
        generar_lecturas(ruta, n)
    return ruta


def ejecutar(ruta: Path) -> dict[str, tuple[float, float]]:
    with open(ruta, encoding="utf-8") as f:
        cabecera = f.readline().strip().split(",")
        lecturas = [dict(zip(cabecera, linea.strip().split(","))) for linea in f]   # todo en RAM
    por_sensor: dict[str, list[float]] = {}
    for l in lecturas:
        por_sensor.setdefault(l["id_sensor"], []).append(float(l["temperatura_c"]))
    return {s: (round(sum(v) / len(v), 3), max(v)) for s, v in sorted(por_sensor.items())}


if __name__ == "__main__":
    import time, tracemalloc
    r = preparar(300_000)
    tracemalloc.start(); t0 = time.perf_counter()
    res = ejecutar(r)
    t = time.perf_counter() - t0; pico = tracemalloc.get_traced_memory()[1] / 2**20; tracemalloc.stop()
    print(f"{len(res)} sensores · tiempo {t:.2f} s (inflado por tracemalloc) · pico {pico:.1f} MiB")
