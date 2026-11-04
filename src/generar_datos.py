"""Genera lecturas SIMULADAS de sensores IoT (semilla fija). Uso: python -m src.generar_datos 2000000"""
import random
import sys
from pathlib import Path


def generar_lecturas(ruta: Path, n: int, n_sensores: int = 200, semilla: int = 4) -> None:
    rng = random.Random(semilla)
    ruta.parent.mkdir(parents=True, exist_ok=True)
    with open(ruta, "w", encoding="utf-8") as f:
        f.write("id_sensor,marca_tiempo_s,temperatura_c,humedad_pct\n")
        for i in range(n):
            s = rng.randrange(n_sensores)
            f.write(f"S{s:04d},{i * 0.5:.1f},{rng.gauss(24 + s % 7, 1.5):.2f},{rng.uniform(30, 90):.1f}\n")


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 2_000_000
    destino = Path(__file__).resolve().parents[1] / "datos" / f"lecturas_{n}.csv"
    generar_lecturas(destino, n)
    print(f"{destino} ({destino.stat().st_size / 1e6:.1f} MB)")
