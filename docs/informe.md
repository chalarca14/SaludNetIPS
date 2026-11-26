# Informe científico breve — Equipo __

**Título:** · **Integrantes:** · **Fecha:** · **Repositorio:**

## Resumen (≤ 150 palabras)
Problema, método, resultado principal con cifras y unidades, conclusión.

## 1. Introducción
Problema empresarial y pregunta de investigación. Principios físicos involucrados (con fórmulas y unidades).

## 2. Hipótesis
H1, H2... (copiadas de docs/hipotesis.md, sin modificarlas después de ver los datos).

## 3. Método
- Estrategias comparadas (descripción, no código completo).
- Variables independientes, dependientes y controladas.
- Entorno (tabla de docs/entorno.md). Instrumentos y su resolución.
- Protocolo: tamaños, repeticiones, calentamiento, orden aleatorio.

## 4. Resultados

**Origen de cada dato:**
- **SIMULADO:** los datos de entrada (lecturas de 200 sensores generadas por `src/generar_datos.py` con semilla 4).
- **MEDIDO:** tiempos (s) y picos de memoria (MiB), en el PC del Integrante A el 25/11/2026 (`resultados/resultados.csv`,
  99 filas = 90 de tiempo + 9 de memoria; entorno en `docs/entorno.md`).
- **ESTIMADO:** ciclos por registro N / n = f · t / n, con f = 2.2 GHz reportada por psutil (no ve el turbo).

**Cómo se calculó** (`python -m experimentos.analizar_resultados`):
- **Tiempo:** solo las 10 corridas con `medicion_memoria = no` por estrategia y n. La corrida de memoria se excluye porque
  tracemalloc infla su tiempo (D-001). Media, desviación estándar muestral s, CV = s / media × 100 e
  IC95 % = media ± 2.262 × s / √10 (t de Student, gl = 9).
- **Memoria:** solo la corrida con `medicion_memoria = si` (k = 1). No tiene desviación ni IC95 % porque una sola medición
  no permite estimar la variación; se justifica porque el pico salió idéntico en 3 corridas previas (D-001).

### 4.1 Tabla resumen

| Estrategia | n | Tiempo medio (s) | s (s) | CV (%) | IC95 % del tiempo (s) | Pico de memoria (MiB) | Ciclos por registro (estimados) |
|---|---|---|---|---|---|---|---|
| A (línea base) | 200 000 | 0.1608 | 0.0055 | 3.41 | [0.1569; 0.1648] | 78.183 | 1 769 |
| A (línea base) | 500 000 | 0.4540 | 0.0119 | 2.62 | [0.4455; 0.4625] | 195.637 | 1 998 |
| A (línea base) | 1 000 000 | 0.9458 | 0.0128 | 1.36 | [0.9367; 0.9550] | 391.632 | 2 081 |
| B (acumuladores) | 200 000 | 0.0843 | 0.0020 | 2.34 | [0.0829; 0.0858] | 0.205 | 928 |
| B (acumuladores) | 500 000 | 0.2159 | 0.0043 | 2.01 | [0.2128; 0.2190] | 0.205 | 950 |
| B (acumuladores) | 1 000 000 | 0.4257 | 0.0081 | 1.91 | [0.4198; 0.4315] | 0.205 | 936 |
| C (array d) | 200 000 | 0.0872 | 0.0010 | 1.18 | [0.0865; 0.0879] | 1.761 | 959 |
| C (array d) | 500 000 | 0.2234 | 0.0040 | 1.79 | [0.2205; 0.2262] | 4.110 | 983 |
| C (array d) | 1 000 000 | 0.4374 | 0.0048 | 1.09 | [0.4340; 0.4408] | 8.022 | 962 |

Los CV del tiempo están entre **1.09 % y 3.41 %**: todas las combinaciones cumplen el criterio del protocolo (CV ≤ 10 %).
Tabla completa (con mínimo, máximo, bytes por registro y pendientes) en `resultados/resumen_estadistico.csv`.

### 4.2 Gráfico 1: tiempo vs. n (log-log)

![Tiempo vs. n en escala log-log con IC95 %](../resultados/grafico_1_tiempo_vs_n_loglog.png)

[`resultados/grafico_1_tiempo_vs_n_loglog.png`](../resultados/grafico_1_tiempo_vs_n_loglog.png). Pendiente del ajuste
lineal de log(t) vs. log(n): **A = 1.102**, **B = 1.007**, **C = 1.003**. Una pendiente cercana a 1 significa que el tiempo
crece en proporción directa a n (si n se multiplica por 5, t también). Las barras de IC95 % son más pequeñas que los marcadores.

### 4.3 Gráfico 2: comparación con n = 1 000 000

![Comparación de tiempo y memoria con n = 1 000 000](../resultados/grafico_2_comparacion_n1M.png)

[`resultados/grafico_2_comparacion_n1M.png`](../resultados/grafico_2_comparacion_n1M.png). Con n = 1 000 000, B tarda el
**45.0 %** del tiempo de A y C el **46.2 %**; el pico de memoria de B es el **0.052 %** del de A y el de C el **2.05 %**.

### 4.4 Decisión sobre las hipótesis

Detalle del criterio y de los cálculos en `docs/hipotesis.md` (sección "Evaluación de las hipótesis").

| Id | Predicción | Resultado (MEDIDO) | Criterio | Estado |
|---|---|---|---|---|
| H1 | M_B < 0.10 × M_A con n = 1 000 000 | 0.205 MiB < 39.163 MiB; M_B / M_A = 0.000523 | Comparación directa, k = 1 (D-001) | **Se confirma** |
| H2 | M(1 000 000) / M(200 000): A y C entre 4 y 6; B entre 0.8 y 1.2 | A = 5.009 · C = 4.555 · B = 1.000 | Los tres cocientes dentro de su rango | **Se confirma** |
| H3 | t_B ≤ 0.80 × t_A con n = 1 000 000 | t_B / t_A = 0.450; peor caso con IC95 % = 0.461. Welch: t = 108.34, gl = 15.21, p < 1e-15; d de Cohen = 48.45 | Welch p < 0.05 y peor caso ≤ 0.80 | **Se confirma** |

**Alcance:** las tres decisiones valen solo para este PC, con estos datos simulados y para n entre 200 000 y 1 000 000. Los
tiempos no se pueden trasladar al servidor de 2 GiB de la empresa; los picos de memoria dependen poco del equipo.

**No se midió:** temperatura ni energía (el PC no las expone; ver `docs/entorno.md`). El uso de CPU del proceso estuvo entre
96.7 % y 100.2 % de un núcleo en promedio por combinación (ver `docs/analisis_preliminar.md`).

## 5. Discusión
- ¿Se confirma o refuta cada hipótesis? Criterio usado.
- Explicación física de los resultados.
- Limitaciones de la medición y amenazas a la validez.

## 6. Propuesta de mejora para la empresa
Recomendación cuantificada, condiciones en que es válida y riesgos.

## 7. Conclusiones

## 8. Referencias (verificables)
## Anexo: uso de IA (resumen de docs/uso_ia.md)
