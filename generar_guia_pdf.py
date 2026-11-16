#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador de la Guía de Estudio Integral para Sustentación del DSL DaZe.
Universidad Sergio Arboleda - Lenguajes de Programación y Traducción
"""

import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle


class NumberedCanvas(canvas.Canvas):
    """Canvas de dos pasadas para calcular dinámicamente el número total de páginas."""
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
            self.drawString(50, 755, "DaZe DSL — Guía de Estudio y Preparación de Sustentación")
            self.drawRightString(562, 755, "Lenguajes de Programación y Traducción")
            self.setStrokeColor(colors.HexColor("#E2E8F0"))
            self.setLineWidth(0.75)
            self.line(50, 748, 562, 748)

        # Pie de página (todas las páginas)
        self.setStrokeColor(colors.HexColor("#E2E8F0"))
        self.setLineWidth(0.75)
        self.line(50, 45, 562, 45)

        self.drawString(50, 32, "Universidad Sergio Arboleda — CC & IA | Repositorio: github.com/27saya/proyecto_lenguajes")
        page_str = f"Página {self._pageNumber} de {total_pages}"
        self.drawRightString(562, 32, page_str)
        self.restoreState()


def crear_guia_estudio_pdf(ruta_salida: str):
    doc = SimpleDocTemplate(
        ruta_salida,
        pagesize=letter,
        leftMargin=50,
        rightMargin=50,
        topMargin=55,
        bottomMargin=55,
    )

    styles = getSampleStyleSheet()

    # Colores corporativos del documento
    c_primary = colors.HexColor("#1A365D")    # Azul institucional oscuro
    c_secondary = colors.HexColor("#2B6CB0")  # Azul medio
    c_accent = colors.HexColor("#C53030")     # Rojo acento
    c_dark = colors.HexColor("#2D3748")       # Texto principal oscuro
    c_light = colors.HexColor("#F7FAFC")      # Fondo claro
    c_code_bg = colors.HexColor("#EDF2F7")    # Fondo cajas de código
    c_border = colors.HexColor("#CBD5E0")     # Bordes suaves

    # Estilos de párrafo personalizados
    title_style = ParagraphStyle(
        "DocTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=20,
        leading=24,
        textColor=c_primary,
        alignment=0,
        spaceAfter=4,
    )

    subtitle_style = ParagraphStyle(
        "DocSubtitle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=11,
        leading=15,
        textColor=c_secondary,
        alignment=0,
        spaceAfter=12,
    )

    h1_style = ParagraphStyle(
        "Heading1_Custom",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=13,
        leading=17,
        textColor=c_primary,
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True,
    )

    h2_style = ParagraphStyle(
        "Heading2_Custom",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=10.5,
        leading=14,
        textColor=c_secondary,
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True,
    )

    body_style = ParagraphStyle(
        "Body_Custom",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=13,
        textColor=c_dark,
        spaceAfter=6,
    )

    bullet_style = ParagraphStyle(
        "Bullet_Custom",
        parent=body_style,
        leftIndent=14,
        firstLineIndent=-10,
        spaceAfter=3,
    )

    code_style = ParagraphStyle(
        "Code_Custom",
        parent=styles["Normal"],
        fontName="Courier",
        fontSize=8,
        leading=10.5,
        textColor=colors.HexColor("#1A202C"),
    )

    callout_style = ParagraphStyle(
        "Callout_Custom",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor("#2C5282"),
    )

    question_title_style = ParagraphStyle(
        "QuestionTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=9.5,
        leading=13,
        textColor=c_accent,
        spaceBefore=6,
        spaceAfter=2,
        keepWithNext=True,
    )

    story = []

    # -------------------------------------------------------------
    # PORTADA / ENCABEZADO PRINCIPAL
    # -------------------------------------------------------------
    story.append(Paragraph("GUÍA INTEGRAL DE ESTUDIO Y SUSTENTACIÓN", title_style))
    story.append(Paragraph("<b>Proyecto DSL DaZe (.dz)</b> — Lenguaje de Dominio Específico para Analítica Deportiva", subtitle_style))

    # Ficha Técnica en tabla
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
            Paragraph("<b>Tecnologías:</b> ANTLR4 (Lexer/Parser) + Python 3 (Visitor & Core)", body_style)
        ]
    ]
    t_ficha = Table(ficha_data, colWidths=[270, 242])
    t_ficha.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F7FAFC")),
        ('BOX', (0,0), (-1,-1), 1, c_border),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_ficha)
    story.append(Spacer(1, 10))

    # Caja de propósito pedagógico
    intro_box = [
        [Paragraph(
            "<b>¿Cómo utilizar esta guía para preparar la sustentación?</b><br/>"
            "Este documento consolida la fundamentación teórica, la arquitectura interna del compilador/intérprete, "
            "las decisiones de diseño, el funcionamiento de nuestro motor de datos propio (<i>racoons</i>) y un banco "
            "de <b>10 preguntas de simulación (Mock Questions)</b> con las respuestas exactas que evaluará el docente. "
            "Úsalo para dominar los conceptos clave de análisis léxico, análisis sintáctico descendente, tablas de símbolos "
            "y evaluación semántica basada en el patrón Visitor.",
            callout_style
        )]
    ]
    t_intro = Table(intro_box, colWidths=[512])
    t_intro.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#EBF8FF")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#BEE3F8")),
        ('LINELEFT', (0,0), (0,0), 3.5, c_secondary),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(t_intro)
    story.append(Spacer(1, 10))

    # -------------------------------------------------------------
    # MÓDULO 1: ARQUITECTURA DEL PROYECTO Y FLUJO DEL COMPILADOR
    # -------------------------------------------------------------
    story.append(Paragraph("Módulo 1: Arquitectura Integral del DSL y Flujo de Procesamiento", h1_style))
    story.append(Paragraph(
        "DaZe es un lenguaje de dominio específico (DSL) declarativo y reproducible orientado a analistas de rendimiento, "
        "entrenadores y directores técnicos. Permite transformar datos de plantillas deportivas, telemetría de sensores GPS "
        "y academias juveniles mediante tuberías (pipelines <code>|&gt;</code>) sin requerir código de propósito general.",
        body_style
    ))

    # Tabla de componentes
    comp_data = [
        [Paragraph("<b>Componente</b>", body_style), Paragraph("<b>Módulo / Archivo</b>", body_style), Paragraph("<b>Función Teórica y Práctica</b>", body_style)],
        [Paragraph("Front-End Léxico", body_style), Paragraph("<code>grammar/DaZeLexer.g4</code>", code_style), Paragraph("Convierte el flujo de caracteres en tokens deportivos sin guiones bajos (ej. <code>desviar</code>, <code>fichar</code>, <code>convocar</code>).", body_style)],
        [Paragraph("Front-End Sintáctico", body_style), Paragraph("<code>grammar/DaZeParser.g4</code>", code_style), Paragraph("Analizador sintáctico descendente LL(*) generado por ANTLR4; construye el árbol de análisis (Parse Tree).", body_style)],
        [Paragraph("Tabla de Símbolos", body_style), Paragraph("<code>src/semantic/tabla_simbolos.py</code>", code_style), Paragraph("Estructura jerárquica con ámbitos (global y local); valida identificadores y esquemas de columnas en plantillas.", body_style)],
        [Paragraph("Motor Semántico (Visitor)", body_style), Paragraph("<code>src/semantic/visitor.py</code>", code_style), Paragraph("Recorre el AST; evalúa expresiones, encadena pipelines fila a fila e inyecta el contexto de fila dinámico.", body_style)],
        [Paragraph("Librería Propia (Core)", body_style), Paragraph("<code>src/core/racoons.py</code><br/><code>src/core/estadistica.py</code>", code_style), Paragraph("Librería nativa en Python puro (<i>racoons</i> y <i>estadistica</i>) para manipulación tabular 2D y cálculos descriptivos sin dependencias externas.", body_style)],
        [Paragraph("Diagnóstico de Errores", body_style), Paragraph("<code>src/errors.py</code>", code_style), Paragraph("Reporte unificado de errores léxicos, sintácticos y semánticos con línea, columna y mensaje comprensible en español.", body_style)],
    ]
    t_comp = Table(comp_data, colWidths=[110, 140, 262])
    t_comp.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#2B6CB0")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F7FAFC")]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_comp)
    story.append(Spacer(1, 10))

    # -------------------------------------------------------------
    # MÓDULO 2: FRONT-END — LÉXICO, SINTÁCTICO Y PRECEDENCIA
    # -------------------------------------------------------------
    story.append(Paragraph("Módulo 2: Especificación Léxica, Gramática EBNF y Precedencia", h1_style))
    story.append(Paragraph(
        "El análisis léxico y sintáctico fue especificado formalmente en notación BNF/EBNF e implementado mediante ANTLR4. "
        "Las decisiones más importantes tomadas en esta etapa fueron:",
        body_style
    ))
    story.append(Paragraph("• <b>Eliminación de guiones bajos en el DSL:</b> Se diseñó un léxico ergonómico donde operaciones como la desviación estándar se escriben <code>desviar</code> (en vez de <code>desv_std</code>), el tratamiento de nulos se nombra <code>sanear</code> o <code>recuperar</code>, y la depuración de duplicados <code>depurar</code> o <code>limpiar</code>.", bullet_style))
    story.append(Paragraph("• <b>Jerarquía y Precedencia de Expresiones:</b> ANTLR4 resuelve la precedencia según el orden en que se declaran las alternativas en la regla <code>expr</code>. Se ordenaron de mayor a menor precedencia: Potencia (<code>^</code>, asociativa por derecha) → Operadores unarios (<code>+</code>, <code>-</code>, <code>no</code>) → Multiplicativos (<code>*</code>, <code>/</code>, <code>%</code>) → Aditivos (<code>+</code>, <code>-</code>) → Relacionales (<code>&gt;</code>, <code>&lt;</code>, <code>&gt;=</code>, <code>&lt;=</code>) → Igualdad (<code>==</code>, <code>!=</code>) → Lógica Y (<code>y</code>) → Lógica O (<code>o</code>).", bullet_style))
    story.append(Paragraph("• <b>Resolución de Ambigüedad en Sentencias:</b> En la regla <code>sentencia</code>, las instrucciones especializadas <code>guardar_stmt</code> (<code>archivar</code>) y <code>mostrar_stmt</code> (<code>proyectar</code>) se ubicaron <b>antes</b> de <code>llamada_stmt</code>. Esto previene que ANTLR las interprete erróneamente como llamadas a tácticas genéricas.", bullet_style))
    story.append(Spacer(1, 10))

    # -------------------------------------------------------------
    # MÓDULO 3: MOTOR PROPIO DE DATOS (RACOONS Y ESTADÍSTICA)
    # -------------------------------------------------------------
    story.append(Paragraph("Módulo 3: Motor Propio de Datos (Librerías Racoons y Estadística)", h1_style))
    story.append(Paragraph(
        "Por indicación docente, <b>no se utilizaron dependencias pesadas de terceros como pandas o numpy</b>. "
        "En su lugar, se construyó una librería nativa en Python puro dividida en dos módulos:",
        body_style
    ))

    core_info = [
        [
            Paragraph("<b>Módulo <code>racoons.py</code> (Clase <code>Tabla</code> / <code>racoons</code>)</b>", h2_style),
            Paragraph("<b>Módulo <code>estadistica.py</code> (Cálculos Descriptivos)</b>", h2_style)
        ],
        [
            Paragraph(
                "• <b>Estructura Interna:</b> Almacena una lista de nombres de columnas y una lista de diccionarios <code>fila = {col: valor}</code>.<br/>"
                "• <b><code>csvread(ruta)</code>:</b> Parser propio con inferencia de tipos (enteros, flotantes, booleanos <code>verdadero</code>/<code>falso</code> y <code>nulo</code>).<br/>"
                "• <b><code>csvsave(ruta)</code>:</b> Exportador con creación automática de subdirectorios.<br/>"
                "• <b>Operaciones:</b> <code>convocar</code> (proyección), <code>descartar</code> (filtrado), <code>contratar</code> (columnas calculadas), <code>rebautizar</code>, <code>clasificar</code>, <code>sanear</code>, <code>depurar</code> y <code>top</code>.<br/>"
                "• <b><code>alinear</code> + <code>balance</code>:</b> Particiona la tabla mediante <code>GrupoTabla</code> usando tablas hash y aplica agregaciones por grupo.",
                body_style
            ),
            Paragraph(
                "• <b>Python Puro:</b> Implementación de algoritmos numéricos sin librerías externas.<br/>"
                "• <b><code>suma(valores)</code>:</b> Acumulador que omite nulos de forma segura.<br/>"
                "• <b><code>media(valores)</code>:</b> Promedio aritmético.<br/>"
                "• <b><code>mediana(valores)</code>:</b> Ordenamiento y selección del elemento central o promedio de dos centrales.<br/>"
                "• <b><code>minimo(valores)</code> / <code>maximo(valores)</code>:</b> Extremos de una serie deportiva.<br/>"
                "• <b><code>desviar(valores)</code>:</b> Desviación estándar muestral con divisor $(n-1)$.<br/>"
                "• <b><code>contar(valores)</code>:</b> Conteo de registros válidos.",
                body_style
            )
        ]
    ]
    t_core = Table(core_info, colWidths=[256, 256])
    t_core.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F7FAFC")),
        ('BOX', (0,0), (-1,-1), 1, c_border),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_core)
    story.append(Spacer(1, 10))

    # -------------------------------------------------------------
    # MÓDULO 4: ANÁLISIS SEMÁNTICO Y TABLA DE SÍMBOLOS
    # -------------------------------------------------------------
    story.append(Paragraph("Módulo 4: Tabla de Símbolos, Ámbitos y Comprobaciones Semánticas", h1_style))
    story.append(Paragraph(
        "La fase semántica verifica que los programas sintácticamente correctos tengan sentido lógico y respeten las reglas del dominio:",
        body_style
    ))
    story.append(Paragraph("• <b>Estructura de la Tabla de Símbolos:</b> Implementada como un árbol de ámbitos (scope tree) donde cada ámbito posee un diccionario de <code>Simbolo</code> y un puntero a su ámbito <code>padre</code>.", bullet_style))
    story.append(Paragraph("• <b>Esquemas en Símbolos Tabulares:</b> Cuando una variable almacena una <code>Tabla</code>, el símbolo registra la lista de columnas disponibles. Esto permite validar rápidamente si una columna existe antes de ejecutar proyecciones o gráficos.", bullet_style))
    story.append(Paragraph("• <b>Ámbitos Locales en Tácticas:</b> Al invocar una <code>tactica</code> (función deportiva), el intérprete crea un nuevo ámbito hijo, asociando los parámetros formales con los argumentos evaluados y aislando las variables locales del entorno global.", bullet_style))
    story.append(Paragraph("• <b>Diagnósticos Semánticos:</b> Se interceptan variables no declaradas, columnas inexistentes en la plantilla, operaciones aritméticas con tipos incompatibles (ej. restar texto de un número) y divisiones por cero.", bullet_style))
    story.append(Spacer(1, 10))

    # -------------------------------------------------------------
    # MÓDULO 5: EL INTÉRPRETE VISITOR (PATRÓN VISITOR DE ANTLR4)
    # -------------------------------------------------------------
    story.append(Paragraph("Módulo 5: Intérprete Semántico Basado en el Patrón Visitor", h1_style))
    story.append(Paragraph(
        "La clase <code>DaZeSemanticVisitor</code> hereda de <code>DaZeParserVisitor</code> y controla de forma explícita el recorrido del AST:",
        body_style
    ))

    visitor_table = [
        [Paragraph("<b>Aspecto Técnico</b>", body_style), Paragraph("<b>Mecanismo Implementado en DaZe</b>", body_style)],
        [
            Paragraph("<b>Visitor vs Listener</b>", body_style),
            Paragraph("El <b>Visitor</b> permite controlar cuándo y cuántas veces visitar los nodos hijos y retornar valores directamente. El Listener realiza un recorrido pasivo y ciego (DFS automático) que dificulta evaluar expresiones dinámicas y condicionales.", body_style)
        ],
        [
            Paragraph("<b>Inyección de Contexto de Fila</b>", body_style),
            Paragraph("En <code>descartar</code> y <code>contratar</code>, el visitor evalúa expresiones fila a fila estableciendo <code>self.contexto_fila = fila</code>. Al resolver un identificador, busca primero en las columnas de la fila actual y luego en la tabla de símbolos.", body_style)
        ],
        [
            Paragraph("<b>Control de Flujo Condicional</b>", body_style),
            Paragraph("En <code>si (expr) { ... } sino { ... }</code>, evalúa la condición booleana y solo visita las sentencias del bloque correspondiente, evitando ejecuciones innecesarias.", body_style)
        ],
        [
            Paragraph("<b>Retorno de Funciones (<code>resultado</code>)</b>", body_style),
            Paragraph("Se implementa mediante una excepción de señal (<code>ReturnSignal(valor)</code>) que desenrolla inmediatamente la pila de llamadas hasta el receptor de la táctica.", body_style)
        ],
        [
            Paragraph("<b>Validación de Pizarras (Visualización)</b>", body_style),
            Paragraph("En la sentencia <code>pizarra</code> se comprueba semánticamente que el dataset exista y que las variables asignadas a <code>eje_x</code> y <code>eje_y</code> correspondan a columnas válidas de la tabla, cumpliendo estrictamente con el alcance actual.", body_style)
        ],
    ]
    t_vis = Table(visitor_table, colWidths=[150, 362])
    t_vis.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#2B6CB0")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F7FAFC")]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_vis)
    story.append(Spacer(1, 14))

    # -------------------------------------------------------------
    # MÓDULO 6: CASOS DE ESTUDIO Y RESULTADOS DE PRUEBA
    # -------------------------------------------------------------
    story.append(Paragraph("Módulo 6: Casos de Estudio Verificados y Suite de Pruebas", h1_style))
    story.append(Paragraph(
        "El proyecto cuenta con <b>40 pruebas unitarias e integración pasando al 100%</b> y tres flujos aplicados a datos reales:",
        body_style
    ))
    story.append(Paragraph("1. <b><code>correcto_ventas.dz</code>:</b> Procesa <code>plantilla_temporada.csv</code>, filtra jugadores aptos, calcula rendimiento e impacto, genera balance por posición y exporta a <code>salidas/resumenposiciones.csv</code>.", bullet_style))
    story.append(Paragraph("2. <b><code>correcto_sensores.dz</code>:</b> Carga telemetría GPS (<code>gps_rendimiento.csv</code>), evalúa la táctica condicional <code>alertasobrecarga</code>, calcula gasto calórico e índice de desgaste y exporta a <code>salidas/telemetrialimpia.csv</code>.", bullet_style))
    story.append(Paragraph("3. <b><code>correcto_estudiantes.dz</code>:</b> Evalúa notas académicas y físicas de canteranos (<code>academia_juvenil.csv</code>), clasifica por promedio general y exporta el balance por categoría a <code>salidas/balancecantera.csv</code>.", bullet_style))
    story.append(Paragraph("4. <b>Pruebas de Diagnóstico Negativo:</b> Comprobación de errores con <code>incorrecto_semantico_variable.dz</code>, <code>incorrecto_semantico_columna.dz</code> e <code>incorrecto_semantico_tipos.dz</code>.", bullet_style))
    story.append(Spacer(1, 10))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#CBD5E0"), spaceBefore=8, spaceAfter=14))
    story.append(Paragraph("Módulo 7: Banco de Preguntas de Sustentación (Mock Questions)", h1_style))
    story.append(Paragraph("Preguntas típicas y retadoras del docente Joaquín F. Sánchez con respuestas modelo y justificación técnica.", subtitle_style))

    # Lista de preguntas y respuestas
    preguntas = [
        (
            "Pregunta 1: ¿Por qué eligieron el patrón Visitor sobre el Listener para implementar la semántica y ejecución?",
            "Evaluar el dominio de los dos mecanismos principales de recorrido de árboles en ANTLR4 y la justificación técnica de la elección.",
            "Elegimos el patrón Visitor porque nos otorga <b>control total y explícito sobre el flujo de navegación del árbol</b>. "
            "A diferencia del Listener, que es guiado ciegamente por un caminador pasivo (<i>ParseTreeWalker</i>) que visita todos los nodos en DFS sin retornar valores, "
            "el Visitor permite que cada método visitante retorne el resultado de su evaluación. Esto es crucial en nuestro DSL para: "
            "(1) evaluar expresiones compuestas y propagar sus valores hacia arriba; (2) controlar estructuras de decisión como <code>si</code>/<code>sino</code> ejecutando únicamente la rama activa; "
            "y (3) evaluar subárboles de expresiones de forma iterativa fila por fila durante las operaciones <code>contratar</code> y <code>descartar</code>.",
            "src/semantic/visitor.py (clase DaZeSemanticVisitor)"
        ),
        (
            "Pregunta 2: ¿Cómo gestiona el DSL el ámbito léxico cuando se invoca una función deportiva (tactica)?",
            "Verificar si el estudiante comprende el ciclo de vida de los ámbitos (scopes), paso de parámetros y aislamiento de memoria.",
            "Lo gestionamos mediante una <b>Tabla de Símbolos jerárquica con enlaces estáticos a su ámbito padre</b>. "
            "Cuando se declara una <code>tactica</code>, el Visitor almacena su definición (nombres de parámetros y el subárbol de sentencias) en la tabla global. "
            "Al ejecutarse la llamada (<code>visitLlamada_stmt</code>), el intérprete evalúa los argumentos en el ámbito actual y luego <b>crea un nuevo ámbito hijo</b> "
            "utilizando <code>crear_ambito_hijo()</code>. Dentro de este entorno local se vinculan los parámetros con sus valores. "
            "Cualquier variable creada dentro de la táctica vive en este ámbito local; al terminar la ejecución (o emitir <code>resultado</code>), el puntero de la tabla de símbolos "
            "se restaura a su ámbito anterior en un bloque <code>finally</code>, garantizando que las variables locales no contaminen el entorno global.",
            "src/semantic/tabla_simbolos.py y src/semantic/visitor.py (_ejecutar_tactica)"
        ),
        (
            "Pregunta 3: En un pipeline como 'datos |> descartar(minutos > 0)', ¿cómo sabe el Visitor qué es 'minutos' si no es una variable global?",
            "Comprobar el mecanismo de enlace dinámico de columnas y contexto de fila.",
            "Implementamos un mecanismo de <b>inyección de contexto de fila</b>. Cuando el Visitor entra a procesar <code>descartar</code> o <code>contratar</code>, "
            "recorre los registros de la tabla y en cada iteración asigna el diccionario de la fila a <code>self.contexto_fila = fila</code> antes de visitar la expresión. "
            "En el método <code>visitExprIdentificador</code>, se aplica una resolución en dos niveles: primero se consulta si el identificador coincide con alguna llave de <code>self.contexto_fila</code>. "
            "Si coincide, retorna el valor del campo para esa fila específica. Si no, busca en la tabla de símbolos global. Si no existe en ninguno de los dos, "
            "se emite un error semántico indicando que la columna no existe en la plantilla deportiva.",
            "src/semantic/visitor.py (visitExprIdentificador y _aplicar_descartar)"
        ),
        (
            "Pregunta 4: ¿Por qué decidieron implementar su propia librería (racoons) en lugar de usar pandas y qué estructura de datos eligieron?",
            "Evaluar comprensión de estructuras de datos internas, algoritmos tabulares y autonomía técnica.",
            "Decidimos crear <b>racoons</b> desde cero para tener control absoluto sobre el modelo de ejecución y cumplir con la directriz de comprender los algoritmos subyacentes sin depender de cajas negras externas. "
            "Internamente, representamos una <code>Tabla</code> con dos atributos: una lista de cadenas para los nombres de columnas y una lista de diccionarios para las filas (<code>List[Dict[str, Any]]</code>). "
            "Esta estructura híbrida nos ofrece acceso directo por nombre de columna en tiempo $O(1)$ por fila, flexibilidad para inferir tipos de datos dinámicos durante la lectura CSV y una "
            "complejidad de $O(N)$ para filtros y transformaciones. Para la operación <code>alinear</code>, construimos la clase <code>GrupoTabla</code>, que particiona los registros "
            "en una tabla hash cuyas claves son tuplas con los valores de las columnas de agrupación.",
            "src/core/racoons.py (clases Tabla y GrupoTabla)"
        ),
        (
            "Pregunta 5: ¿Cómo resolvieron la ambigüedad en la gramática para instrucciones como 'archivar' o 'proyectar'?",
            "Conocimiento del análisis sintáctico descendente predictivo y el orden de producción de reglas en ANTLR4.",
            "En ANTLR4, cuando varias reglas pueden coincidir con el mismo prefijo de tokens, el parser favorece la regla declarada primero en el archivo de gramática. "
            "Inicialmente, la regla <code>llamada_stmt</code> (que reconoce <code>identificador LPAREN ... RPAREN</code>) estaba antes que <code>guardar_stmt</code> y <code>mostrar_stmt</code>. "
            "Como palabras como <code>archivar</code> y <code>proyectar</code> también están permitidas como identificadores en ciertos contextos, ANTLR absorbía estas sentencias como llamadas a funciones genéricas. "
            "La solución consistió en <b>reordenar la regla sentencia en DaZeParser.g4</b>, colocando <code>guardar_stmt</code> y <code>mostrar_stmt</code> antes de <code>llamada_stmt</code>. "
            "Así, el parser comprueba primero la sintaxis específica del almacenamiento y la proyección antes de recurrir a la llamada genérica.",
            "grammar/DaZeParser.g4 (regla sentencia)"
        ),
        (
            "Pregunta 6: ¿Cuál es la diferencia exacta entre un error sintáctico y uno semántico en DaZe? Dé un ejemplo concreto de cada uno en el proyecto.",
            "Claridad conceptual entre la forma (sintaxis) y el significado/validez de tipos (semántica).",
            "Un <b>error sintáctico</b> ocurre cuando la secuencia de tokens viola la estructura gramatical del lenguaje. Por ejemplo, en <code>resultado = |&gt; descartar(x &gt; 0)</code>, "
            "falta la expresión fuente a la izquierda del pipeline; el parser detecta que la regla <code>pipeline_stmt</code> no se cumple y reporta un error sintáctico sin llegar a ejecutar nada.<br/>"
            "Un <b>error semántico</b> ocurre cuando el código está perfectamente bien escrito gramaticalmente, pero es lógicamente inválido en el contexto de ejecución. "
            "Por ejemplo, en <code>cantera |&gt; convocar(dorsal, salario)</code>, la gramática es impecable (identificadores separados por comas dentro de convocar), "
            "pero al ejecutarse en el Visitor, se consulta el esquema de <code>cantera</code> y se descubre que la columna <code>salario</code> no existe en la plantilla juvenil. "
            "El Visitor detiene la operación y emite un <code>SemanticError</code> detallado.",
            "src/errors.py, examples/incorrecto_sintaxis.dz y examples/incorrecto_semantico_columna.dz"
        ),
        (
            "Pregunta 7: ¿Qué ocurre si un analista intenta dividir por cero o restar un texto de un número dentro de 'contratar'?",
            "Manejo de excepciones en tiempo de ejecución, tipado dinámico y robustez del intérprete.",
            "El Visitor implementa validación de tipos defensiva en los métodos de visita de operadores aritméticos (<code>visitExprMulDivMod</code> y <code>visitExprSumaResta</code>). "
            "En la división (<code>/</code>), verifica si el operando derecho evaluado es numérico y diferente de cero; si es igual a cero, no permite que Python lance un <i>ZeroDivisionError</i> descontrolado, "
            "sino que eleva un <code>SemanticError('Division por cero no permitida en calculos de rendimiento')</code> indicando línea y columna. "
            "En la resta (<code>-</code>), si alguno de los operandos no es entero o flotante, eleva un <code>SemanticError</code> informando los tipos incompatibles recibidos (ej. <code>int</code> y <code>str</code>).",
            "src/semantic/visitor.py (visitExprMulDivMod y visitExprSumaResta)"
        ),
        (
            "Pregunta 8: ¿Cómo funciona el retorno de valor en una 'tactica' utilizando la palabra reservada 'resultado'?",
            "Comprensión del desenrollado de pila de llamadas (unwinding) en lenguajes interpretados sobre árboles.",
            "Como el Visitor recorre el AST de manera recursiva, si una instrucción <code>resultado expr;</code> está dentro de un bloque condicional anidado (por ejemplo, dentro de un <code>si</code>), "
            "un simple <code>return</code> de Python solo saldría de la función visitante local de ese bloque, pero las sentencias posteriores de la táctica se seguirían ejecutando. "
            "Para resolver esto elegantemente, implementamos la clase <code>ReturnSignal(Exception)</code>. Cuando el Visitor encuentra <code>visitRetornar_stmt</code>, evalúa la expresión "
            "y lanza esta señal. El método <code>_ejecutar_tactica</code> captura específicamente <code>ReturnSignal</code>, extrae el valor retornado y finaliza la ejecución de la táctica de forma limpia.",
            "src/semantic/visitor.py (clase ReturnSignal y visitRetornar_stmt)"
        ),
        (
            "Pregunta 9: En la sentencia 'pizarra', ¿por qué el intérprete valida las columnas pero no genera el gráfico PNG?",
            "Defensa del alcance modular del proyecto según las fases definidas en la guía del curso.",
            "Porque el proyecto fue estructurado siguiendo la arquitectura modular y las especificaciones de la Sección 5 del documento del curso. "
            "En el alcance actual, el objetivo es completar la <b>semántica, la tabla de símbolos y el motor de datos tabulares</b>. "
            "Por ende, en <code>visitGraficar_stmt</code> comprobamos que el dataset referenciado exista y que las columnas configuradas en <code>eje_x</code> y <code>eje_y</code> "
            "formen parte del esquema real de la tabla. Al validarlo, el sistema garantiza la correctitud semántica de la visualización, dejando la renderización física con librerías gráficas "
            "para la entrega de visualización final sin mezclar alcances.",
            "src/semantic/visitor.py (visitGraficar_stmt)"
        ),
        (
            "Pregunta 10: Si mañana quisiéramos agregar una nueva operación de pipeline, por ejemplo 'fusionar' (join entre dos tablas), ¿qué pasos exactos debemos seguir?",
            "Demostrar visión global de la extensibilidad del compilador/intérprete en todas sus capas.",
            "Debemos intervenir tres capas de forma ordenada: "
            "(1) <b>Capa Léxica y Sintáctica:</b> En <code>DaZeLexer.g4</code> agregar el token <code>FUSIONAR: 'fusionar';</code> y en <code>DaZeParser.g4</code> añadir <code>op_fusionar: FUSIONAR LPAREN expr (COMA POR ASIGNAR lista_columnas)? RPAREN;</code> como alternativa de <code>operacion_pipeline</code>, regenerando el parser con ANTLR. "
            "(2) <b>Capa del Motor de Datos (Core):</b> En <code>src/core/racoons.py</code>, implementar el método <code>fusionar(self, otra_tabla, clave)</code> realizando la combinación de filas según la clave común. "
            "(3) <b>Capa Semántica (Visitor):</b> En <code>src/semantic/visitor.py</code>, agregar el método <code>_aplicar_fusionar</code>, verificando que la segunda tabla exista en la tabla de símbolos, que la clave pertenezca a ambos esquemas y llamando al método del core.",
            "grammar/DaZeParser.g4, src/core/racoons.py y src/semantic/visitor.py"
        )
    ]

    for i, (q_text, eval_intent, ideal_ans, code_ref) in enumerate(preguntas, 1):
        q_card = [
            [Paragraph(f"<b>{q_text}</b>", question_title_style)],
            [Paragraph(f"<b>¿Qué evalúa el profesor?:</b> <i>{eval_intent}</i>", callout_style)],
            [Paragraph(f"<b>Respuesta recomendada para la sustentación:</b><br/>{ideal_ans}", body_style)],
            [Paragraph(f"<b>Ubicación en el código para mostrar:</b> <code>{code_ref}</code>", code_style)]
        ]
        t_q = Table(q_card, colWidths=[512])
        t_q.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F7FAFC")),
            ('BOX', (0,0), (-1,-1), 1, c_border),
            ('LINELEFT', (0,0), (0,-1), 3.5, c_secondary if i % 2 == 1 else c_accent),
            ('TOPPADDING', (0,0), (-1,-1), 4),
            ('BOTTOMPADDING', (0,0), (-1,-1), 4),
            ('LEFTPADDING', (0,0), (-1,-1), 8),
            ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ]))
        story.append(KeepTogether([t_q, Spacer(1, 6)]))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Guía de estudio generada exitosamente en: {ruta_salida}")


if __name__ == "__main__":
    salida = "/home/shibakude-_-/Downloads/Proyecto_lenguajes/Guia_de_Estudio_Sustentacion_DaZe.pdf"
    if len(sys.argv) > 1:
        salida = sys.argv[1]
    crear_guia_estudio_pdf(salida)
