import argparse
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src import parse_file, tokenize_code, format_parse_tree, DaZeSemanticVisitor, SemanticError


def main():
    parser = argparse.ArgumentParser(
        description="Analizador e interprete para el lenguaje de analitica deportiva DaZe (.dz)"
    )
    parser.add_argument("archivo", help="Ruta al archivo fuente en lenguaje DaZe (.dz)")
    parser.add_argument("--tree", "-t", action="store_true", help="Imprimir el arbol de analisis sintactico")
    parser.add_argument("--tokens", "-k", action="store_true", help="Listar la secuencia de tokens reconocidos")
    parser.add_argument("--check", "-c", action="store_true", help="Solo verificar la sintaxis sin ejecutar")

    args = parser.parse_args()

    if not os.path.exists(args.archivo):
        print(f"Error: El archivo '{args.archivo}' no existe.")
        sys.exit(1)

    with open(args.archivo, "r", encoding="utf-8") as f:
        codigo = f.read()

    if args.tokens:
        print(f"--- Secuencia de tokens para: {args.archivo} ---")
        tokens = tokenize_code(codigo)
        for tok in tokens:
            if tok.text == "<EOF>":
                continue
            print(f"Token: {tok.text:<20} Linea: {tok.line:<4} Col: {tok.column:<4} Tipo ID: {tok.type}")
        print()

    tree, parser_instance, errors = parse_file(args.archivo)

    if errors:
        print(f"Se encontraron {len(errors)} error(es) de sintaxis en '{args.archivo}':")
        for err in errors:
            print(f"  {err}")
        sys.exit(1)

    if args.tree:
        print("\n--- Arbol de analisis sintactico ---")
        print(format_parse_tree(tree, parser_instance))
        print()

    if args.check:
        print(f"Validacion exitosa: El archivo '{args.archivo}' es sintacticamente correcto.")
        return

    # Ejecucion semantica
    base_dir = os.path.dirname(os.path.abspath(args.archivo))
    visitor = DaZeSemanticVisitor(base_dir=base_dir)

    try:
        visitor.visit(tree)
    except SemanticError:
        pass

    if visitor.errores_semanticos:
        print(f"Se encontraron {len(visitor.errores_semanticos)} error(es) semantico(s) en '{args.archivo}':")
        for err in visitor.errores_semanticos:
            print(f"  {err}")
        sys.exit(1)

    print(f"Ejecucion completada con exito para '{args.archivo}'.")


if __name__ == "__main__":
    main()
