import unittest
import sys
import os
import tempfile

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.semantic.visitor import ejecutar_codigo, ejecutar_archivo
from src.core.tabla import Tabla


class TestInterpreter(unittest.TestCase):

    def setUp(self):
        self.base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    def test_pipeline_completo_con_balance_y_guardado(self):
        with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as tmp:
            tmp_csv = tmp.name

        codigo = f"""
        jugadores = fichar("datos/plantilla_temporada.csv");
        delanteros = jugadores
            |> convocar(dorsal, nombre, posicion, minutos, goles)
            |> descartar(posicion == "Delantero")
            |> contratar(goles_por_minuto = (goles * 90) / minutos)
            |> clasificar(por=[goles], descendente=verdadero);

        resumen = delanteros
            |> alinear(por=[posicion])
            |> balance(
                total_goles = suma(goles),
                media_goles = media(goles),
                cuenta = contar()
            );

        archivar(resumen, en="{tmp_csv}");
        """

        try:
            visitor, errores = ejecutar_codigo(codigo, base_dir=self.base_dir)
            self.assertEqual(len(errores), 0, f"Errores encontrados: {errores}")
            self.assertTrue(os.path.exists(tmp_csv))

            tabla_guardada = Tabla.csvread(tmp_csv)
            self.assertEqual(len(tabla_guardada), 1)
            self.assertEqual(tabla_guardada.filas[0]["total_goles"], 58)
            self.assertEqual(tabla_guardada.filas[0]["cuenta"], 4)
        finally:
            if os.path.exists(tmp_csv):
                os.remove(tmp_csv)

    def test_tactica_con_control_de_flujo(self):
        codigo = """
        tactica evaluar_rendimiento(goles, asistencias) {
            total = goles + asistencias;
            si (total >= 10) {
                resultado "Destacado";
            } sino {
                resultado "En desarrollo";
            }
        }

        calificacion1 = evaluar_rendimiento(8, 4);
        calificacion2 = evaluar_rendimiento(2, 1);
        """
        visitor, errores = ejecutar_codigo(codigo)
        self.assertEqual(len(errores), 0)
        self.assertEqual(visitor.tabla_simbolos.obtener("calificacion1").valor, "Destacado")
        self.assertEqual(visitor.tabla_simbolos.obtener("calificacion2").valor, "En desarrollo")

    def test_operaciones_sanear_y_top(self):
        codigo = """
        cantera = fichar("datos/academia_juvenil.csv");
        top2 = cantera
            |> clasificar(por=[nota_tactica], descendente=verdadero)
            |> top(2);
        """
        visitor, errores = ejecutar_codigo(codigo, base_dir=self.base_dir)
        self.assertEqual(len(errores), 0)
        t_top = visitor.tabla_simbolos.obtener("top2").valor
        self.assertEqual(len(t_top), 2)


if __name__ == "__main__":
    unittest.main()
