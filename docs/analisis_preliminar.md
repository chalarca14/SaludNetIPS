# Análisis preliminar del experimento formal (Clase 4)

**Datos:** `resultados/resultados.csv` (99 filas: 90 de tiempo + 9 de memoria) · **Equipo:** PC del Integrante A
(ver `docs/entorno.md`) · **Fecha:** 25/11/2026, 11:39 – 11:40 · **Monitoreo:** `resultados/monitor.csv`

> Es un análisis **preliminar** (media, desviación y CV). El análisis estadístico completo con IC95 % y los
> gráficos se hacen en la Clase 5 (issue #4). Los datos de entrada son **SIMULADOS** (`src/generar_datos.py`,
> semilla 4); las mediciones de tiempo y memoria sí son reales, hechas en este PC.

## 1. Resumen
Tiempo: promedio de 10 corridas sin tracemalloc. Memoria: 1 corrida con tracemalloc (decisión D-001).

| Estrategia | n | Tiempo medio (s) | Desviación (s) | CV | Pico de memoria (MiB) |
|---|---|---|---|---|---|
| A (línea base) | 200 000 | 0.161 | 0.0055 | 3.4 % | 78.18 |
| B (línea por línea) | 200 000 | 0.084 | 0.0020 | 2.3 % | 0.205 |
| C (array) | 200 000 | 0.087 | 0.0010 | 1.2 % | 1.76 |
| A | 500 000 | 0.454 | 0.0119 | 2.6 % | 195.64 |
| B | 500 000 | 0.216 | 0.0043 | 2.0 % | 0.205 |
| C | 500 000 | 0.223 | 0.0040 | 1.8 % | 4.11 |
| A | 1 000 000 | 0.946 | 0.0128 | 1.4 % | 391.63 |
| B | 1 000 000 | 0.426 | 0.0081 | 1.9 % | 0.205 |
| C | 1 000 000 | 0.437 | 0.0048 | 1.1 % | 8.02 |

Todas las combinaciones cumplen el criterio de calidad del protocolo (CV ≤ 10 %).

## 2. ¿Las tendencias van en la dirección de las hipótesis?
| Hipótesis | Predicción | Medido | ¿Dirección correcta? |
|---|---|---|---|
| H1 | M_B < 0.10 × M_A con n = 1 000 000 | M_B / M_A = 0.205 / 391.63 ≈ **0.0005** (0.05 %) | Sí |
| H2 | M(1 000 000) / M(200 000): A y C entre 4 y 6; B entre 0.8 y 1.2 | A: **5.01** · C: **4.56** · B: **1.00** | Sí, las tres |
| H3 | t_B ≤ 0.80 × t_A con n = 1 000 000 | t_B / t_A = 0.426 / 0.946 ≈ **0.45** | Sí |

La decisión formal (con IC95 %) se toma en la Clase 5.

## 3. Interpretación física
- **Memoria de A ∝ n.** 391.63 MiB × 1 048 576 B/MiB ÷ 1 000 000 ≈ **410.7 B por registro**, casi igual a los ≈ 411 B
  medidos en la Clase 3 con n = 300 000. El protocolo estimó ≈ 392 MiB para n = 1 000 000 con M ≈ n × 411 B, y
  se midió 391.6 MiB: el modelo lineal funciona. Con ese ritmo, 2 GiB alcanzan para unos 2 147 483 648 B ÷ 411 B
  ≈ **5.2 millones de registros** (sin contar el resto del sistema), que es por qué el tablero falla con archivos grandes.
- **Memoria de B constante.** Siempre 0.205 MiB (≈ 210 KiB) para cualquier n: solo guarda suma, cantidad y máxima de
  200 sensores, más lo que necesita para leer el archivo línea por línea. No depende de n.
- **Memoria de C ∝ n, pero pequeña.** 8.02 MiB con n = 1 000 000 ≈ **8.4 B por registro**: los 8 B de cada número
  `double` más un poco de espacio extra que `array` reserva al crecer. Es ≈ 2 % de la memoria de A.
- **Tiempo ∝ n en las tres.** De n = 200 000 a 1 000 000 (×5), el tiempo creció ×5.05 en B, ×5.02 en C y ×5.88 en A.
  A crece algo más que lineal; una explicación posible (sin comprobar) es que crear y guardar n diccionarios hace
  más trabajo de gestión de memoria cuando la lista es más grande.
- **Ciclos por registro (estimación, N = f · t).** Con f = 2.2 × 10⁹ Hz y n = 1 000 000: A ≈ 2 081 ciclos por registro,
  B ≈ 936 y C ≈ 962. B y C se ahorran más de la mitad de los ciclos porque no crean un diccionario con 4 textos por línea.

## 4. Preguntas de análisis de la guía

**1. ¿Qué estrategia muestra mayor dispersión entre repeticiones? ¿A qué lo atribuye?**
A con n = 200 000 (CV = 3.4 %). Con corridas tan cortas (0.16 s), cualquier interrupción de Windows (antivirus,
WhatsApp, Vínculo con el teléfono, que seguían en segundo plano según D-003) pesa más en proporción. Además A crea
muchos objetos, y Python puede hacer limpieza de memoria en medio de la corrida (posible causa, sin comprobar).
Con n = 1 000 000 el CV de A baja a 1.4 %.

**2. ¿La relación t_CPU / t_pared confirma si el problema está limitado por CPU o por espera?**
Está **limitado por CPU**: el uso de CPU del proceso dio en promedio entre 96.7 % y 100.2 % en las nueve combinaciones,
es decir, el procesador estuvo trabajando casi todo el tiempo y no esperando al disco. El archivo ya estaba en
la caché del sistema operativo por la corrida de calentamiento. Importante: esto es **un núcleo** de los 12 lógicos
(el CPU del sistema completo en el monitor fue 17 % en promedio).

**3. ¿Qué limitación de los instrumentos debe declarar en el informe?**
- `time.process_time()` en Windows avanza de a **15.625 ms** (todos los `cpu_proceso_s` son múltiplos de 1/64 s).
  En corridas de 0.08 s eso es un error de hasta ±20 %, por eso hay corridas con `uso_cpu_pct` de 72 % o 115 %.
  Hay que mirar el promedio, no una corrida sola.
- **tracemalloc** solo cuenta la memoria que reserva Python, no toda la del proceso (la memoria residente `rss_mib`
  estuvo entre 77 y 101 MiB porque incluye el intérprete y lo demás).
- La **frecuencia** reportada es siempre 2200 MHz: psutil no ve el turbo, así que los ciclos N = f · t son estimaciones.
- **No hay temperatura ni energía** en este PC (plan B en `docs/entorno.md`).
- Se midió en un PC de 15.63 GiB, **no** en el servidor de 2 GiB: el pico de memoria casi no depende del equipo, pero el
  tiempo sí, así que el tiempo solo sirve para comparar A, B y C entre sí.

**4. ¿Las tendencias preliminares van en la dirección de su hipótesis?**
Sí, las tres (ver sección 2).

## 5. Errores sistemáticos y aleatorios
| Tipo | Ejemplo en este experimento | Cómo se manejó |
|---|---|---|
| **Sistemático** (siempre empuja hacia el mismo lado) | tracemalloc infla el tiempo de la corrida de memoria | Esa corrida no se usa para el tiempo (D-001) |
| Sistemático | Resolución de 15.625 ms de `process_time()` | Se reporta el promedio de 10 corridas |
| Sistemático | PC distinto del servidor de la empresa | El tiempo solo se usa para comparar estrategias |
| **Aleatorio** (cambia de corrida en corrida) | Procesos de Windows en segundo plano (CV entre 1.1 % y 3.4 %) | 10 repeticiones, orden aleatorio, calentamiento y monitoreo |
