# Manual de Usuario: DaZe (Sports Analytics DSL)

**Versión:** 1.0.0  
**Extensión de archivos:** `.dz`  
**Dominio:** Analítica Deportiva y Ciencia de Datos Tabular  
**Repositorio Oficial:** [https://github.com/27saya/proyecto_lenguajes.git](https://github.com/27saya/proyecto_lenguajes.git)

---

## 1. Introducción

**DaZe** es un Lenguaje de Dominio Específico (*Domain-Specific Language*, DSL) diseñado para analistas de rendimiento deportivo, preparadores físicos y cuerpos técnicos. Permite cargar plantillas de jugadores desde archivos CSV, limpiar y transformar métricas mediante tuberías funcionales (`|>`), ejecutar modelos predictivos de Machine Learning y generar visualizaciones gráficas sin necesidad de programar en lenguajes de propósito general ni instalar librerías pesadas externas.

---

## 2. Requisitos e Instalación

* **Sistema Operativo:** Linux (Ubuntu / Amazon Linux 2023), macOS o Windows (WSL).
* **Python:** Versión 3.11 o superior.
* **Dependencia única:** Runtime oficial de ANTLR4 (`antlr4-python3-runtime`).

### Pasos de instalación

```bash
# 1. Clonar el repositorio oficial
git clone https://github.com/27saya/proyecto_lenguajes.git
cd proyecto_lenguajes

# 2. Crear y activar el entorno virtual
python3 -m venv venv
source venv/bin/activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Otorgar permisos de ejecución al lanzador interactivo
chmod +x daze
```

---

## 3. Modos de Ejecución

### 3.1. Ejecución de Scripts por Lotes (`.dz`)

Para ejecutar un programa completo almacenado en un archivo fuente:

```bash
./daze caso_estudio.dz
# O bien:
python3 src/cli.py caso_estudio.dz
```

### 3.2. Herramientas de Diagnóstico del Compilador

La interfaz de línea de comandos (`src/cli.py`) incluye opciones para inspeccionar el flujo de análisis:

* **Validar sintaxis sin ejecutar:**
  ```bash
  ./daze --check caso_estudio.dz
  ```
* **Inspeccionar la secuencia de tokens del analizador léxico:**
  ```bash
  ./daze --tokens caso_estudio.dz
  ```
* **Visualizar el Árbol de Sintaxis Concreta (CST):**
  ```bash
  ./daze --tree caso_estudio.dz
  ```

### 3.3. Consola Interactiva en Vivo (REPL)

Para iniciar el entorno interactivo línea por línea:

```bash
./daze
```

* **Memoria persistente:** Las variables, listas, modelos y tablas creadas permanecen vivas en memoria durante toda la sesión.
* **Bloques multilínea:** Al abrir una llave `{` (en ciclos `ronda`, `enjuego`, subrutinas `tactica` o bloques `pizarra`), el prompt cambia de `daze> ` a `...   `, permitiendo ingresar saltos de línea hasta cerrar la llave `}`.
* **Comandos internos de sesión:**
  * `ayuda`: Muestra el resumen de comandos disponibles.
  * `simbolos`: Lista todas las variables activas en memoria y sus valores actuales.
  * `limpiar`: Limpia la pantalla de la terminal.
  * `salir`: Cierra el entorno interactivo.

---

## 4. Catálogo de Instrucciones del Lenguaje

### 4.1. Entrada, Salida y Persistencia

* **`fichar(ruta, separador=",", encabezado=verdadero)`**: Carga un archivo CSV desde disco como una tabla en memoria con inferencia automática de tipos.
* **`proyectar(expresion)`**: Imprime texto, números, modelos o tablas en consola.
* **`archivar(tabla, en="ruta/salida.csv", separador=",")`**: Exporta una tabla resultante a un archivo CSV en disco.

### 4.2. Operaciones de Tubería (`|>`)

Las transformaciones tabulares se encadenan secuencialmente de forma inmutable:

* **`convocar(col1, col2, ...)`**: Selecciona un subconjunto específico de columnas.
* **`descartar(condicion)`**: Filtra registros conservando las filas que cumplen el predicado lógico (`y`, `o`, `no`, `>`, `<`, `>=`, `<=`, `==`, `!=`).
* **`contratar(nueva_col = formula, ...)`**: Crea nuevas columnas calculadas fila por fila a partir de expresiones aritméticas.
* **`rebautizar(vieja = nueva, ...)`**: Renombra columnas existentes en el esquema de la tabla.
* **`clasificar(por=[col], descendente=verdadero)`**: Ordena los registros según una o más métricas.
* **`top(n)`**: Conserva únicamente los primeros $n$ registros de la tabla.
* **`alinear(por=[col])`**: Agrupa los registros según categorías discretas (por ejemplo, posición táctica o club).
* **`balance(metrica = funcion(col), ...)`**: Calcula resúmenes estadísticos sobre grupos o sobre toda la tabla (`suma`, `media`, `mediana`, `minimo`, `maximo`, `desviar`, `contar`).
* **`sanear(col = valor)`**: Imputa valores nulos o faltantes en la plantilla.
* **`depurar(col1, col2)`**: Elimina registros duplicados.

### 4.3. Estructuras de Datos y Control de Flujo

* **Colecciones:**
  * Listas indexables: `dorsales = [10, 7, 9];`
  * Mutación indexada: `dorsales[0] = 99;`
  * Diccionarios asociativos: `jugador = {"nombre": "Messi", "goles": 14};`
  * Pilas (LIFO): `p = pila(); apilar(p, val); desapilar(p); tope(p);`
  * Colas (FIFO): `c = cola(); encolar(c, val); desencolar(c); frente(c);`
* **Bifurcación condicional:**
  ```daze
  si (goles >= 10) {
      proyectar("Goleador destacado");
  } sino {
      proyectar("En desarrollo");
  }
  ```
* **Ciclos temáticos:**
  * Bucle condicional (*while*): `enjuego (minutos > 0) { ... }` (o `en_juego`)
  * Bucle iterativo (*for-in*): `ronda (elemento en lista) { ... }`
* **Subrutinas modulares:**
  ```daze
  tactica eficacia(goles, minutos) {
      resultado (goles * 90) / minutos;
  }
  ```

### 4.4. Matemática Pura y Machine Learning

* **Funciones matemáticas:** `raiz(x)`, `seno(x)`, `coseno(x)`, `tangente(x)`, `potencia(base, exp)`, `abs(x)`.
* **Correlación de Pearson:**
  ```daze
  r = correlacion(lista_x, lista_y);
  ```
* **Regresión Lineal Simple (MCO) e Inferencia:**
  ```daze
  modelo = regresionlineal(lista_x, lista_y);
  estimado = predecir(modelo, nuevo_x);
  ```
* **Agrupamiento No Supervisado K-Means:**
  ```daze
  clusters = agruparkmedias(matriz_datos, k);
  ```

### 4.5. Visualización Gráfica (`pizarra`)

Soporta cinco tipos de gráficos (`barras`, `dispersion`, `histograma`, `lineas` y `caja`), renderizando una vista previa en arte ASCII en consola y exportando físicamente la imagen `.png` en disco:

```daze
pizarra barras(resumen_posiciones) {
    eje_x = "posicion";
    eje_y = "total_goles";
    titulo = "Goles Totales por Posicion";
    color = "royalblue";
    guardar = "salidas/goles_posicion.png";
}
```

---

## 5. Interpretación de Errores

El compilador reporta diagnósticos claros en español indicando la ubicación exacta del fallo:

* **`[Error Léxico] Línea X:Y`**: Uso de caracteres no permitidos en el alfabeto del lenguaje (por ejemplo, `@` o `$`).
* **`[Error Sintáctico] Línea X:Y`**: Estructura gramatical incompleta, llaves `{ ... }` sin cerrar o delimitadores faltantes.
* **`[Error Semántico]`**: Referencia a variables no declaradas, columnas inexistentes en el archivo CSV o tipos incompatibles.
