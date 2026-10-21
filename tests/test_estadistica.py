import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.core.estadistica import suma, media, mediana, minimo, maximo, desviar, contar


class TestEstadistica(unittest.TestCase):

    def test_suma_basica_y_nulos(self):
        self.assertEqual(suma([10, 20, 30]), 60)
        self.assertEqual(suma([10, None, 20, "", 5.5]), 35.5)
        self.assertEqual(suma([]), 0)

    def test_contar(self):
        self.assertEqual(contar([1, 2, 3, 4]), 4)
        self.assertEqual(contar([1, None, "", 4]), 2)
        self.assertEqual(contar([]), 0)

    def test_media(self):
        self.assertEqual(media([10, 20, 30]), 20.0)
        self.assertEqual(media([10, None, 20]), 15.0)
        self.assertEqual(media([]), 0.0)

    def test_mediana_impar_y_par(self):
        self.assertEqual(mediana([5, 1, 9]), 5)
        self.assertEqual(mediana([1, 2, 3, 4]), 2.5)
        self.assertEqual(mediana([]), 0.0)

    def test_minimo_y_maximo(self):
        self.assertEqual(minimo([10, -5, 20, 0]), -5)
        self.assertEqual(maximo([10, -5, 20, 0]), 20)
        self.assertEqual(minimo([]), 0.0)
        self.assertEqual(maximo([]), 0.0)

    def test_desviar(self):
        # Datos: [2, 4, 4, 4, 5, 5, 7, 9] -> media = 5.0
        # Varianza muestral = 32 / 7 = 4.5714 -> std = ~2.1381
        datos = [2, 4, 4, 4, 5, 5, 7, 9]
        self.assertAlmostEqual(desviar(datos, muestral=True), 2.1381, places=3)
        self.assertEqual(desviar([10]), 0.0)
        self.assertEqual(desviar([]), 0.0)


if __name__ == "__main__":
    unittest.main()
