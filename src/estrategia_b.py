"""
Estrategia B — Equipo 4: Gestión eficiente de memoria.

Lee el CSV línea por línea y acumula solo suma, cantidad y temperatura
máxima por sensor, sin guardar listas de lecturas ni diccionarios por fila.

preparar(n) -> ruta del archivo de lecturas (lo genera si no existe)
ejecutar(ruta) -> {id_sensor: (media, maxima)}
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
    # Por cada sensor guardamos: [suma, cantidad, maxima]
    acumulados: dict[str, list[float | int]] = {}

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

            estado = acumulados.get(sensor)
            if estado is None:
                acumulados[sensor] = [temp, 1, temp]
            else:
                estado[0] += temp
                estado[1] += 1
                if temp > estado[2]:
                    estado[2] = temp

    return {
        sensor: (round(datos[0] / datos[1], 3), float(datos[2]))
        for sensor, datos in sorted(acumulados.items())
    }


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
        f"[Estrategia B] {len(res)} sensores · tiempo {t:.2f} s · pico {pico:.2f} MiB"
    )
