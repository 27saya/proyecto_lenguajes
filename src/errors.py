from dataclasses import dataclass
from typing import List, Optional
from antlr4.error.ErrorListener import ErrorListener
from antlr4.Recognizer import Recognizer
from antlr4.Token import Token


@dataclass
class DiagnosticError:
    line: int
    column: int
    message: str
    offending_symbol: Optional[str] = None
    error_type: str = "Sintactico"

    def __str__(self) -> str:
        symbol_info = f" en '{self.offending_symbol}'" if self.offending_symbol else ""
        return f"[{self.error_type}] Linea {self.line}:{self.column}{symbol_info} -> {self.message}"


class SemanticError(Exception):
    """Excepcion personalizada para diagnosticos semanticos."""

    def __init__(
        self,
        message: str,
        line: int = 0,
        column: int = 0,
        offending_symbol: Optional[str] = None,
    ):
        super().__init__(message)
        self.message = message
        self.line = line
        self.column = column
        self.offending_symbol = offending_symbol
        self.error_type = "Semantico"

    def to_diagnostic(self) -> DiagnosticError:
        return DiagnosticError(
            line=self.line,
            column=self.column,
            message=self.message,
            offending_symbol=self.offending_symbol,
            error_type=self.error_type,
        )

    def __str__(self) -> str:
        return str(self.to_diagnostic())


class DaZeErrorListener(ErrorListener):
    def __init__(self, error_type: str = "Sintactico"):
        super().__init__()
        self.error_type = error_type
        self.errors: List[DiagnosticError] = []

    def syntaxError(
        self,
        recognizer: Recognizer,
        offendingSymbol: Optional[Token],
        line: int,
        column: int,
        msg: str,
        e: Optional[Exception],
    ):
        symbol_text = None
        if offendingSymbol is not None and hasattr(offendingSymbol, "text"):
            symbol_text = offendingSymbol.text

        readable_msg = self._humanize_message(msg)
        error = DiagnosticError(
            line=line,
            column=column,
            message=readable_msg,
            offending_symbol=symbol_text,
            error_type=self.error_type,
        )
        self.errors.append(error)

    def _humanize_message(self, raw_msg: str) -> str:
        if "mismatched input" in raw_msg:
            return raw_msg.replace("mismatched input", "Entrada inesperada").replace("expecting", "se esperaba")
        elif "extraneous input" in raw_msg:
            return raw_msg.replace("extraneous input", "Elemento no esperado").replace("expecting", "se esperaba")
        elif "missing" in raw_msg:
            return raw_msg.replace("missing", "Falta el elemento").replace("at", "en")
        elif "no viable alternative at input" in raw_msg:
            return raw_msg.replace("no viable alternative at input", "Estructura no valida cerca de")
        elif "token recognition error at:" in raw_msg:
            return raw_msg.replace("token recognition error at:", "Caracter o simbolo no reconocido:")
        return raw_msg

    def has_errors(self) -> bool:
        return len(self.errors) > 0

    def print_diagnostics(self) -> None:
        for err in self.errors:
            print(str(err))
