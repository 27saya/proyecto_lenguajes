"""
Modulo de Machine Learning y Metodos Numericos Puros para DaZe.
Implementado sin dependencias externas (sin numpy, scipy ni scikit-learn).
"""


def _raiz(n, tolerancia=1e-12):
    """Raiz cuadrada por algoritmo iterativo de Newton-Raphson."""
    if n < 0:
        raise ValueError("No se puede calcular raiz de numero negativo")
    if n == 0:
        return 0.0
    x = n / 2.0 if n >= 1 else 1.0
    for _ in range(100):
        sig = 0.5 * (x + n / x)
        if abs(x - sig) < tolerancia:
            return sig
        x = sig
    return x


def correlacion_pearson(x, y):
    """Calcula el coeficiente de correlacion r de Pearson en [-1.0, 1.0]."""
    if len(x) != len(y) or len(x) < 2:
        return 0.0
    n = len(x)
    media_x = sum(x) / n
    media_y = sum(y) / n

    num = sum((xi - media_x) * (yi - media_y) for xi, yi in zip(x, y))
    den_x = sum((xi - media_x) ** 2 for xi in x)
    den_y = sum((yi - media_y) ** 2 for yi in y)

    denominador = _raiz(den_x * den_y)
    if denominador == 0:
        return 0.0
    return num / denominador


# Alias de correlacion
correlacion = correlacion_pearson


class RegresionLineal:
    """Modelo de regresion lineal simple (y = mx + b) por Minimos Cuadrados Ordinarios."""

    def __init__(self):
        self.m = 0.0
        self.b = 0.0
        self.r2 = 0.0

    def __getitem__(self, clave):
        if hasattr(self, clave):
            return getattr(self, clave)
        raise KeyError(clave)

    def ajustar(self, x, y):
        n = len(x)
        if n < 2 or n != len(y):
            raise ValueError("Se requieren al menos 2 pares de datos para ajustar regresion.")

        media_x = sum(x) / n
        media_y = sum(y) / n

        num = sum((xi - media_x) * (yi - media_y) for xi, yi in zip(x, y))
        den = sum((xi - media_x) ** 2 for xi in x)

        self.m = (num / den) if den != 0 else 0.0
        self.b = media_y - (self.m * media_x)

        ss_tot = sum((yi - media_y) ** 2 for yi in y)
        ss_res = sum((yi - (self.m * xi + self.b)) ** 2 for xi, yi in zip(x, y))
        if ss_tot == 0:
            self.r2 = 1.0 if ss_res == 0 else 0.0
        else:
            self.r2 = max(0.0, min(1.0, 1.0 - (ss_res / ss_tot)))

        return self

    def predecir(self, x_val):
        return self.m * x_val + self.b


def regresion_lineal(x, y):
    """Ajusta una regresion lineal simple y retorna metricas en un diccionario."""
    modelo = RegresionLineal()
    modelo.ajustar(x, y)
    return {
        "m": modelo.m,
        "b": modelo.b,
        "r2": modelo.r2,
        "modelo": modelo
    }


def predecir_regresion(modelo, x_val):
    """Estima el valor de y para un x_val dado a partir de un modelo de regresion."""
    if isinstance(modelo, dict):
        if "m" in modelo and "b" in modelo:
            return modelo["m"] * x_val + modelo["b"]
        elif "modelo" in modelo:
            return modelo["modelo"].predecir(x_val)
    elif hasattr(modelo, "predecir"):
        return modelo.predecir(x_val)
    raise ValueError("Objeto de modelo no valido para inferencia")


class KMeans:
    """Algoritmo de clustering no supervisado en D dimensiones."""

    def __init__(self, k=2, max_iter=20):
        self.k = k
        self.max_iter = max_iter
        self.centroides = []
        self.etiquetas = []

    def __getitem__(self, clave):
        if hasattr(self, clave):
            return getattr(self, clave)
        raise KeyError(clave)

    def _distancia_euclidiana(self, p1, p2):
        return _raiz(sum((a - b) ** 2 for a, b in zip(p1, p2)))

    def ajustar(self, datos):
        if not datos or self.k <= 0:
            return self

        k = min(self.k, len(datos))
        self.centroides = [list(datos[i]) for i in range(k)]
        self.etiquetas = [0] * len(datos)
        dim = len(datos[0])

        for _ in range(self.max_iter):
            nuevas_etiquetas = []
            for punto in datos:
                distancias = [self._distancia_euclidiana(punto, c) for c in self.centroides]
                min_idx = distancias.index(min(distancias))
                nuevas_etiquetas.append(min_idx)

            clusters = {i: [] for i in range(k)}
            for idx, c_idx in enumerate(nuevas_etiquetas):
                clusters[c_idx].append(datos[idx])

            nuevos_centroides = []
            for i in range(k):
                if clusters[i]:
                    n_puntos = len(clusters[i])
                    nuevo_c = [sum(p[d] for p in clusters[i]) / n_puntos for d in range(dim)]
                else:
                    nuevo_c = self.centroides[i]
                nuevos_centroides.append(nuevo_c)

            self.centroides = nuevos_centroides
            if nuevas_etiquetas == self.etiquetas:
                break
            self.etiquetas = nuevas_etiquetas

        return self


def agrupar_kmedias(datos, k=2, max_iter=20):
    """Ejecuta agrupamiento K-Means y retorna centroides y etiquetas."""
    km = KMeans(k=k, max_iter=max_iter)
    km.ajustar(datos)
    return {
        "centroides": km.centroides,
        "etiquetas": km.etiquetas,
        "modelo": km
    }


# Alias sin guiones bajos para uso comodo en el DSL
regresionlineal = regresion_lineal
predecir = predecir_regresion
agruparkmedias = agrupar_kmedias
kmedias = agrupar_kmedias


class PerceptronMulticapaXOR:
    """
    Red Neuronal Multicapa (MLP) para resolver el problema no lineal XOR.
    Arquitectura: 2 entradas -> 2 neuronas ocultas (sigmoide) -> 1 salida (sigmoide).
    Entrenamiento puro mediante retropropagacion (backpropagation).
    """

    def __init__(self):
        self.w_ih = [[0.5, -0.5], [-0.5, 0.5]]
        self.b_h = [0.0, 0.0]
        self.w_ho = [0.5, 0.5]
        self.b_o = 0.0
        self.historial = []

    def __getitem__(self, clave):
        if hasattr(self, clave):
            return getattr(self, clave)
        if clave == "modelo":
            return self
        if clave == "predicciones":
            return self.evaluar_tabla()
        raise KeyError(clave)

    def _sigmoide(self, x):
        from .matematica import exp
        if x < -50:
            return 0.0
        if x > 50:
            return 1.0
        return 1.0 / (1.0 + exp(-x))

    def _d_sigmoide(self, y):
        return y * (1.0 - y)

    def ajustar(self, epocas=6000, lr=0.8):
        import random
        random.seed(42)
        self.w_ih = [[random.uniform(-1.0, 1.0) for _ in range(2)] for _ in range(2)]
        self.b_h = [random.uniform(-1.0, 1.0) for _ in range(2)]
        self.w_ho = [random.uniform(-1.0, 1.0) for _ in range(2)]
        self.b_o = random.uniform(-1.0, 1.0)

        X = [[0, 0], [0, 1], [1, 0], [1, 1]]
        Y = [0, 1, 1, 0]

        historial_perdida = []
        intervalo = max(1, epocas // 10)

        for epoca in range(epocas):
            error_total = 0.0
            for x, y_target in zip(X, Y):
                # Propagacion hacia adelante
                h_net = [x[0] * self.w_ih[0][j] + x[1] * self.w_ih[1][j] + self.b_h[j] for j in range(2)]
                h_out = [self._sigmoide(val) for val in h_net]

                o_net = h_out[0] * self.w_ho[0] + h_out[1] * self.w_ho[1] + self.b_o
                o_out = self._sigmoide(o_net)

                err = y_target - o_out
                error_total += err ** 2

                # Retropropagacion del error
                delta_o = err * self._d_sigmoide(o_out)
                delta_h = [delta_o * self.w_ho[j] * self._d_sigmoide(h_out[j]) for j in range(2)]

                # Actualizacion capa de salida
                for j in range(2):
                    self.w_ho[j] += lr * delta_o * h_out[j]
                self.b_o += lr * delta_o

                # Actualizacion capa oculta
                for i in range(2):
                    for j in range(2):
                        self.w_ih[i][j] += lr * delta_h[j] * x[i]
                for j in range(2):
                    self.b_h[j] += lr * delta_h[j]

            mse = error_total / 4.0
            if epoca % intervalo == 0 or epoca == epocas - 1:
                historial_perdida.append({"epoca": epoca, "perdida": round(mse, 6)})

        self.historial = historial_perdida
        return self

    def predecir(self, x):
        h_net = [x[0] * self.w_ih[0][j] + x[1] * self.w_ih[1][j] + self.b_h[j] for j in range(2)]
        h_out = [self._sigmoide(val) for val in h_net]
        o_net = h_out[0] * self.w_ho[0] + h_out[1] * self.w_ho[1] + self.b_o
        return round(self._sigmoide(o_net), 4)

    def evaluar_tabla(self):
        casos = [[0, 0], [0, 1], [1, 0], [1, 1]]
        esperados = [0, 1, 1, 0]
        filas = []
        for x, y_esp in zip(casos, esperados):
            y_pred = self.predecir(x)
            filas.append({
                "x1": x[0],
                "x2": x[1],
                "esperado": y_esp,
                "estimado": y_pred,
                "clasificacion": 1 if y_pred >= 0.5 else 0
            })
        return filas


def entrenar_mlp_xor(epocas=6000, lr=0.8):
    """Entrena un perceptron multicapa para XOR y retorna el modelo e historial."""
    mlp = PerceptronMulticapaXOR()
    mlp.ajustar(epocas=epocas, lr=lr)
    return {
        "modelo": mlp,
        "historial": mlp.historial,
        "predicciones": mlp.evaluar_tabla(),
        "_modelo": mlp
    }


def predecir_mlp(modelo, x):
    """Estima la salida de un vector x usando el perceptron multicapa."""
    if isinstance(modelo, dict):
        if "modelo" in modelo:
            return modelo["modelo"].predecir(x)
        if "_modelo" in modelo:
            return modelo["_modelo"].predecir(x)
    if hasattr(modelo, "predecir"):
        return modelo.predecir(x)
    raise ValueError("Objeto de modelo MLP no valido para inferencia.")


mlp_xor = entrenar_mlp_xor

