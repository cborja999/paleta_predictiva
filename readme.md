# paleta_predictiva

**Paleta predictiva** es una web app que arma un brief de las fashion weeks (Nueva York, Londres, Milán y París) y dice qué tendencias **tienden a quedarse**, para marcas de indumentaria argentinas chicas y medianas que no pueden ir a los desfiles ni pagar un servicio de forecasting.

Proyecto de la materia K576 - IA Aplicada al diseño de productos digitales (Universidad de San Andrés).
Integrantes: Beltrán Martínez, Borja Centeno y Luigi Bonomi.

## Hipótesis

> **Una tendencia de pasarela que gana búsquedas en su primer año rara vez se desploma en el segundo.**

**Confirmada con datos nuevos.** En 57 tendencias de 2016-2018 (no usadas para formular la hipótesis, reglas fijadas antes de bajar los datos), de las que ganaron búsquedas el primer año solo **1 de 17 (6%)** fue pasajera. En los 8 ciclos de 2016→2017 a 2023→2024 nunca pasó del 20%. En total, **9 de cada 10** tendencias que ganan búsquedas siguen ahí al segundo año.

**Las que pierden búsquedas:** los datos de 2021 a 2024 muestran que las tendencias que pierden búsquedas en su primer año tienen más del triple de chances de ser pasajeras: **9 de 16 (56%)** contra **2 de 19 (11%)** de las que las ganan.

Definiciones, resultados ciclo por ciclo y límites: **[`hipotesis.md`](hipotesis.md)**.

## Cómo se mide

1. Medios de moda nombran las tendencias principales de cada fashion week (listas elegidas por ellos en su momento).
2. Cada tendencia se pasa a un término de búsqueda literal (documentado fila por fila).
3. Google Trends, mundo, mensual: se compara el año antes del desfile, el primer año y el segundo, descontando lo que se movió toda la temporada.
4. **Ganó búsquedas** = subió al menos 10% el primer año. **Pasajera** = perdió más de ~10% el segundo.

## La página

`app/index.html`: la hipótesis al frente, el resultado de la prueba, la tabla ciclo por ciclo, las curvas de las 178 tendencias con filtros y el brief de hoy (colores, prendas y largos con su lectura de búsquedas). Se publica en Netlify desde `app/`.

Los datos de la página se arman con `python3 -I app/armar_datos.py` y `python3 -I app/armar_microtendencias.py`.

## Datasets

Todos los datasets están en la repo, salvo los que no se pueden redistribuir (ver al final).

### Prueba de la hipótesis

| Archivo | Qué es | Fuente |
|---|---|---|
| `analisis/hipotesis/datos/trends_c1_web.csv` | Google Trends mensual 2011-2024 de 57 tendencias de 2016-2018 | Google Trends (bajado el 20/10/2026) |
| `analisis/hipotesis/fuentes_listas_c1.csv` | Las 9 listas de tendencias usadas, con fecha y link | Sandra's Closet, W Magazine, Fashionista |
| `analisis/hipotesis/terminos_declarados_c1.csv` | Cada tendencia y su término de búsqueda (y las descartadas, con motivo) | Elaboración propia |
| `analisis/hipotesis/c1_detalle.csv` | Resultado por tendencia (grupo, se quedó o no) | `c1.py` |
| `analisis/hipotesis/ciclos.csv` | Resultado por ciclo 2016→2017 a 2023→2024 | `c1.py` |
| `analisis/microtendencias/datos/trends_microtendencias_web.csv` | Google Trends de 68 tendencias de Who What Wear 2019-2023 | Google Trends |
| `analisis/microtendencias/datos/trends_microtendencias_web_m2.csv` | Google Trends de 54 tendencias de Sandra's Closet 2020-2023 | Google Trends |
| `analisis/microtendencias/datos/trends_microtendencias_shopping.csv` | Lo mismo que el primero, en Google Shopping | Google Trends |
| `analisis/microtendencias/fuentes_listas.csv`, `fuentes_listas_m2.csv` | Listas de 2019-2023, con fecha y link | Who What Wear, Sandra's Closet |
| `analisis/microtendencias/terminos_declarados*.csv`, `m1_detalle.csv`, `m2_detalle.csv` | Términos y resultado por tendencia | Elaboración propia |

### Pasarela

| Archivo | Qué es | Fuente |
|---|---|---|
| `datasets/muestra_vogue_para_gemini.csv` | 2.430 looks de Vogue Runway (15 casas, FW2011-SS2024), sin imágenes | Hugging Face `tonyassi/vogue-runway-top15-512px` |
| `datasets_procesados/resultados_gemini.csv` | Color, prenda, silueta y largo de cada look, clasificado con Gemini | Elaboración propia |
| `analisis/validacion_gemini_muestra.csv` | Validación a mano de 40 fotos | Elaboración propia |
| `analisis/participacion_por_temporada.csv` | % de looks por color, prenda y largo en cada temporada | A partir de la clasificación |
| `analisis/color_real_por_categoria.csv` | Color medido en las fotos para cada etiqueta | A partir de las fotos |
| `datasets/runway_reportes_2025_2026.csv` | 110 datos públicos de presencia en pasarela 2025-2026 | T-Fashion y reportes públicos de WGSN (resúmenes secundarios) |

### Búsquedas por categoría y marcas

| Archivo | Qué es | Fuente |
|---|---|---|
| `datasets/trends/trends_unificado.csv` | Google Trends de colores, prendas y largos | Google Trends |
| `analisis/persistencia/datos/trends_nuevos_2026-10-19.csv` | Google Trends mundo y Argentina 2011-2026, dos formas de buscar | Google Trends |
| `analisis/persistencia/datos/trends_shopping_2026-10-19.csv`, `trends_shopping_AR_2026-10-20.csv` | Google Shopping mundo y Argentina | Google Trends |
| `analisis/persistencia/prediccion_congelada_2026-10-19.csv` | Brief congelado el 19/10/2026 (63 filas, huella sha256) | Elaboración propia |
| `datasets/trends_marcas/*.csv`, `marcas_unificado.csv` | Búsquedas de casas de lujo, marcas masivas y argentinas 2004-2026 | Google Trends |
| `datasets/trends_casos/*.csv` | Casos Triple S, rosa Barbie y minifalda Miu Miu | Google Trends |

### Prensa y medios

| Archivo | Qué es | Fuente |
|---|---|---|
| `datasets/prensa_argentina/planilla_prensa_notas_2026-10-20.csv` | 83 notas de prensa argentina sobre tendencias (fecha, título, link y etiquetas) | Cargada por el grupo |
| `datasets/prensa_internacional/notas_2022.csv` | 15 notas internacionales de SS2022-SS2023 con etiquetas | Fashionista, Who What Wear, Vogue Scandinavia |
| `datasets/corpus_medios/` | Protocolo, lista de fuentes y plantilla del corpus de medios | Elaboración propia |
| `datasets/fuentes_candidatas.md` | Fuentes de datos evaluadas | Elaboración propia |

De las notas se guardan solo etiquetas, fecha, título y link; no se copia texto.

Diccionario de columnas: `datasets/diccionario.md`.

### No incluidos (derechos)

- Fotos de Vogue Runway: `runway_gemini/bajar_fotos_vogue.py` las descarga.
- Datos crudos del Lyst Index (Lyst no permite redistribuirlos); en la repo solo hay agregados (`analisis/lyst_*.csv`).
- Claves de API: nunca se suben. Para clasificar con Gemini hace falta una propia (`export GEMINI_API_KEY=...`).

## Estructura

| Carpeta / archivo | Qué hay |
|---|---|
| `hipotesis.md` | La hipótesis, definiciones, resultados y límites |
| `analisis/hipotesis/` | Prueba con datos nuevos 2016-2018: reglas, datos, `c1.py`, `salida_c1.txt` |
| `analisis/microtendencias/` | Tendencias 2019-2023: reglas, datos, `m1.py`, `m2.py`, salidas |
| `analisis/persistencia/` | Búsquedas por categoría, Shopping, Argentina y predicción congelada |
| `analisis/` | Cruce pasarela-búsquedas, marcas, casos, Lyst, backtest y validación de Gemini |
| `runway_gemini/` | Scripts para bajar y clasificar fotos de pasarela |
| `datasets/`, `datasets_procesados/` | Datos de entrada y clasificación |
| `app/` | La página y los scripts que arman sus datos |
| `entregas/` | Material de las entregas |
| `decisiones.md` | Registro de decisiones con fecha |

## Cómo repetir la prueba

```
cd analisis/hipotesis && python3 -I c1.py          # da salida_c1.txt
cd analisis/microtendencias && python3 -I m1.py    # da salida_m1.txt
cd analisis/microtendencias && python3 -I m2.py    # da salida_m2.txt
```

Las reglas de cada prueba se escribieron antes de correrla (`REGLAS_*.txt`) y tienen huella sha256 para comprobar que no cambiaron.
