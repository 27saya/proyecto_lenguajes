"""
Generador visual dual para DaZe.
Traza graficos en consola y genera fisicamente archivos PNG validos con CanvasPNG
utilizando unicamente modulos estandar (zlib y struct) y tipografia bitmap nativa 5x7.
"""

import os
import struct
import zlib

# Matriz de fuentes bitmap 5x7 para los 95 caracteres ASCII imprimibles (32 a 126).
# Cada caracter esta representado por 5 columnas de 7 bits (bit 0 = fila superior).
FONT_5X7 = {
    " ": [0, 0, 0, 0, 0],
    "!": [0, 0, 95, 0, 0],
    "\"": [0, 7, 0, 7, 0],
    "#": [20, 127, 20, 127, 20],
    "$": [36, 42, 127, 42, 18],
    "%": [35, 19, 8, 100, 98],
    "&": [54, 73, 85, 34, 80],
    "'": [0, 5, 3, 0, 0],
    "(": [0, 28, 34, 65, 0],
    ")": [0, 65, 34, 28, 0],
    "*": [20, 8, 62, 8, 20],
    "+": [8, 8, 62, 8, 8],
    ",": [0, 80, 48, 0, 0],
    "-": [8, 8, 8, 8, 8],
    ".": [0, 96, 96, 0, 0],
    "/": [32, 16, 8, 4, 2],
    "0": [62, 81, 73, 69, 62],
    "1": [0, 66, 127, 64, 0],
    "2": [66, 97, 81, 73, 70],
    "3": [33, 65, 69, 75, 49],
    "4": [24, 20, 18, 127, 16],
    "5": [39, 69, 69, 69, 57],
    "6": [60, 74, 73, 73, 48],
    "7": [1, 113, 9, 5, 3],
    "8": [54, 73, 73, 73, 54],
    "9": [6, 73, 73, 41, 30],
    ":": [0, 54, 54, 0, 0],
    ";": [0, 86, 54, 0, 0],
    "<": [8, 20, 34, 65, 0],
    "=": [20, 20, 20, 20, 20],
    ">": [0, 65, 34, 20, 8],
    "?": [2, 1, 81, 9, 6],
    "@": [50, 73, 121, 65, 62],
    "A": [126, 17, 17, 17, 126],
    "B": [127, 73, 73, 73, 54],
    "C": [62, 65, 65, 65, 34],
    "D": [127, 65, 65, 34, 28],
    "E": [127, 73, 73, 73, 65],
    "F": [127, 9, 9, 9, 1],
    "G": [62, 65, 73, 73, 122],
    "H": [127, 8, 8, 8, 127],
    "I": [0, 65, 127, 65, 0],
    "J": [32, 64, 65, 63, 1],
    "K": [127, 8, 20, 34, 65],
    "L": [127, 64, 64, 64, 64],
    "M": [127, 2, 12, 2, 127],
    "N": [127, 4, 8, 16, 127],
    "O": [62, 65, 65, 65, 62],
    "P": [127, 9, 9, 9, 6],
    "Q": [62, 65, 81, 33, 94],
    "R": [127, 9, 25, 41, 70],
    "S": [70, 73, 73, 73, 49],
    "T": [1, 1, 127, 1, 1],
    "U": [63, 64, 64, 64, 63],
    "V": [31, 32, 64, 32, 31],
    "W": [63, 64, 56, 64, 63],
    "X": [99, 20, 8, 20, 99],
    "Y": [7, 8, 112, 8, 7],
    "Z": [97, 81, 73, 69, 67],
    "[": [0, 127, 65, 65, 0],
    "\\": [2, 4, 8, 16, 32],
    "]": [0, 65, 65, 127, 0],
    "^": [4, 2, 1, 2, 4],
    "_": [64, 64, 64, 64, 64],
    "`": [0, 1, 2, 4, 0],
    "a": [32, 84, 84, 84, 120],
    "b": [127, 72, 68, 68, 56],
    "c": [56, 68, 68, 68, 32],
    "d": [56, 68, 68, 72, 127],
    "e": [56, 84, 84, 84, 24],
    "f": [8, 126, 9, 1, 2],
    "g": [24, 164, 164, 164, 124],
    "h": [127, 8, 4, 4, 120],
    "i": [0, 68, 125, 64, 0],
    "j": [32, 64, 68, 61, 0],
    "k": [127, 16, 40, 68, 0],
    "l": [0, 65, 127, 64, 0],
    "m": [124, 4, 24, 4, 120],
    "n": [124, 8, 4, 4, 120],
    "o": [56, 68, 68, 68, 56],
    "p": [252, 36, 36, 36, 24],
    "q": [24, 36, 36, 36, 252],
    "r": [124, 8, 4, 4, 8],
    "s": [72, 84, 84, 84, 32],
    "t": [4, 63, 68, 64, 32],
    "u": [60, 64, 64, 32, 124],
    "v": [28, 32, 64, 32, 28],
    "w": [60, 64, 48, 64, 60],
    "x": [68, 40, 16, 40, 68],
    "y": [156, 160, 160, 160, 124],
    "z": [68, 100, 84, 76, 68],
    "{": [0, 8, 54, 65, 0],
    "|": [0, 0, 127, 0, 0],
    "}": [0, 65, 54, 8, 0],
    "~": [16, 8, 16, 32, 16]
}


def _empaquetar_png(ancho, alto, pixeles):
    """Genera los bytes de un archivo PNG valido usando unicamente zlib estandar."""
    header = b"\x89PNG\r\n\x1a\n"
    ihdr_data = struct.pack(">IIBBBBB", ancho, alto, 8, 2, 0, 0, 0)
    ihdr_crc = zlib.crc32(b"IHDR" + ihdr_data)
    ihdr = struct.pack(">I", len(ihdr_data)) + b"IHDR" + ihdr_data + struct.pack(">I", ihdr_crc)

    raw_data = bytearray()
    for y in range(alto):
        raw_data.append(0)  # Filtro PNG 0: None
        for x in range(ancho):
            r, g, b = pixeles[y][x]
            raw_data.extend((r, g, b))

    comprimido = zlib.compress(bytes(raw_data), level=6)
    idat_crc = zlib.crc32(b"IDAT" + comprimido)
    idat = struct.pack(">I", len(comprimido)) + b"IDAT" + comprimido + struct.pack(">I", idat_crc)

    iend_crc = zlib.crc32(b"IEND")
    iend = struct.pack(">I", 0) + b"IEND" + struct.pack(">I", iend_crc)
    return header + ihdr + idat + iend


class CanvasPNG:
    """Lienzo grafico 2D en memoria para trazado de primitivas geometricas y texto bitmap."""

    def __init__(self, ancho=640, alto=420, color_fondo=(250, 250, 252)):
        self.ancho = ancho
        self.alto = alto
        self.pixeles = [[color_fondo for _ in range(ancho)] for _ in range(alto)]

    def set_pixel(self, x, y, color):
        if 0 <= x < self.ancho and 0 <= y < self.alto:
            self.pixeles[y][x] = color

    def rectangulo(self, x1, y1, x2, y2, color):
        xa, xb = max(0, min(x1, x2)), min(self.ancho - 1, max(x1, x2))
        ya, yb = max(0, min(y1, y2)), min(self.alto - 1, max(y1, y2))
        for y in range(ya, yb + 1):
            for x in range(xa, xb + 1):
                self.pixeles[y][x] = color

    def linea(self, x0, y0, x1, y1, color):
        """Algoritmo de Bresenham para trazar lineas de ejes y curvas."""
        dx = abs(x1 - x0)
        dy = -abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx + dy
        while True:
            self.set_pixel(x0, y0, color)
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                x0 += sx
            if e2 <= dx:
                err += dx
                y0 += sy

    def linea_punteada(self, x0, y0, x1, y1, color=(225, 225, 230), paso=5):
        """Dibuja una linea de referencia horizontal punteada."""
        xa, xb = min(x0, x1), max(x0, x1)
        for x in range(xa, xb + 1):
            if (x // paso) % 2 == 0:
                self.set_pixel(x, y0, color)

    def circulo(self, cx, cy, radio, color):
        for y in range(cy - radio, cy + radio + 1):
            for x in range(cx - radio, cx + radio + 1):
                if (x - cx) ** 2 + (y - cy) ** 2 <= radio ** 2:
                    self.set_pixel(x, y, color)

    def texto(self, x, y, txt, color=(40, 40, 40), escala=1):
        """Dibuja texto usando la tipografia bitmap 5x7 pura."""
        cur_x = x
        for char in str(txt):
            patron = FONT_5X7.get(char, FONT_5X7.get("?", [0, 0, 0, 0, 0]))
            for col_idx, col_bits in enumerate(patron):
                for row_idx in range(8):
                    if col_bits & (1 << row_idx):
                        if escala == 1:
                            self.set_pixel(cur_x + col_idx, y + row_idx, color)
                        else:
                            for dx in range(escala):
                                for dy in range(escala):
                                    self.set_pixel(
                                        cur_x + col_idx * escala + dx,
                                        y + row_idx * escala + dy,
                                        color,
                                    )
            cur_x += 6 * escala

    def texto_centrado(self, y, txt, color=(30, 30, 40), escala=2):
        """Centra horizontalmente una linea de texto en el lienzo."""
        ancho_txt = len(str(txt)) * 6 * escala
        x = max(10, (self.ancho - ancho_txt) // 2)
        self.texto(x, y, txt, color, escala=escala)

    def guardar(self, ruta):
        dir_padre = os.path.dirname(ruta)
        if dir_padre:
            os.makedirs(dir_padre, exist_ok=True)
        datos_png = _empaquetar_png(self.ancho, self.alto, self.pixeles)
        with open(ruta, "wb") as f:
            f.write(datos_png)


def _obtener_rgb(nombre_color):
    colores = {
        "azul": (41, 128, 185),
        "royalblue": (41, 128, 185),
        "rojo": (231, 76, 60),
        "crimson": (231, 76, 60),
        "verde": (39, 174, 96),
        "seagreen": (39, 174, 96),
        "naranja": (230, 126, 34),
        "darkorange": (230, 126, 34),
        "morado": (142, 68, 173),
    }
    return colores.get(str(nombre_color).lower(), (52, 73, 94))


def _formatear_numero(val):
    """Retorna representacion limpia de un flotante o entero."""
    try:
        f = float(val)
        if f.is_integer():
            return str(int(f))
        return f"{f:.1f}"
    except (ValueError, TypeError):
        return str(val)


def renderizar_pizarra_nativa(tipo, filas, config):
    """
    Renderiza el grafico de forma dual:
    1. Grafico en consola en caracteres ASCII.
    2. Archivo fisico .png mediante CanvasPNG nativo con texto bitmap completo.
    """
    eje_x = config.get("eje_x", "").strip("'\"")
    eje_y = config.get("eje_y", "").strip("'\"")
    titulo = config.get("titulo", f"Pizarra {tipo.capitalize()}").strip("'\"")
    color_nombre = config.get("color", "azul").strip("'\"")
    salida = config.get("guardar", f"salidas/pizarra_{tipo}.png").strip("'\"")
    color_rgb = _obtener_rgb(color_nombre)

    # 1. RENDERIZADO EN CONSOLA (ASCII)
    print(f"\n\033[1;36m┌────────────────────────────────────────────────────────┐\033[0m")
    print(f"\033[1;36m│ [Pizarra {tipo}] {titulo[:44]:<44} │\033[0m")
    print(f"\033[1;36m└────────────────────────────────────────────────────────┘\033[0m")

    canvas = CanvasPNG(ancho=640, alto=420)

    # Titulo principal en el PNG (escala 2x, centrado)
    canvas.texto_centrado(12, titulo, (25, 25, 35), escala=2)

    # Marco interior y area de graficacion
    x_orig = 80
    x_fin = 590
    y_top = 48
    y_base = 330

    canvas.rectangulo(x_orig - 25, y_top - 5, x_fin + 20, y_base + 65, (255, 255, 255))
    canvas.linea(x_orig, y_base, x_fin, y_base, (50, 50, 50))  # Eje X
    canvas.linea(x_orig, y_top, x_orig, y_base, (50, 50, 50))  # Eje Y

    # Etiqueta vertical (eje_y) en parte superior izquierda
    if eje_y:
        canvas.texto(x_orig - 10, y_top - 12, eje_y, (100, 100, 110), escala=1)

    # Etiqueta horizontal (eje_x) en parte inferior central
    if eje_x:
        canvas.texto(int((x_orig + x_fin) / 2) - len(eje_x) * 3, y_base + 45, eje_x, (100, 100, 110), escala=1)

    if tipo == "barras":
        etiquetas = [str(f.get(eje_x, f"Item {i+1}")) for i, f in enumerate(filas)]
        valores = [float(f.get(eje_y, 0)) for f in filas]
        max_v = max(valores) if valores and max(valores) > 0 else 1.0

        for etq, val in zip(etiquetas, valores):
            long_barra = int((val / max_v) * 28)
            barra_ascii = "█" * long_barra
            print(f"  {etq:>14} │ {barra_ascii} {val}")

        # Marcas y valores de referencia en el eje Y
        pasos_y = [0.0, 0.25, 0.5, 0.75, 1.0]
        for frac in pasos_y:
            y_tick = int(y_base - (frac * (y_base - y_top - 20)))
            val_tick = _formatear_numero(frac * max_v)
            canvas.linea(x_orig - 4, y_tick, x_orig, y_tick, (70, 70, 70))
            if frac > 0:
                canvas.linea_punteada(x_orig + 1, y_tick, x_fin, y_tick, (230, 230, 235))
            canvas.texto(x_orig - 8 - len(val_tick) * 6, y_tick - 4, val_tick, (90, 90, 90), escala=1)

        # Trazado de barras con texto en PNG
        n = max(1, len(valores))
        paso = int((x_fin - x_orig - 20) / n)
        ancho_barra = min(55, paso - 16)

        for i, (etq, val) in enumerate(zip(etiquetas, valores)):
            altura = int((val / max_v) * (y_base - y_top - 20))
            x0 = x_orig + 18 + (i * paso)
            y0 = y_base - altura
            # Barra
            canvas.rectangulo(x0, y0, x0 + ancho_barra, y_base - 1, color_rgb)

            # Valor numerico sobre la barra
            val_str = _formatear_numero(val)
            x_val = x0 + max(0, (ancho_barra - len(val_str) * 6) // 2)
            canvas.texto(x_val, max(y_top, y0 - 11), val_str, (30, 30, 30), escala=1)

            # Etiqueta de categoria bajo el eje X
            lbl = etq[:10]
            x_lbl = x0 + max(0, (ancho_barra - len(lbl) * 6) // 2)
            canvas.texto(x_lbl, y_base + 8, lbl, (50, 50, 60), escala=1)

    elif tipo == "dispersion":
        vx = [float(f.get(eje_x, 0)) for f in filas]
        vy = [float(f.get(eje_y, 0)) for f in filas]
        min_x, max_x = (min(vx), max(vx)) if vx else (0, 1)
        min_y, max_y = (min(vy), max(vy)) if vy else (0, 1)
        rango_x = (max_x - min_x) if max_x != min_x else 1.0
        rango_y = (max_y - min_y) if max_y != min_y else 1.0

        print(f"  Puntos proyectados (Total: {len(vx)} registros):")
        for i in range(min(5, len(vx))):
            print(f"    • ({eje_x}: {vx[i]}, {eje_y}: {vy[i]})")
        if len(vx) > 5:
            print(f"    ... [{len(vx) - 5} puntos adicionales procesados]")

        # Marcas y valores de referencia en el eje Y
        for frac in [0.0, 0.5, 1.0]:
            y_tick = int(y_base - (frac * (y_base - y_top - 20)))
            val_y = _formatear_numero(min_y + frac * rango_y)
            canvas.linea(x_orig - 4, y_tick, x_orig, y_tick, (70, 70, 70))
            if frac > 0:
                canvas.linea_punteada(x_orig + 1, y_tick, x_fin, y_tick, (230, 230, 235))
            canvas.texto(x_orig - 8 - len(val_y) * 6, y_tick - 4, val_y, (90, 90, 90), escala=1)

        # Marcas y valores de referencia en el eje X
        for frac in [0.0, 0.5, 1.0]:
            x_tick = int(x_orig + (frac * (x_fin - x_orig - 20)))
            val_x = _formatear_numero(min_x + frac * rango_x)
            canvas.linea(x_tick, y_base, x_tick, y_base + 4, (70, 70, 70))
            canvas.texto(x_tick - (len(val_x) * 3), y_base + 8, val_x, (90, 90, 90), escala=1)

        # Trazado de puntos en PNG
        for x, y in zip(vx, vy):
            px = int(x_orig + ((x - min_x) / rango_x) * (x_fin - x_orig - 20))
            py = int(y_base - ((y - min_y) / rango_y) * (y_base - y_top - 20))
            canvas.circulo(px, py, 4, color_rgb)
            canvas.circulo(px, py, 1, (255, 255, 255))

    elif tipo == "histograma":
        col = eje_x if eje_x else eje_y
        vals = [float(f.get(col, 0)) for f in filas]
        min_v, max_v = (min(vals), max(vals)) if vals else (0, 1)
        bins = 5
        ancho_bin = (max_v - min_v) / bins if max_v != min_v else 1.0
        conteos = [0] * bins

        for v in vals:
            idx = int((v - min_v) / ancho_bin)
            if idx >= bins:
                idx = bins - 1
            conteos[idx] += 1

        max_c = max(conteos) if conteos and max(conteos) > 0 else 1
        for b in range(bins):
            r0 = min_v + b * ancho_bin
            r1 = r0 + ancho_bin
            barra_ascii = "▓" * int((conteos[b] / max_c) * 25)
            print(f"  [{r0:>5.1f} - {r1:>5.1f}] │ {barra_ascii} ({conteos[b]})")

        # Marcas y valores de referencia en eje Y (frecuencia)
        for frac in [0.0, 0.5, 1.0]:
            y_tick = int(y_base - (frac * (y_base - y_top - 20)))
            val_c = str(int(round(frac * max_c)))
            canvas.linea(x_orig - 4, y_tick, x_orig, y_tick, (70, 70, 70))
            if frac > 0:
                canvas.linea_punteada(x_orig + 1, y_tick, x_fin, y_tick, (230, 230, 235))
            canvas.texto(x_orig - 8 - len(val_c) * 6, y_tick - 4, val_c, (90, 90, 90), escala=1)

        # Trazado de bins en PNG
        paso = int((x_fin - x_orig - 20) / bins)
        for b in range(bins):
            altura = int((conteos[b] / max_c) * (y_base - y_top - 20))
            x0 = x_orig + 10 + (b * paso)
            y0 = y_base - altura
            canvas.rectangulo(x0, y0, x0 + paso - 8, y_base - 1, color_rgb)

            # Conteo de frecuencia sobre cada barra
            cnt_str = str(conteos[b])
            canvas.texto(x0 + max(0, (paso - 8 - len(cnt_str) * 6) // 2), max(y_top, y0 - 11), cnt_str, (30, 30, 30), escala=1)

            # Rango bajo cada barra
            r0 = min_v + b * ancho_bin
            r1 = r0 + ancho_bin
            r_str = f"{int(r0)}-{int(r1)}"
            canvas.texto(x0 + max(0, (paso - 8 - len(r_str) * 6) // 2), y_base + 8, r_str, (60, 60, 70), escala=1)

    elif tipo in ("lineas", "caja"):
        etiquetas = [str(f.get(eje_x, f"P{i+1}")) for i, f in enumerate(filas)]
        valores = [float(f.get(eje_y, 0)) for f in filas]
        min_v = min(valores) if valores else 0.0
        max_v = max(valores) if valores else 1.0
        base_v = 0.0 if min_v >= 0.0 else min_v
        rango_v = (max_v - base_v) if max_v != base_v else 1.0

        for etq, val in zip(etiquetas, valores):
            long_p = max(0, int(((val - base_v) / rango_v) * 25))
            punto = "─" * long_p + "●"
            print(f"  {etq:>14} │ {punto} {val}")

        # Marcas y valores de referencia en el eje Y
        for frac in [0.0, 0.25, 0.5, 0.75, 1.0]:
            y_tick = int(y_base - (frac * (y_base - y_top - 20)))
            val_tick = _formatear_numero(base_v + frac * rango_v)
            canvas.linea(x_orig - 4, y_tick, x_orig, y_tick, (70, 70, 70))
            if frac > 0:
                canvas.linea_punteada(x_orig + 1, y_tick, x_fin, y_tick, (230, 230, 235))
            canvas.texto(x_orig - 8 - len(val_tick) * 6, y_tick - 4, val_tick, (90, 90, 90), escala=1)

        # Trazado de puntos y lineas en PNG
        puntos = []
        n = max(1, len(valores))
        paso = int((x_fin - x_orig - 40) / max(1, n - 1)) if n > 1 else int((x_fin - x_orig) / 2)

        for i, (etq, val) in enumerate(zip(etiquetas, valores)):
            px = x_orig + 20 + i * paso
            py = int(y_base - ((val - base_v) / rango_v) * (y_base - y_top - 20))
            puntos.append((px, py))

            # Circulo del dato
            canvas.circulo(px, py, 4, (40, 40, 40))
            canvas.circulo(px, py, 2, color_rgb)

            # Valor numerico sobre el punto
            val_str = _formatear_numero(val)
            canvas.texto(px - len(val_str) * 3, py - 12, val_str, (30, 30, 30), escala=1)

            # Etiqueta de la entidad (nombre abreviado si es largo) debajo del eje X
            partes = etq.split()
            lbl = partes[-1] if len(partes) > 1 and len(etq) > 9 else etq[:9]
            canvas.texto(px - len(lbl) * 3, y_base + 8 + (12 if (i % 2 == 1 and n > 6) else 0), lbl, (60, 60, 70), escala=1)

        # Lineas de conexion
        for i in range(len(puntos) - 1):
            canvas.linea(puntos[i][0], puntos[i][1], puntos[i + 1][0], puntos[i + 1][1], color_rgb)

    # 2. GUARDAR ARCHIVO PNG FISICO
    canvas.guardar(salida)
    print(f"Pizarra '{tipo}' guardada con exito: {salida}\n")
