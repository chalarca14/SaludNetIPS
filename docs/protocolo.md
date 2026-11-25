# Protocolo experimental reproducible

**Responsable:** R1 (Santiago) · **Revisado por:** todos · **Versión:** 2 · **Fecha:** 25/11/2026

> **Cambios de la versión 2 (Clase 4):** se agrega el monitoreo con `monitor_sistema.py`, la revisión de
> RAM libre y de suspensión antes de medir, la regla de no usar el PC durante la medición, el número de
> filas esperado en el CSV y la lista de chequeo para revisar los resultados (sección 7).

## 1. Objetivo del experimento
Comparar el **pico de memoria (MiB)** y el **tiempo de ejecución (s)** de tres estrategias para resumir
las lecturas de los sensores (temperatura media y máxima por sensor):
A = línea base, B = procesar línea por línea, C = guardar en formato compacto (`array('d')`).
Todas deben dar el **mismo resultado** que la línea base (ver `pruebas/test_correccion.py`).

## 2. Preparación del entorno (antes de cada sesión)
1. Equipo conectado al cargador. Plan de energía: **"Turbo"** (el que tiene el PC del Integrante A; no se
   cambia entre sesiones). Revisar con `powercfg /getactivescheme`.
2. Cerrar el navegador, VS Code, NVIDIA Overlay y sincronizadores de archivos. Ejecutar desde
   **Windows Terminal**, no desde la terminal de VS Code.
3. Ejecutar `diagnostico_entorno.py` y comparar con `docs/entorno.md`. Si algo cambió (por ejemplo, la
   versión de Python), anotarlo en la sección 6.
4. Los datos se generan solos con semilla fija (**semilla = 4**, en `src/generar_datos.py`): la función
   `preparar(n)` crea `datos/lecturas_<n>.csv` si no existe. Para crearlos a mano: `python -m src.generar_datos <n>`.
5. Revisar la RAM ocupada: `python -c "import psutil; print(psutil.virtual_memory().percent)"`. Si pasa
   del **50 %**, cerrar más programas. (El 25/11/2026 estaba en 88 % con el navegador y VS Code abiertos.)
6. Desactivar la suspensión y el apagado de pantalla mientras se mide (Configuración → Sistema →
   Inicio/apagado y suspensión → "Nunca") y activar "No molestar" para que no salgan notificaciones.
7. **No usar el computador durante la medición**: no mover el mouse ni abrir programas hasta que termine.

## 3. Procedimiento
| Paso | Acción | Comando | Evidencia |
|---|---|---|---|
| 1 | Pruebas de corrección | `python -m unittest discover -s pruebas` | captura |
| 2 | Prueba de humo | `python -m experimentos.ejecutar_experimento --rapido` | CSV (se borra después: no es el resultado formal) |
| 3 | Iniciar monitoreo **en otra terminal**, justo antes del paso 4 | `python herramientas/monitor_sistema.py --duracion 900 --intervalo 1 --salida resultados/monitor.csv` | `resultados/monitor.csv` |
| 4 | Experimento formal | `python -m experimentos.ejecutar_experimento` | `resultados/resultados.csv` y `resultados/resultados.entorno.json` |
| 5 | Detener el monitoreo con Ctrl+C cuando el paso 4 diga "Listo" | — | — |
| 6 | Revisar el CSV con la lista de la sección 7 | — | lista marcada en el PR |

Si el paso 1 falla, **no** se mide: una estrategia que da otro resultado no es una mejora.

El monitoreo registra cada 1 s el CPU % del sistema, la frecuencia (MHz) y la memoria usada del sistema (%).
La temperatura y la energía quedan vacías porque este PC no las expone (ver `docs/entorno.md`). Sirve para
ver si algo raro pasó en el PC durante la medición (por ejemplo, un pico de CPU de otro programa).

## 4. Parámetros
- **Tamaños n:** 200 000, 500 000 y 1 000 000 registros (los de `experimentos/ejecutar_experimento.py`).
  **Justificación:** con tres tamaños se ve si la memoria crece en línea recta con n (lo que esperamos de
  A y C) o se queda casi igual (lo que esperamos de B). Con A, 1 000 000 de registros daría un pico de unos
  1 000 000 × 411 B ≈ 392 MiB (estimación), que cabe sin problema en los 15.63 GiB del PC.
- **Repeticiones por combinación:** 10 para el tiempo y 1 para la memoria.
  **Justificación:** el tiempo varía entre corridas (la línea base dio 1.88 s y luego 1.69 – 1.70 s), así
  que hay que repetir para sacar promedio y desviación. El pico de memoria salió igual en 3 corridas
  (117.5 MiB), por eso basta una corrida de memoria por combinación. El código la hace aparte
  (`medir_memoria=True`) porque tracemalloc vuelve lento el programa.
- **Calentamiento:** 1 ejecución por estrategia antes de medir, que no se registra (función `calentar`).
- **Orden:** aleatorio con semilla 42 (`random.Random(42).shuffle(plan)`), para que un cambio del PC a mitad
  del experimento (por ejemplo, que se caliente) no afecte siempre a la misma estrategia.
- **Filas esperadas en el CSV:** 3 estrategias × 3 tamaños × 10 repeticiones = **90 filas de tiempo**
  (`medicion_memoria = no`) + 3 × 3 = **9 filas de memoria** (`medicion_memoria = si`, `repeticion = 0`) =
  **99 filas** en total.
- **Duración estimada:** entre 5 y 15 minutos (estimación; la corrida de memoria de A con n = 1 000 000 es la
  más lenta). Por eso el monitoreo se programa para 900 s y se detiene a mano al terminar.
  **Duración real (25/11/2026):** 62 s (de 11:39:44 a 11:40:46). La estimación se hizo con los tiempos de
  la Clase 3, que tenían tracemalloc encendido y eran mucho más lentos.

## 5. Criterios de calidad de los datos
- CV ≤ 10 % por combinación (CV = desviación / promedio × 100). Si se supera: revisar la sección 6 por
  incidentes, cerrar programas y **repetir solo esa combinación**, dejando anotado por qué.
- Valores atípicos (regla de Tukey): se reportan; solo se excluyen con causa documentada.

## 6. Registro de incidentes
| Fecha/hora | Incidente (p. ej. actualización del SO, batería) | Corridas afectadas | Decisión |
|---|---|---|---|
| 18/11/2026 22:34 | Medición preliminar de la línea base con Brave, VS Code y NVIDIA Overlay abiertos. El tiempo dio 1.69 – 1.70 s, contra 1.88 s de la primera medición. | Solo mediciones preliminares (Clase 3) | Para el experimento formal se cierran esos programas (sección 2, paso 2). El pico de memoria no cambió (117.5 MiB). |
| 25/11/2026 | Prueba de 3 s de `monitor_sistema.py`: la RAM del sistema estaba al 88 % con varios programas abiertos. | Ninguna (fue solo una prueba del script) | Se agrega la revisión de RAM antes de medir (sección 2, paso 5). |
| 25/11/2026 11:31 | Antes del experimento formal la RAM estaba en 54.5 % (máximo del protocolo: 50 %). | Todas las del experimento formal | Se mide igual: ver D-003 en `docs/decisiones.md`. |
| 25/11/2026 | Las pruebas de Durman (B y C contra la línea base) todavía no están en `main`; solo corre `test_linea_base_ejecuta`. | Todas las del experimento formal | Se mide igual: la verificación de corrección de `ejecutar_experimento.py` compara B y C con la línea base para cada n antes de medir. Las pruebas se agregan cuando se una el PR de Durman. |
| 25/11/2026 | La suspensión con cargador estaba en 5 min y el experimento dura más. | Todas | Se cambió a "Nunca" antes de medir y se devuelve a 5 min al terminar. |

## 7. Lista de chequeo para revisar el CSV (antes de abrir el PR)
- [ ] El CSV tiene **99 filas** de datos (90 de tiempo + 9 de memoria).
- [ ] Están las 3 estrategias (`A_linea_base`, `B_...`, `C_...`) y los 3 tamaños (200 000, 500 000, 1 000 000).
- [ ] Cada combinación tiene repeticiones 1 a 10 (tiempo) y una repetición 0 (memoria).
- [ ] `pico_mem_mib` solo tiene valor en las filas con `medicion_memoria = si`.
- [ ] Todos los `tiempo_s` son mayores que 0, y no hay valores rarísimos (por ejemplo, uno 10 veces más grande
      que los demás de su grupo). Si los hay, buscar la causa en `monitor.csv` y anotarla en la sección 6.
- [ ] Unidades: `tiempo_s` y `cpu_proceso_s` en s, `pico_mem_mib` y `rss_mib` en MiB, `uso_cpu_pct` en %,
      `frecuencia_mhz` en MHz.
- [ ] `resultados/resultados.entorno.json` coincide con `docs/entorno.md` (mismo equipo y versión de Python).
- [ ] Para el análisis: los tiempos se calculan **solo** con las filas `medicion_memoria = no`; la corrida de
      memoria tiene el tiempo inflado por tracemalloc (decisión D-001).
