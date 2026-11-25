"""
Pruebas de corrección (R2). Ejecutar:  python -m unittest discover -s pruebas
Una estrategia más rápida pero incorrecta NO es una mejora.
"""
import importlib
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
    def test_linea_base_ejecuta(self):
        d = linea_base.preparar(1000)
        self.assertIsNotNone(linea_base.ejecutar(d))

    def comprobar_igual_a_linea_base(self, estrategia):
        ruta = linea_base.preparar(1000)
        esperado = linea_base.ejecutar(ruta)
        obtenido = estrategia.ejecutar(ruta)

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
