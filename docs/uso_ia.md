# Bitácora de uso de inteligencia artificial

La IA es una herramienta de apoyo permitida. Cada uso relevante se registra. **Usted es responsable de
verificar todo lo que la IA produce y de poder explicarlo sin ella.**

| # | Fecha | Integrante | Herramienta | Propósito (investigar, depurar, alternativas...) | Consulta (resumen) | ¿Qué se usó de la respuesta? | ¿Cómo se verificó? | Errores o suposiciones detectadas en la respuesta |
|---|---|---|---|---|---|---|---|---|
| 1 | 2026-11-25 | Durman | Copilot | Entender la línea base y añadir comprobaciones de corrección | Revisar el cálculo de la línea base, escribir pruebas comparativas para B y C y completar la comparación tolerante del experimento | Se añadieron pruebas por sensor para verificar los 200 sensores y comparar media y máxima; el experimento compara los mismos datos con tolerancia | `py -m unittest discover -s pruebas` | B y C no están en la rama local, así que sus pruebas quedan omitidas hasta integrar esos módulos. En este equipo se usó `py` porque `python` no está disponible en el PATH |

## Reflexión individual (Clase 5, una por integrante)
- **Nombre:** Durman
- La IA me ayudó a entender cómo se comparan las estrategias con la línea base y a completar las pruebas. Al principio asumió que las estrategias B y C estaban disponibles en mi rama; al revisar los archivos vi que todavía no estaban ahí, así que las pruebas quedan preparadas para ejecutarse cuando se integren.
- Detecté que el comando `python` que se había propuesto no funcionaba en mi equipo. Lo comprobé al ejecutarlo y usé `py` en su lugar. También confirmé que las pruebas de B y C se omitían porque sus módulos no estaban presentes.
- Puedo explicar cómo la línea base lee el CSV, guarda cada fila como un diccionario y agrupa las temperaturas por sensor para calcular la media y la máxima. Al conservar todas esas filas y además crear las listas de temperaturas, su consumo de memoria crece bastante.
