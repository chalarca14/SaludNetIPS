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

## Lista de verificación
- [X] Tiene dirección (aumenta/disminuye) y una magnitud aproximada.
- [X] La VD es medible con las herramientas disponibles en el laboratorio.
- [X] Indica qué resultado la **refutaría**.
- [X] Explica el mecanismo con al menos una magnitud física y su unidad SI.
- [X] No afirma ahorro de energía si no se va a medir energía.
