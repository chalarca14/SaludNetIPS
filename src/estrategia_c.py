"""
Estrategia C — Equipo 4: Gestión eficiente de memoria.

Guarda solo las temperaturas en un array('d') por sensor (sin diccionarios
por fila ni listas de floats) y calcula media redondeada a 3 decimales y
máxima por sensor, devolviendo el diccionario ordenado por id_sensor.

preparar(n) -> ruta del archivo de lecturas (lo genera si no existe)
ejecutar(ruta) -> {id_sensor: (media, maxima)}
"""

from array import array
from pathlib import Path

from src.generar_datos import generar_lecturas

DATOS = Path(__file__).resolve().parents[1] / "datos"


def preparar(n: int) -> Path:
    ruta = DATOS / f"lecturas_{n}.csv"
    if not ruta.exists():
        generar_lecturas(ruta, n)
    return ruta


def ejecutar(ruta: Path) -> dict[str, tuple[float, float]]:
    por_sensor: dict[str, array] = {}

    with open(ruta, encoding="utf-8") as f:
        cabecera = f.readline().strip().split(",")
        idx_sensor = cabecera.index("id_sensor")
        idx_temp = cabecera.index("temperatura_c")

        for linea in f:
            fila = linea.strip().split(",")
            if len(fila) <= max(idx_sensor, idx_temp):
                continue
            sensor = fila[idx_sensor]
            temp = float(fila[idx_temp])

            arr = por_sensor.get(sensor)
            if arr is None:
                arr = array("d")
                por_sensor[sensor] = arr
            arr.append(temp)

    resultado: dict[str, tuple[float, float]] = {}
    for sensor in sorted(por_sensor):
        arr = por_sensor[sensor]
        cantidad = len(arr)
        media = round(sum(arr) / cantidad, 3)
        maxima = max(arr)
        resultado[sensor] = (media, maxima)

    return resultado


if __name__ == "__main__":
    import time
    import tracemalloc

    r = preparar(300_000)
    tracemalloc.start()
    t0 = time.perf_counter()
    res = ejecutar(r)
    t = time.perf_counter() - t0
    pico = tracemalloc.get_traced_memory()[1] / 2**20
    tracemalloc.stop()
    print(
        f"[Estrategia C] {len(res)} sensores · tiempo {t:.2f} s · pico {pico:.2f} MiB"
    )
