"""
Pruebas de corrección (R2). Ejecutar:  python -m unittest discover -s pruebas
Una estrategia más rápida pero incorrecta NO es una mejora.
"""
import importlib
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from src import linea_base


def cargar_estrategia(nombre):
    try:
        return importlib.import_module(f"src.{nombre}")
    except ModuleNotFoundError as error:
        if error.name == f"src.{nombre}":
            return None
        raise


estrategia_b = cargar_estrategia("estrategia_b")
estrategia_c = cargar_estrategia("estrategia_c")


class TestCorreccion(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        temporal = TemporaryDirectory()
        cls.addClassCleanup(temporal.cleanup)
        cls.ruta_prueba = Path(temporal.name) / "lecturas_1000.csv"
        with cls.ruta_prueba.open("w", encoding="utf-8") as archivo:
            archivo.write("id_sensor,marca_tiempo_s,temperatura_c,humedad_pct\n")
            for i in range(1000):
                sensor = i % 200
                temperatura = 20 + sensor % 7 + (i // 200) / 10
                archivo.write(
                    f"S{sensor:04d},{i * 0.5:.1f},{temperatura:.2f},50.0\n"
                )

    def test_linea_base_ejecuta(self):
        d = linea_base.preparar(1000)
        self.assertIsNotNone(linea_base.ejecutar(d))

    def comprobar_igual_a_linea_base(self, estrategia):
        esperado = linea_base.ejecutar(self.ruta_prueba)
        obtenido = estrategia.ejecutar(self.ruta_prueba)

        self.assertEqual(len(esperado), 200)
        self.assertEqual(obtenido.keys(), esperado.keys())
        for sensor, (media_esperada, maxima_esperada) in esperado.items():
            with self.subTest(sensor=sensor):
                media, maxima = obtenido[sensor]
                self.assertAlmostEqual(media, media_esperada, delta=1e-9)
                self.assertAlmostEqual(maxima, maxima_esperada, delta=1e-9)

    @unittest.skipIf(estrategia_b is None, "estrategia_b no está disponible")
    def test_estrategia_b_igual_a_base(self):
        self.comprobar_igual_a_linea_base(estrategia_b)

    @unittest.skipIf(estrategia_c is None, "estrategia_c no está disponible")
    def test_estrategia_c_igual_a_base(self):
        self.comprobar_igual_a_linea_base(estrategia_c)


if __name__ == "__main__":
    unittest.main()
