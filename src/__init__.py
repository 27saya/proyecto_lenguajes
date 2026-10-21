from antlr4 import InputStream, FileStream, CommonTokenStream
from .generated.DaZeLexer import DaZeLexer
from .generated.DaZeParser import DaZeParser
from .errors import DaZeErrorListener, DiagnosticError, SemanticError
from .tree_viewer import format_parse_tree, print_parse_tree
from .core import Tabla, GrupoTabla, suma, media, mediana, minimo, maximo, desviar, contar
from .semantic import TablaSimbolos, Simbolo, DaZeSemanticVisitor, ejecutar_codigo, ejecutar_archivo
from typing import Tuple, List


def parse_code(code: str) -> Tuple[DaZeParser.ProgramaContext, DaZeParser, List[DiagnosticError]]:
    input_stream = InputStream(code)
    lexer = DaZeLexer(input_stream)
    lexer_error_listener = DaZeErrorListener(error_type="Lexico")
    lexer.removeErrorListeners()
    lexer.addErrorListener(lexer_error_listener)

    token_stream = CommonTokenStream(lexer)
    parser = DaZeParser(token_stream)
    parser_error_listener = DaZeErrorListener(error_type="Sintactico")
    parser.removeErrorListeners()
    parser.addErrorListener(parser_error_listener)

    tree = parser.programa()
    all_errors = lexer_error_listener.errors + parser_error_listener.errors
    return tree, parser, all_errors


def parse_file(file_path: str) -> Tuple[DaZeParser.ProgramaContext, DaZeParser, List[DiagnosticError]]:
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    return parse_code(content)


def tokenize_code(code: str):
    input_stream = InputStream(code)
    lexer = DaZeLexer(input_stream)
    token_stream = CommonTokenStream(lexer)
    token_stream.fill()
    return token_stream.tokens


__all__ = [
    "parse_code",
    "parse_file",
    "tokenize_code",
    "DaZeLexer",
    "DaZeParser",
    "DaZeErrorListener",
    "DiagnosticError",
    "SemanticError",
    "format_parse_tree",
    "print_parse_tree",
    "Tabla",
    "GrupoTabla",
    "suma",
    "media",
    "mediana",
    "minimo",
    "maximo",
    "desviar",
    "contar",
    "TablaSimbolos",
    "Simbolo",
    "DaZeSemanticVisitor",
    "ejecutar_codigo",
    "ejecutar_archivo",
]
