# Equipo 4 — Gestión eficiente de memoria

> Proyecto: *Laboratorio colaborativo de rendimiento y eficiencia computacional desde la física aplicada*
> Física Aplicada al Desarrollo de Software · SENA · ADSO · 7.º trimestre

## 1. Problema empresarial
**Empresa (caso simulado):** SaludNet IPS, monitoreo de sensores ambientales en 200 salas de vacunas

El tablero que resume las lecturas de los sensores falla con archivos grandes por falta de memoria en un servidor virtual de 2 GiB.

## 2. Situación inicial medible
src/linea_base.py convierte cada línea en un diccionario y guarda todas en una lista.

Comando: `python -m src.linea_base`

| Medición preliminar (Clase 3) | Valor | Unidad |
|---|---|---|
| n utilizado | 300 000 (200 sensores) | registros |
| Tiempo de ejecución (1 corrida) | 1.88 (inflado porque se midió con tracemalloc encendido) | s |
| Pico de memoria (1 corrida) | 117.5 | MiB |
| Memoria por registro (117.5 MiB × 1 048 576 B/MiB ÷ 300 000) | ≈ 411 | B/registro |
| Equipo y fecha | PC del Integrante A: Windows 11, Intel 8 núcleos físicos / 12 lógicos, 15.63 GiB de RAM, Python 3.14.3 · 18/11/2026 | — |
| Repetición (3 corridas, 18/11/2026 22:34, con cargador y navegador abierto) | tiempo: 1.70, 1.69 y 1.70 s · pico: 117.5 MiB en las 3 | s · MiB |

**Impacto (estimación, no medido):** si la memoria crece en proporción a n (≈ 411 B por registro),
2 GiB alcanzarían para unos 2 × 1 073 741 824 B ÷ 411 B ≈ **5.2 millones de registros**, y eso sin contar
lo que usan el sistema operativo y el resto del tablero. Por eso, con archivos grandes el servidor de
2 GiB se queda sin memoria. Esta estimación supone crecimiento lineal y se debe comprobar midiendo
con varios n.

> Es una sola corrida en un equipo distinto al servidor: sirve como punto de partida, no como resultado final.

### Física del problema: magnitudes que intervienen

| Magnitud | Símbolo | Unidad | Valor en nuestro caso | Por qué importa |
|---|---|---|---|---|
| Memoria (cantidad de información guardada) | M | byte (B); 1 MiB = 2²⁰ B = 1 048 576 B | pico de 117.5 MiB con n = 300 000; límite del servidor: 2 GiB = 2 147 483 648 B | Es la **magnitud principal**: si el pico supera lo que tiene el servidor, el tablero falla. |
| Memoria por registro | m = M / n | B/registro | ≈ 411 B/registro | Dice cuánto "pesa" cada lectura guardada. Una temperatura sola cabe en 8 B, pero la línea base guarda un diccionario con 4 textos por cada lectura. |
| Tiempo | t | segundo (s) | 1.69 – 1.88 s (inflado por tracemalloc) | Una estrategia que ahorra memoria pero se vuelve mucho más lenta no sirve para el tablero. |
| Frecuencia del procesador | f | hertz (Hz = 1/s) | 2.2 GHz = 2.2 × 10⁹ Hz (reportada por psutil) | Indica cuántos ciclos hace el procesador por segundo. |
| Periodo de reloj | T = 1/f | s | 1 / (2.2 × 10⁹ Hz) ≈ 0.455 ns | Es lo que dura un ciclo. |
| Ciclos | N = f · t | ciclos (sin unidad) | ≈ 2.2 × 10⁹ Hz × 1.70 s ≈ 3.7 × 10⁹ ciclos → ≈ 12 000 ciclos por registro (estimación, inflada por tracemalloc) | Muestra que procesar cada lectura cuesta miles de ciclos: crear el diccionario y los textos es trabajo real del procesador. |
| Energía | E = P · t | joule (J) | **no se mide** (RAPL no disponible en Windows) | Guardar y mover bytes gasta energía, pero no afirmamos ahorro de energía porque no lo podemos medir. |

**Mecanismo (por qué falla):** la RAM guarda cada bit como una carga eléctrica en una celda física, y hay un
número limitado de celdas (2 GiB en el servidor). La línea base crea un diccionario con 4 textos por cada
línea del CSV y los guarda **todos a la vez**, así que la memoria ocupada crece con n (≈ 411 B por registro).
Cuando el archivo es grande, el programa pide más bytes de los que el servidor tiene y el tablero falla.
Si en vez de guardar todas las lecturas guardamos solo lo necesario (suma, cantidad y máxima por sensor),
la memoria dejaría de depender de n (ver estrategias en §5).

## 3. Pregunta de investigación
¿Cómo cambian el **pico de memoria (MiB)** y el **tiempo de ejecución (s)** cuando se cambia la
**estrategia de procesamiento** (A = línea base, B = línea por línea, C = formato compacto) y el
**número de registros n** (200 000, 500 000 y 1 000 000), manteniendo el mismo equipo, la versión de
Python, los datos de entrada (semilla 4) y el plan de energía?

## 4. Hipótesis
Ver [docs/hipotesis.md](docs/hipotesis.md).

## 5. Estrategias
| Id | Estrategia | Idea principal | Efecto físico esperado | Responsable |
|---|---|---|---|---|
| A | Línea base | Carga todas las lecturas como diccionarios en una lista y luego agrupa las temperaturas por sensor | — (medido: 117.5 MiB con n = 300 000, ≈ 411 bytes/registro) | R2 |
| B | Procesar línea por línea (`src/estrategia_b.py`) | Lee una línea, actualiza suma, cantidad y máxima de su sensor, y la descarta | La memoria deja de depender de n: solo se guardan 3 números por cada uno de los 200 sensores → pico casi constante y más de 90 % menor que A (preliminar en el PC de Andres: 0.20 MiB con n = 300 000) | R3 |
| C | Guardar en formato compacto (`src/estrategia_c.py`) | Guarda solo las temperaturas, como números de 8 bytes en un `array('d')` por sensor, sin diccionarios ni textos | Sigue guardando las n lecturas (sirve si después se necesita, por ejemplo, la mediana), pero cada una ocupa ≈ 8 bytes en vez de ≈ 411 → la memoria crece con n, pero mucho menos que A (preliminar en el PC de Andres: 2.54 MiB con n = 300 000) | R3 |

- **Por qué B usa menos memoria:** lee cada fila del CSV y solo actualiza suma, conteo y máximo por sensor; como no guarda lecturas individuales ni diccionarios por fila, su memoria depende de los sensores (200) y no del total de registros `n`.
- **Por qué C usa menos memoria que la línea base:** aunque conserva las lecturas de cada sensor, evita crear diccionarios por fila y usa `array('d')` (números flotantes de doble precisión contiguos en C) en lugar de estructuras y objetos más pesados de Python.

## 6. Cómo reproducir
```bash
python -m venv .venv && source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt                          # opcional: psutil, matplotlib
python -m src.linea_base                                 # situación inicial
python -m unittest discover -s pruebas                   # corrección
python -m experimentos.ejecutar_experimento              # experimento formal -> resultados/resultados.csv
python ruta/a/analizar_resultados.py resultados/resultados.csv
```

## 7. Integrantes y roles
| Rol | Integrante | Responsabilidad principal |
|---|---|---|
| R1 — Coordinación y protocolo experimental | Santiago (Integrante A) | Mantiene el protocolo y la bitácora de decisiones; controla variables; modera issues y la planeación. |
| R2 — Desarrollo de estrategia base | Durman (Integrante B) | Comprende y documenta la línea base; asegura la verificación de corrección (pruebas) de todas las estrategias. |
| R3 — Estrategias alternativas y optimización | Andres (Integrante C) | Diseña e implementa las estrategias alternativas y justifica físicamente por qué deberían cambiar las magnitudes. |
| R4 — Automatización de mediciones y análisis | Santiago (entorno y ejecución) y Andres (análisis y gráficos) | Automatiza experimentos y registro CSV; produce estadísticas y gráficos; documenta el entorno. |

Los roles son flexibles: **todos** participan en la comprensión física y en el código.

## 8. Documentación
- [Variables](docs/variables.md) · [Protocolo](docs/protocolo.md) · [Entorno](docs/entorno.md)
- [Decisiones técnicas](docs/decisiones.md) · [Uso de IA](docs/uso_ia.md) · [Informe](docs/informe.md)

## 9. Resultados y conclusiones (Clase 5)
_Resumen de máximo 5 líneas con cifras, unidades e intervalo de confianza._