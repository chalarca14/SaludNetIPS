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

## 3. Pregunta de investigación
_¿Cómo cambia ________ (VD, unidad) cuando ________ (VI), manteniendo ________ (VC)?_

## 4. Hipótesis
Ver [docs/hipotesis.md](docs/hipotesis.md).

## 5. Estrategias
| Id | Estrategia | Idea principal | Efecto físico esperado | Responsable |
|---|---|---|---|---|
| A | Línea base | Carga todas las lecturas como diccionarios en una lista y luego agrupa las temperaturas por sensor | — (medido: 117.5 MiB con n = 300 000, ≈ 411 bytes/registro) | R2 |
| B | Procesar línea por línea | Lee una línea, actualiza suma, cantidad y máxima de su sensor, y la descarta | La memoria deja de depender de n: solo se guardan 3 números por cada uno de los 200 sensores → pico casi constante y más de 90 % menor que A | R3 |
| C | Guardar en formato compacto | Guarda solo las temperaturas, como números de 8 bytes en un `array('d')` por sensor, sin diccionarios ni textos | Sigue guardando las n lecturas (sirve si después se necesita, por ejemplo, la mediana), pero cada una ocupa ≈ 8 bytes en vez de ≈ 411 → la memoria crece con n, pero mucho menos que A | R3 |

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
| R1 — Coordinación y protocolo experimental | _(nombre)_ | Mantiene el protocolo y la bitácora de decisiones; controla variables; modera issues y la planeación. |
| R2 — Desarrollo de estrategia base | _(nombre)_ | Comprende y documenta la línea base; asegura la verificación de corrección (pruebas) de todas las estrategias. |
| R3 — Estrategias alternativas y optimización | _(nombre)_ | Diseña e implementa las estrategias alternativas y justifica físicamente por qué deberían cambiar las magnitudes. |
| R4 — Automatización de mediciones y análisis | _(nombre)_ | Automatiza experimentos y registro CSV; produce estadísticas y gráficos; documenta el entorno. |

Los roles son flexibles: **todos** participan en la comprensión física y en el código.

## 8. Documentación
- [Variables](docs/variables.md) · [Protocolo](docs/protocolo.md) · [Entorno](docs/entorno.md)
- [Decisiones técnicas](docs/decisiones.md) · [Uso de IA](docs/uso_ia.md) · [Informe](docs/informe.md)

## 9. Resultados y conclusiones (Clase 5)
_Resumen de máximo 5 líneas con cifras, unidades e intervalo de confianza._