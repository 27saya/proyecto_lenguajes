#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador de la Guía Integral de Estudio y Sustentación - FASE FINAL (3/3)
Proyecto DSL DaZe (.dz) - Lenguaje de Dominio Específico para Analítica Deportiva
Universidad Sergio Arboleda - Lenguajes de Programación y Traducción
Docente: Joaquín F. Sánchez
"""

import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle


class NumberedCanvas(canvas.Canvas):
    """Canvas de dos pasadas para calcular dinámicamente el número total de páginas y encabezados/pies."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, total_pages):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#718096"))

        # Encabezado (a partir de página 2)
        if self._pageNumber > 1:
            self.drawString(45, 755, "DaZe DSL — Guía de Estudio y Sustentación Final (Fase 3)")
            self.drawRightString(567, 755, "Lenguajes de Programación y Traducción | U. Sergio Arboleda")
            self.setStrokeColor(colors.HexColor("#CBD5E0"))
            self.setLineWidth(0.75)
            self.line(45, 747, 567, 747)

        # Pie de página (todas las páginas)
        self.setStrokeColor(colors.HexColor("#CBD5E0"))
        self.setLineWidth(0.75)
        self.line(45, 42, 567, 42)

        self.drawString(45, 30, "CC & IA — Repositorio Oficial: github.com/27saya/proyecto_lenguajes")
        page_str = f"Página {self._pageNumber} de {total_pages}"
        self.drawRightString(567, 30, page_str)
        self.restoreState()


def crear_guia_estudio_pdf(ruta_salida: str):
    # Márgenes de 45 pt -> Ancho disponible = 612 - 90 = 522 pt
    doc = SimpleDocTemplate(
        ruta_salida,
        pagesize=letter,
        leftMargin=45,
        rightMargin=45,
        topMargin=50,
        bottomMargin=50,
    )

    styles = getSampleStyleSheet()

    # Colores institucionales y de diseño
    c_primary = colors.HexColor("#1A365D")    # Azul institucional oscuro
    c_secondary = colors.HexColor("#2B6CB0")  # Azul medio
    c_accent = colors.HexColor("#9B2C2C")     # Rojo acento académico
    c_dark = colors.HexColor("#2D3748")       # Texto principal
    c_light = colors.HexColor("#F7FAFC")      # Fondo claro
    c_border = colors.HexColor("#CBD5E0")     # Borde suave
    c_callout_bg = colors.HexColor("#EBF8FF") # Fondo de llamada
    c_callout_border = colors.HexColor("#3182CE")

    title_style = ParagraphStyle(
        "DocTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=18,
        leading=22,
        textColor=c_primary,
        spaceAfter=3,
    )

    subtitle_style = ParagraphStyle(
        "DocSubtitle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=10.5,
        leading=14,
        textColor=c_secondary,
        spaceAfter=10,
    )

    h1_style = ParagraphStyle(
        "Heading1_Custom",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=12,
        leading=16,
        textColor=c_primary,
        spaceBefore=12,
        spaceAfter=5,
        keepWithNext=True,
    )

    h2_style = ParagraphStyle(
        "Heading2_Custom",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=9.5,
        leading=13,
        textColor=c_secondary,
        spaceBefore=6,
        spaceAfter=3,
        keepWithNext=True,
    )

    body_style = ParagraphStyle(
        "Body_Custom",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8.5,
        leading=12,
        textColor=c_dark,
        spaceAfter=5,
    )

    bullet_style = ParagraphStyle(
        "Bullet_Custom",
        parent=body_style,
        leftIndent=12,
        firstLineIndent=-8,
        spaceAfter=2.5,
    )

    code_style = ParagraphStyle(
        "Code_Custom",
        parent=styles["Normal"],
        fontName="Courier",
        fontSize=7.5,
        leading=9.5,
        textColor=colors.HexColor("#1A202C"),
    )

    callout_style = ParagraphStyle(
        "Callout_Custom",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8,
        leading=11.5,
        textColor=colors.HexColor("#2C5282"),
    )

    question_title_style = ParagraphStyle(
        "QuestionTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=9,
        leading=12,
        textColor=c_accent,
        spaceBefore=4,
        spaceAfter=2,
        keepWithNext=True,
    )

    story = []

    # -------------------------------------------------------------
    # PORTADA Y FICHA TÉCNICA
    # -------------------------------------------------------------
    story.append(Paragraph("GUÍA INTEGRAL DE ESTUDIO Y SUSTENTACIÓN — FASE FINAL (3/3)", title_style))
    story.append(Paragraph("<b>Proyecto DSL DaZe (.dz)</b> — Lenguaje de Dominio Específico para Analítica Deportiva y Ciencia de Datos", subtitle_style))

    ficha_data = [
        [
            Paragraph("<b>Asignatura:</b> Lenguajes de Programación y Traducción", body_style),
            Paragraph("<b>Docente:</b> Joaquín F. Sánchez", body_style)
        ],
        [
            Paragraph("<b>Programa:</b> Ciencias de la Computación e Inteligencia Artificial", body_style),
            Paragraph("<b>Institución:</b> Universidad Sergio Arboleda", body_style)
        ],
        [
            Paragraph("<b>Estudiante / Repositorio:</b> 27saya (github.com/27saya/proyecto_lenguajes)", body_style),
            Paragraph("<b>Entrega:</b> Tercera y última fase (Corte 3 - Producto final)", body_style)
        ],
        [
            Paragraph("<b>Front-End:</b> ANTLR4 (Lexer + Parser LL(*))", body_style),
            Paragraph("<b>Back-End:</b> Python 3 (Visitor, Core Racoons, CanvasPNG, ML Nativo)", body_style)
        ]
    ]
    t_ficha = Table(ficha_data, colWidths=[261, 261])
    t_ficha.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F7FAFC")),
        ('BOX', (0,0), (-1,-1), 1, c_border),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 7),
        ('RIGHTPADDING', (0,0), (-1,-1), 7),
    ]))
    story.append(t_ficha)
    story.append(Spacer(1, 7))

    # Caja de propósito y estrategia de sustentación
    intro_box = [
        [Paragraph(
            "<b>Estrategia recomendada para la sustentación final:</b><br/>"
            "El profesor Joaquín F. Sánchez evaluará la coherencia global entre el diseño sintáctico, la formalidad de la gramática, "
            "la robustez semántica y la capacidad del compilador/intérprete para ejecutar un flujo completo de ciencia de datos sin dependencias pesadas. "
            "Estructura tu intervención en cuatro momentos clave: "
            "<b>(1) Dominio y gramática:</b> Justifica el vocabulario deportivo ergonómico y el orden de precedencia. "
            "<b>(2) Arquitectura interna:</b> Explica por qué el patrón Visitor y cómo la inyección de contexto de fila resuelve las operaciones en tubería (<code>|&gt;</code>). "
            "<b>(3) Autonomía algorítmica:</b> Destaca que el motor tabular (<i>racoons</i>), los modelos de Machine Learning (regresión y K-Means) y el renderizador de gráficos (<i>CanvasPNG</i> con tipografía bitmap nativa) fueron desarrollados en Python puro sin pandas, NumPy ni Matplotlib. "
            "<b>(4) Demostración en vivo:</b> Ejecuta <code>./daze caso_estudio.dz</code> mostrando la salida tabular, los 4 archivos PNG generados con títulos y marcas graduadas, y la suite de 49 pruebas unitarias.",
            callout_style
        )]
    ]
    t_intro = Table(intro_box, colWidths=[522])
    t_intro.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_callout_bg),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#BEE3F8")),
        ('LINELEFT', (0,0), (0,0), 3.5, c_callout_border),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_intro)
    story.append(Spacer(1, 8))

    # -------------------------------------------------------------
    # MÓDULO 1: ARQUITECTURA INTEGRAL Y PIPELINE DEL COMPILADOR
    # -------------------------------------------------------------
    story.append(Paragraph("Módulo 1: Arquitectura Integral del DSL y Ciclo de Ejecución", h1_style))
    story.append(Paragraph(
        "DaZe es un lenguaje de dominio específico (DSL) declarativo, modular y reproducible diseñado para analistas de rendimiento, "
        "cuerpos técnicos y directores deportivos. Su arquitectura desacopla estrictamente cada una de las fases del proceso de traducción y ejecución:",
        body_style
    ))

    comp_data = [
        [Paragraph("<b>Capa Arquitectural</b>", body_style), Paragraph("<b>Módulo / Archivos</b>", body_style), Paragraph("<b>Función Técnica y Algorítmica</b>", body_style)],
        [
            Paragraph("<b>Front-End Léxico</b>", body_style),
            Paragraph("<code>grammar/DaZeLexer.g4</code>", code_style),
            Paragraph("Convierte el flujo de caracteres del archivo <code>.dz</code> en un flujo estructurado de tokens sin guiones bajos (ej. <code>convocar</code>, <code>descartar</code>, <code>enjuego</code>).", body_style)
        ],
        [
            Paragraph("<b>Front-End Sintáctico</b>", body_style),
            Paragraph("<code>grammar/DaZeParser.g4</code>", code_style),
            Paragraph("Analizador sintáctico descendente LL(*) generado con ANTLR4. Construye el árbol de sintaxis abstracta (AST) y resuelve precedencias formales.", body_style)
        ],
        [
            Paragraph("<b>Tabla de Símbolos</b>", body_style),
            Paragraph("<code>src/semantic/tabla_simbolos.py</code>", code_style),
            Paragraph("Estructura jerárquica de ámbitos (Scope Tree) para variables escalares, esquemas de columnas en tablas deportivas y firmas de funciones (tácticas).", body_style)
        ],
        [
            Paragraph("<b>Intérprete Semántico</b>", body_style),
            Paragraph("<code>src/semantic/visitor.py</code>", code_style),
            Paragraph("Implementación del patrón Visitor (<code>DaZeSemanticVisitor</code>). Evalúa expresiones, administra bucles, controla el flujo condicional e inyecta el contexto de fila dinámico.", body_style)
        ],
        [
            Paragraph("<b>Motor Tabular Propio</b>", body_style),
            Paragraph("<code>src/core/racoons.py</code><br/><code>src/core/estadistica.py</code>", code_style),
            Paragraph("Estructuras de datos bidimensionales en Python puro (<code>Tabla</code> y <code>GrupoTabla</code>). Implementa proyección, filtrado, ordenamiento, agrupación hash y cálculo estadístico sin pandas.", body_style)
        ],
        [
            Paragraph("<b>Estructuras Lineales</b>", body_style),
            Paragraph("<code>src/core/estructuras.py</code>", code_style),
            Paragraph("Implementación nativa de pilas (LIFO) y colas (FIFO) integradas al lenguaje para el seguimiento cronológico y táctico de jugadores.", body_style)
        ],
        [
            Paragraph("<b>Machine Learning Nativo</b>", body_style),
            Paragraph("<code>src/core/modelos.py</code><br/><code>src/core/matematica.py</code>", code_style),
            Paragraph("Algoritmos de Regresión Lineal por Mínimos Cuadrados Ordinarios (MCO), correlación de Pearson, coeficiente $R^2$ y agrupamiento no supervisado K-Means en 2D sin bibliotecas externas.", body_style)
        ],
        [
            Paragraph("<b>Renderizador Gráfico</b>", body_style),
            Paragraph("<code>src/core/visualizador.py</code>", code_style),
            Paragraph("Motor de renderizado binario PNG nativo (<code>CanvasPNG</code> con compresión zlib) y tipografía de mapa de bits 5x7 ASCII pura para títulos, ejes, cuadrículas y etiquetas numéricas.", body_style)
        ],
        [
            Paragraph("<b>CLI y Diagnóstico</b>", body_style),
            Paragraph("<code>src/cli.py</code><br/><code>daze</code> (ejecutable)", code_style),
            Paragraph("Interfaz de línea de comandos con modo interactivo (REPL), ejecución por lotes y captura unificada de errores léxicos, sintácticos y semánticos con línea y columna.", body_style)
        ]
    ]
    t_comp = Table(comp_data, colWidths=[105, 135, 282])
    t_comp.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#2B6CB0")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F7FAFC")]),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_comp)
    story.append(Spacer(1, 8))

    # -------------------------------------------------------------
    # MÓDULO 2: FRONT-END LÉXICO Y SINTÁCTICO
    # -------------------------------------------------------------
    story.append(Paragraph("Módulo 2: Especificación Léxica, Gramática EBNF y Precedencia en ANTLR4", h1_style))
    story.append(Paragraph(
        "El front-end fue formalizado en notación BNF/EBNF y compilado con ANTLR4 generando analizadores en Python 3:",
        body_style
    ))
    story.append(Paragraph("• <b>Léxico Deportivo y Ergonómico:</b> Se eliminaron guiones bajos de todos los identificadores del sistema: <code>desviar</code> (desviación estándar), <code>sanear</code> (imputación de nulos), <code>depurar</code> (deduplicación), <code>archivar</code> (exportar CSV), <code>proyectar</code> (mostrar en consola) y <code>pizarra</code> (graficar).", bullet_style))
    story.append(Paragraph("• <b>Jerarquía y Precedencia de Operadores:</b> ANTLR4 resuelve la precedencia según el orden vertical de las alternativas en la regla <code>expr</code>. El orden formal implementado es: Potencia (<code>^</code>, asociatividad por derecha con <code>&lt;assoc=right&gt;</code>) → Operadores unarios (<code>+</code>, <code>-</code>, <code>no</code>) → Multiplicativos (<code>*</code>, <code>/</code>, <code>%</code>) → Aditivos (<code>+</code>, <code>-</code>) → Relacionales (<code>&gt;</code>, <code>&lt;</code>, <code>&gt;=</code>, <code>&lt;=</code>) → Igualdad (<code>==</code>, <code>!=</code>) → Lógicos conjuntivos (<code>y</code>) → Lógicos disyuntivos (<code>o</code>).", bullet_style))
    story.append(Paragraph("• <b>Resolución de Ambigüedades Sintácticas:</b> En la regla <code>sentencia</code>, instrucciones especializadas como <code>guardar_stmt</code> (<code>archivar</code>), <code>mostrar_stmt</code> (<code>proyectar</code>) y <code>graficar_stmt</code> (<code>pizarra</code>) se declararon <b>antes</b> de <code>llamada_stmt</code>. Esto evita que el analizador descendente consuma estas palabras clave como identificadores de tácticas genéricas.", bullet_style))
    story.append(Paragraph("• <b>Manejo de Errores Sintácticos:</b> Se integró <code>DaZeErrorListener</code> para interceptar discrepancias léxicas o sintácticas antes de la fase de ejecución, emitiendo mensajes de diagnóstico en español con ubicación precisa.", bullet_style))
    story.append(Spacer(1, 8))

    # -------------------------------------------------------------
    # MÓDULO 3: MOTOR TABULAR PROPIO (RACOONS Y ESTADÍSTICA)
    # -------------------------------------------------------------
    story.append(Paragraph("Módulo 3: Motor Propio de Datos (Librerías Racoons y Estadística)", h1_style))
    story.append(Paragraph(
        "Cumpliendo el principio de autonomía algorítmica, <b>no se utilizaron dependencias pesadas de terceros (como pandas o numpy)</b>. "
        "En su lugar, se desarrollaron módulos nativos con complejidades óptimas:",
        body_style
    ))

    core_table = [
        [Paragraph("<b>Componente</b>", body_style), Paragraph("<b>Estructura Interna</b>", body_style), Paragraph("<b>Operaciones y Algoritmos Implementados</b>", body_style)],
        [
            Paragraph("<b><code>Tabla</code> (racoons)</b>", body_style),
            Paragraph("<code>columnas: List[str]</code><br/><code>filas: List[Dict[str, Any]]</code>", code_style),
            Paragraph(
                "• <b><code>csvread / csvsave</code>:</b> Parser propio con inferencia de tipos (enteros, flotantes, booleanos y nulos).<br/>"
                "• <b><code>convocar</code>:</b> Proyección de columnas en tiempo $O(N \\times K)$.<br/>"
                "• <b><code>descartar</code>:</b> Filtrado de registros en tiempo lineal $O(N)$.<br/>"
                "• <b><code>contratar</code>:</b> Creación de columnas evaluadas dinámicamente.<br/>"
                "• <b><code>clasificar</code>:</b> Ordenamiento con clave personalizada y reversibilidad.<br/>"
                "• <b><code>sanear</code> y <code>depurar</code>:</b> Imputación de nulos y eliminación de duplicados.<br/>"
                "• <b><code>top</code>:</b> Extracción acotada de las primeras $K$ filas.",
                body_style
            )
        ],
        [
            Paragraph("<b><code>GrupoTabla</code> (Agrupación)</b>", body_style),
            Paragraph("<code>grupos: Dict[Tuple, List[Dict]]</code>", code_style),
            Paragraph(
                "• <b><code>alinear(columnas)</code>:</b> Particiona los registros en una tabla hash indexada por tuplas de valores únicos de las columnas clave.<br/>"
                "• <b><code>balance(agregaciones)</code>:</b> Aplica funciones descriptivas sobre cada partición y consolida una nueva <code>Tabla</code> en $O(N)$.",
                body_style
            )
        ],
        [
            Paragraph("<b><code>estadistica.py</code></b>", body_style),
            Paragraph("Algoritmos numéricos puros", code_style),
            Paragraph(
                "• <b><code>suma</code> / <code>contar</code>:</b> Acumuladores con omisión segura de valores nulos.<br/>"
                "• <b><code>media</code>:</b> Promedio aritmético $\\bar{x} = \\frac{1}{n}\\sum x_i$.<br/>"
                "• <b><code>mediana</code>:</b> Ordenamiento y selección del centroide estadístico.<br/>"
                "• <b><code>desviar</code>:</b> Desviación estándar muestral con divisor $(n-1)$.<br/>"
                "• <b><code>minimo</code> / <code>maximo</code>:</b> Detección de extremos en series numéricas.",
                body_style
            )
        ]
    ]
    t_core = Table(core_table, colWidths=[105, 140, 277])
    t_core.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#2B6CB0")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F7FAFC")]),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_core)
    story.append(Spacer(1, 8))

    # -------------------------------------------------------------
    # MÓDULO 4: TABLA DE SÍMBOLOS Y EVALUACIÓN SEMÁNTICA
    # -------------------------------------------------------------
    story.append(Paragraph("Módulo 4: Sistema de Tipos, Ámbitos y Tabla de Símbolos Jerárquica", h1_style))
    story.append(Paragraph(
        "La tabla de símbolos garantiza la consistencia del programa antes y durante la ejecución:",
        body_style
    ))
    story.append(Paragraph("• <b>Árbol de Ámbitos (Scope Tree):</b> Cada bloque de código delimitado o llamada a función crea un ámbito local conectado a su ámbito padre. Al buscar una variable o táctica, el evaluador asciende por la cadena estática de padres hasta el entorno global.", bullet_style))
    story.append(Paragraph("• <b>Símbolos con Esquemas de Columnas:</b> Cuando un identificador contiene una <code>Tabla</code>, el símbolo asocia la lista de columnas válidas. Esto permite validar semánticamente si una columna existe antes de proyectar, filtrar o graficar.", bullet_style))
    story.append(Paragraph("• <b>Comprobaciones Semánticas Estrictas:</b> Se detectan e interrumpen limpiamente: (1) uso de identificadores no declarados, (2) columnas inexistentes en pipelines, (3) incompatibilidad de tipos en operaciones aritméticas (ej. sumar número con texto), y (4) divisiones por cero.", bullet_style))
    story.append(Paragraph("• <b>Aislamiento en Tácticas y Señal de Retorno:</b> Las tácticas ejecutan sus parámetros en un nuevo ámbito local. La instrucción <code>resultado expr;</code> lanza una excepción controlada <code>ReturnSignal(valor)</code> que desenrolla la pila de llamadas hasta el llamador de forma inmediata y limpia.", bullet_style))
    story.append(Spacer(1, 8))

    # -------------------------------------------------------------
    # MÓDULO 5: EL INTÉRPRETE VISITOR Y CONTEXTO DE FILA
    # -------------------------------------------------------------
    story.append(Paragraph("Módulo 5: Intérprete Semántico Basado en el Patrón Visitor", h1_style))
    story.append(Paragraph(
        "<code>DaZeSemanticVisitor</code> hereda de <code>DaZeParserVisitor</code> y comanda el recorrido del árbol de sintaxis abstracta (AST):",
        body_style
    ))

    visitor_info = [
        [Paragraph("<b>Decisión de Diseño</b>", body_style), Paragraph("<b>Mecanismo Técnico en DaZe</b>", body_style)],
        [
            Paragraph("<b>¿Por qué Visitor y no Listener?</b>", body_style),
            Paragraph("El <b>Visitor</b> permite controlar cuándo y cuántas veces visitar los nodos hijos y retornar valores directamente. El <b>Listener</b> realiza un recorrido pasivo y automático (DFS ciego) sin retorno de valores, lo cual impide evaluar expresiones compuestas y saltar bloques en condicionales y bucles.", body_style)
        ],
        [
            Paragraph("<b>Inyección de Contexto de Fila</b>", body_style),
            Paragraph("En <code>descartar</code> y <code>contratar</code>, el Visitor itera fila por fila asignando <code>self.contexto_fila = fila</code>. Al resolver un identificador en <code>visitExprIdentificador</code>, busca primero en las columnas de la fila actual; si no existe, busca en la tabla de símbolos del programa.", body_style)
        ],
        [
            Paragraph("<b>Control de Flujo Condicional</b>", body_style),
            Paragraph("En <code>si (condicion) { ... } sino { ... }</code>, evalúa la condición booleana y solo visita las sentencias de la rama activa, evitando evaluaciones innecesarias o efectos secundarios indeseados.", body_style)
        ]
    ]
    t_vis = Table(visitor_info, colWidths=[150, 372])
    t_vis.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#2B6CB0")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F7FAFC")]),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_vis)
    story.append(Spacer(1, 8))

    # -------------------------------------------------------------
    # MÓDULO 6: ESTRUCTURAS DE DATOS LINEALES Y BUCLES (FASE 3)
    # -------------------------------------------------------------
    story.append(Paragraph("Módulo 6: Extensiones Avanzadas de Fase 3: Estructuras Lineales y Bucles", h1_style))
    story.append(Paragraph(
        "En la tercera fase se expandieron las capacidades de programación estructurada y gestión secuencial de datos:",
        body_style
    ))
    story.append(Paragraph("• <b>Estructuras Lineales Nativas:</b> Se incorporaron tipos de datos abstractos sin bibliotecas externas:<br/>"
                           "- <b><code>pila</code> (LIFO):</b> Permite <code>apilar(item)</code>, <code>desapilar()</code>, <code>cima()</code> y <code>longitud()</code>. Utilizada en analítica deportiva para retrocesos tácticos o historiales recientes de jugadas.<br/>"
                           "- <b><code>cola</code> (FIFO):</b> Permite <code>encolar(item)</code>, <code>desencolar()</code>, <code>frente()</code> y <code>longitud()</code>. Empleada para el procesamiento secuencial de turnos de entrenamiento o telemetría cronológica.", bullet_style))
    story.append(Paragraph("• <b>Bucle Condicional <code>enjuego (condicion) { ... }</code>:</b> Estructura de control iterativa tipo <i>while</i>. El Visitor evalúa dinámicamente la condición booleana y repite la visita del cuerpo de sentencias mientras permanezca verdadera.", bullet_style))
    story.append(Paragraph("• <b>Bucle Iterativo <code>ronda (variable en coleccion) { ... }</code>:</b> Estructura de control tipo <i>for-in</i>. Recorre elementos de listas o filas de una tabla, inyectando la variable de iteración en el ámbito activo durante cada ciclo.", bullet_style))
    story.append(Spacer(1, 8))

    # -------------------------------------------------------------
    # MÓDULO 7: MACHINE LEARNING Y MODELADO CIENTÍFICO NATIVO
    # -------------------------------------------------------------
    story.append(Paragraph("Módulo 7: Modelos Estadísticos y Machine Learning en Python Puro", h1_style))
    story.append(Paragraph(
        "El compilador incorpora modelos analíticos avanzados programados matemáticamente desde cero (<code>src/core/modelos.py</code> y <code>matematica.py</code>) sin NumPy ni Scikit-learn:",
        body_style
    ))

    ml_data = [
        [Paragraph("<b>Modelo / Algoritmo</b>", body_style), Paragraph("<b>Fundamento Matemático Implementado</b>", body_style), Paragraph("<b>Aplicación en DaZe</b>", body_style)],
        [
            Paragraph("<b>Regresión Lineal MCO</b>", body_style),
            Paragraph("Mínimos Cuadrados Ordinarios:<br/>"
                      "Pendiente: $m = \\frac{n\\sum xy - \\sum x \\sum y}{n\\sum x^2 - (\\sum x)^2}$<br/>"
                      "Intercepto: $b = \\bar{y} - m\\bar{x}$<br/>"
                      "Predicción: $\\hat{y} = m \\cdot x + b$", code_style),
            Paragraph("Estimación continua de variables deportivas (ej. proyección de goles esperados o fatiga muscular según minutos jugados).", body_style)
        ],
        [
            Paragraph("<b>Correlación y Bondad de Ajuste</b>", body_style),
            Paragraph("Pearson: $r = \\frac{Cov(x,y)}{\\sigma_x \\sigma_y}$<br/>"
                      "Bondad: $R^2 = r^2$ (proporción de varianza explicada).", code_style),
            Paragraph("Evaluación de la fuerza y dirección de la relación entre variables de telemetría y rendimiento ofensivo.", body_style)
        ],
        [
            Paragraph("<b>K-Means Clustering (2D)</b>", body_style),
            Paragraph("Agrupamiento no supervisado:<br/>"
                      "1. Inicialización determinista de $K$ centroides.<br/>"
                      "2. Asignación por distancia euclidiana: $d(p, c) = \\sqrt{(p_x - c_x)^2 + (p_y - c_y)^2}$.<br/>"
                      "3. Recálculo del centroide promediando coordenadas del grupo hasta convergencia.", code_style),
            Paragraph("Segmentación táctica de futbolistas en 3 perfiles (ej. titulares de alto impacto, revulsivos estratégicos y juveniles en formación).", body_style)
        ]
    ]
    t_ml = Table(ml_data, colWidths=[110, 212, 200])
    t_ml.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#2B6CB0")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F7FAFC")]),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_ml)
    story.append(Spacer(1, 8))

    # -------------------------------------------------------------
    # MÓDULO 8: MOTOR DE VISUALIZACIÓN PNG Y TIPOGRAFÍA BITMAP
    # -------------------------------------------------------------
    story.append(Paragraph("Módulo 8: Motor de Visualización PNG Nativo y Tipografía de Mapa de Bits", h1_style))
    story.append(Paragraph(
        "La generación gráfica se realiza directamente en binario puro (<code>src/core/visualizador.py</code>), "
        "creando imágenes PNG válidas sin Pillow, Matplotlib ni dependencias de sistema:",
        body_style
    ))
    story.append(Paragraph("• <b>Estructura Binaria del Archivo PNG:</b><br/>"
                           "1. <b>Firma mágica:</b> 8 bytes estándar <code>\\x89PNG\\r\\n\\x1a\\n</code>.<br/>"
                           "2. <b>Chunk IHDR:</b> Define ancho (640 px), alto (420 px), profundidad (8 bits por canal) y modo de color RGB (tipo 2).<br/>"
                           "3. <b>Filtros y Scanlines:</b> Cada fila horizontal de 640 píxeles es precedida por el byte de filtro <code>0x00</code> (filtro None).<br/>"
                           "4. <b>Chunk IDAT:</b> Comprime el flujo de píxeles RGB usando el algoritmo DEFLATE mediante <code>zlib.compress(datos, level=6)</code>.<br/>"
                           "5. <b>Chunk IEND:</b> Marca de finalización con verificación CRC32 obligatoria.", bullet_style))
    story.append(Paragraph("• <b>Tipografía Nativa de Mapa de Bits (ASCII 5x7):</b> Para asegurar que las imágenes contengan títulos, nombres de jugadores y valores numéricos claros, se embebió una matriz binaria para los 95 caracteres ASCII imprimibles. El método <code>texto(x, y, txt, color, escala)</code> rasteriza cada glifo píxel a píxel, y <code>texto_centrado(y, txt, color, escala=2)</code> centra títulos con tamaño doble.", bullet_style))
    story.append(Paragraph("• <b>Marcas de Graduación y Guías de Lectura:</b> Las pizarras incluyen 5 marcas de referencia en el eje Y (0%, 25%, 50%, 75%, 100% del valor máximo), líneas punteadas horizontales (<code>linea_punteada</code>), etiquetas de categorías en el eje X y valores numéricos exactos sobre cada barra o punto.", bullet_style))
    story.append(Paragraph("• <b>Cuatro Tipos de Pizarras Soportadas:</b><br/>"
                           "1. <code>barras</code>: Comparación de métricas categóricas con valores numéricos y nombres alineados.<br/>"
                           "2. <code>dispersion</code>: Proyección bivariada con ejes etiquetados y valores mínimos, medios y máximos.<br/>"
                           "3. <code>histograma</code>: Distribución de frecuencias con cálculo automático de intervalos (bins) y conteo sobre cada columna.<br/>"
                           "4. <code>lineas</code> (y <code>caja</code>): Tendencias de rendimiento individual y curvas de progresión.", bullet_style))
    story.append(Spacer(1, 8))

    # -------------------------------------------------------------
    # MÓDULO 9: CLI, REPL Y DIAGNÓSTICO
    # -------------------------------------------------------------
    story.append(Paragraph("Módulo 9: Interfaz de Línea de Comandos (CLI) y Entorno Interactivo (REPL)", h1_style))
    story.append(Paragraph(
        "El punto de entrada unificado <code>./daze</code> (enlazado a <code>src/cli.py</code>) detecta automáticamente el entorno virtual "
        "y ofrece una experiencia completa de desarrollo:",
        body_style
    ))
    story.append(Paragraph("• <b>Ejecución por Lotes:</b> <code>./daze caso_estudio.dz</code> procesa el programa, reporta avances y exporta resultados CSV y PNG.", bullet_style))
    story.append(Paragraph("• <b>Consola Interactiva (REPL):</b> <code>./daze --interactivo</code> (o <code>-i</code>) permite declarar variables, ejecutar tácticas y probar transformaciones en tiempo real con comandos como <code>ayuda</code>, <code>variables</code>, <code>limpiar</code> y <code>salir</code>.", bullet_style))
    story.append(Paragraph("• <b>Diagnóstico de Errores:</b> Intercepta excepciones y presenta mensajes comprensibles en español indicando el archivo, la línea y la columna exacta de cualquier fallo léxico, sintáctico o semántico.", bullet_style))
    story.append(Spacer(1, 8))

    # -------------------------------------------------------------
    # MÓDULO 10: CASO DE ESTUDIO OFICIAL Y SUITE DE PRUEBAS
    # -------------------------------------------------------------
    story.append(Paragraph("Módulo 10: Caso de Estudio Oficial (caso_estudio.dz) y Suite de Pruebas", h1_style))
    story.append(Paragraph(
        "El proyecto fue validado de forma integral mediante un caso de estudio real en analítica deportiva y una rigurosa suite de pruebas:",
        body_style
    ))
    story.append(Paragraph("• <b>Flujo en 5 Etapas del Caso de Estudio (<code>caso_estudio.dz</code>):</b><br/>"
                           "1. <b>Carga:</b> Lee <code>plantilla_temporada.csv</code> (15 futbolistas profesionales con minutos, goles, asistencias y distancia).<br/>"
                           "2. <b>Transformación:</b> Filtra jugadores aptos y calcula <code>contribucion = goles + asistencias</code> y <code>desgaste_minuto</code>.<br/>"
                           "3. <b>Agrupación:</b> Particiona por <code>posicion</code> (<code>alinear</code>) y resume con <code>balance</code> (total de goles, media de asistencias, mediana de minutos y desviación estándar), archivando en <code>salidas/resumen_posiciones.csv</code>.<br/>"
                           "4. <b>Machine Learning Puro:</b> Calcula la correlación de Pearson ($r=0.525$), la pendiente y el intercepto de regresión lineal para estimar goles esperados ($4.42$ goles a los 1000 minutos) y aplica K-Means para clasificar a los jugadores en 3 grupos tácticos.<br/>"
                           "5. <b>Visualización:</b> Renderiza y exporta 4 pizarras PNG legibles en <code>salidas/</code> con títulos, cuadrículas y etiquetas.", bullet_style))
    story.append(Paragraph("• <b>Batería de Pruebas de Regresión:</b> <b>49 pruebas unitarias y de integración pasando al 100%</b> en menos de 0.3 segundos, cubriendo lexer, parser, semántica, pipeline, estructuras de datos, ML y generación de PNG con texto bitmap.", bullet_style))
    story.append(Spacer(1, 8))

    # -------------------------------------------------------------
    # MÓDULO 11: BANCO EXHAUSTIVO DE PREGUNTAS (MOCK QUESTIONS)
    # -------------------------------------------------------------
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#CBD5E0"), spaceBefore=6, spaceAfter=10))
    story.append(Paragraph("Módulo 11: Banco Exhaustivo de Preguntas de Sustentación (Mock Questions)", h1_style))
    story.append(Paragraph("Preguntas clave que formulará el docente Joaquín F. Sánchez, con justificación conceptual y respuesta técnica modelo.", subtitle_style))

    preguntas = [
        (
            "Pregunta 1: ¿Por qué eligieron el patrón Visitor sobre el Listener para implementar la semántica y ejecución?",
            "Dominio de los patrones de recorrido de árboles en compiladores y justificación técnica.",
            "Elegimos el patrón Visitor porque nos otorga <b>control total y explícito sobre la navegación del árbol (AST)</b>. "
            "A diferencia del Listener, que es guiado ciegamente por un caminador pasivo (<i>ParseTreeWalker</i>) en recorrido DFS sin retornar valores, "
            "el Visitor permite que cada método visitante retorne el resultado de su evaluación. Esto es fundamental en DaZe para: "
            "(1) evaluar expresiones compuestas y propagar valores hacia los nodos padre; "
            "(2) controlar sentencias condicionales (<code>si</code> / <code>sino</code>) y bucles (<code>enjuego</code>, <code>ronda</code>) ejecutando selectivamente las ramas activas; "
            "y (3) evaluar subárboles de expresiones fila por fila durante las operaciones de pipeline <code>contratar</code> y <code>descartar</code>.",
            "src/semantic/visitor.py (clase DaZeSemanticVisitor)"
        ),
        (
            "Pregunta 2: ¿Cómo gestiona el DSL el ámbito léxico cuando se invoca una función deportiva (tactica)?",
            "Gestión de memoria, ciclos de vida de ámbitos y aislamiento léxico en funciones.",
            "Lo gestionamos mediante una <b>Tabla de Símbolos jerárquica con punteros a su ámbito padre</b>. "
            "Cuando se declara una <code>tactica</code>, el Visitor guarda su definición formal en la tabla global. "
            "Al ejecutarse la llamada (<code>visitLlamada_stmt</code>), el intérprete evalúa los argumentos en el ámbito del llamador y luego "
            "<b>crea un nuevo ámbito hijo</b> mediante <code>crear_ambito_hijo()</code>. En este entorno local se asocian los parámetros formales con sus valores evaluados. "
            "Cualquier variable creada dentro de la táctica vive únicamente en ese ámbito local; al concluir la ejecución o emitirse la instrucción <code>resultado expr;</code>, "
            "el puntero del ámbito activo se restaura a su padre dentro de un bloque <code>finally</code>, garantizando que el entorno global jamás sea contaminado.",
            "src/semantic/tabla_simbolos.py y src/semantic/visitor.py (_ejecutar_tactica)"
        ),
        (
            "Pregunta 3: En un pipeline como 'datos |> descartar(minutos > 0)', ¿cómo sabe el Visitor qué es 'minutos' si no es una variable global?",
            "Enlace dinámico de identificadores y mecanismo de inyección de contexto de fila.",
            "Implementamos un mecanismo de <b>inyección de contexto de fila</b>. Cuando el Visitor entra a procesar <code>descartar</code> o <code>contratar</code>, "
            "recorre secuencialmente las filas de la tabla y en cada iteración asigna el diccionario de la fila a <code>self.contexto_fila = fila</code> antes de visitar la expresión. "
            "En el método <code>visitExprIdentificador</code>, se aplica una resolución en dos niveles: primero verifica si el identificador coincide con alguna llave de <code>self.contexto_fila</code>. "
            "Si coincide, retorna inmediatamente el valor de esa columna para la fila actual. Si no, busca en la tabla de símbolos del programa. Si tampoco existe, "
            "se lanza un error semántico indicando que la columna no existe en la plantilla deportiva.",
            "src/semantic/visitor.py (visitExprIdentificador y _aplicar_descartar)"
        ),
        (
            "Pregunta 4: ¿Por qué decidieron implementar su propia librería (racoons) en lugar de usar pandas y qué estructura interna eligieron?",
            "Diseño de estructuras de datos internas, complejidad computacional y autonomía algorítmica.",
            "Decidimos crear <b>racoons</b> desde cero para tener control absoluto sobre el modelo computacional y cumplir el propósito pedagógico de comprender "
            "los algoritmos subyacentes sin depender de cajas negras externas. "
            "Internamente, representamos una <code>Tabla</code> con dos atributos: una lista de cadenas para los nombres de columnas y una lista de diccionarios para las filas (<code>List[Dict[str, Any]]</code>). "
            "Esta estructura híbrida nos ofrece acceso directo por nombre de columna en tiempo $O(1)$ por fila, flexibilidad para inferir tipos de datos durante la lectura CSV y una "
            "complejidad de $O(N)$ para filtros y transformaciones. Para la operación <code>alinear</code>, construimos la clase <code>GrupoTabla</code>, que particiona los registros "
            "en una tabla hash cuyas claves son tuplas con los valores de las columnas de agrupación.",
            "src/core/racoons.py (clases Tabla y GrupoTabla)"
        ),
        (
            "Pregunta 5: ¿Cómo resolvieron la ambigüedad en la gramática para instrucciones como 'archivar', 'proyectar' o 'pizarra'?",
            "Comprensión del análisis sintáctico descendente predictivo y resolución de conflictos de prefijo.",
            "En ANTLR4, cuando varias reglas pueden coincidir con el mismo prefijo de tokens, el parser favorece la regla declarada primero en el archivo de gramática. "
            "Inicialmente, la regla <code>llamada_stmt</code> (que reconoce <code>identificador LPAREN ... RPAREN</code>) estaba antes que <code>guardar_stmt</code>, <code>mostrar_stmt</code> y <code>graficar_stmt</code>. "
            "Como palabras como <code>archivar</code> o <code>pizarra</code> son léxicamente identificadores, el parser las absorbía erróneamente como llamadas a tácticas genéricas. "
            "La solución consistió en <b>reordenar la regla sentencia en DaZeParser.g4</b>, ubicando las instrucciones especializadas antes de la llamada a función genérica. "
            "Así, el parser comprueba primero la sintaxis específica del almacenamiento, proyección y visualización antes de considerar una llamada ordinaria.",
            "grammar/DaZeParser.g4 (regla sentencia)"
        ),
        (
            "Pregunta 6: ¿Cómo genera DaZe un archivo PNG válido en binario puro sin usar Matplotlib, Pillow ni ninguna biblioteca externa?",
            "Conocimiento de formatos binarios, especificaciones de archivos y manipulación a bajo nivel en Python.",
            "Se implementó la clase <code>CanvasPNG</code> siguiendo la especificación oficial W3C de PNG. "
            "Un archivo PNG es una secuencia binaria que inicia con una firma mágica de 8 bytes (<code>\\x89PNG\\r\\n\\x1a\\n</code>), seguida de bloques estructurados llamados <i>chunks</i>. "
            "Nuestro motor construye: (1) el chunk <code>IHDR</code> con las dimensiones (640x420) y modo de color RGB a 8 bits por canal; "
            "(2) el chunk <code>IDAT</code>, formateando cada fila con un byte de filtro <code>0x00</code> (None) seguido de los bytes RGB de cada píxel, y comprimiendo todo el flujo con el algoritmo DEFLATE estándar mediante el módulo nativo <code>zlib</code>; "
            "y (3) el chunk <code>IEND</code> de finalización. Cada chunk incluye su longitud, tipo de 4 letras, datos y un código de redundancia cíclica (CRC32).",
            "src/core/visualizador.py (clase CanvasPNG y renderizar_pizarra_nativa)"
        ),
        (
            "Pregunta 7: ¿Cómo resolvieron que las gráficas PNG tengan títulos, nombres de jugadores y valores numéricos legibles sin librerías gráficas?",
            "Ingeniería de renderizado visual y rasterización tipográfica nativa.",
            "Desarrollamos un <b>motor de tipografía de mapa de bits (5x7 ASCII)</b> dentro de <code>visualizador.py</code>. "
            "Definimos una matriz binaria para los 95 caracteres imprimibles de ASCII. El método <code>texto(x, y, txt, color, escala)</code> recorre cada carácter de la cadena, "
            "lee su patrón de bits y pinta en la matriz de píxeles los puntos correspondientes, escalando el tamaño según sea necesario. "
            "Con esto, <code>renderizar_pizarra_nativa</code>: (1) imprime el título centrado en escala 2; (2) traza marcas de graduación en el eje vertical con cuadrícula punteada; "
            "(3) escribe los nombres de jugadores, categorías o intervalos bajo el eje horizontal; y (4) plasma los valores numéricos exactos sobre cada barra o punto.",
            "src/core/visualizador.py (FONT_5X7, CanvasPNG.texto y renderizar_pizarra_nativa)"
        ),
        (
            "Pregunta 8: ¿Cómo se implementaron las estructuras lineales (pila, cola) y los bucles (enjuego, ronda) en la gramática y el Visitor?",
            "Extensibilidad gramatical y semántica para estructuras de datos y bucles.",
            "En la gramática (<code>DaZeParser.g4</code>) agregamos reglas dedicadas para declarar <code>pila</code> y <code>cola</code>, y sentencias específicas para sus métodos (<code>apilar</code>, <code>desapilar</code>, <code>encolar</code>, <code>desencolar</code>). "
            "En el Visitor, se conectaron directamente con las clases <code>Pila</code> y <code>Cola</code> implementadas en <code>src/core/estructuras.py</code>.<br/>"
            "Para los bucles: en <code>enjuego_stmt</code>, el Visitor evalúa la condición booleana en un bucle <code>while</code> interno de Python y re-visita el bloque de sentencias en cada iteración mientras la condición sea verdadera; "
            "en <code>ronda_stmt</code>, evalúa la colección iterable (lista o tabla) y en cada paso asigna el elemento actual a la variable de iteración en el ámbito activo antes de ejecutar el bloque.",
            "grammar/DaZeParser.g4, src/core/estructuras.py y src/semantic/visitor.py"
        ),
        (
            "Pregunta 9: ¿Cómo funcionan los modelos de Machine Learning (Regresión MCO y K-Means) implementados en el lenguaje?",
            "Comprensión de fundamentos matemáticos de aprendizaje automático en Python puro.",
            "Se implementaron matemáticamente en <code>src/core/modelos.py</code> y <code>src/core/matematica.py</code>:<br/>"
            "• <b>Regresión Lineal:</b> Resuelve analíticamente las ecuaciones normales de Mínimos Cuadrados Ordinarios para calcular la pendiente $m$, el intercepto $b$, "
            "el coeficiente de correlación de Pearson $r$ y la bondad de ajuste $R^2$, permitiendo proyectar valores esperados ($\\hat{y} = mx + b$).<br/>"
            "• <b>K-Means:</b> Selecciona $K$ centroides iniciales en un espacio bidimensional, asigna iterativamente cada punto al centroide más cercano calculando distancias euclidianas, "
            "y recalcula las coordenadas de los centroides promediando los puntos de cada cluster hasta alcanzar la convergencia matemática.",
            "src/core/modelos.py y src/core/matematica.py"
        ),
        (
            "Pregunta 10: ¿Cuál es la diferencia entre un error léxico, sintáctico y semántico en DaZe? Dé un ejemplo concreto de cada uno.",
            "Diferenciación conceptual clara entre las etapas del front-end y back-end del compilador.",
            "• <b>Error Léxico:</b> Ocurre cuando un carácter no pertenece al alfabeto del lenguaje. Ej: incluir el símbolo <code>@</code> o <code>$</code> en el código genera un <code>LexerError</code> inmediato.<br/>"
            "• <b>Error Sintáctico:</b> Ocurre cuando los tokens son válidos pero violan la gramática formal. Ej: escribir <code>resultado = |&gt; descartar(minutos &gt; 0)</code> carece de operando a la izquierda del pipeline; ANTLR detecta que no se cumple <code>pipeline_stmt</code> y aborta.<br/>"
            "• <b>Error Semántico:</b> Ocurre cuando la estructura es gramaticalmente correcta pero carece de sentido lógico en el dominio. Ej: escribir <code>cantera |&gt; convocar(salario)</code> cuando la columna <code>salario</code> no existe en el esquema tabular, o intentar restar un texto de un entero. El Visitor detecta la incoherencia y lanza un <code>SemanticError</code> detallado.",
            "src/errors.py, examples/incorrecto_sintaxis.dz e incorrecto_semantico_columna.dz"
        ),
        (
            "Pregunta 11: Si quisiéramos agregar un nuevo tipo de gráfico (por ejemplo, gráfico de pastel 'torta'), ¿cuáles son los pasos exactos en el compilador?",
            "Visión global de la modularidad y extensibilidad del compilador/intérprete en todas sus capas.",
            "Se deben seguir cuatro pasos de forma ordenada:<br/>"
            "1. <b>Front-End:</b> En <code>DaZeLexer.g4</code> agregar el token <code>TORTA: 'torta';</code> y en <code>DaZeParser.g4</code> incluir <code>TORTA</code> en la regla <code>tipo_grafica</code>, regenerando el parser con ANTLR.<br/>"
            "2. <b>Semántica (Visitor):</b> En <code>visitGraficar_stmt</code> en <code>visitor.py</code>, permitir el tipo <code>torta</code> y validar que la columna de valores numéricos y la de etiquetas pertenezcan al esquema de la tabla.<br/>"
            "3. <b>Motor de Visualización:</b> En <code>visualizador.py</code>, implementar la función <code>dibujar_torta(canvas, datos, ...)</code> que calcule los ángulos proporcionales de cada categoría y trace los sectores circulares con relleno de color usando trigonometría básica.<br/>"
            "4. <b>Pruebas de Regresión:</b> Agregar un test unitario en <code>test_visualizacion_ml.py</code> y un ejemplo en <code>examples/</code> para asegurar su funcionamiento continuo.",
            "grammar/DaZeParser.g4, src/semantic/visitor.py y src/core/visualizador.py"
        ),
        (
            "Pregunta 12: ¿Qué valor aporta el caso de estudio oficial (caso_estudio.dz) y cómo se demuestra la reproducibilidad del DSL?",
            "Demostración del dominio de aplicación, valor práctico y cumplimiento de requisitos del curso.",
            "El caso de estudio demuestra un flujo reproducible de ciencia de datos deportiva de extremo a extremo: "
            "(1) carga 15 futbolistas profesionales; (2) transforma variables y calcula métricas clave de impacto y desgaste; "
            "(3) realiza agrupación y balance estadístico exportando a CSV; (4) modela regresión lineal para predecir goles esperados y segmenta a la plantilla en 3 perfiles tácticos con K-Means; "
            "y (5) exporta 4 pizarras visuales PNG con títulos, marcas de graduación y etiquetas numéricas legibles.<br/>"
            "La <b>reproducibilidad</b> se demuestra porque cualquier analista puede ejecutar <code>./daze caso_estudio.dz</code> desde la terminal y regenerar exactamente las mismas tablas, cálculos y gráficos en menos de un segundo sin tocar ni una sola línea del código Python subyacente.",
            "caso_estudio.dz, salidas/ y README.md"
        )
    ]

    for i, (q_text, eval_intent, ideal_ans, code_ref) in enumerate(preguntas, 1):
        q_card = [
            [Paragraph(f"<b>{q_text}</b>", question_title_style)],
            [Paragraph(f"<b>¿Qué evalúa el profesor?:</b> <i>{eval_intent}</i>", callout_style)],
            [Paragraph(f"<b>Respuesta recomendada para la sustentación:</b><br/>{ideal_ans}", body_style)],
            [Paragraph(f"<b>Ubicación en el código para mostrar:</b> <code>{code_ref}</code>", code_style)]
        ]
        t_q = Table(q_card, colWidths=[522])
        t_q.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F7FAFC")),
            ('BOX', (0,0), (-1,-1), 1, c_border),
            ('LINELEFT', (0,0), (0,-1), 3.5, c_secondary if i % 2 == 1 else c_accent),
            ('TOPPADDING', (0,0), (-1,-1), 3.5),
            ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
            ('LEFTPADDING', (0,0), (-1,-1), 7),
            ('RIGHTPADDING', (0,0), (-1,-1), 7),
        ]))
        story.append(KeepTogether([t_q, Spacer(1, 5)]))

    # Construir documento
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Guía de estudio generada exitosamente en: {ruta_salida}")


if __name__ == "__main__":
    salida = "/home/shibakude-_-/Downloads/lenguajes/proyecto_lenguajes/docs/Guia_de_Estudio_Sustentacion_DaZe.pdf"
    if len(sys.argv) > 1:
        salida = sys.argv[1]
    
    # Crear directorio si no existe
    os.makedirs(os.path.dirname(os.path.abspath(salida)), exist_ok=True)
    crear_guia_estudio_pdf(salida)
