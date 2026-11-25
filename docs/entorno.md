# Entorno experimental

Salida de `diagnostico_entorno.py` (Clase 3), ejecutado en el PC del Integrante A el 18/11/2026.

| Característica | Valor |
|---|---|
| sistema_operativo | Windows 11 (10.0.26200) |
| arquitectura | AMD64 |
| procesador | Intel64 Family 6 Model 186 Stepping 2, GenuineIntel |
| nucleos_logicos | 12 |
| python | 3.14.3 |
| nucleos_fisicos | 8 |
| memoria_total_gib | 15.63 |
| frecuencia_actual_mhz | 2200.0 |
| frecuencia_min_mhz | None |
| frecuencia_max_mhz | 2200.0 |
| sensores | {'frecuencia': True, 'temperatura': False, 'energia_rapl': False, 'psutil': True} |
| temperatura_actual_c | None |

> Generado con diagnostico_entorno.py. Los resultados de este equipo solo son
> comparables con otros obtenidos en ESTE mismo entorno.

## Condiciones del experimento

Revisado el 18/11/2026 a las 22:34, justo antes de repetir la línea base:

- **¿Conectado a corriente?:** sí (cargador conectado, batería al 79 %, según `psutil.sensors_battery()`).
  Plan de energía: "Turbo" (según `powercfg /getactivescheme`).
- **Aplicaciones abiertas durante la medición:** Brave (navegador), VS Code, Windows Terminal,
  NVIDIA Overlay y Configuración de Windows (lista de programas con ventana, según `Get-Process`).
  Para el experimento formal se deben cerrar el navegador y VS Code (ver `docs/protocolo.md`).
- **Temperatura disponible (sí/no) y plan B:** no. Plan B: dejar una pausa de 30 s entre corridas y
  revisar si el tiempo aumenta corrida tras corrida (señal de calentamiento).
- **Energía RAPL disponible (sí/no):** no (RAPL no funciona en Windows). No se mide energía y no se
  afirma nada sobre ahorro de energía.

## Observaciones

- psutil siempre reporta 2200 MHz, pero la frecuencia real puede subir (turbo) o bajar (ahorro).
  Por eso los ciclos calculados como N = f·t son solo una estimación.
- El servidor real de la empresa tiene 2 GiB de RAM; este PC tiene 15.63 GiB. Aquí el programa no
  se queda sin memoria, así que medimos el **pico de memoria (MiB)** y lo comparamos con el límite
  de 2 GiB.
