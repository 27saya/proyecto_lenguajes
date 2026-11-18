import os
import unittest
from src.core.racoons import Tabla
import src.core.matematica as mate
from src.core.ml import PerceptronMulticapaXOR, entrenar_mlp_xor, predecir_mlp
from src.semantic.visitor import ejecutar_archivo, ejecutar_codigo


class TestProgramasAdicionales(unittest.TestCase):
    """Pruebas unitarias para las extensiones matematicas, de excel, ml y programas adicionales."""

    def test_carga_excel_nativa(self):
        ruta_excel = os.path.join(os.path.dirname(__file__), "..", "data.xlsx")
        self.assertTrue(os.path.exists(ruta_excel), "El archivo data.xlsx debe existir en el repositorio.")
        tabla = Tabla.excelread(ruta_excel)
        self.assertGreater(len(tabla), 10000)
        self.assertIn("ingreso_mensual", tabla.columnas)
        self.assertIn("sex", tabla.columnas)
        self.assertIn("edad", tabla.columnas)
        self.assertIsInstance(tabla.filas[0]["edad"], (int, float))

    def test_matematica_pura_avanzada(self):
        # Factorial
        self.assertEqual(mate.factorial(5), 120)
        self.assertEqual(mate.factorial(6), 720)
        fact_100 = mate.factorial(100)
        self.assertGreater(fact_100, 10**150)

        # Exp y Sigmoide
        self.assertAlmostEqual(mate.exp(0), 1.0, places=5)
        self.assertAlmostEqual(mate.sigmoide(0), 0.5, places=5)
        self.assertGreater(mate.sigmoide(5), 0.99)
        self.assertLess(mate.sigmoide(-5), 0.01)

        # Es primo
        self.assertFalse(mate.es_primo(1))
        self.assertTrue(mate.es_primo(2))
        self.assertTrue(mate.es_primo(3))
        self.assertFalse(mate.es_primo(4))
        self.assertTrue(mate.es_primo(17))
        self.assertTrue(mate.es_primo(97))
        self.assertFalse(mate.es_primo(100))

    def test_perceptron_multicapa_xor(self):
        modelo = PerceptronMulticapaXOR()
        modelo.ajustar(epocas=6000, lr=0.8)

        p00 = modelo.predecir([0, 0])
        p01 = modelo.predecir([0, 1])
        p10 = modelo.predecir([1, 0])
        p11 = modelo.predecir([1, 1])

        # Verificar que XOR fue resuelto
        self.assertLess(p00, 0.1)
        self.assertGreater(p01, 0.9)
        self.assertGreater(p10, 0.9)
        self.assertLess(p11, 0.1)

        # Verificar historial de perdida decreciente
        self.assertGreater(len(modelo.historial), 3)
        self.assertLess(modelo.historial[-1]["perdida"], modelo.historial[0]["perdida"])

    def test_pipeline_filtro_funcional_primos_dsl(self):
        codigo = """
        tactica es_primo_local(n) {
            si (n <= 1) { resultado falso; }
            si (n <= 3) { resultado verdadero; }
            si (n % 2 == 0) { resultado falso; }
            resultado verdadero;
        }
        filas = [
            {"num": 1},
            {"num": 2},
            {"num": 3},
            {"num": 4},
            {"num": 5}
        ];
        t = crear_tabla(filas);
        filtrados = t |> descartar(es_primo_local(num));
        """
        visitor, errores = ejecutar_codigo(codigo)
        self.assertEqual(len(errores), 0, f"Errores encontrados: {errores}")
        res_tabla = visitor.tabla_simbolos.obtener("filtrados").valor
        self.assertEqual(len(res_tabla), 3)
        valores = [f["num"] for f in res_tabla.filas]
        self.assertEqual(valores, [2, 3, 5])

    def test_ejecucion_programas_individuales(self):
        dir_prog = os.path.join(os.path.dirname(__file__), "..", "programas")
        for num in [1, 2, 3, 4, 5]:
            archivos = [f for f in os.listdir(dir_prog) if f.startswith(f"{num}_")]
            self.assertEqual(len(archivos), 1, f"Debe existir archivo para programa {num}")
            ruta = os.path.join(dir_prog, archivos[0])
            visitor, errores = ejecutar_archivo(ruta)
            self.assertEqual(len(errores), 0, f"Error ejecutando {archivos[0]}: {errores}")
            # Validar que se registraron tiempo_ejecucion y memoria_usada
            simbolo_t = visitor.tabla_simbolos.obtener("tiempo_ejecucion")
            simbolo_m = visitor.tabla_simbolos.obtener("memoria_usada")
            self.assertIsNotNone(simbolo_t, f"Debe existir 'tiempo_ejecucion' en {archivos[0]}")
            self.assertIsNotNone(simbolo_m, f"Debe existir 'memoria_usada' en {archivos[0]}")
            self.assertGreaterEqual(simbolo_t.valor, 0.0)
            self.assertGreater(simbolo_m.valor, 0.0)

    def test_metricas_tiempo_y_memoria(self):
        codigo = """
        t0 = cronometro();
        m0 = memoria();
        lista = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
        t1 = cronometro();
        tiempo_ejecucion = t1 - t0;
        memoria_usada = memoria();
        """
        visitor, errores = ejecutar_codigo(codigo)
        self.assertEqual(len(errores), 0, f"Errores al medir metricas: {errores}")
        t = visitor.tabla_simbolos.obtener("tiempo_ejecucion").valor
        m = visitor.tabla_simbolos.obtener("memoria_usada").valor
        self.assertIsInstance(t, float)
        self.assertGreaterEqual(t, 0.0)
        self.assertIsInstance(m, float)
        self.assertGreater(m, 0.0)


if __name__ == "__main__":
    unittest.main()
