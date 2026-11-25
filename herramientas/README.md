# Scripts · Clase 3 — Diseño de soluciones y formulación experimental

Requisitos: Python 3.10+. Opcional: `pip install psutil` (más datos del entorno y frecuencia).

| Script | Qué hace | Magnitud física | Uso |
|---|---|---|---|
| `diagnostico_entorno.py` | Ficha técnica del equipo (SO, CPU, núcleos, RAM, frecuencia, sensores disponibles). Genera `entorno_equipo.json/.md` | f [MHz], θ [°C] si existe | `python diagnostico_entorno.py` |
| `ciclos_y_frecuencia.py` | Mide un bucle y estima ciclos N = f·t y ciclos por iteración | t [s], f [Hz], N | `python ciclos_y_frecuencia.py 5000000` |
| `prototipo_estrategias.py` | Plantilla de prototipo: datos con semilla, 3 estrategias, verificación de corrección, medición preliminar (problema neutro) | t [s] | `python prototipo_estrategias.py 200000` |

**Advertencias:** N = f·t es una estimación (la frecuencia cambia). Una sola corrida no es un experimento.
`diagnostico_entorno.py` reutiliza `../../02_Clase_4/Scripts/sensores.py` si está disponible.

---

# Práctica: datos de prueba en el PC del Integrante A

> ⚠️ **IMPORTANTE:** todo lo que sigue son **pruebas de práctica** hechas en el PC del Integrante A
> (Santiago) para aprender a usar los scripts de la Clase 3. Casi todo usa el **problema neutro del
> profesor** (concatenación, join y buffer), que **NO es el problema del Equipo 4**.
> Son **corridas únicas** (no son un experimento formal) y **no** se deben presentar como resultados
> del proyecto. Las hipótesis y variables oficiales del equipo están en `docs/hipotesis.md` y
> `docs/variables.md`.

**Equipo usado:** Windows 11, Intel (8 núcleos físicos / 12 lógicos), 15.63 GiB de RAM, Python 3.14.3.
**Fecha:** 18/11/2026.

## 1. diagnostico_entorno.py

```
py diagnostico_entorno.py
sistema_operativo       : Windows 11 (10.0.26200)
arquitectura            : AMD64
procesador              : Intel64 Family 6 Model 186 Stepping 2, GenuineIntel
nucleos_logicos         : 12
python                  : 3.14.3
nucleos_fisicos         : 8
memoria_total_gib       : 15.63
frecuencia_actual_mhz   : 2200.0
frecuencia_min_mhz      : None
frecuencia_max_mhz      : 2200.0
sensores                : {'frecuencia': True, 'temperatura': False, 'energia_rapl': False, 'psutil': True}
temperatura_actual_c    : None
```

## 2. sensores.py

```
py sensores.py
Sistema: Windows 11 · AMD64
Núcleos lógicos: 12
psutil instalado: sí
Frecuencia actual: 2200.0 MHz
Temperatura: no disponible -> usar plan B (ver Guía de medición)
Energía RAPL: no disponible (normal sin Intel/Linux o sin permisos de root)
```

## 3. ciclos_y_frecuencia.py (5 000 000 y 10 000 000 iteraciones)

```
py ciclos_y_frecuencia.py 5000000
Iteraciones n           : 5,000,000
Tiempo medido t         : 0.3509 s
Frecuencia f            : 2.20 GHz (medida con psutil)
Periodo de reloj T = 1/f: 0.455 ns
Ciclos estimados f·t    : 7.719e+08 ciclos
Ciclos por iteración    : 154

py ciclos_y_frecuencia.py 10000000
Iteraciones n           : 10,000,000
Tiempo medido t         : 0.8150 s        <- cambió
Frecuencia f            : 2.20 GHz (medida con psutil)
Periodo de reloj T = 1/f: 0.455 ns
Ciclos estimados f·t    : 1.793e+09 ciclos  <- cambió
Ciclos por iteración    : 179             <- cambió
```

**Lo que observé:** a mayor número de iteraciones, mayor tiempo medido, más ciclos estimados (f·t)
y también más ciclos por iteración (154 → 179). Si el trabajo fuera exactamente proporcional, los
ciclos por iteración deberían quedar casi iguales.

## 4. prototipo_estrategias.py (problema neutro del profesor)

| Corrida | n | concatenación | join | buffer |
|---|---|---|---|---|
| 1 | 200 000 (por defecto) | 0.4662 s | 0.0512 s | 0.0486 s |
| 2 | 200 000 | 0.5709 s | 0.0511 s | 0.0494 s |
| 3 | 2 000 000 | 42.3394 s | 0.5038 s | 0.4582 s |
| 4 | 200 000 | 0.4646 s | 0.0512 s | 0.0467 s |

Corrección verificada en todas: las 3 estrategias dan el mismo texto (3 956 707 caracteres con
n = 200 000 y 39 567 216 con n = 2 000 000).

**Cuántas veces crece el tiempo si n crece 10 veces** (usando la corrida 4 y la 3):

| Estrategia | n = 200 000 | n = 2 000 000 | Cuántas veces más |
|---|---|---|---|
| join | 0.0512 s | 0.5038 s | ≈ 10× |
| buffer | 0.0467 s | 0.4582 s | ≈ 10× |
| concatenación | 0.4646 s | 42.34 s | ≈ 91× |

- join y buffer crecen de forma normal (lineal): 10 veces más datos, 10 veces más tiempo.
- concatenación crece de forma acelerada (casi cuadrática): 10 veces más datos, casi 100 veces más tiempo.
- Con el **mismo** n = 200 000, la concatenación dio 0.4662 s, 0.5709 s y 0.4646 s (≈ 23 % de
  diferencia entre la más lenta y la más rápida). Por eso una sola corrida no basta: hay que repetir.

## 5. Hipótesis de práctica (sobre el problema neutro)

| Id | Hipótesis | VI | VD (unidad) | Predicción | Cómo la refutaríamos |
|---|---|---|---|---|---|
| H1-práctica | **Si** n aumenta 10 veces (de 200 000 a 2 000 000), **entonces** el tiempo (s) de join y buffer **aumentará** aproximadamente 10 veces, **porque** cada línea se formatea y se copia en memoria un número fijo de veces. | n (líneas) | t (s) | t(2 000 000) / t(200 000) ≈ 10 (entre 8 y 13) | Si el cociente es menor que 8 o mayor que 13 en el promedio de 5 repeticiones. |
| H2-práctica | **Si** n aumenta 10 veces, **entonces** el tiempo (s) de la concatenación **aumentará** mucho más de 10 veces (cerca de 100), **porque** el texto acumulado se copia muchas veces a otra zona de la RAM (los bytes copiados crecen como n²). | n (líneas) | t (s) | cociente > 20 (esperado cerca de 100) | Si el cociente es menor que 20. |
| H3-práctica | **Si** n aumenta de 5 000 000 a 10 000 000 iteraciones, **entonces** los ciclos por iteración **aumentarán** al menos un 10 %, **porque** los datos dejan de caber en la caché y el procesador espera a la RAM. | n (iteraciones) | ciclos por iteración (ciclos = f·t) | aumento ≥ 10 % (preliminar: 154 → 179, +16 %) | Si en 5 repeticiones el aumento es menor que 10 % o cambia de signo. |

> **Nota de revisión sobre H3-práctica:** el bucle de `ciclos_y_frecuencia.py` (`acumulado += i * i`)
> no guarda una lista de datos, así que "los datos no caben en la caché" probablemente **no** es la
> explicación. Una explicación posible (sin comprobar) es que `acumulado` se vuelve un número muy
> grande y Python tarda más en sumar números grandes. Además viene de una sola corrida: podría ser ruido.

## 6. Variables de práctica (sobre el problema neutro)

| Tipo | Variable | Unidad | Valores | Justificación |
|---|---|---|---|---|
| Independiente | Estrategia | — | concatenación, join, buffer (StringIO) | Tres formas de producir el mismo texto que difieren en cuántas veces se copian bytes en memoria. |
| Independiente | Tamaño n | líneas | 200 000 y 2 000 000 | Multiplicar n por 10 permite ver si el tiempo crece 10× (lineal) o cerca de 100× (cuadrático). |
| Dependiente | Tiempo t | s | — | time.perf_counter() |
| Controlada | Semilla | — | 7 (la del prototipo del profesor) | Las tres estrategias procesan los mismos datos. |

Mapa de dependencias de la práctica:
- `Concatenación → copias del texto acumulado (crecen como n²) → bytes movidos en la RAM → tiempo t`
- `Join y buffer → pocas copias (crecen como n) → bytes movidos en la RAM → tiempo t`
