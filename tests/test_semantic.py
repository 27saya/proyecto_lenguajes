import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.semantic.tabla_simbolos import TablaSimbolos, Simbolo
from src.core.tabla import Tabla
from src.semantic.visitor import ejecutar_codigo


class TestSemantic(unittest.TestCase):

    def test_tabla_simbolos_definir_y_obtener(self):
        ts = TablaSimbolos()
        ts.definir("salario", 5000)
        ts.definir("nombre", "Cristiano")
        ts.definir("titular", True)

        self.assertTrue(ts.existe("salario"))
        self.assertEqual(ts.obtener("salario").valor, 5000)
        self.assertEqual(ts.obtener("salario").tipo, "NUMERO")
        self.assertEqual(ts.obtener("titular").tipo, "BOOLEANO")

    def test_tabla_simbolos_ambitos_anidados(self):
        global_scope = TablaSimbolos(nombre_ambito="global")
        global_scope.definir("x", 100)

        local_scope = global_scope.crear_ambito_hijo(nombre="local_1")
        local_scope.definir("y", 200)

        self.assertTrue(local_scope.existe("x"))
        self.assertTrue(local_scope.existe("y"))
        self.assertEqual(local_scope.obtener("x").valor, 100)

        # Global no debe ver variables locales
        self.assertFalse(global_scope.existe("y"))

    def test_error_variable_no_declarada(self):
        codigo = """
        x = 10;
        y = x + variable_fantasma;
        """
        visitor, errores = ejecutar_codigo(codigo)
        self.assertGreater(len(errores), 0)
        self.assertTrue(any("variable_fantasma" in e.message for e in errores))

    def test_error_columna_inexistente_en_pipeline(self):
        codigo = """
        datos = fichar("datos/plantilla_temporada.csv");
        filtrado = datos
            |> convocar(dorsal, columna_que_no_existe);
        """
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        visitor, errores = ejecutar_codigo(codigo, base_dir=base_dir)
        self.assertGreater(len(errores), 0)
        self.assertTrue(any("columna_que_no_existe" in e.message for e in errores))

    def test_error_operacion_tipos_incompatibles(self):
        codigo = """
        valor = 50 - "invalido";
        """
        visitor, errores = ejecutar_codigo(codigo)
        self.assertGreater(len(errores), 0)
        self.assertTrue(any("Operacion resta requiere operandos numericos" in e.message for e in errores))


if __name__ == "__main__":
    unittest.main()
