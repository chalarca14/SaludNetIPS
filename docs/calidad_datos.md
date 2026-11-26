# Calidad de los datos (Clase 5, pasos 1 y 3)

**Responsable:** Santiago (R1) · **Fecha:** 25/11/2026 · **Datos:** `resultados/resultados.csv` y `resultados/monitor.csv`
(experimento formal del 25/11/2026, 11:39 – 11:40, PC del Integrante A).

## Paso 1. Inspección del CSV

**Filas:** 99 = 90 de tiempo (`medicion_memoria = no`, repeticiones 1 a 10) + 9 de memoria (`medicion_memoria = si`,
repetición 0). Es lo que el protocolo esperaba (3 estrategias × 3 tamaños × 10 + 9). **No falta ninguna fila.**

| Columna | Unidad | ¿Tiene datos? | Comentario |
|---|---|---|---|
| `marca_tiempo` | fecha y hora | 99 de 99 | Todas distintas, de 11:39:52.8 a 11:40:46.9 |
| `equipo` | — | 99 de 99 | Siempre "Equipo 4" |
| `estrategia` | — | 99 de 99 | `A_linea_base`, `B_acumuladores`, `C_array_d` |
| `n` | registros | 99 de 99 | 200 000, 500 000 y 1 000 000 |
| `repeticion` | — | 99 de 99 | 0 (memoria) y 1 a 10 (tiempo) |
| `tiempo_s` | s | 99 de 99 | Todos mayores que 0. En las filas de memoria está inflado por tracemalloc (D-001): **no se usa** |
| `cpu_proceso_s` | s | 99 de 99 | Solo 30 valores distintos: en Windows avanza de a 15.625 ms (1/64 s) |
| `uso_cpu_pct` | % | 99 de 99 | Entre 72 % y 115 % por la resolución de `cpu_proceso_s`; el promedio por combinación está entre 96.7 % y 100.2 % |
| `pico_mem_mib` | MiB | 9 de 99 | Solo en las filas de memoria, como debe ser |
| `rss_mib` | MiB | 99 de 99 | Memoria total del proceso (77 – 101 MiB): incluye el intérprete de Python |
| `frecuencia_mhz` | MHz | 99 de 99 | Siempre 2200.0: psutil no ve el turbo |
| `temperatura_c` | °C | 0 de 99 | **Vacía:** el PC no expone temperatura (plan B en `docs/entorno.md`) |
| `energia_j`, `potencia_w` | J, W | 0 de 99 | **Vacías:** no hay RAPL en Windows. No se afirma nada sobre energía |
| `medicion_memoria` | — | 99 de 99 | "si" o "no" |
| `observacion` | — | 9 de 99 | "corrida de memoria" en las 9 filas de memoria |

**Corridas de memoria:** hay una por combinación (9). Su `tiempo_s` es entre 6.9 y 9.1 veces más largo que el de las
corridas normales porque tracemalloc vigila cada reserva de memoria. Por eso el tiempo se analiza solo con las
filas `medicion_memoria = no`.

## Paso 3. Revisión de atípicos

**Criterio del protocolo:** si una combinación tiene CV > 10 %, se busca la causa. Los atípicos (regla de Tukey) se
reportan, y **solo se excluyen si hay una causa documentada**.

**Resultado:** **ninguna combinación pasa del 10 % de CV** (el mayor es 3.4 %, en A con n = 200 000).

La regla de Tukey (fuera del rango Q1 − 1.5·IQR a Q3 + 1.5·IQR) se aplicó de dos formas, porque los cuartiles
se pueden calcular con dos métodos:
- **Script del curso** `herramientas/analizar_resultados.py` (usa `estadistica.py`, método *exclusive*, el que trae
  Python por defecto): marca **4 corridas** de 90 (A 200 000 rep. 9, B 200 000 rep. 1, A 500 000 rep. 4 y
  B 1 000 000 rep. 7). Este es el resultado oficial.
- **Revisión propia** con el método *inclusive* (rango un poco más estrecho): marca **7 corridas**, que incluyen las 4
  anteriores. Se dejan todas en la tabla para mostrar que ni siquiera con el criterio más estricto cambia la decisión.

| Combinación | Repetición | Tiempo (s) | Diferencia con la mediana | CPU del sistema en ese momento (monitor) | Media con ella → sin ella |
|---|---|---|---|---|---|
| A, n = 200 000 | 9 | 0.1743 | +9.3 % | 14 – 22 % | 0.1608 → 0.1594 s (−0.9 %) |
| B, n = 200 000 | 1 | 0.0889 | +5.6 % | 22 % | 0.0843 → 0.0841 s (−0.3 %) |
| B, n = 200 000 | 10 | 0.0815 | −3.1 % | 16 – 22 % | (incluida en la fila anterior) |
| C, n = 200 000 | 7 | 0.0892 | +2.1 % | 17 – 25 % | 0.0872 → 0.0870 s (−0.3 %) |
| A, n = 500 000 | 4 | 0.4820 | +6.8 % | 18 – 22 % | 0.4540 → 0.4509 s (−0.7 %) |
| B, n = 500 000 | 6 | 0.2250 | +4.6 % | 13 – 19 % | 0.2159 → 0.2149 s (−0.5 %) |
| B, n = 1 000 000 | 7 | 0.4446 | +4.7 % | 12 – 14 % | 0.4257 → 0.4236 s (−0.5 %) |

**Decisión: no se excluye ninguna corrida.**
1. No hay **causa documentada**: en esos momentos el monitor muestra el CPU del sistema normal (12 – 25 %; la
   mediana de todo el experimento fue 15.8 %) y no hay incidentes anotados en el protocolo.
2. Son diferencias **pequeñas** (máximo 9.3 %). Tukey marca varios puntos porque, con 10 datos tan parecidos entre sí,
   el rango "normal" (IQR) es muy estrecho.
3. Quitarlas cambiaría la media **menos de 1 %**, así que no cambian ninguna conclusión.

La posible causa de estos pequeños saltos (sin comprobar) son interrupciones de Windows y de los programas que seguían
en segundo plano (ver D-003). Es un **error aleatorio**: unas veces sube y otras baja (la repetición 10 de B fue más rápida).

**Único pico del monitor:** 49.2 % de CPU del sistema a los ≈ 6 s de iniciar (≈ 11:39:51). Fue **antes de la primera
medición** (11:39:52.8), mientras se preparaban los datos y se hacía la verificación de corrección y el calentamiento,
así que no afecta ninguna corrida.

> Nota: la hora de inicio del monitor (≈ 11:39:45) se calculó con la hora de la última escritura del archivo menos el
> tiempo registrado (81.1 s). Es una estimación de ± 1 s; por eso se compara con las muestras de ± 1 s alrededor.
