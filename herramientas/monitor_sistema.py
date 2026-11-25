"""
monitor_sistema.py — Serie temporal de CPU %, frecuencia, temperatura y memoria.

Se ejecuta en una terminal APARTE mientras corre el experimento. Produce un
CSV con una fila cada --intervalo segundos, útil para el gráfico
"magnitud vs. tiempo" de la Clase 5 (incluye inercia térmica).

Requiere psutil para CPU % y memoria del sistema. Sin psutil registra solo
frecuencia y temperatura (si el sistema las expone).

Uso:
    python monitor_sistema.py --duracion 120 --salida monitor.csv
    (Ctrl+C detiene antes y conserva lo registrado)
"""
import argparse
import csv
import time

import sensores

try:
    import psutil
except ImportError:
    psutil = None

p = argparse.ArgumentParser()
p.add_argument("--duracion", type=float, default=60, help="segundos totales")
p.add_argument("--intervalo", type=float, default=0.5, help="segundos entre muestras")
p.add_argument("--salida", default="monitor.csv")
a = p.parse_args()

campos = ["t_s", "cpu_sistema_pct", "frecuencia_mhz", "temperatura_c", "mem_usada_pct", "energia_acum_j"]
inicio = time.perf_counter()
e_inicio = sensores.energia_rapl_j()
if psutil:
    psutil.cpu_percent(None)  # la primera lectura de psutil siempre es 0: se descarta

with open(a.salida, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=campos)
    w.writeheader()
    try:
        while (t := time.perf_counter() - inicio) < a.duracion:
            time.sleep(a.intervalo)
            w.writerow({
                "t_s": f"{time.perf_counter() - inicio:.2f}",
                "cpu_sistema_pct": psutil.cpu_percent(None) if psutil else "",
                "frecuencia_mhz": sensores.frecuencia_mhz() or "",
                "temperatura_c": sensores.temperatura_c() or "",
                "mem_usada_pct": psutil.virtual_memory().percent if psutil else "",
                "energia_acum_j": "" if e_inicio is None
                else f"{sensores.delta_energia_j(e_inicio, sensores.energia_rapl_j()):.3f}",
            })
            f.flush()
            print(f"\r{t:6.1f} s registrados", end="", flush=True)
    except KeyboardInterrupt:
        pass
print(f"\nSerie guardada en {a.salida}")
