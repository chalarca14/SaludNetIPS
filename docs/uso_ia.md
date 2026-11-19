# Bitácora de uso de inteligencia artificial

La IA es una herramienta de apoyo permitida. Cada uso relevante se registra. **Usted es responsable de
verificar todo lo que la IA produce y de poder explicarlo sin ella.**

| # | Fecha | Integrante | Herramienta | Propósito (investigar, depurar, alternativas...) | Consulta (resumen) | ¿Qué se usó de la respuesta? | ¿Cómo se verificó? | Errores o suposiciones detectadas en la respuesta |
|---|---|---|---|---|---|---|---|---|
| 1 | Antes del 18/11/2026 | Santiago (A) | _(completar: herramienta usada)_ | Investigar conceptos | Explicación de conceptos de la clase y de cosas que no sabía hacer (por ejemplo, correr los scripts) | Las explicaciones, para entender los temas | Comparando con la guía y con las salidas de los scripts en mi PC | _(completar si se detectó alguno)_ |
| 2 | 18/11/2026 | Santiago (A) | Claude (Claude Code) | Revisar el proyecto | Comparar la guía de la actividad con los archivos del repositorio y decir qué faltaba, qué estaba mal y qué le tocaba a cada rol; explicar cada paso | La lista de pendientes. Me hizo notar que mis hipótesis y variables de práctica eran sobre el ejemplo neutro del profesor y no sobre nuestro problema, y que la semilla de nuestros datos es 4 y no 7 | Revisé `src/generar_datos.py` (semilla 4) y la plantilla de hipótesis, que dice que el ejemplo no es de ningún equipo | — |
| 3 | 18/11/2026 | Santiago (A) | Claude (Claude Code) | Organizar el trabajo | Repartir los roles de Integrante B y C y redactar un issue por rol | El texto de los issues #1 a #4 | Los leí, los creé yo en GitHub y los asigné; la IA comprobó en GitHub que quedaron asignados | — |
| 4 | 18/11/2026 | Santiago (A) | Claude (Claude Code) | Medir y documentar | Redactar README §2, §3, física del problema y §7, `docs/entorno.md`, `docs/protocolo.md` y `docs/decisiones.md` a partir de mis mediciones | Borradores de esos archivos. La IA también ejecutó en mi PC la línea base (3 corridas: 1.70, 1.69 y 1.70 s; 117.5 MiB) y revisó el cargador, el plan de energía y los programas abiertos | Revisé cada archivo antes de hacer el commit. Los datos vienen de mis salidas y de las corridas hechas en mi PC | La IA había escrito en `entorno.md` que el plan era "Alto rendimiento" y que solo estaba abierta la terminal; era falso (el plan es "Turbo" y había otros programas abiertos). Se corrigió midiendo. Las cifras ≈ 5.2 millones de registros y ≈ 392 MiB son **estimaciones** que suponen crecimiento lineal |
| 5 | 18/11/2026 | Santiago (A) | Claude (Claude Code) | Redactar hipótesis | Adaptar mis hipótesis y variables de práctica al problema de memoria (H1, H2 y H3) | La redacción de `docs/hipotesis.md` y `docs/variables.md`, manteniendo mi estructura y mis planes B | Revisé que usaran mis datos (117.5 MiB, 411 B/registro, 2.2 GHz) y la semilla del código. Se verifican con el experimento formal | Los umbrales (90 %, 4 – 6, 0.8 – 1.2, 20 %) son **predicciones propuestas por la IA**, no datos. La IA corrigió una frase suya que atribuía al navegador un cambio de tiempo sin evidencia |

## Reflexión individual (Clase 5, una por integrante)
- **Nombre:**
- ¿En qué le ayudó la IA y en qué lo confundió?
- Un error o afirmación sin evidencia que detectó en la IA y cómo lo comprobó:
- ¿Qué parte del proyecto puede explicar completamente sin ayuda?
