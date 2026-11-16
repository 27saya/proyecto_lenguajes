# Reporte de Pruebas Automatizadas y Regresión: DaZe

**Framework de Pruebas:** `unittest` (Biblioteca Estándar de Python)  
**Total de Pruebas Ejecutadas:** 48  
**Estado Global:** 48 / 48 EXITOSAS (`OK`)  
**Tiempo de Ejecución:** ~0.3 segundos

---

## 1. Procedimiento de Ejecución

Para reproducir la batería completa de pruebas automatizadas desde la raíz del repositorio:

```bash
python3 -m unittest discover -s tests -p "test_*.py" -v
```

---

## 2. Matriz de Cobertura por Componente

| Archivo de Prueba | Componente Evaluado | Cantidad | Estado | Descripción de Casos Validados |
| :--- | :--- | :---: | :---: | :--- |
| `tests/test_lexer.py` | Front-End Léxico (`DaZeLexer`) | 5 | OK | Palabras reservadas deportivas, literales numéricos y de cadena, operadores lógicos/relacionales y descarte de comentarios (`-> skip`). |
| `tests/test_parser.py` | Front-End Sintáctico (`DaZeParser`) | 6 | OK | Asignaciones, expresiones con precedencia matemática, `fichar`, tuberías (`\|>`), estructuras de control (`si`, `tactica`) y bloques `pizarra`. |
| `tests/test_errors.py` | Diagnóstico de Errores (`DaZeErrorListener`) | 5 | OK | Captura controlada en español de caracteres ilegales (`@`, `$`), bloques sin cerrar, paréntesis incompletos y tuberías malformadas. |
| `tests/test_core_tabla.py` | Motor Tabular (`racoons.py`) | 10 | OK | Lectura y escritura CSV (`csvread`/`csvsave`), `convocar`, `descartar`, `contratar`, `clasificar`, `alinear`, `balance`, `rebautizar`, `sanear` y validación de columnas inexistentes. |
| `tests/test_estadistica.py` | Estadística Descriptiva (`estadistica.py`) | 6 | OK | Cálculo determinístico de `suma` (con manejo de valores nulos), `media`, `mediana` (listas pares e impares), `minimo`, `maximo`, `contar` y `desviar`. |
| `tests/test_semantic.py` | Tabla de Símbolos (`TablaSimbolos`) | 5 | OK | Resolución de ámbitos globales y locales anidados, detección de variables no declaradas, columnas inexistentes y errores por tipos incompatibles. |
| `tests/test_interpreter.py` | Intérprete Semántico (`visitor.py`) | 3 | OK | Ejecución integral de pipelines con agrupación y guardado físico en CSV, operaciones `sanear`/`top` y subrutinas `tactica` con control de flujo. |
| `tests/test_visualizacion_ml.py` | Visualizador, ML y Estructuras | 8 | OK | Correlación de Pearson ($r = 1.0$), regresión lineal MCO ($m, b, R^2$) e inferencia, agrupamiento K-Means ($k=2$), validación de cabecera binaria PNG (`\x89PNG\r\n\x1a\n`), renderizado de `pizarra barras`, matemáticas puras, pilas/colas nativas y bucles `enjuego`/`ronda`. |

---

## 3. Estrategia de Pruebas de Regresión

Durante la consolidación de todas las capacidades del lenguaje (incorporación de ciclos temáticos `enjuego`/`ronda`, modelos de Machine Learning puro, rasterizador binario PNG y consola interactiva REPL), se ejecutó de forma continua la suite acumulada de pruebas para garantizar estabilidad arquitectónica.

### Resultados de la Regresión

* **Compatibilidad Léxica y Sintáctica:** Las reglas añadidas para bucles iterativos y funciones nativas no introdujeron ambigüedades ni conflictos en las pruebas del Front-End (`test_lexer`, `test_parser`, `test_errors`).
* **Integridad del Motor Tabular y Semántico:** Todas las pruebas del motor tabular y descriptivo (`test_core_tabla`, `test_estadistica`, `test_semantic`, `test_interpreter`) mantuvieron el 100% de aprobación tras integrar el despachador gráfico nativo en `visitor.py`.
* **Validación Integral del Caso de Estudio:** Adicionalmente a las pruebas unitarias, se verificó la ejecución de extremo a extremo de `caso_estudio.dz`, comprobando la creación física en disco de `salidas/resumen_posiciones.csv` y las 4 imágenes PNG (`1_goles_por_posicion.png`, `2_dispersion_minutos_contribucion.png`, `3_histograma_minutos.png` y `4_lineas_top_ofensivo.png`).
