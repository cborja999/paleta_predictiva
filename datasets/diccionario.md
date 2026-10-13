# Diccionario de datos

Los datasets finales siguen en redefinicion. Por ahora estan documentados los generados por el analisis de octubre 2026.

## runway_gemini/resultados_gemini.csv
Una fila por foto de Vogue Runway clasificada con Gemini (2.430 fotos, FW2011 a SS2024, 90 por temporada).
- `id`, `temporada`, `anio`, `ciudad`, `marca`, `look`: identifican la foto.
- `color_dominante`, `color_secundario`, `prenda_principal`, `silueta`, `largo`: clasificacion de Gemini.
- `confianza`: confianza declarada por el modelo. `error`: vacio si la clasificacion salio bien.
Fuente de las fotos: `tonyassi/vogue-runway-top15-512px` (Hugging Face).

## datasets/trends/trends_unificado.csv
Google Trends mensual por termino (todas las tandas unidas).
- `termino`, `tipo`, `categoria_gemini`: termino buscado y categoria de la clasificacion a la que se asocia.
- `mes`, `valor`: mes y valor (0 a 100, relativo a cada serie).
- `archivo_origen`, `max_serie`, `usable`: origen y maximo de la serie; `usable` es falso si el volumen es muy bajo.

## datasets/runway_reportes_2025_2026.csv
Reportes publicos de presencia en pasarela (T-Fashion y otros), 110 filas.
- `temporada`, `ciudad`, `genero`, `fuente`, `fecha_publicacion`, `alcance`, `tipo`, `tendencia`, `metrica`, `valor`, `url`, `nota`.
- Son resumenes secundarios publicos, no datos propios.
