# Bitácora de uso de inteligencia artificial

La IA es una herramienta de apoyo permitida. Cada uso relevante se registra. **Usted es responsable de
verificar todo lo que la IA produce y de poder explicarlo sin ella.**

| #   | Fecha | Integrante | Herramienta | Propósito (investigar, depurar, alternativas...) | Consulta (resumen) | ¿Qué se usó de la respuesta? | ¿Cómo se verificó? | Errores o suposiciones detectadas en la respuesta |
| --- | ----- | ---------- | ----------- | ------------------------------------------------ | ------------------ | ---------------------------- | ------------------ | ------------------------------------------------- |
| 1   |       |            |             |                                                  |                    |                              |                    |                                                   |

## Reflexión individual (Clase 5, una por integrante)

- **Nombre:** Andrés Felipe Vargas Metrio
- **¿En qué le ayudó la IA y en qué lo confundió?** Me ayudó a estructurar rápido `estrategia_b.py` y `estrategia_c.py` respetando la firma de `linea_base.py`, a conectarlas en `ejecutar_experimento.py` y a redactar la explicación del `README.md` §5; también me ayudó a armar `experimentos/analizar_resultados.py` para R4 y a entender qué significaban los números de memoria y tiempo. Me confundió un poco cuando recibí varios pasos a la vez, al correr el comando desde la ruta equivocada y al ver que faltaban librerías (`numpy`, `pandas`, `matplotlib`), además de tener que comprobar que las hipótesis `H1–H3` en `docs/hipotesis.md` estaban vacías.
- **Un error o afirmación sin evidencia que detectó en la IA y cómo lo comprobó:** No dar por sentado un consumo de memoria sin medirlo; lo comprobé ejecutando con `n = 300 000` (`0.20 MiB` en Estrategia B y `2.54 MiB` en Estrategia C) y corriendo `--rapido`. En R4, lo comprobé ejecutando `python experimentos/analizar_resultados.py` sobre `resultados/resultados.csv` (`n = 200000`: `0.205 MiB` en B, `1.761 MiB` en C y `78.183 MiB` en A; `CV` entre `1.23` y `1.29` en tiempo) y abriendo `docs/hipotesis.md` para ver que `H1–H3` aún no estaban diligenciadas.
- **Qué parte del proyecto puede explicar completamente sin ayuda:** Puedo explicar de forma sencilla lo que hice y comprobé en la práctica: cómo correr las estrategias y el experimento rápido, qué archivos se generan en `resultados/` al ejecutar `experimentos/analizar_resultados.py`, qué muestran los valores de memoria y tiempo para `n = 200000` (incluyendo que la repetición `0` con medición de memoria eleva la dispersión del tiempo) y el flujo básico de ramas y Pull Request en Git. Todavía estoy afianzando con más calma los detalles teóricos profundos de estadística y la comparación formal de hipótesis cuando el equipo complete `docs/hipotesis.md`.
