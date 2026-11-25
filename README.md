# Equipo 4 — Gestión eficiente de memoria

# Equipo 4 — Gestión eficiente de memoria

> Proyecto: _Laboratorio colaborativo de rendimiento y eficiencia computacional desde la física aplicada_
> Física Aplicada al Desarrollo de Software · SENA · ADSO · 7.º trimestre

## 1. Problema empresarial

**Empresa (caso simulado):** SaludNet IPS, monitoreo de sensores ambientales en 200 salas de vacunas

El tablero que resume las lecturas de los sensores falla con archivos grandes por falta de memoria en un servidor virtual de 2 GiB.

## 2. Situación inicial medible

src/linea_base.py convierte cada línea en un diccionario y guarda todas en una lista.

| Medición preliminar (Clase 3)   | Valor | Unidad    |
| ------------------------------- | ----- | --------- |
| n utilizado                     |       | registros |
| Tiempo de ejecución (1 corrida) |       | s         |
| Equipo y fecha                  |       | —         |

## 3. Pregunta de investigación

_¿Cómo cambia **\_\_\_\_** (VD, unidad) cuando **\_\_\_\_** (VI), manteniendo **\_\_\_\_** (VC)?_

## 4. Hipótesis

Ver [docs/hipotesis.md](docs/hipotesis.md).

## 5. Estrategias

| Id  | Estrategia                               | Idea principal                                                                                                                | Efecto físico esperado                                                                                                                                                                            | Responsable |
| --- | ---------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------- |
| A   | Línea base                               | (situación inicial)                                                                                                           | —                                                                                                                                                                                                 | R2          |
| B   | Acumulación en línea (`estrategia_b.py`) | Leer el CSV línea por línea y guardar solo la suma, cantidad y temperatura máxima de cada sensor, sin almacenar las lecturas. | Reduce drásticamente el uso de RAM a un consumo casi constante (3 valores por sensor, sin crecer con `n`; 0.20 MiB preliminares con `n = 300 000`).                                               | R3          |
| C   | Arreglo compacto (`estrategia_c.py`)     | Eliminar diccionarios por fila y guardar solo las temperaturas de cada sensor en un arreglo `array('d')`.                     | Disminuye el uso de RAM frente a la línea base al evitar diccionarios por fila y objetos/textos pesados de Python, usando arreglos numéricos compactos (2.54 MiB preliminares con `n = 300 000`). | R3          |

- **Por qué B usa menos memoria:** lee cada fila del CSV y solo actualiza suma, conteo y máximo por sensor; como no guarda lecturas individuales ni diccionarios por fila, su memoria depende de los sensores (200) y no del total de registros `n`.
- **Por qué C usa menos memoria que la línea base:** aunque conserva las lecturas de cada sensor, evita crear diccionarios por fila y usa `array('d')` (números flotantes de doble precisión contiguos en C) en lugar de estructuras y objetos más pesados de Python.[cite: 1, 2, 3]

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

| Rol                                          | Integrante | Responsabilidad principal                                                                                         |
| -------------------------------------------- | ---------- | ----------------------------------------------------------------------------------------------------------------- |
| R1 — Coordinación y protocolo experimental   | _(nombre)_ | Mantiene el protocolo y la bitácora de decisiones; controla variables; modera issues y la planeación.             |
| R2 — Desarrollo de estrategia base           | _(nombre)_ | Comprende y documenta la línea base; asegura la verificación de corrección (pruebas) de todas las estrategias.    |
| R3 — Estrategias alternativas y optimización | _(nombre)_ | Diseña e implementa las estrategias alternativas y justifica físicamente por qué deberían cambiar las magnitudes. |
| R4 — Automatización de mediciones y análisis | _(nombre)_ | Automatiza experimentos y registro CSV; produce estadísticas y gráficos; documenta el entorno.                    |

Los roles son flexibles: **todos** participan en la comprensión física y en el código.

## 8. Documentación

- [Variables](docs/variables.md) · [Protocolo](docs/protocolo.md) · [Entorno](docs/entorno.md)
- [Decisiones técnicas](docs/decisiones.md) · [Uso de IA](docs/uso_ia.md) · [Informe](docs/informe.md)

## 9. Resultados y conclusiones (Clase 5)

_Resumen de máximo 5 líneas con cifras, unidades e intervalo de confianza._
