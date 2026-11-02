# FW2025 (02/11/2026)

## Resultado

**FW2025 lleva veredicto.** Pasó el chequeo fijado de antemano en `REGLAS_BRIEF_FW2025.txt` (huellas en `SHA256_reglas_fw2025.txt`, escritas antes de bajar datos):

| Chequeo | FW2025 | Límite |
|---|---|---|
| V1: el veredicto depende del volumen del término | −0,21 | falla si \|rho\| ≥ 0,5 |
| V3: el cambio de enero de 2025 depende del volumen | −0,16 | falla si \|rho\| ≥ 0,5 |
| V4: 12 meses contra mar-jul 2025 (antes de la suba de Google) | +0,70, ningún veredicto opuesto | falla si rho < 0,50 o más de 1 opuesto |
| V2: salto de 2026 (solo se informa) | +0,18 | no decide |

- 20 términos usables: **7 tienden a quedarse, 6 con riesgo de moda pasajera, 7 sin señal clara.**
- La referencia de V4 se calculó con datos limpios antes de bajar nada de FW2025 (`referencia_lectura_corta_fw.py`): en temporadas FW de 2016 a 2024 la coincidencia entre 12 meses y mar-jul va de +0,05 a +0,96, con mediana +0,75. FW2025 da +0,70.

## Cuidado (descriptivo, agregado después de ver los resultados; no cambia ningún veredicto)

- **El primer año de FW2025 tiene 7 de 12 meses en el período en que Google empezó a medir distinto.** El chequeo pasa, pero la lectura es menos firme que la de 2024.
- **8 de los 13 veredictos cambian si se mira solo mar-jul 2025:** brooch, black lace, statement coat, ruffle collar y floral print pasan de "se queda" a "sin señal clara"; cardigan, pearl necklace y jogging pants pasan de "riesgo" a "sin señal clara". Ninguno se da vuelta (de "se queda" a "riesgo" o al revés). En temporadas FW limpias, el mismo veredicto entre las dos lecturas va de 40% a 78% (mediana 57%); acá es 38% (5 de 13). La app marca la nota en cada una (`lectura_marjul`).
- **Los dos "se queda" más fuertes son términos muy chicos:** statement coat y asymmetric jacket tienen volumen 0 contra el ancla "midi skirt", y la mayor parte de su suba está en ago-2025 a feb-2026. V1 pasa para la temporada entera (−0,21), pero estos dos casos son el tipo de término que más infló Google (ver `../brief_2026/DIAGNOSTICO_2026.md`).
- floral print se apoya además en un pico de un solo mes (feb-2026).

## Archivos

1. `fuentes_listas_fw2025.csv` y `terminos_declarados_fw2025.csv`: Who What Wear (copia de Wayback del 2025-03-27), CBC Life (copia de Wayback del 2025-03-17) y Harper's Bazaar en Yahoo Lifestyle (2025-03-24). 29 temas, 20 términos, 9 descartados con su motivo.
2. `REGLAS_BRIEF_FW2025.txt`, `SHA256_reglas_fw2025.txt`, `referencia_lectura_corta_fw.py` y su salida.
3. `datos/`: Google Trends bajado el 02/11/2026 desde el navegador con `descargar_trends_fw2025.js` (mismas consultas que SS2025, adaptadas); los tres archivos coinciden con el checksum que calculó el navegador (A 938586702, B 548144662, V 388783141).
4. `brief_fw2025.py`: aplica las reglas. Escribe `salida_brief_fw2025.txt`, `brief_fw2025_detalle.csv` y `app/datos/brief_fw2025.json`.

Para repetir: `cd analisis/brief_fw2025 && shasum -a 256 -c SHA256_reglas_fw2025.txt && python3 -I brief_fw2025.py`
