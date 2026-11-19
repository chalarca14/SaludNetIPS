# Registro de decisiones técnicas (ADR breve)

Cada decisión importante se registra aquí y se enlaza desde el issue o PR correspondiente.

## D-001 — Medir el tiempo y la memoria en corridas separadas
- **Fecha:** 18/11/2026 · **Autor(es):** Santiago (R1) · **Issue/PR:** # _(número del issue de R1)_
- **Contexto:** el problema de SaludNet es de memoria, así que necesitamos el pico de memoria (MiB). Pero
  tracemalloc, la herramienta que mide la memoria, hace el programa más lento: la línea base dio 1.69 – 1.88 s
  con tracemalloc encendido.
- **Opciones consideradas:** 1) medir tiempo y memoria en la misma corrida; 2) medir solo memoria;
  3) medir en corridas separadas.
- **Decisión:** opción 3. En cada combinación (estrategia, n) se hacen 10 corridas de tiempo sin tracemalloc
  y 1 corrida de memoria con tracemalloc.
- **Justificación (incluya evidencia o principio físico):** tracemalloc registra cada vez que Python reserva
  memoria, y eso es trabajo extra del procesador (más ciclos, N = f·t), que infla el tiempo. El pico de
  memoria salió igual en 3 corridas (117.5 MiB), así que una corrida de memoria basta.
- **Consecuencias / riesgos:** el tiempo de la corrida de memoria **no** se usa para comparar.
  tracemalloc solo ve la memoria que reserva Python, no toda la del proceso.

## D-002 — Dejar el plan de energía "Turbo" fijo
- **Fecha:** 18/11/2026 · **Autor(es):** Santiago (R1) · **Issue/PR:** # _(número del issue de R1)_
- **Contexto:** el plan de energía cambia la frecuencia del procesador y, con ella, el tiempo. El PC tiene
  el plan "Turbo" (revisado con `powercfg /getactivescheme`).
- **Opciones consideradas:** 1) cambiar a "Equilibrado"; 2) dejar "Turbo" en todas las sesiones.
- **Decisión:** opción 2.
- **Justificación (incluya evidencia o principio físico):** lo importante es que el plan **no cambie** entre
  corridas (variable controlada). Si el plan cambia, la frecuencia f cambia, y el tiempo t = N / f también.
- **Consecuencias / riesgos:** los tiempos solo son comparables con otros medidos en este mismo PC y con este
  mismo plan.
