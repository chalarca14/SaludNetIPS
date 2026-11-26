# Plantilla de hipótesis

Una hipótesis verificable **predice un resultado medible** y **puede resultar falsa**.

## Estructura
> **Si** _(cambio en la variable independiente)_, **entonces** _(variable dependiente, con unidad)_
> **aumentará / disminuirá** aproximadamente _(magnitud o factor)_, **porque** _(mecanismo físico/computacional)_,
> **manteniendo constantes** _(variables controladas)_.

## Ejemplo (problema neutro de la demostración, NO de un equipo)
> **Si** se reemplaza la lista intermedia por un generador al sumar n cuadrados, **entonces** el pico de memoria
> (MiB) **disminuirá** en más de un 90 % para n = 10⁶ y el tiempo (s) variará menos de un 20 %, **porque** el
> generador no almacena los n valores (memoria constante) pero realiza el mismo número de operaciones,
> **manteniendo** el mismo equipo, versión de Python y n.

## Hipótesis del equipo

**Punto de partida medido:** línea base (A) con n = 300 000 → pico de 117.5 MiB (≈ 411 B por registro).
**Variables controladas en las tres hipótesis:** mismo equipo, Python 3.14.3, plan de energía "Turbo" con
cargador conectado, mismos datos (semilla 4, 200 sensores) y programas cerrados (ver `docs/variables.md`).

| Id | Hipótesis completa | VI | VD (unidad) | Predicción cuantitativa | Mecanismo físico | ¿Cómo la refutaríamos? |
|---|---|---|---|---|---|---|
| H1 | **Si** se usa la estrategia B (línea por línea) en vez de la A (línea base) con n = 1 000 000, **entonces** el pico de memoria (MiB) **disminuirá** más de un 90 %, **porque** B solo guarda suma, cantidad y máxima de los 200 sensores en vez de guardar los n registros como diccionarios con textos, **manteniendo constantes** las variables controladas. | Estrategia (A → B) | Pico de memoria M (MiB) | M_B < 0.10 × M_A (con A esperamos ≈ 392 MiB, así que B debería quedar por debajo de ≈ 39 MiB) | A ocupa ≈ 411 B por registro y los guarda **todos a la vez**; B guarda unos 200 × 3 = 600 números sin importar n. Menos bytes guardados = menos celdas de RAM ocupadas. | Si en la corrida de memoria con n = 1 000 000, M_B es mayor o igual que el 10 % de M_A. |
| H2 | **Si** n aumenta 5 veces (de 200 000 a 1 000 000), **entonces** el pico de memoria (MiB) de A y de C **aumentará** aproximadamente 5 veces, y el de B **casi no cambiará** (menos de 20 %), **porque** A y C guardan cada registro (A ≈ 411 B, C ≈ 8 B por temperatura) y B no guarda ninguno, **manteniendo constantes** las variables controladas. | n (registros) | Pico de memoria M (MiB) | A y C: M(1 000 000) / M(200 000) entre 4 y 6. B: el cociente entre 0.8 y 1.2 | Si cada registro guardado ocupa un número fijo de bytes, la memoria total es M ≈ n × (bytes por registro): crece en línea recta con n. Si no se guarda nada por registro, M no depende de n. | Si el cociente de A o de C queda fuera de 4 – 6, o si el de B queda fuera de 0.8 – 1.2. |
| H3 | **Si** se usa la estrategia B en vez de la A con n = 1 000 000, **entonces** el tiempo de ejecución (s) **disminuirá** al menos un 20 %, **porque** B no crea un diccionario por registro ni recorre una lista de n elementos por segunda vez, **manteniendo constantes** las variables controladas. | Estrategia (A → B) | Tiempo t (s), promedio de 10 corridas sin tracemalloc | t_B ≤ 0.80 × t_A | Crear cada diccionario y reservar su memoria son operaciones extra que gastan ciclos del procesador (N = f·t, con f = 2.2 GHz y un ciclo de T ≈ 0.455 ns). Menos operaciones por registro = menos ciclos = menos tiempo. | Si el promedio de t_B es mayor que 0.80 × el promedio de t_A, o si B resulta más lenta que A. |

**Lo que NO afirmamos:** no decimos nada sobre ahorro de **energía** (J), porque en este equipo no se
puede medir (RAPL no disponible en Windows).

## Evaluación de las hipótesis (Clase 5)

**Responsable:** Andrés (R4) · **Fecha:** 25/11/2026 · **Script:** `python -m experimentos.analizar_resultados`
(salida en `resultados/resumen_estadistico.csv`). Las hipótesis de arriba **no se modificaron** después de ver los datos.

**Origen de los datos:** datos de entrada **SIMULADOS** (`src/generar_datos.py`, semilla 4); tiempos y picos de memoria
**MEDIDOS** en el PC del Integrante A el 25/11/2026 (`resultados/resultados.csv`, 99 filas); ciclos N = f · t **ESTIMADOS**.

**Alcance de las tres decisiones:** válidas **solo en este PC** (Windows 11, Python 3.14.3, plan "Turbo", 15.63 GiB),
**con estos datos simulados** y para n entre 200 000 y 1 000 000. No se comprobaron en el servidor de 2 GiB de la empresa
(el pico de memoria casi no depende del equipo; el tiempo sí).

| Id | Estado | Criterio | Números | Alcance |
|---|---|---|---|---|
| H1 | **Se confirma** | Comparación directa de la corrida de memoria (k = 1): se confirma si M_B < 0.10 × M_A con n = 1 000 000. | M_A = 391.632 MiB, M_B = 0.205 MiB; 0.10 × M_A = 39.163 MiB. M_B / M_A = 0.000523 (**0.052 %**). | Este PC y estos datos; memoria medida con tracemalloc (solo memoria reservada por Python). |
| H2 | **Se confirma** | Cociente M(1 000 000) / M(200 000): A y C dentro de 4 – 6; B dentro de 0.8 – 1.2. Las tres condiciones deben cumplirse. | A: 391.632 / 78.183 = **5.009** · C: 8.022 / 1.761 = **4.555** · B: 0.205 / 0.205 = **1.000**. Pendientes log-log de memoria: A = 1.001, C = 0.941, B = 0.000. | Este PC, estos datos y n entre 200 000 y 1 000 000 (tres puntos). |
| H3 | **Se confirma** | (1) Prueba t de Welch A vs. B con p < 0.05 **y** (2) cociente en el peor caso, IC95 sup(t_B) / IC95 inf(t_A), ≤ 0.80. | t_A = 0.945836 s, IC95 [0.936658; 0.955014] · t_B = 0.425653 s, IC95 [0.419844; 0.431461] · t_B / t_A = **0.450**; peor caso = **0.461**. Welch: diferencia A − B = 0.520183 s, IC95 [0.509962; 0.530405] s, t = 108.34, gl = 15.21, p < 1e-15. Tamaño de efecto: d de Cohen = 48.45 (g de Hedges = 46.40). | Este PC (el tiempo depende del equipo), estos datos y n = 1 000 000. |

**Por qué H1 y H2 se deciden con una sola corrida de memoria (k = 1).** En la Clase 3 el pico de memoria de la línea base
salió **idéntico en 3 corridas** (117.5 MiB) y por eso D-001 fija 1 corrida de memoria por combinación. El pico depende de
cuántos objetos se guardan, no del azar del sistema operativo. Con k = 1 no hay desviación estándar ni IC95 %, así que la
decisión es una comparación directa. El margen es tan grande (el umbral de 39.163 MiB es unas 191 veces M_B, y los
cocientes de H2 no están cerca de los bordes) que una variación pequeña no cambiaría la decisión.

**Por qué este criterio para H3.** La hipótesis no dice solo "B es más rápida", sino "B tarda **como máximo el 80 %** de A".
Por eso se usan dos condiciones:
1. **Welch** responde si la diferencia entre A y B es real o puede ser azar. Se eligió Welch y no la prueba t clásica porque no
   supone que A y B tengan la misma varianza (s_A = 0.0128 s y s_B = 0.0081 s). Con p < 1e-15 la diferencia no es azar.
2. El **cociente en el peor caso** responde si se cumple el 80 %: se divide el límite **superior** del IC95 de B entre el límite
   **inferior** del IC95 de A (lo más desfavorable para la hipótesis). Si aun así da ≤ 0.80, se cumple con margen. Dio 0.461.

El tamaño de efecto (d = 48) indica que la diferencia entre medias es unas 48 veces la desviación típica de las corridas: las
distribuciones de A y B no se tocan (máximo de B = 0.445 s, mínimo de A = 0.928 s en las 10 corridas).

**Observación adicional (no era una hipótesis).** La pendiente log-log del tiempo de A es **1.10**, algo mayor que la de B (1.007)
y C (1.003). A crece un poco más rápido que lineal; una posible causa (sin comprobar) es el trabajo extra de gestión de memoria
al crear y guardar n diccionarios.

## Lista de verificación
- [X] Tiene dirección (aumenta/disminuye) y una magnitud aproximada.
- [X] La VD es medible con las herramientas disponibles en el laboratorio.
- [X] Indica qué resultado la **refutaría**.
- [X] Explica el mecanismo con al menos una magnitud física y su unidad SI.
- [X] No afirma ahorro de energía si no se va a medir energía.
