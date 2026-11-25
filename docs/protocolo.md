# Protocolo experimental reproducible

**Responsable:** R1 (Santiago) · **Revisado por:** todos · **Versión:** 1 · **Fecha:** 18/11/2026

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

## 3. Procedimiento
| Paso | Acción | Comando | Evidencia |
|---|---|---|---|
| 1 | Pruebas de corrección | `python -m unittest discover -s pruebas` | captura |
| 2 | Prueba de humo | `python -m experimentos.ejecutar_experimento --rapido` | CSV |
| 3 | Experimento formal | `python -m experimentos.ejecutar_experimento` | `resultados/resultados.csv` y `resultados/resultados.entorno.json` |
| 4 | (Opcional) monitoreo | `monitor_sistema.py` no está en el repositorio: por ahora no se usa | — |

Si el paso 1 falla, **no** se mide: una estrategia que da otro resultado no es una mejora.

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

## 5. Criterios de calidad de los datos
- CV ≤ 10 % por combinación (CV = desviación / promedio × 100). Si se supera: revisar la sección 6 por
  incidentes, cerrar programas y **repetir solo esa combinación**, dejando anotado por qué.
- Valores atípicos (regla de Tukey): se reportan; solo se excluyen con causa documentada.

## 6. Registro de incidentes
| Fecha/hora | Incidente (p. ej. actualización del SO, batería) | Corridas afectadas | Decisión |
|---|---|---|---|
| 18/11/2026 22:34 | Medición preliminar de la línea base con Brave, VS Code y NVIDIA Overlay abiertos. El tiempo dio 1.69 – 1.70 s, contra 1.88 s de la primera medición. | Solo mediciones preliminares (Clase 3) | Para el experimento formal se cierran esos programas (sección 2, paso 2). El pico de memoria no cambió (117.5 MiB). |
