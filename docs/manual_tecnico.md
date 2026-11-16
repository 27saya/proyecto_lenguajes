# Manual Técnico: Arquitectura e Implementación de DaZe

**Lenguaje de Implementación:** Python 3.11+ y ANTLR4  
**Paradigma del DSL:** Declarativo-Funcional con soporte Imperativo Modular  
**Restricción Arquitectónica:** Cero dependencias externas de cómputo o graficación (*Zero-Dependency Runtime*)  
**Repositorio Oficial:** [https://github.com/27saya/proyecto_lenguajes.git](https://github.com/27saya/proyecto_lenguajes.git)

---

## 1. Arquitectura General del Compilador

El sistema implementa una arquitectura de intérprete basado en Árbol de Sintaxis Concreta/Abstracta dividido en tres capas desacopladas:

```text
Código Fuente (.dz)
       │
       ▼
┌─────────────────────────────────────────┐
│ FRONT-END (ANTLR4 - grammar/)           │
│ • DaZeLexer.g4  -> Flujo de Tokens      │
│ • DaZeParser.g4 -> Árbol Sintáctico     │
│ • src/errors.py -> DaZeErrorListener    │
└──────────────────┬──────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────┐
│ BACK-END SEMÁNTICO (src/semantic/)      │
│ • visitor.py        -> Patrón Visitor   │
│ • tabla_simbolos.py -> Ámbitos y Tipos  │
└──────────────────┬──────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────┐
│ RUNTIME NATIVO PURO (src/core/)         │
│ • racoons.py      -> Motor Tabular      │
│ • matematica.py   -> Métodos Numéricos  │
│ • estadistica.py  -> Descriptiva        │
│ • estructuras.py  -> Pila y Cola        │
│ • ml.py           -> Pearson, MCO, KM   │
│ • visualizador.py -> PNG Binario + ASCII│
└─────────────────────────────────────────┘
```

---

## 2. Front-End: Gramática ANTLR4 (`grammar/`)

* **`grammar/DaZeLexer.g4`**: Define los tokens terminales en mayúsculas. Utiliza reglas de prioridad por orden de declaración para evitar colisiones entre palabras reservadas (`FICHAR`, `CONVOCAR`, `DESCARTAR`, `EN_JUEGO`, `RONDA`, etc.) e identificadores genéricos (`ID`). Emplea la directiva `-> skip` para descartar espacios en blanco y comentarios de línea (`#`) o de bloque (`/* ... */`).
* **`grammar/DaZeParser.g4`**: Importa el vocabulario léxico mediante `options { tokenVocab=DaZeLexer; }`. La regla inicial `programa : sentencia* EOF;` garantiza el consumo completo del flujo de entrada. La precedencia de operadores en la regla `expr` se resuelve mediante recursividad por la izquierda en orden estricto:
  $$\text{Potencia} \rightarrow \text{Unarios} \rightarrow \text{Multiplicativos} \rightarrow \text{Aditivos} \rightarrow \text{Relacionales} \rightarrow \text{Igualdad} \rightarrow \text{Lógicos (Y/O)}$$
* **`src/errors.py`**: Implementa `DaZeErrorListener` heredando de `antlr4.error.ErrorListener.ErrorListener`, interceptando `syntaxError` para traducir y formatear mensajes en español con línea, columna y token conflictivo.
* **`src/tree_viewer.py`**: Recorre recursivamente los nodos del árbol sintáctico generado por ANTLR4 para renderizar su jerarquía en consola.

---

## 3. Análisis Semántico y Gestión de Memoria (`src/semantic/`)

* **Tabla de Símbolos (`tabla_simbolos.py`)**: Implementa una cadena jerárquica de entornos enlazados mediante referencia al ámbito padre (`padre`). El entorno raíz almacena variables, modelos y tablas globales; cada invocación a una subrutina `tactica` instancia un ámbito local aislado que se destruye al finalizar la ejecución de la función.
* **Intérprete Visitor (`visitor.py`)**: Hereda de `DaZeParserVisitor`. Se seleccionó el patrón de diseño *Visitor* sobre el *Listener* para controlar explícitamente el flujo de evaluación (cortocircuito lógico, ciclos `enjuego`/`ronda` y bifurcaciones `si`/`sino`) y propagar valores de retorno entre nodos. Dentro de operaciones tabulares (`descartar`, `contratar`), el Visitor enlaza temporalmente las columnas de cada registro en el contexto de evaluación.

---

## 4. Motores Nativos en Python Puro (`src/core/`)

### 4.1. Motor Tabular (`racoons.py`)

Implementa las clases `Tabla` y `GrupoTabla` sin depender de `pandas`. Al leer archivos CSV mediante el módulo estándar `csv`, infiere dinámicamente los tipos primitivos (`int`, `float`, `bool`, `None`, `str`). Cada operación de tubería (`|>`) retorna una nueva instancia inmutable de `Tabla`, garantizando ausencia de efectos colaterales sobre los datos fuente.

### 4.2. Matemática y Estadística (`matematica.py`, `estadistica.py`)

* **Raíz Cuadrada (`raiz`)**: Aproximación iterativa de Newton-Raphson / Método Babilónico sin importar `math`:
  $$x_{k+1} = \frac{1}{2}\left(x_k + \frac{n}{x_k}\right)$$
  con criterio de parada $|x_{k+1} - x_k| < 10^{-7}$.
* **Trigonometría (`seno`, `coseno`, `tangente`)**: Expansión en Series de Taylor previa reducción modular al intervalo $[-\pi, \pi]$.
* **Desviación Estándar (`desviar`)**: Varianza muestral combinada con la raíz babilónica pura:
  $$s = \sqrt{\frac{1}{N-1}\sum_{i=1}^{N}(x_i - \bar{x})^2}$$

### 4.3. Machine Learning Puro (`ml.py`)

* **Correlación de Pearson (`correlacion` / `correlacion_pearson`)**: Razón entre covarianza muestral y producto de desviaciones estándar:
  $$r = \frac{\sum_{i=1}^N (x_i - \bar{x})(y_i - \bar{y})}{\sqrt{\sum_{i=1}^N (x_i - \bar{x})^2} \cdot \sqrt{\sum_{i=1}^N (y_i - \bar{y})^2}}$$
* **Regresión Lineal (`regresionlineal` / `regresion_lineal`)**: Parámetros ajustados por Mínimos Cuadrados Ordinarios (MCO):
  $$m = \frac{\sum_{i=1}^N (x_i - \bar{x})(y_i - \bar{y})}{\sum_{i=1}^N (x_i - \bar{x})^2}, \quad b = \bar{y} - m\bar{x}, \quad R^2 = 1 - \frac{SS_{\text{res}}}{SS_{\text{tot}}}$$
* **Agrupamiento K-Means (`agruparkmedias` / `agrupar_kmedias`)**: Inicializa $k$ centroides, calcula distancias euclidianas multidimensionales:
  $$d(p, q) = \sqrt{\sum_{j=1}^D (p_j - q_j)^2}$$
  reasigna etiquetas y actualiza centroides por promedio vectorial iterativo.

### 4.4. Rasterizador Binario PNG (`visualizador.py`)

Prescinde de `matplotlib` y `Pillow` construyendo archivos PNG conformes a la especificación estándar mediante los módulos nativos `struct` y `zlib`:
1. **`CanvasPNG`**: Mantiene un búfer bidimensional de píxeles RGB e implementa primitivas de dibujo (líneas mediante algoritmo de Bresenham, rectángulos rellenos y círculos).
2. **Empaquetado de Chunks**: Escribe la firma binaria de 8 bytes (`\x89PNG\r\n\x1a\n`), cabecera `IHDR` (dimensiones y profundidad de 8 bits), datos de imagen comprimidos en `IDAT` con sumas de verificación `CRC32`, y el bloque de terminación `IEND`.

---

## 5. Procedimiento para Extender el Lenguaje

1. Agregar el nuevo token en `grammar/DaZeLexer.g4` y la regla sintáctica en `grammar/DaZeParser.g4`.
2. Recompilar la gramática:
   ```bash
   cd grammar
   antlr4 -Dlanguage=Python3 -o ../src/generated DaZeLexer.g4
   antlr4 -Dlanguage=Python3 -visitor -listener -lib ../src/generated -o ../src/generated DaZeParser.g4
   cd ..
   ```
3. Implementar la lógica algorítmica nativa en `src/core/` y conectar el método `visit...` correspondiente en `src/semantic/visitor.py`.
4. Añadir pruebas en `tests/` y ejecutar la suite completa de pruebas:
   ```bash
   python3 -m unittest discover -s tests -p "test_*.py" -v
   ```
