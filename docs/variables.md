# Plantilla de variables experimentales

| Tipo | Variable | Símbolo | Unidad | Valores / rango | Instrumento o forma de obtención | Justificación |
|---|---|---|---|---|---|---|
| Independiente | Estrategia | — | — | A = línea base (diccionarios en lista), B = línea por línea (suma, cantidad y máxima por sensor), C = formato compacto (`array('d')` por sensor) | — | Son tres formas de calcular el mismo resumen que difieren en **cuántos bytes guardan a la vez** en la RAM. |
| Independiente | Tamaño de entrada | n | registros (líneas del CSV) | 200 000, 500 000 y 1 000 000 | `experimentos/ejecutar_experimento.py` | Con tres tamaños se ve si la memoria crece en línea recta con n (A y C) o se queda casi igual (B). |
| Dependiente | Pico de memoria | M | MiB | — | tracemalloc (corrida separada) | Es la **medida principal**: el tablero falla cuando la memoria supera los 2 GiB del servidor (H1 y H2). Se mide aparte porque tracemalloc hace el programa más lento. |
| Dependiente | Tiempo de ejecución | t | s | — | time.perf_counter() | Una estrategia que ahorra memoria pero se vuelve mucho más lenta no le sirve al tablero (H3). |
| Dependiente | Uso de CPU | U | % | — | t_CPU / t, con t_CPU = time.process_time() | Indica si el programa estuvo trabajando todo el tiempo o esperando (por ejemplo, a leer el archivo del disco). |
| Dependiente (opcional) | Temperatura | θ | °C | — | sensores.py | Plan B si no disponible: no está disponible en este equipo. Se revisa si el tiempo aumenta corrida tras corrida (señal de calentamiento) y el orden aleatorio reparte ese efecto entre las estrategias. |
| Dependiente (opcional) | Energía | E | J | — | RAPL / vatímetro | Plan B si no disponible: no está disponible (RAPL no funciona en Windows). No se mide energía y no se afirma nada sobre ahorro de energía. |
| Controlada | Equipo | — | — | PC del Integrante A: Windows 11 (10.0.26200), AMD64, Intel64 Family 6 Model 186, 8 núcleos físicos / 12 lógicos, 15.63 GiB de RAM | diagnostico_entorno.py | Otro equipo daría tiempos distintos; todas las mediciones se hacen en el mismo. |
| Controlada | Versión de Python | — | — | 3.14.3 | diagnostico_entorno.py | Versiones distintas de Python pueden ocupar distinta memoria por diccionario o por texto. |
| Controlada | Alimentación (corriente/batería) | — | — | Cargador conectado, plan de energía "Turbo" | `psutil.sensors_battery()` y `powercfg /getactivescheme` antes de medir | Con batería o con otro plan, Windows puede cambiar la frecuencia del procesador y alargar los tiempos. |
| Controlada | Programas abiertos | — | — | Navegador, VS Code y NVIDIA Overlay cerrados; se ejecuta desde Windows Terminal | Revisión con el Administrador de tareas | Otros programas compiten por la CPU y la memoria. En mediciones preliminares hechas en condiciones distintas, el tiempo de la línea base varió entre 1.69 s y 1.88 s. |
| Controlada | Datos de entrada (semilla) | — | — | Semilla = 4, 200 sensores (`src/generar_datos.py`) | Constante en el código | Las tres estrategias procesan exactamente los mismos registros en todas las corridas. |
| Controlada | Estado de la memoria antes de medir | — | — | `gc.collect()` antes de cada medición + 1 corrida de calentamiento | `herramientas/labmedicion.py` | Así cada medición empieza con la memoria "limpia" y no carga basura de la corrida anterior. |

## Mapa de dependencias
`Estrategia A → un diccionario con 4 textos por registro, todos guardados a la vez (≈ 411 B/registro) → bytes en la RAM ∝ n → pico de memoria M`
`Estrategia B → solo suma, cantidad y máxima de 200 sensores → bytes casi constantes → M casi no depende de n`
`Estrategia C → una temperatura de 8 B por registro en array('d') → bytes ∝ n, pero ≈ 8 B en vez de ≈ 411 B → M`
`n → líneas leídas y convertidas (split, float) → ciclos (N = f·t) → tiempo t (en las tres estrategias)`
`Objetos creados por registro (A crea más que C, y C más que B) → reservas de memoria → más ciclos → tiempo t`

## Variables que NO controlamos y cómo las mitigamos
| Variable no controlada | Efecto posible | Mitigación (repeticiones, orden aleatorio, calentamiento...) |
|---|---|---|
| Frecuencia dinámica (turbo/ahorro) | El procesador cambia su velocidad solo; psutil siempre muestra 2200 MHz, pero la frecuencia real puede ser mayor (turbo) o menor (ahorro). | Cargador conectado, plan "Turbo" fijo, una corrida de calentamiento que no se cuenta y 10 repeticiones de tiempo por combinación. |
| Procesos del sistema operativo | Windows Update, el antivirus u otros procesos en segundo plano pueden robar tiempo de CPU en una corrida y no en otra. | Cerrar programas, 10 repeticiones, orden aleatorio de las corridas (semilla 42) y anotar incidentes en `docs/protocolo.md`. |
| Caché de archivos del SO | **Sí aplica:** el programa lee el CSV. La primera lectura viene del disco (más lenta) y las siguientes de la RAM donde Windows guarda el archivo (más rápidas). | Los CSV se generan antes de medir, se hace una corrida de calentamiento y el orden aleatorio evita que siempre le toque la "primera lectura" a la misma estrategia. |
| Memoria que tracemalloc no ve | tracemalloc solo cuenta la memoria que reserva Python, no toda la del proceso. | Se usa igual para las tres estrategias (la comparación es justa) y se dice en el informe. |
