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
- **Temperatura disponible (sí/no) y plan B:** no. Plan B: revisar si el tiempo aumenta corrida tras
  corrida (señal de calentamiento), con el orden aleatorio de las corridas repartiendo ese efecto entre
  las estrategias, y registrar la frecuencia y el CPU % con `monitor_sistema.py`.
  (Antes decía "pausa de 30 s entre corridas", pero `ejecutar_experimento.py` no hace pausas; se corrige
  para que el documento diga lo que de verdad se hace.)
- **Energía RAPL disponible (sí/no):** no (RAPL no funciona en Windows). No se mide energía y no se
  afirma nada sobre ahorro de energía.

## Sesión del experimento formal: 25/11/2026

`diagnostico_entorno.py` dio **los mismos valores** de la tabla de arriba (mismo SO, procesador, núcleos,
15.63 GiB de RAM, Python 3.14.3 y 2200 MHz). Revisado a las 11:31, antes de medir:

- **Cargador:** conectado (batería al 79 %). **Plan de energía:** "Turbo".
- **RAM del sistema usada:** 54.5 % (8.53 de 15.63 GiB; 7.11 GiB libres), después de cerrar Brave y VS Code
  (antes estaba en 72.7 %). Ver decisión D-003.
- **Programas con ventana abiertos:** Windows Terminal (desde donde se ejecuta), NVIDIA Overlay,
  Configuración de Windows. En segundo plano: WhatsApp y Vínculo con el teléfono.
- **CPU % del sistema en reposo:** 9.3 % (medido con psutil durante 2 s).
- **Suspensión con cargador:** se cambió de 5 min a "Nunca" (`powercfg /change standby-timeout-ac 0`)
  para que el PC no se suspendiera durante la medición. Se devuelve a 5 min al terminar.
- **Pruebas de corrección:** OK. **Prueba de humo (`--rapido`):** OK, 9 filas, las 3 estrategias dan el
  mismo resultado que la línea base.

## Observaciones

- psutil siempre reporta 2200 MHz, pero la frecuencia real puede subir (turbo) o bajar (ahorro).
  Por eso los ciclos calculados como N = f·t son solo una estimación.
- El servidor real de la empresa tiene 2 GiB de RAM; este PC tiene 15.63 GiB. Aquí el programa no
  se queda sin memoria, así que medimos el **pico de memoria (MiB)** y lo comparamos con el límite
  de 2 GiB.
