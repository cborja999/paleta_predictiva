# Diccionario de datos

Los datasets finales siguen en redefinicion. Por ahora estan documentados los generados por el analisis de octubre 2026.

## datasets_procesados/resultados_gemini.csv
Una fila por foto de Vogue Runway clasificada con Gemini (2.430 fotos, FW2011 a SS2024, 90 por temporada).
- `id`, `temporada`, `anio`, `ciudad`, `marca`, `look`: identifican la foto.
- `color_dominante`, `color_secundario`, `prenda_principal`, `silueta`, `largo`: clasificacion de Gemini.
- `confianza`: confianza declarada por el modelo. `error`: vacio si la clasificacion salio bien.
La muestra de fotos de Vogue (sin las imagenes) esta en `datasets/muestra_vogue_para_gemini.csv`. Fuente de las fotos: `tonyassi/vogue-runway-top15-512px` (Hugging Face).

## datasets/trends/trends_unificado.csv
Google Trends mensual por termino (todas las tandas unidas).
- `termino`, `tipo`, `categoria_gemini`: termino buscado y categoria de la clasificacion a la que se asocia.
- `mes`, `valor`: mes y valor (0 a 100, relativo a cada serie).
- `archivo_origen`, `max_serie`, `usable`: origen y maximo de la serie; `usable` es falso si el volumen es muy bajo.

## datasets/runway_reportes_2025_2026.csv
Reportes publicos de presencia en pasarela (T-Fashion y otros), 110 filas.
- `temporada`, `ciudad`, `genero`, `fuente`, `fecha_publicacion`, `alcance`, `tipo`, `tendencia`, `metrica`, `valor`, `url`, `nota`.
- Son resumenes secundarios publicos, no datos propios.

## datasets/trends_marcas/
Ocho consultas de Google Trends (busqueda web, mensual 2004 a oct 2026) tal como se bajaron. El nombre indica la zona (`MUNDO` o `AR`) y los terminos. Cada consulta esta en su propia escala (0 a 100 dentro de esa consulta).

## datasets/trends_marcas/marcas_unificado.csv
Las ocho consultas unidas en una escala comparable (encadenadas por la marca ancla Gucci o Zara).
- `marca`, `grupo` (lujo, masiva o argentina), `geo` (MUNDO o AR), `mes`.
- `valor_normalizado`: indice de busqueda reescalado. Los de MUNDO son comparables entre si; los de AR tienen su propia escala (Zara de Argentina como referencia).
- `archivo_origen`: consulta de la que sale el dato.
- `volumen_bajo`: si el maximo de la serie fue menor a 12 sobre 100 en su consulta.
- `termino_ambiguo`: palabras que pueden mezclar otras busquedas (hermes, cos, mimo, vitamina, ayres, awada, mango, valentino).

## analisis/marcas_relevancia_por_temporada.csv
Para cada temporada de desfile y cada casa: indice de busqueda de los 12 meses previos al desfile, porcentaje entre las 14 casas y cantidad de fotos de esa casa.

## analisis/marcas_perfil_ponderado.csv
Correlacion promedio por desfase de 0 a 24 meses, con y sin ponderar cada foto por la relevancia de su casa.

## trends_casos/ y casos_resumen.csv / casos_pasarela.csv
- `trends_casos/CASO__*.csv`: Google Trends mundo, mensual, 2 o 3 terminos por archivo en la misma escala. `<1` se lee como 0,5.
- `casos_resumen.csv`: por termino, promedio de la base (12 meses previos al desfile) y de los años 1, 2 y 3; `mes_pico_media_movil` es poco confiable (saltos 2025-2026).
- `casos_pasarela.csv`: % de fotos con el rasgo (rosa o mini) en la temporada del desfile vs promedio del resto de temporadas.

## lyst/ (no versionado) y analisis/lyst_*.csv
- `datasets/lyst/lyst_index__34_trimestres.csv` (local, ignorado por git): trimestre, marca, puesto. Q1-18 a Q2-26; 2018 es top 10, desde Q1-19 top 20. Fuente: Lyst Index, via CICLO.
- `lyst_cobertura.csv`: por trimestre, cuantos puestos ocupan casas que estan en nuestras fotos.
- `lyst_vs_trends.csv`: puntos Lyst (21 - puesto, ultimos 4 trimestres) vs indice de Trends (12 meses) por casa, con rangos.
