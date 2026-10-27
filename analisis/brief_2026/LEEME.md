# Brief de la temporada (27/10/2026)

Qué hay en esta carpeta y qué usa la página.

## Lo que usa la página: `app/datos/brief_temporada.json`

- **Con veredicto: SS2024 y FW2024** (31 tendencias puntuales). Es la última temporada cuyo primer año se puede medir con datos limpios de Google. Mismo método que la hipótesis: búsquedas del primer año después del desfile contra el año previo, descontando lo que se movió toda la temporada.
  - SS2024: 4 tienden a quedarse, 4 con riesgo de pasajera, 8 sin señal clara.
  - FW2024: 4 tienden a quedarse, 7 con riesgo de pasajera, 4 sin señal clara.
  - Control de volumen: sin sesgo (Spearman −0,04 y −0,23).
  - Dos lecturas se apoyan en un pico de un solo mes (pillbox hat y faux fur coat): el JSON lo marca en `aviso`.
- **Sin veredicto: SS2026 y FW2026** (36 tendencias en `vistas_2026`). Se muestran como "lo que se vio". Desde mediados de 2025 Google Trends cambió cómo mide y los términos chicos salen inflados (ver `DIAGNOSTICO_2026.md`).

## Archivos

| Archivo | Qué es |
|---|---|
| `REGLAS_BRIEF_2024.txt`, `SHA256_reglas_2024.txt` | Reglas fijadas antes de bajar los datos, con los ajustes fechados |
| `fuentes_listas_2024.csv`, `terminos_declarados_2024.csv` | Listas de Who What Wear, CBC Life y Yahoo Lifestyle y su término de búsqueda |
| `datos/trends_2024_web.csv` | Google Trends mundo mensual ene-2011 a feb-2025 |
| `brief_temporada.py` | Arma `salida_brief_2024.txt`, `brief_2024_detalle.csv` y el JSON de la página |
| `salida_brief_2024_corrida_con_error.txt` | Primera corrida, con ene-feb 2025 faltantes contados como cero (error corregido) |
| `DIAGNOSTICO_2026.md`, `diagnostico_2026.py` | Por qué 2026 no tiene veredicto |
| `REGLAS_BRIEF_2026.txt`, `fuentes_listas_2026.csv`, `terminos_declarados_2026.csv`, `datos/trends_2026_web.csv` | Tendencias de SS2026 y FW2026 |

## Límite

El veredicto es la lectura del primer año, que es lo que usa la hipótesis para anticipar. El segundo año de estas tendencias (2025-2026) no se puede medir limpio, así que todavía no sabemos si se quedaron.

Para repetir: `cd analisis/brief_2026 && python3 -I brief_temporada.py`
