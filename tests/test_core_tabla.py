import unittest
import sys
import os
import tempfile

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.core.racoons import Tabla, racoons


class TestCoreTabla(unittest.TestCase):

    def setUp(self):
        self.columnas = ["dorsal", "nombre", "posicion", "goles", "asistencias"]
        self.filas = [
            {"dorsal": 10, "nombre": "Messi", "posicion": "Delantero", "goles": 14, "asistencias": 9},
            {"dorsal": 7, "nombre": "Ronaldo", "posicion": "Delantero", "goles": 16, "asistencias": 3},
            {"dorsal": 8, "nombre": "Iniesta", "posicion": "Mediocampista", "goles": 2, "asistencias": 8},
            {"dorsal": 4, "nombre": "Ramos", "posicion": "Defensa", "goles": 3, "asistencias": 1},
        ]
        self.tabla = Tabla(self.columnas, self.filas)

    def test_convocar(self):
        seleccion = self.tabla.convocar(["nombre", "goles"])
        self.assertEqual(seleccion.columnas, ["nombre", "goles"])
        self.assertEqual(len(seleccion), 4)
        self.assertEqual(seleccion.filas[0], {"nombre": "Messi", "goles": 14})

    def test_convocar_columna_inexistente(self):
        with self.assertRaises(ValueError):
            self.tabla.convocar(["nombre", "sueldo_ficticio"])

    def test_descartar(self):
        filtrada = self.tabla.descartar(lambda f: f["goles"] > 5)
        self.assertEqual(len(filtrada), 2)
        nombres = [f["nombre"] for f in filtrada.filas]
        self.assertIn("Messi", nombres)
        self.assertIn("Ronaldo", nombres)

    def test_contratar(self):
        calculada = self.tabla.contratar({
            "total_puntos": lambda f: f["goles"] + f["asistencias"]
        })
        self.assertIn("total_puntos", calculada.columnas)
        self.assertEqual(calculada.filas[0]["total_puntos"], 23)
        self.assertEqual(calculada.filas[1]["total_puntos"], 19)

    def test_rebautizar(self):
        renombrada = self.tabla.rebautizar({"goles": "tantos"})
        self.assertIn("tantos", renombrada.columnas)
        self.assertNotIn("goles", renombrada.columnas)
        self.assertEqual(renombrada.filas[0]["tantos"], 14)

    def test_clasificar(self):
        ordenada = self.tabla.clasificar(["goles"], descendente=True)
        self.assertEqual(ordenada.filas[0]["nombre"], "Ronaldo")
        self.assertEqual(ordenada.filas[-1]["nombre"], "Iniesta")

    def test_alinear_y_balance(self):
        resumen = self.tabla.alinear(["posicion"]).balance({
            "goles_totales": ("suma", "goles"),
            "total": ("contar", None),
        })
        self.assertIn("posicion", resumen.columnas)
        self.assertIn("goles_totales", resumen.columnas)
        self.assertEqual(len(resumen), 3)  # Defensa, Delantero, Mediocampista

        delanteros = [f for f in resumen.filas if f["posicion"] == "Delantero"][0]
        self.assertEqual(delanteros["goles_totales"], 30)
        self.assertEqual(delanteros["total"], 2)

    def test_sanear_y_depurar(self):
        filas_con_nulos = [
            {"dorsal": 1, "nombre": "JugadorA", "posicion": None},
            {"dorsal": 1, "nombre": "JugadorA", "posicion": None},
            {"dorsal": 2, "nombre": "JugadorB", "posicion": "Portero"},
        ]
        t = Tabla(["dorsal", "nombre", "posicion"], filas_con_nulos)
        saneada = t.sanear({"posicion": "SinPosicion"})
        self.assertEqual(saneada.filas[0]["posicion"], "SinPosicion")

        depurada = saneada.depurar(["dorsal"])
        self.assertEqual(len(depurada), 2)

    def test_csvsave_y_csvread(self):
        with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as tmp:
            tmp_path = tmp.name

        try:
            self.tabla.csvsave(tmp_path)
            leida = Tabla.csvread(tmp_path)
            self.assertEqual(leida.columnas, self.tabla.columnas)
            self.assertEqual(len(leida), len(self.tabla))
            self.assertEqual(leida.filas[0]["nombre"], "Messi")
            self.assertEqual(leida.filas[0]["goles"], 14)
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

    def test_alias_racoons_como_libreria(self):
        from src import racoons as rc
        self.assertIs(rc, Tabla)
        instancia = rc(["col1"], [{"col1": 100}])
        self.assertEqual(len(instancia), 1)
        self.assertEqual(instancia.filas[0]["col1"], 100)


if __name__ == "__main__":
    unittest.main()
