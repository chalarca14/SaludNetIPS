# Propuesta de mejora para SaludNet IPS (Clase 5, paso 7)

**Responsable:** Santiago (R1) · **Fecha:** 25/11/2026 · **Evidencia:** `resultados/resultados.csv` (experimento formal,
PC del Integrante A) y `docs/calidad_datos.md`.

> **Medido / estimado / simulado:** los picos de memoria y los tiempos son **medidos**. Los registros que caben en
> 2 GiB y los días de datos son **estimaciones** (suponen que la memoria sigue creciendo en línea recta). Los datos
> de entrada son **simulados** (`src/generar_datos.py`): una lectura cada 0.5 s.

## 1. Recomendación
**Cambiar el tablero a la estrategia B (procesar línea por línea).** Si en el futuro el tablero necesita
estadísticas que requieren todas las lecturas (por ejemplo la mediana), usar la **estrategia C** para esa parte.

## 2. Por qué (cuantificado, con n = 1 000 000)

| | A (actual) | B (recomendada) | C (alternativa) |
|---|---|---|---|
| Pico de memoria (medido) | 391.6 MiB | **0.205 MiB** | 8.02 MiB |
| Memoria por registro | ≈ 410.7 B | no depende de n | ≈ 8.41 B |
| Ahorro de memoria frente a A | — | **99.95 %** (≈ 1 900 veces menos) | 98.0 % (≈ 49 veces menos) |
| Tiempo medio (medido, 10 corridas) | 0.946 s | **0.426 s** | 0.437 s |
| Ahorro de tiempo frente a A | — | **55 %** | 54 % |
| Registros que caben en 2 GiB (estimado) | ≈ 5.2 millones | sin límite por memoria | ≈ 255 millones |
| Con 1 lectura cada 0.5 s (simulado), eso es | **≈ 30 días** de datos | sin límite por memoria | ≈ 4 años |

**Lo que significa para la empresa:**
- Con la estrategia actual (A), **un mes de lecturas** (≈ 5.2 millones de registros ≈ 2 GiB) ya llena el servidor, y
  eso sin contar lo que usan el sistema operativo y el resto del tablero, así que en la práctica falla **antes**.
  Esto explica el problema descrito en el README §1.
- Con B, el resumen ocupa unos **0.2 MiB sin importar cuántos días de datos haya**: el servidor de 2 GiB deja de
  quedarse sin memoria por este motivo.
- Además, B tarda **un 55 % menos** en este PC (0.43 s contra 0.95 s por cada millón de registros).

## 3. Por qué funciona (física)
La RAM tiene un número limitado de celdas (2 GiB = 2 147 483 648 B en el servidor). A guarda **todos** los registros a
la vez como diccionarios con 4 textos (≈ 411 B cada uno), así que la memoria crece con n: M ≈ n × 411 B. B no guarda
los registros: solo suma, cantidad y máxima de los 200 sensores, así que M casi no depende de n. Y como B no crea un
diccionario por línea, el procesador hace menos operaciones: ≈ 936 ciclos por registro contra ≈ 2 081 de A
(estimación con N = f · t, f = 2.2 GHz).

## 4. Condiciones de validez (cuándo aplica esta recomendación)
1. El tablero solo necesita **media y máxima por sensor** (lo que calculan A, B y C). Para la mediana, percentiles o
   gráficos de todas las lecturas, B no sirve: usar C.
2. Medido en **Python 3.14.3** en el PC del Integrante A (15.63 GiB). El **pico de memoria casi no depende del equipo**
   (A dio 78.183 MiB con n = 200 000 en el PC de Andres y en el del Integrante A), pero **el tiempo sí**: en el servidor
   los tiempos serán distintos; lo que se mantiene es que B es más rápida que A.
3. Probado hasta **n = 1 000 000**. Los 5.2 millones y los 30 días son una **extrapolación** que supone crecimiento
   lineal (H2 lo apoya: la memoria de A creció 5.01 veces cuando n creció 5 veces).
4. tracemalloc solo mide la memoria que reserva Python; el proceso completo usa más (`rss_mib` ≈ 77 – 101 MiB, que
   incluye el intérprete). La comparación entre estrategias es justa porque se midió igual en las tres.
5. Los datos de entrada son simulados; con datos reales (otros formatos o tamaños de línea) hay que repetir la medición.

## 5. Riesgos
| Riesgo | Por qué importa | Cómo mitigarlo |
|---|---|---|
| **B y C saltan líneas dañadas sin avisar** | Probado el 25/11/2026 con un CSV de prueba con una línea incompleta: A se detiene con error (`KeyError`), pero B y C la ignoran en silencio. En un tablero de vacunas, perder lecturas sin enterarse es peligroso | Contar las líneas saltadas y mostrar una alerta o guardarlas en un registro (cambio pendiente para R3) |
| B no guarda las lecturas | Si mañana piden otra estadística, hay que volver a leer todo el archivo | Usar C para esa parte, o leer el archivo otra vez (B es rápida) |
| El servidor no es el PC donde se midió | Los tiempos pueden cambiar | Repetir el experimento en el servidor antes de cambiar el tablero en producción |
| Archivos con más de 1 000 000 de registros | No se midió | Medir con n más grandes; con B se espera que la memoria siga constante |

## 6. Lo que NO afirmamos
- **No decimos que B ahorre energía.** Probablemente sí (menos operaciones), pero este PC no mide energía
  (sin RAPL), así que no hay evidencia.
- No damos el tiempo exacto en el servidor: solo que B es más rápida que A en el mismo equipo.
