# Especificacion del Lenguaje DaZe (.dz) - Sports Analytics DSL

## 1. Delimitacion del Dominio y Casos de Uso

DaZe es un lenguaje de dominio especifico (DSL) disenado para modelar flujos de trabajo reproducibles en analitica deportiva, preparacion de plantillas y generacion de pizarras tacticas. El lenguaje combina una sintaxis funcional/declarativa basada en pipelines (`|>`) con una estructura en espanol adaptada al ambito tecnico del deporte, facilitando el diseno de transformaciones sin requerir codigo complejo de proposito general.

### Perfil de Usuarios
- Analistas de rendimiento, directores tecnicos y cuerpos tecnicos deportivos.
- Desarrolladores e investigadores que requieran procesar telemetria, estadisticas de jugadores y metricas de partidos de forma compacta y legible.

### Entradas y Salidas
- **Entradas**: Archivos tabulares en formato CSV con metricas de rendimiento deportivo (con soporte de delimitadores y encabezados), literales escalares y expresiones evaluadas.
- **Salidas**: Tablas transformadas y consolidadas exportables a CSV, declaraciones estructuradas de pizarras visuales (barras, lineas, histogramas, dispersion, caja) y proyecciones en consola.

### Restricciones
- El lenguaje no busca ser un sustituto de proposito general para Python, sino un DSL declarativo enfocado en analisis y rendimiento deportivo.
- Toda operacion en un pipeline recibe una plantilla/conjunto de datos y genera una nueva transformacion sin mutacion destructiva de estados anteriores.

---

## 2. Tipos de Datos y Literales

| Tipo | Descripcion | Sintaxis / Ejemplos |
|---|---|---|
| Entero | Valores numericos enteros | `10`, `0`, `-5` |
| Decimal | Valores numericos en punto flotante | `3.1416`, `0.05`, `99.9` |
| Cadena | Texto delimitado por comillas simples o dobles | `"plantilla.csv"`, `'Delantero'` |
| Booleano | Valores logicos | `verdadero`, `falso`, `true`, `false` |
| Nulo | Ausencia de registro o valor faltante | `nulo`, `null` |
| Lista | Coleccion de elementos o columnas | `[dorsal, goles]`, `["A", "B"]` |
| Tabla | Coleccion tabular cargada o derivada | Resultado de `fichar(...)` o `|>` |

---

## 3. Operadores y Precedencia

### Aritmeticos
- Potencia: `^` o `**` (asociatividad a derecha)
- Unarios: `+`, `-`, `no` / `not` / `!`
- Multiplicativos: `*`, `/`, `%`
- Aditivos: `+`, `-`

### Relacionales
- Comparaciones: `<`, `<=`, `>`, `>=`
- Igualdad: `==`, `!=`

### Logicos
- Conjuncion: `y`, `and`, `&&`
- Disyuncion: `o`, `or`, `||`
- Negacion: `no`, `not`, `!`

---

## 4. Catalogo de Instrucciones y Palabras Reservadas

### 4.1. Carga y Guardado de Datos
- **`fichar(ruta, ...)`**: Carga una plantilla desde disco. Permite configurar argumentos con nombre como `separador=","` y `encabezado=verdadero`.
  ```daze
  datos = fichar("datos/plantilla_temporada.csv", separador=",", encabezado=verdadero);
  ```
- **`archivar(tabla, en=ruta, ...)`**: Exporta la tabla de datos a un archivo CSV en disco.
  ```daze
  archivar(resumenposiciones, en="salidas/resumenposiciones.csv", separador=",");
  ```
- **`proyectar(expr)`**: Imprime una expresion, texto o el contenido tabular formateado en la consola.
  ```daze
  proyectar("Resumen calculado:");
  proyectar(resumenposiciones);
  ```

### 4.2. Operaciones de Pipeline (`|>`)
Las operaciones sobre tablas deportivas se encadenan mediante el operador tubería (`|>`):
- **`convocar(...)`**: Selecciona y proyecta un subconjunto de columnas.
- **`descartar(...)`**: Filtra filas mediante expresiones lógicas evaluadas sobre cada registro.
- **`contratar(...)`**: Agrega o actualiza columnas calculadas a partir de expresiones aritméticas.
- **`rebautizar(...)`**: Renombra columnas existentes en la plantilla.
- **`clasificar(...)`**: Ordena los registros según una o varias columnas (con `descendente=verdadero` o `ascendente=verdadero`).
- **`alinear(...)`**: Agrupa registros por una o varias columnas clave.
- **`balance(...)`**: Aplica funciones de agregación (`suma`, `media`, `mediana`, `minimo`, `maximo`, `desviar`, `contar`) por grupo o sobre la tabla entera.
- **`sanear(...)`** (o `recuperar`): Imputa valores nulos o faltantes en columnas específicas.
- **`depurar(...)`** (o `limpiar`): Elimina registros duplicados en la plantilla.
- **`top(n)`**: Limita la salida a los primeros `n` registros de la tabla.

### 4.3. Control de Flujo y Funciones (Tácticas)
- **`tactica nombre(params) { ... }`**: Define una función reutilizable de análisis deportivo con ámbito local.
- **`resultado expr;`**: Retorna el valor evaluado de la táctica.
- **`si (condicion) { ... } sino { ... }`**: Bifurcación condicional.

### 4.4. Declaración de Pizarras Visuales
- **`pizarra tipo(tabla) { config }`**: Especifica declaraciones de representaciones gráficas (`barras`, `lineas`, `histograma`, `dispersion`, `caja`), validando semánticamente que la tabla y las columnas indicadas pertenezcan al contexto deportivo.
