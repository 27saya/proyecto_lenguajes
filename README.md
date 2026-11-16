# DaZe: DSL para analisis deportivo

Este repositorio contiene la implementación de **DaZe** (`.dz`), un lenguaje de dominio específico diseñado para modelar flujos reproducibles de análisis de datos deportivos, preparación de plantillas de atletas, simulaciones predictivas y generación de pizarras visuales.

El objetivo de DaZe es que cualquier persona del ámbito deportivo (analistas de rendimiento, directores técnicos o cuerpos médicos) pueda transformar datos de manera sencilla y declarativa mediante pipelines secuenciales (`|>`), bucles temáticos y herramientas analíticas, utilizando un vocabulario propio del deporte y sin enredarse con código complejo de propósito general.

El proyecto utiliza **ANTLR4** para el front-end (análisis léxico y sintáctico) y **Python 3.11+** para el análisis semántico y la ejecución interpretada con el patrón **Visitor**. Además, desarrollamos **nuestras propias librerías nativas** de procesamiento tabular, estadística descriptiva, métodos numéricos, estructuras lineales, modelos de Machine Learning y renderizado gráfico en PNG, de modo que el lenguaje funciona de manera 100% autónoma sin requerir librerías externas como `pandas`, `numpy`, `scikit-learn`, `matplotlib` ni el módulo `math`.

---

## Nuestras librerías propias (`src/core/`)

Para asegurar el control total del cómputo y entender a fondo cómo operan las estructuras de datos y los algoritmos, construimos nuestras propias soluciones en Python puro dentro del paquete `src/core/`:

### 1. `racoons` (`src/core/racoons.py`)
Es nuestro motor principal para manejar colecciones de datos tabulares en memoria (equivalente propio a un DataFrame):
- **`csvread(ruta, separador=',', encabezado=verdadero)`**: Lee archivos delimitados e infiere automáticamente los tipos de datos (enteros, decimales, booleanos `verdadero`/`falso` y valores `nulo`).
- **`csvsave(ruta, separador=',')`**: Exporta tablas a disco asegurando la creación recursiva de directorios de destino.
- **`convocar(columnas)`**: Proyecta las variables solicitadas validando la existencia en el esquema.
- **`descartar(condicion)`**: Filtra atletas o registros evaluando expresiones lógicas fila a fila.
- **`contratar(columnas_dict)`**: Crea o actualiza columnas calculadas dinámicamente.
- **`rebautizar(mapeo)`**: Renombra atributos de la plantilla.
- **`clasificar(columnas, descendente)`**: Algoritmo de ordenamiento determinístico por una o varias métricas.
- **`alinear(columnas_grupo)`**: Segmenta la plantilla en subgrupos tácticos (`GrupoTabla`).
- **`balance(agregaciones)`**: Realiza agregaciones multivariable por grupo o sobre la tabla global.
- **`sanear(reemplazos)`**: Imputa valores nulos o faltantes.
- **`depurar(columnas)`**: Deduplica registros repetidos.
- **`top(n)`**: Conserva los primeros $n$ registros destacados.
- **`mostrar(limite=10)`**: Renderiza vistas de tabla con bordes y alineación ASCII en consola.

### 2. Estadística descriptiva (`src/core/estadistica.py`)
Cálculos descriptivos que operan sobre secuencias numéricas ignorando valores nulos:
- **`suma(valores)`**: Acumulación aritmética.
- **`media(valores)`**: Promedio aritmético.
- **`mediana(valores)`**: Mediana estadística (para listas de cardinalidad par o impar).
- **`minimo(valores)`** y **`maximo(valores)`**: Detección de extremos en colecciones.
- **`desviar(valores)`**: Desviación estándar muestral calculada con raíz babilónica pura.
- **`contar(valores)`**: Conteo de registros válidos.

### 3. Motor matemático puro (`src/core/matematica.py`)
Implementación de métodos numéricos y funciones trascendentes desde cero:
- **`raiz_cuadrada(x)` / `raiz(x)`**: Algoritmo iterativo de Newton-Raphson / Método Babilónico con tolerancia $10^{-7}$.
- **`seno(x)`**, **`coseno(x)`** y **`tangente(x)`**: Evaluación trigonométrica de alta precisión mediante Series de Taylor con normalización al ciclo $[-\pi, \pi]$.
- **`potencia(base, exp)`**: Exponenciación para exponentes enteros positivos y negativos.
- **`valor_absoluto(x)` / `abs(x)`**: Magnitud escalar.

### 4. Estructuras de datos lineales (`src/core/estructuras.py`)
Estructuras nativas integradas directamente en el lenguaje:
- **`Pila` (LIFO)**: `pila()`, `apilar(p, elemento)`, `desapilar(p)` y `tope(p)`.
- **`Cola` (FIFO)**: `cola()`, `encolar(c, elemento)`, `desencolar(c)` y `frente(c)`.
- **Arreglos y Diccionarios**: Soporte para listas indexables (`tiempos[0] = 99`), diccionarios con pares clave-valor (`{"posicion": "Delantero"}`) y función `longitud(coleccion)`.

### 5. Machine Learning y modelos predictivos (`src/core/ml.py`)
Algoritmos de aprendizaje supervisado y no supervisado desarrollados sin dependencias externas:
- **`correlacion(x, y)` / `correlacion_pearson(x, y)`**: Coeficiente de correlación lineal de Pearson ($r \in [-1.0, 1.0]$).
- **`regresionlineal(x, y)` / `regresion_lineal(x, y)`**: Ajuste de regresión lineal simple ($y = mx + b$) por Mínimos Cuadrados Ordinarios, calculando pendiente ($m$), intercepto ($b$) y coeficiente de determinación ($R^2$).
- **`predecir(modelo, x)` / `predecir_regresion(modelo, x)`**: Función de inferencia para proyectar métricas futuras a partir del modelo entrenado.
- **`agruparkmedias(datos, k)` / `agrupar_kmedias(datos, k)`**: Clustering K-Means multidimensional con convergencia por distancia euclidiana y recálculo de centroides.

### 6. Visualizador autónomo PNG y ASCII (`src/core/visualizador.py`)
Generador gráfico con renderizado dual:
- **`CanvasPNG`**: Lienzo gráfico en memoria con rasterización de líneas (algoritmo de Bresenham), rectángulos y círculos.
- **Empaquetador binario PNG**: Genera los bloques estándar `IHDR`, `IDAT` y `IEND` calculando sumas de chequeo `CRC32` y comprimiendo con `zlib` nativo.
- Produce simultáneamente arte ASCII en la terminal para previsualización inmediata y archivos físicos `.png` válidos en `salidas/`. Soporta `barras`, `dispersion`, `histograma`, `lineas` y `caja`.

---

## Tabla de Símbolos y Ámbitos (`src/semantic/tabla_simbolos.py`)

Para que el intérprete controle las variables, tablas, estructuras y subrutinas en tiempo de ejecución:
- **Ámbito global**: Mantiene las plantillas cargadas, resultados de pipelines y variables globales.
- **Ámbitos locales**: Se generan dinámicamente al invocar funciones (`tactica`), aislando los argumentos y variables locales.
- **Tipado dinámico**: Clasifica identificadores en `ENTERO`, `DECIMAL`, `CADENA`, `BOOLEANO`, `TABLA`, `PILA`, `COLA`, `LISTA` y `DICCIONARIO`.

---

## Intérprete semántico con patrón Visitor (`src/semantic/visitor.py`)

Heredando de `DaZeParserVisitor` (generado por ANTLR), `DaZeSemanticVisitor` recorre el AST y se encarga de:
1. **Evaluar expresiones**: Aritmética (`+`, `-`, `*`, `/`, `%`, `^`), comparaciones (`==`, `!=`, `<`, `>`, `<=`, `>=`) y lógica booleana (`y`, `o`, `no`).
2. **Contexto dinámico en pipelines**: Al procesar operaciones fila a fila (`descartar`, `contratar`), enlaza directamente los nombres de las columnas para que las expresiones las resuelvan sin sintaxis extraña.
3. **Control de flujo**: Bifurcaciones `si`/`sino`, bucle condicional `enjuego` (o `en_juego`) y bucle iterador `ronda`.
4. **Despacho de funciones nativas**: Reconoce llamadas a matemáticas puras, estructuras de datos, subrutinas tácticas y algoritmos de Machine Learning.
5. **Ejecución de pizarras gráficas**: Valida la existencia de la tabla y columnas, genera el gráfico en consola y exporta el `.png` físico a disco.

---

## Características y sintaxis del lenguaje

### 1. Carga y guardado de datos
```daze
plantilla = fichar("datos/rendimiento_jugadores.csv", separador=",", encabezado=verdadero);
archivar(resumen_posiciones, en="salidas/resumen_posiciones.csv", separador=",");
```

### 2. Tuberías de transformación (`|>`)
```daze
analisis_ofensivo = plantilla
    |> convocar(dorsal, nombre, posicion, minutos, goles, asistencias, distancia_km)
    |> descartar(minutos >= 800)
    |> contratar(
        contribucion = goles + asistencias,
        promedio_gol = (goles * 90) / minutos,
        desgaste_minuto = distancia_km / minutos
    )
    |> clasificar(por=[contribucion], descendente=verdadero);

resumen_posiciones = analisis_ofensivo
    |> alinear(por=[posicion])
    |> balance(
        total_goles = suma(goles),
        media_asistencias = media(asistencias),
        mediana_minutos = mediana(minutos),
        desv_distancia = desviar(distancia_km),
        total_jugadores = contar()
    );
```

### 3. Bucles temáticos y estructuras
```daze
# Bucle condicional (while)
contador = 1;
enjuego (contador <= 3) {
    proyectar(contador);
    contador = contador + 1;
}

# Bucle iterador (for-in)
tiempos = [10, 20, 30];
ronda (t en tiempos) {
    proyectar(t);
}

# Pila y Cola
p = pila();
apilar(p, "Atleta 1");
proyectar(tope(p));
desapilar(p);
```

### 4. Modelos de Machine Learning
```daze
# Correlacion de Pearson
minutos = [120, 340, 500, 750, 900, 1100, 1300];
goles   = [1, 3, 4, 7, 8, 11, 14];
r = correlacion(minutos, goles);

# Regresion lineal e inferencia
modelo = regresionlineal(minutos, goles);
proyectar(modelo["r2"]);
prediccion = predecir(modelo, 1000);

# Clustering K-Means
clusters = agruparkmedias([[1250, 23], [1180, 22], [890, 10], [1020, 4]], 2);
```

### 5. Pizarras visuales (exportación física a PNG)
```daze
pizarra barras(resumen_posiciones) {
    eje_x = "posicion";
    eje_y = "total_goles";
    titulo = "Goles Totales por Posicion Tactica";
    color = "royalblue";
    guardar = "salidas/1_goles_por_posicion.png";
}

pizarra dispersion(analisis_ofensivo) {
    eje_x = "minutos";
    eje_y = "contribucion";
    titulo = "Minutos Disputados vs Contribucion Ofensiva";
    color = "crimson";
    guardar = "salidas/2_dispersion_minutos_contribucion.png";
}
```

---

## Guía de ejecución (Linux)

### 1. Requisitos previos
Tener instalado Python 3.11 o superior. El proyecto solo requiere el paquete oficial de ANTLR4:

```bash
git clone https://github.com/27saya/proyecto_lenguajes.git
cd proyecto_lenguajes
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
chmod +x daze
```

### 2. Consola interactiva (REPL Oficial)
Puedes iniciar la terminal interactiva de DaZe directamente con el comando:

```bash
./daze
# O bien:
python3 src/cli.py
```

Dentro del REPL dispones de comandos de utilidad:
- `ayuda`: Muestra la guía de instrucciones disponibles.
- `simbolos`: Imprime el estado actual de las variables y tablas cargadas en memoria.
- `limpiar`: Limpia la pantalla de la terminal.
- `salir`: Cierra la sesión interactiva.

### 3. Ejecución del caso de estudio oficial
Para ejecutar el flujo completo con datos reales de atletas profesionales y generar las 4 pizarras visuales en formato PNG:

```bash
./daze caso_estudio.dz
```

Al terminar, se habrán generado en la carpeta `salidas/`:
- `salidas/resumen_posiciones.csv`
- `salidas/1_goles_por_posicion.png` (Barras)
- `salidas/2_dispersion_minutos_contribucion.png` (Dispersión)
- `salidas/3_histograma_minutos.png` (Histograma)
- `salidas/4_lineas_top_ofensivo.png` (Líneas)

### 4. Ejecución de otros ejemplos y scripts de prueba
```bash
./daze prueba_estructuras_bucles.dz
./daze prueba_ml.dz
./daze examples/correcto_ventas.dz
./daze examples/correcto_sensores.dz
./daze examples/correcto_estudiantes.dz
```

### 5. Opciones de diagnóstico y visualización
- **Solo validar sintaxis sin ejecutar:**
  ```bash
  ./daze --check caso_estudio.dz
  ```
- **Ver el flujo de tokens reconocidos por el lexer:**
  ```bash
  ./daze --tokens caso_estudio.dz
  ```
- **Imprimir el árbol sintáctico (parse tree) en consola:**
  ```bash
  ./daze --tree caso_estudio.dz
  ```

### 6. Ejecución de la suite completa de pruebas
Para verificar la suite de 48 pruebas unitarias y de integración:

```bash
python3 -m unittest discover -s tests -p "test_*.py" -v
```
