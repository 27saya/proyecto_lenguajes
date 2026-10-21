# DaZe: DSL para analisis deportivo

Este repositorio contiene la implementación de **DaZe** (`.dz`), un lenguaje de dominio específico diseñado para modelar flujos reproducibles de análisis de datos deportivos, preparación de plantillas de jugadores y generación de pizarras de rendimiento.

El objetivo de DaZe es que cualquier persona interesada en analítica deportiva (como analistas de rendimiento, directores técnicos o cuerpos técnicos) pueda transformar datos de manera sencilla y declarativa mediante pipelines secuenciales (`|>`), utilizando palabras clave del mundo deportivo y sin tener que enredarse con código complejo de propósito general.

El proyecto utiliza **ANTLR4** para el front-end (análisis léxico y sintáctico) y **Python 3.11+** para el análisis semántico y la ejecución a través del patrón **Visitor**. Además, desarrollamos **nuestras propias librerías nativas** de procesamiento tabular y estadística descriptiva para no depender de librerías externas pesadas como pandas o numpy.

---

## Nuestras librerías propias (`src/core/`)

En lugar de usar librerías de terceros como pandas o numpy, construimos nuestras propias soluciones en Python dentro del módulo `src/core/`. Esto nos permitió entender de raíz cómo se representan y manipulan las estructuras de datos tabulares en memoria y cómo se aplican las operaciones sobre los datos.

### 1. `Tabla` (`src/core/tabla.py`)
Es nuestra clase principal para manejar conjuntos de datos bidimensionales (filas y columnas):
- **`csvread(ruta, separador=',', encabezado=verdadero)`**: Lee archivos delimitados utilizando el módulo nativo de CSV de Python, infiriendo automáticamente tipos de datos (enteros, decimales, booleanos `verdadero`/`falso` y valores `nulo`).
- **`csvsave(ruta, separador=',')`**: Escribe la tabla en disco y crea automáticamente las carpetas de salida si no existen.
- **`convocar(columnas)`**: Proyecta únicamente las columnas indicadas, validando que todas existan en el esquema.
- **`descartar(condicion)`**: Filtra registros aplicando funciones lógicas fila por fila.
- **`contratar(columnas_dict)`**: Crea o actualiza columnas calculadas a partir de expresiones.
- **`rebautizar(mapeo)`**: Cambia los nombres de variables existentes.
- **`clasificar(columnas, descendente)`**: Ordena las filas según una o varias columnas de forma ascendente o descendente.
- **`alinear(columnas_grupo)`**: Particiona la tabla en grupos según las variables clave (`GrupoTabla`).
- **`balance(agregaciones)`**: Aplica funciones de agregación por grupo o sobre la tabla entera para producir una nueva tabla resumen.
- **`sanear(reemplazos)`**: Imputa datos faltantes o nulos en columnas determinadas.
- **`depurar(columnas)`**: Limpia registros duplicados de la plantilla.
- **`top(n)`**: Conserva los primeros `n` registros.
- **`mostrar(limite=10)`**: Genera una vista en texto alineada con bordes ASCII para imprimir en la consola.

### 2. `Estadistica` (`src/core/estadistica.py`)
Módulo numérico puro que implementa cálculos descriptivos sin dependencias externas:
- **`suma(valores)`**: Acumula valores numéricos ignorando nulos.
- **`media(valores)`**: Calcula el promedio aritmético.
- **`mediana(valores)`**: Determina el valor central (o el promedio de los dos centrales si la cantidad es par).
- **`minimo(valores)`** y **`maximo(valores)`**: Encuentran los valores extremos.
- **`desviar(valores)`**: Calcula la desviación estándar muestral.
- **`contar(valores)`**: Cuenta la cantidad de registros válidos.

---

## Tabla de Símbolos y Ámbitos (`src/semantic/tabla_simbolos.py`)

Para que el intérprete sepa en todo momento qué variables, tablas y funciones existen, implementamos una `TablaSimbolos` jerárquica con soporte de ámbitos:
- **Ámbito global**: Almacena las tablas cargadas con `fichar`, los resultados de pipelines y las variables generales.
- **Ámbitos locales**: Se crean automáticamente al ejecutar funciones (`tactica`), aislando los parámetros y variables locales del resto del programa.
- **Validación de esquemas**: Cuando un símbolo es de tipo `TABLA`, la tabla de símbolos guarda el listado de columnas disponibles para validar rápidamente si una columna existe antes de intentar operarla.

---

## Intérprete semántico con patrón Visitor (`src/semantic/visitor.py`)

Heredando de `DaZeParserVisitor` (generado por ANTLR), `DaZeSemanticVisitor` recorre el árbol sintáctico y se encarga de:
1. **Evaluar expresiones**: Aritmética (`+`, `-`, `*`, `/`, `%`, `^`), comparaciones (`==`, `!=`, `<`, `>`, `<=`, `>=`) y lógica (`y`, `o`, `no`).
2. **Conectar columnas en pipelines**: Al ejecutar operaciones fila por fila (como en `descartar` o `contratar`), inyecta los valores de las columnas del registro actual para que las expresiones las resuelvan directamente.
3. **Controlar el flujo**: Ejecuta bloques `si` y `sino` según la condición evaluada.
4. **Ejecutar tácticas**: Gestiona llamadas a funciones, evalúa argumentos, crea el ámbito local y captura el valor de retorno emitido por `resultado`.
5. **Validar declaraciones de pizarra**: Revisa semánticamente que la tabla exista y que las columnas configuradas (como `eje_x` o `eje_y`) pertenezcan efectivamente a la plantilla.
6. **Reportar diagnósticos claros**: Si ocurre un error semántico (por ejemplo, usar una variable no definida o una columna que no está en la plantilla), reporta el mensaje exacto con el número de línea y columna.

---

## Características y sintaxis del lenguaje

### 1. Carga y guardado de datos
```daze
jugadores = fichar("datos/plantilla_temporada.csv", separador=",", encabezado=verdadero);
archivar(resumenposiciones, en="salidas/resumenposiciones.csv", separador=",");
```

### 2. Pipelines de transformación (`|>`)
Las operaciones se encadenan de forma limpia y legible:
```daze
jugadoresaptos = jugadores
    |> convocar(dorsal, club, posicion, minutos, goles, asistencias)
    |> descartar(minutos > 0 y goles >= 0)
    |> contratar(
        contribucion = goles + asistencias,
        promediogol = (goles * 90) / minutos,
        rendimientototal = (contribucion * 1.5) + (minutos / 100)
    )
    |> clasificar(por=[rendimientototal], descendente=verdadero);

resumenposiciones = jugadoresaptos
    |> alinear(por=[posicion])
    |> balance(
        golestotales = suma(goles),
        mediaasistencias = media(asistencias),
        medianaminutos = mediana(minutos),
        desviarendimiento = desviar(rendimientototal),
        totalconvocados = contar()
    );
```

### 3. Proyecciones en consola
```daze
proyectar("Resumen calculado exitosamente:");
proyectar(resumenposiciones);
```

### 4. Tácticas (funciones) y condicionales
```daze
tactica alertasobrecarga(frecuenciacardiaca, distanciakm) {
    si (frecuenciacardiaca > 185) {
        proyectar("Alerta: Sobrecarga cardiovascular detectada");
    } sino {
        proyectar("Rango aerobico optimo");
    }
    resultado frecuenciacardiaca * 1.05;
}

ajuste = alertasobrecarga(188, 10.5);
```

### 5. Pizarras visuales
```daze
pizarra barras(resumenposiciones) {
    eje_x = posicion;
    eje_y = golestotales;
    titulo = "Goles Totales por Posicion";
    color = "azul";
    guardar = "salidas/golesporposicion.png";
}
```

---

## Guía de ejecución (Linux)

### 1. Requisitos previos
Tener instalados Python 3.11 o superior, `python3-venv` y Java (JRE 11+ únicamente en caso de querer recompilar las gramáticas `.g4` de ANTLR): (usar apt solo si la distro lo permite, usa el package manager de la distro que tengas xd)

```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv openjdk-17-jre -y
```

### 2. Preparar el entorno virtual
Se recomienda aislar el entorno de trabajo para evitar conflictos con dependencias existentes:

```bash
cd Proyecto_lenguajes
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias
Instalar el runtime de ANTLR4 (nuestro motor de datos y estadísticas no requiere paquetes externos adicionales):

```bash
pip install -r requirements.txt
```

### 4. Ejecutar un programa en DaZe

```bash
python3 src/cli.py examples/correcto_ventas.dz
python3 src/cli.py examples/correcto_sensores.dz
python3 src/cli.py examples/correcto_estudiantes.dz
```

Al ejecutarse, el flujo procesa los datos, muestra las tablas y mensajes en consola, valida las especificaciones de las pizarras y genera los archivos CSV correspondientes dentro del directorio `salidas/`.

### 5. Opciones adicionales (opcionales)
- **Solo validar sintaxis sin ejecutar:**
  ```bash
  python3 src/cli.py --check examples/correcto_ventas.dz
  ```
- **Ver la secuencia de tokens reconocidos por el lexer:**
  ```bash
  python3 src/cli.py --tokens examples/correcto_ventas.dz
  ```
- **Imprimir el árbol sintáctico (parse tree) en formato texto:**
  ```bash
  python3 src/cli.py --tree examples/correcto_ventas.dz
  ```
- **Probar el diagnóstico de errores semánticos:**
  ```bash
  python3 src/cli.py examples/incorrecto_semantico_variable.dz
  python3 src/cli.py examples/incorrecto_semantico_columna.dz
  python3 src/cli.py examples/incorrecto_semantico_tipos.dz
  ```

### 6. Ejecución de pruebas
Para correr todas las pruebas

```bash
python3 -m unittest discover -s tests -p "test_*.py" -v
```

### 7. Regeneración de la gramática (opcional)
Los archivos de ANTLR ya se encuentran generados en `src/generated/`. Sin embargo, si se modifican `grammar/DaZeLexer.g4` o `grammar/DaZeParser.g4`, se pueden recompilar con:

```bash
antlr4 -Dlanguage=Python3 -visitor -o src/generated grammar/DaZeLexer.g4 grammar/DaZeParser.g4
```
