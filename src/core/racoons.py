import csv
import os
from typing import List, Dict, Any, Optional, Union, Callable
from .estadistica import suma, media, mediana, minimo, maximo, desviar, contar


def _inferir_tipo(valor_texto: str) -> Any:
    val = valor_texto.strip()
    if val == "" or val.lower() in ("null", "nulo", "na", "nan", "none"):
        return None
    val_lower = val.lower()
    if val_lower in ("verdadero", "true"):
        return True
    if val_lower in ("falso", "false"):
        return False
    # Intentar entero
    try:
        if val.isdigit() or (val.startswith("-") and val[1:].isdigit()):
            return int(val)
    except ValueError:
        pass
    # Intentar flotante
    try:
        return float(val)
    except ValueError:
        pass
    return val


class GrupoTabla:
    """Estructura para representar particiones agrupadas de una Tabla."""

    def __init__(self, tabla: "Tabla", columnas_grupo: List[str]):
        self.tabla_origen = tabla
        self.columnas_grupo = columnas_grupo
        self.grupos: Dict[tuple, List[Dict[str, Any]]] = {}
        self._agrupar()

    def _agrupar(self) -> None:
        for col in self.columnas_grupo:
            if col not in self.tabla_origen.columnas:
                raise ValueError(f"Columna de agrupacion '{col}' no existe en la tabla.")

        for fila in self.tabla_origen.filas:
            clave = tuple(fila.get(c) for c in self.columnas_grupo)
            if clave not in self.grupos:
                self.grupos[clave] = []
            self.grupos[clave].append(fila)

    def balance(self, agregaciones: Dict[str, tuple]) -> "Tabla":
        nuevas_columnas = list(self.columnas_grupo) + list(agregaciones.keys())
        filas_resultado = []

        # Ordenar claves de grupo para resultados deterministas
        claves_ordenadas = sorted(
            self.grupos.keys(),
            key=lambda k: tuple("" if elem is None else str(elem) for elem in k)
        )

        for clave in claves_ordenadas:
            filas_del_grupo = self.grupos[clave]
            nueva_fila = {}
            for col, val in zip(self.columnas_grupo, clave):
                nueva_fila[col] = val

            for nombre_salida, info_agregacion in agregaciones.items():
                func_nombre, col_origen = info_agregacion
                valores_columna = [f.get(col_origen) for f in filas_del_grupo] if col_origen else filas_del_grupo

                resultado_val = _aplicar_agregacion(func_nombre, valores_columna)
                nueva_fila[nombre_salida] = resultado_val

            filas_resultado.append(nueva_fila)

        return Tabla(nuevas_columnas, filas_resultado)


def _aplicar_agregacion(func_nombre: str, valores: List[Any]) -> Any:
    fn = func_nombre.lower().strip()
    if fn in ("contar", "conteo"):
        return contar(valores)
    elif fn == "suma":
        return suma(valores)
    elif fn in ("media", "promedio"):
        return media(valores)
    elif fn == "mediana":
        return mediana(valores)
    elif fn in ("minimo", "min"):
        return minimo(valores)
    elif fn in ("maximo", "max"):
        return maximo(valores)
    elif fn in ("desviar", "desviacion", "desv_std"):
        return desviar(valores)
    else:
        raise ValueError(f"Funcion de agregacion desconocida: '{func_nombre}'")


class Tabla:
    """Librería propia para gestión y manipulación de datos tabulares deportivos."""

    def __init__(self, columnas: Optional[List[str]] = None, filas: Optional[List[Dict[str, Any]]] = None):
        self.columnas: List[str] = list(columnas) if columnas is not None else []
        self.filas: List[Dict[str, Any]] = [dict(f) for f in filas] if filas is not None else []

    @classmethod
    def csvread(cls, ruta: str, separador: str = ",", encabezado: bool = True, encoding: str = "utf-8") -> "Tabla":
        if not os.path.exists(ruta):
            raise FileNotFoundError(f"No se encontro el archivo de datos: '{ruta}'")

        filas_procesadas: List[Dict[str, Any]] = []
        columnas_finales: List[str] = []

        with open(ruta, "r", encoding=encoding, errors="replace") as f:
            reader = csv.reader(f, delimiter=separador)
            primeras_filas = list(reader)

        if not primeras_filas:
            return cls([], [])

        if encabezado:
            columnas_finales = [c.strip() for c in primeras_filas[0]]
            datos_filas = primeras_filas[1:]
        else:
            total_cols = len(primeras_filas[0])
            columnas_finales = [f"col_{i}" for i in range(total_cols)]
            datos_filas = primeras_filas

        for fila in datos_filas:
            if not fila or all(c.strip() == "" for c in fila):
                continue
            dict_fila = {}
            for i, col_name in enumerate(columnas_finales):
                val_raw = fila[i] if i < len(fila) else ""
                dict_fila[col_name] = _inferir_tipo(val_raw)
            filas_procesadas.append(dict_fila)

        return cls(columnas_finales, filas_procesadas)

    def csvsave(self, ruta: str, separador: str = ",", encoding: str = "utf-8") -> None:
        directorio = os.path.dirname(ruta)
        if directorio and not os.path.exists(directorio):
            os.makedirs(directorio, exist_ok=True)

        with open(ruta, "w", encoding=encoding, newline="") as f:
            writer = csv.writer(f, delimiter=separador)
            writer.writerow(self.columnas)
            for fila in self.filas:
                fila_salida = []
                for col in self.columnas:
                    val = fila.get(col, "")
                    if val is None:
                        fila_salida.append("")
                    elif isinstance(val, bool):
                        fila_salida.append("verdadero" if val else "falso")
                    else:
                        fila_salida.append(str(val))
                writer.writerow(fila_salida)

    def convocar(self, columnas: List[str]) -> "Tabla":
        for col in columnas:
            if col not in self.columnas:
                raise ValueError(f"Columna '{col}' no existe en la plantilla. Disponibles: {', '.join(self.columnas)}")

        nuevas_filas = []
        for fila in self.filas:
            nueva_fila = {col: fila.get(col) for col in columnas}
            nuevas_filas.append(nueva_fila)

        return Tabla(columnas, nuevas_filas)

    def descartar(self, condicion_func: Callable[[Dict[str, Any]], bool]) -> "Tabla":
        nuevas_filas = []
        for fila in self.filas:
            try:
                cumple = bool(condicion_func(fila))
            except Exception as e:
                cumple = False
            if cumple:
                nuevas_filas.append(dict(fila))

        return Tabla(list(self.columnas), nuevas_filas)

    def contratar(self, columnas_calculadas: Dict[str, Union[Callable[[Dict[str, Any]], Any], Any]]) -> "Tabla":
        nuevas_columnas = list(self.columnas)
        for nueva_col in columnas_calculadas.keys():
            if nueva_col not in nuevas_columnas:
                nuevas_columnas.append(nueva_col)

        nuevas_filas = []
        for fila in self.filas:
            fila_copia = dict(fila)
            for col_nombre, val_o_func in columnas_calculadas.items():
                if callable(val_o_func):
                    res = val_o_func(fila_copia)
                else:
                    res = val_o_func
                fila_copia[col_nombre] = res
            nuevas_filas.append(fila_copia)

        return Tabla(nuevas_columnas, nuevas_filas)

    def rebautizar(self, mapeo: Dict[str, str]) -> "Tabla":
        for col_vieja in mapeo.keys():
            if col_vieja not in self.columnas:
                raise ValueError(f"No se puede rebautizar la columna inexistente '{col_vieja}'.")

        nuevas_columnas = [mapeo.get(c, c) for c in self.columnas]
        nuevas_filas = []
        for fila in self.filas:
            nueva_fila = {}
            for col_vieja, valor in fila.items():
                col_nueva = mapeo.get(col_vieja, col_vieja)
                nueva_fila[col_nueva] = valor
            nuevas_filas.append(nueva_fila)

        return Tabla(nuevas_columnas, nuevas_filas)

    def clasificar(self, columnas: List[str], descendente: bool = False) -> "Tabla":
        for col in columnas:
            if col not in self.columnas:
                raise ValueError(f"Columna de ordenamiento '{col}' no encontrada en la tabla.")

        def clave_orden(fila):
            valores = []
            for col in columnas:
                v = fila.get(col)
                if v is None:
                    # Nulos van al final
                    valores.append((1, ""))
                elif isinstance(v, (int, float)):
                    valores.append((0, float(v)))
                else:
                    valores.append((0, str(v)))
            return tuple(valores)

        filas_ordenadas = sorted(self.filas, key=clave_orden, reverse=descendente)
        return Tabla(list(self.columnas), [dict(f) for f in filas_ordenadas])

    def alinear(self, columnas_grupo: List[str]) -> GrupoTabla:
        return GrupoTabla(self, columnas_grupo)

    def balance(self, agregaciones: Dict[str, tuple]) -> "Tabla":
        nuevas_columnas = list(agregaciones.keys())
        fila_resumen = {}
        for nombre_salida, info_agregacion in agregaciones.items():
            func_nombre, col_origen = info_agregacion
            valores_columna = [f.get(col_origen) for f in self.filas] if col_origen else self.filas
            fila_resumen[nombre_salida] = _aplicar_agregacion(func_nombre, valores_columna)

        return Tabla(nuevas_columnas, [fila_resumen])

    def sanear(self, reemplazos: Union[Dict[str, Any], Any]) -> "Tabla":
        nuevas_filas = []
        for fila in self.filas:
            fila_nueva = dict(fila)
            for col, val in fila_nueva.items():
                if val is None or val == "":
                    if isinstance(reemplazos, dict):
                        if col in reemplazos:
                            fila_nueva[col] = reemplazos[col]
                    else:
                        fila_nueva[col] = reemplazos
            nuevas_filas.append(fila_nueva)
        return Tabla(list(self.columnas), nuevas_filas)

    def depurar(self, columnas: Optional[List[str]] = None) -> "Tabla":
        cols_clave = columnas if columnas else self.columnas
        vistos = set()
        filas_unicas = []

        for fila in self.filas:
            clave = tuple(fila.get(c) for c in cols_clave)
            if clave not in vistos:
                vistos.add(clave)
                filas_unicas.append(dict(fila))

        return Tabla(list(self.columnas), filas_unicas)

    def top(self, n: int) -> "Tabla":
        limite = max(0, int(n))
        return Tabla(list(self.columnas), [dict(f) for f in self.filas[:limite]])

    def copiar(self) -> "Tabla":
        return Tabla(list(self.columnas), [dict(f) for f in self.filas])

    def obtenercolumna(self, nombre: str) -> List[Any]:
        if nombre not in self.columnas:
            raise ValueError(f"Columna '{nombre}' no encontrada.")
        return [f.get(nombre) for f in self.filas]

    def mostrar(self, limite: int = 10) -> str:
        if not self.columnas:
            return "Tabla vacia (0 columnas, 0 filas)"

        filas_mostrar = self.filas[:limite]
        # Calcular anchos de columna
        anchos = {}
        for col in self.columnas:
            longitud_max = len(str(col))
            for f in filas_mostrar:
                v_str = str(f.get(col, ""))
                if len(v_str) > longitud_max:
                    longitud_max = len(v_str)
            anchos[col] = max(longitud_max, 4)

        linea_separadora = "+" + "+".join("-" * (anchos[c] + 2) for c in self.columnas) + "+"
        encabezado = "| " + " | ".join(str(c).ljust(anchos[c]) for c in self.columnas) + " |"

        lineas = [linea_separadora, encabezado, linea_separadora]
        for f in filas_mostrar:
            fila_txt = "| " + " | ".join(str(f.get(c, "") if f.get(c) is not None else "nulo").ljust(anchos[c]) for c in self.columnas) + " |"
            lineas.append(fila_txt)
        lineas.append(linea_separadora)

        total = len(self.filas)
        if total > limite:
            lineas.append(f"... mostrando {limite} de {total} registros totales.")
        else:
            lineas.append(f"Total: {total} registro(s).")

        return "\n".join(lineas)

    def __len__(self) -> int:
        return len(self.filas)

    def __repr__(self) -> str:
        return f"<Tabla {len(self.columnas)} cols, {len(self.filas)} filas>"


# Alias para permitir usar racoons como nombre de la libreria/clase
racoons = Tabla
