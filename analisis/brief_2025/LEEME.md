# SS2025 (01/11/2026)

## Resultado

**SS2025 lleva veredicto.** Pasó el chequeo fijado de antemano en `REGLAS_BRIEF_2025.txt`:

| Chequeo | SS2025 | Referencia 2024 (datos limpios) | Límite |
|---|---|---|---|
| V1: el veredicto depende del volumen real del término | −0,01 | −0,22 | 0,5 |
| V2: el veredicto depende de cuánto se infló el término en 2026 | −0,08 | +0,02 | 0,5 |
| V3: el cambio de enero de 2025 depende del volumen | +0,26 | +0,04 | 0,5 |

- 26 términos usables: **8 tienden a quedarse, 5 con riesgo de moda pasajera, 13 sin señal clara.**
- La lectura corta, que no cruza enero de 2025 (oct-dic), coincide como en temporadas limpias: Spearman +0,67 contra una mediana limpia de +0,68. Ningún veredicto va en sentido contrario.
- **Cuidado.** Sin agosto y septiembre de 2025 (cuando empieza la suba de Google), cambian 5 lecturas. Tres de ellas son "se queda" que pasarían a "sin señal clara": statement sunglasses, one leg pants y dress over pants. Statement sunglasses además se apoya en un pico de un solo mes (sep-2025). Los veredictos quedan como dicen las reglas. La app muestra esta nota en cada una; es un dato descriptivo que se agregó después de ver los resultados.

## ¿Se quedó en 2026? No se puede saber con Google Trends

La prueba de factibilidad del segundo año **no pasa**:

- Después de descontar el volumen, la dispersión del salto de 2026 es 0,59, contra 0,18 en un año limpio (2024 contra 2023). Es 3,2 veces más; el límite era 1,25.
- El salto de feb-may 2026 es enorme (mediana: 3,6 veces el nivel de 2025) y distinto en cada término, y el volumen explica poco de esa diferencia (Spearman −0,36).
- Comparar contra términos de volumen parecido no alcanza para separar un cambio real de ±10% del problema de medición.

Una corrección para el diagnóstico de 2026: ahí se dijo que el salto "es más grande cuanto más chico el término" (Spearman −0,84). Esa medida usaba el nivel de cada término en su propia escala de 0 a 100, y eso infla la relación. Medido contra un ancla común, el efecto existe, pero es más débil (−0,36).

## Archivos

1. `fuentes_listas_2025.csv` y `terminos_declarados_2025.csv`: listas de SS2025 y el término de cada tendencia (26).
2. `REGLAS_BRIEF_2025.txt` y `SHA256_reglas_2025.txt`: reglas y chequeo, fijados antes de bajar datos (27/10/2026). `referencia_lectura_corta.py` calcula, con datos limpios, cuánto coincide la lectura oct-dic con la de 12 meses.
3. `datos/`: Google Trends bajado el 01/11/2026 con las mismas consultas de `descargar_trends.js`, verificado con checksum.
   - `trends_A_2011_2025-09.csv`: mensual, ene-2011 a sep-2025.
   - `trends_B_2024_2026.csv`: semanal pasado a meses, dic-2023 a sep-2026. El primer mes tiene una sola semana.
   - `volumen_ancla.csv`: cada término contra "midi skirt", oct-2023 a sep-2024.
4. `brief_ss2025.py`: aplica las reglas. Escribe `salida_brief_ss2025.txt`, `brief_ss2025_detalle.csv` y `app/datos/brief_ss2025.json`.

Para repetir: `cd analisis/brief_2025 && sha256sum -c SHA256_reglas_2025.txt && python3 -I brief_ss2025.py`
