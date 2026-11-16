import unittest
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.core.ml import (
    correlacion_pearson,
    correlacion,
    RegresionLineal,
    KMeans,
    regresion_lineal,
    regresionlineal,
    agrupar_kmedias,
    agruparkmedias,
    predecir_regresion,
    predecir,
)
from src.core.visualizador import CanvasPNG, renderizar_pizarra_nativa
from src.core.matematica import raiz_cuadrada, seno, coseno, potencia, valor_absoluto
from src.core.estructuras import Pila, Cola
from src.semantic.visitor import ejecutar_codigo


class TestVisualizacionYML(unittest.TestCase):

    def test_correlacion_pearson_positiva(self):
        x = [10, 20, 30, 40, 50]
        y = [2, 4, 6, 8, 10]
        r = correlacion_pearson(x, y)
        self.assertAlmostEqual(r, 1.0, places=4)
        r_alias = correlacion(x, y)
        self.assertAlmostEqual(r_alias, 1.0, places=4)

    def test_regresion_lineal_mco_y_prediccion(self):
        x = [1, 2, 3, 4, 5]
        y = [3, 5, 7, 9, 11]  # y = 2x + 1

        # Prueba sobre la clase
        modelo = RegresionLineal()
        res = modelo.ajustar(x, y)
        self.assertAlmostEqual(res.m, 2.0, places=4)
        self.assertAlmostEqual(res.b, 1.0, places=4)
        self.assertAlmostEqual(res.r2, 1.0, places=4)
        pred_val = modelo.predecir(6)
        self.assertAlmostEqual(pred_val, 13.0, places=4)

        # Prueba sobre el helper funcional con alias sin guion bajo
        res_dict = regresionlineal(x, y)
        self.assertAlmostEqual(res_dict["m"], 2.0, places=4)
        self.assertAlmostEqual(res_dict["b"], 1.0, places=4)
        self.assertAlmostEqual(res_dict["r2"], 1.0, places=4)
        pred_dict = predecir(res_dict, 6)
        self.assertAlmostEqual(pred_dict, 13.0, places=4)

    def test_kmeans_agrupamiento(self):
        datos = [[1.0, 1.0], [1.5, 2.0], [10.0, 10.0], [11.0, 9.5]]

        # Prueba sobre la clase
        km = KMeans(k=2, max_iter=20)
        res = km.ajustar(datos)
        self.assertEqual(len(res.centroides), 2)
        self.assertEqual(len(res.etiquetas), 4)
        self.assertEqual(res.etiquetas[0], res.etiquetas[1])
        self.assertEqual(res.etiquetas[2], res.etiquetas[3])
        self.assertNotEqual(res.etiquetas[0], res.etiquetas[2])

        # Prueba sobre el helper funcional con alias
        res_dict = agruparkmedias(datos, 2)
        self.assertEqual(len(res_dict["centroides"]), 2)
        self.assertEqual(len(res_dict["etiquetas"]), 4)

    def test_generacion_fisica_png_valido(self):
        ruta_test_png = "/tmp/test_verificacion.png"
        canvas = CanvasPNG(ancho=100, alto=100)
        canvas.rectangulo(10, 10, 90, 90, (255, 0, 0))
        canvas.guardar(ruta_test_png)

        self.assertTrue(os.path.exists(ruta_test_png))
        with open(ruta_test_png, "rb") as f:
            cabecera = f.read(8)
        self.assertEqual(cabecera, b"\x89PNG\r\n\x1a\n")

        if os.path.exists(ruta_test_png):
            os.remove(ruta_test_png)

    def test_renderizado_pizarra_nativa_barras_con_texto(self):
        filas = [{"pos": "DEL", "goles": 10}, {"pos": "MED", "goles": 5}]
        config = {
            "eje_x": "pos",
            "eje_y": "goles",
            "titulo": "Goles por posicion",
            "guardar": "/tmp/test_barras.png",
        }
        renderizar_pizarra_nativa("barras", filas, config)
        self.assertTrue(os.path.exists("/tmp/test_barras.png"))
        if os.path.exists("/tmp/test_barras.png"):
            os.remove("/tmp/test_barras.png")

    def test_canvas_png_texto_bitmap(self):
        canvas = CanvasPNG(ancho=200, alto=100)
        canvas.texto(10, 10, "DaZe 10", color=(10, 10, 10), escala=1)
        canvas.texto_centrado(30, "Titulo", color=(20, 20, 20), escala=2)

        # Verificar que se modificaron pixeles con el color del texto
        pixeles_texto = sum(
            1 for fila in canvas.pixeles for p in fila if p in ((10, 10, 10), (20, 20, 20))
        )
        self.assertGreater(pixeles_texto, 20)

    def test_matematica_pura(self):
        self.assertAlmostEqual(raiz_cuadrada(49), 7.0, places=4)
        self.assertAlmostEqual(seno(0), 0.0, places=4)
        self.assertAlmostEqual(coseno(0), 1.0, places=4)
        self.assertEqual(potencia(2, 4), 16.0)
        self.assertEqual(valor_absoluto(-42), 42)

    def test_estructuras_pila_y_cola(self):
        pila = Pila()
        pila.apilar("A")
        pila.apilar("B")
        self.assertEqual(pila.tope(), "B")
        self.assertEqual(pila.desapilar(), "B")
        self.assertEqual(len(pila), 1)

        cola = Cola()
        cola.encolar(10)
        cola.encolar(20)
        self.assertEqual(cola.frente(), 10)
        self.assertEqual(cola.desencolar(), 10)
        self.assertEqual(len(cola), 1)

    def test_bucle_enjuego_y_ronda_dsl(self):
        codigo = """
        acc = 0;
        i = 1;
        enjuego (i <= 3) {
            acc = acc + i;
            i = i + 1;
        }
        items = [10, 20];
        total = 0;
        ronda (elem en items) {
            total = total + elem;
        }
        """
        visitor, errores = ejecutar_codigo(codigo)
        self.assertEqual(len(errores), 0)
        self.assertEqual(visitor.tabla_simbolos.obtener("acc").valor, 6)
        self.assertEqual(visitor.tabla_simbolos.obtener("total").valor, 30)


if __name__ == "__main__":
    unittest.main()
