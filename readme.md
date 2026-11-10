# Paleta predictiva

**¿Qué tendencia de la pasarela va a durar y cuál es moda pasajera?** Paleta predictiva es una web app que le contesta eso a las marcas de ropa argentinas chicas y medianas, con datos y sin pagar un servicio de forecasting.

**App:** https://paleta-predictiva.netlify.app

Proyecto de la materia K576 (IA aplicada al diseño de productos digitales, Universidad de San Andrés).
Integrantes: Beltrán Martínez, Borja Centeno y Luigi Bonomi.

## El problema

Dos veces por año, las fashion weeks de Nueva York, Londres, Milán y París marcan lo que viene. Las marcas grandes pagan servicios de tendencias que les dicen en qué apostar. Una marca argentina chica no puede: se entera por notas de medios que dicen "esto es tendencia", pero que no dicen si va a durar.

Y para una marca chica, equivocarse cuesta caro: producir de más algo que pasa de moda en seis meses es stock que no se vende. La decisión que queremos ayudar a tomar es concreta: **en qué tendencia apostar fuerte y en cuál probar poco.**

## Lo que probamos primero (y no funcionó)

La primera idea fue que **la pasarela anticipa las ventas masivas 12 a 18 meses después**. Para probarla clasificamos con Gemini 2.430 looks de Vogue Runway (15 casas, de 2011 a 2024) por color, prenda, silueta y largo, y los cruzamos con Google Trends.

No apareció ningún desfase entre lo que se vio en la pasarela y lo que se buscó después. Lo presentamos como resultado nulo en la Entrega 2 y cambiamos de pregunta.

## La hipótesis que sí se sostuvo

> Una tendencia de pasarela que gana búsquedas en su primer año rara vez se desploma en el segundo, y las que las pierden tienen más del triple de chances de ser pasajeras.

En vez de mirar la pasarela, miramos **qué pasa con las búsquedas de Google el año después del desfile**, comparado con el resto de las tendencias de esa temporada.

- **Lo que sube se queda.** La idea salió de 122 tendencias de 2019 a 2023. Después la probamos con 57 tendencias nuevas de 2016 a 2018 (56 con datos suficientes), con las reglas escritas antes de bajar los datos: de las 17 que ganaron búsquedas, **solo 1 fue pasajera**. En 8 ciclos, de 2016 a 2024, nunca pasó del 20%. Con las 178 tendencias juntas, **9 de cada 10** de las que suben siguen al segundo año.
- **Lo que cae es el riesgo.** De 2021 a 2024, **9 de 16** tendencias que perdieron búsquedas fueron pasajeras, contra **2 de 19** de las que ganaron: unas 5 veces más.
- **Lo que descartamos.** También creíamos que lo que queda plano es pasajero. No se sostuvo: las planas se quedan 73% de las veces.

Definiciones, resultados ciclo por ciclo y límites: [`hipotesis.md`](hipotesis.md).

## La app

Para cada temporada (primavera y otoño 2024 y 2025), la app muestra las tendencias que nombraron Who What Wear, CBC Life y Yahoo Lifestyle después de los desfiles, con fotos de dos desfiles y:

- **Veredicto:** se queda o en riesgo. Son 77 tendencias: 45 con veredicto (23 se quedan y 22 en riesgo) y 32 sin señal clara.
- **Confianza:** alta o media, según qué tan grande fue el movimiento.
- **Cuánto apostar:** probar poco, moderada o fuerte, con una regla fija a partir del veredicto, la confianza y los avisos.
- **El porqué:** cuánto se buscó el año después del desfile contra el resto de la temporada, con la curva de Google.

Las tendencias de 2026 aparecen sin veredicto: desde mediados de 2025 Google Trends mide distinto y lo comprobamos con los datos.

### Dónde está la IA

- **En la app:** al abrir una tendencia, la marca puede pedirle a una IA (GPT-OSS 120B, vía Groq) qué haría con ella según su rubro. **La IA no decide nada:** el veredicto, la confianza y la apuesta ya están calculados. Explica los datos frase por frase, cada frase dice de qué dato sale, y un control en el código revisa que no invente números. Lo único que agrega son ideas de producto, marcadas como sugerencia. Detalle: [`entrega3/IA.md`](entrega3/IA.md).
- **En el análisis:** Gemini clasificó los 2.430 looks. Revisamos 40 a mano: coincidió en el color en 33 y en la prenda en 28, por eso la app usa solo el color.

## Por qué creerle a los números

- **Reglas antes que datos.** Cada prueba tiene sus reglas escritas y firmadas con una huella sha256 antes de bajar los datos (`REGLAS_*.txt` y `SHA256_*.txt`), para no poder acomodarlas después.
- **Un chequeo extra donde los datos son más débiles.** Otoño 2025 cae en el período en que Google empezó a medir distinto. Por eso tuvo un chequeo más estricto, fijado de antemano, y si no pasaba no iba a la app. Pasó, y las tendencias donde la lectura es más frágil están marcadas.
- **Cada número se puede rehacer.** `trazabilidad/verificar_numeros.py` recalcula todos los números de la app desde los CSV crudos de Google Trends y de Gemini y los compara con lo que se ve en pantalla: 620 de 620 coinciden. Qué es cada número y de dónde sale: [`trazabilidad/LEEME.md`](trazabilidad/LEEME.md).

## Lo que los datos no dicen

- Las búsquedas miden interés, no ventas.
- Son búsquedas de todo el mundo; con búsquedas solo de Argentina la regla no se confirmó.
- Las tendencias las eligieron medios de moda en inglés.
- El veredicto lee el primer año. El segundo año de 2024 y 2025 todavía no se puede medir limpio con Google.
- Las muestras son chicas: de 15 a 68 tendencias por prueba.

## Cómo correrla

```bash
python3 prototipo/armar_datos.py              # arma los datos de la app desde los análisis
python3 trazabilidad/verificar_numeros.py     # recalcula cada número desde lo crudo y lo compara
python3 -m http.server                        # y entrar a http://localhost:8000/prototipo/
```

La IA necesita el servidor de Netlify (`netlify dev`) y una clave de Groq propia en la variable `GROQ_API_KEY`. Nunca se sube al repo.

Repetir las pruebas de la hipótesis:

```bash
cd analisis/hipotesis && python3 -I c1.py          # da salida_c1.txt
cd analisis/microtendencias && python3 -I m1.py    # da salida_m1.txt
cd analisis/microtendencias && python3 -I m2.py    # da salida_m2.txt
```

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

### Brief de la temporada

| Archivo | Qué es | Fuente |
|---|---|---|
| `analisis/brief_2026/datos/trends_2024_web.csv` | Google Trends mensual 2011-feb 2025 de 31 tendencias de SS2024 y FW2024 | Google Trends (bajado el 27/10/2026) |
| `analisis/brief_2026/fuentes_listas_2024.csv`, `terminos_declarados_2024.csv` | Listas de SS2024 y FW2024 y su término de búsqueda | Who What Wear, CBC Life, Yahoo Lifestyle |
| `analisis/brief_2026/datos/trends_2026_web.csv` | Google Trends 2011-sep 2026 de 36 tendencias de SS2026 y FW2026 | Google Trends (bajado el 27/10/2026) |
| `analisis/brief_2026/fuentes_listas_2026.csv`, `terminos_declarados_2026.csv` | Listas de SS2026 y FW2026 | Who What Wear, W Magazine, Marie Claire, Coveteur, The Impression |
| `analisis/brief_2025/datos/`, `terminos_declarados_2025.csv` | Google Trends y listas de SS2025 (26 tendencias) | Google Trends; Who What Wear, CBC Life, Yahoo Lifestyle |
| `analisis/brief_fw2025/datos/`, `terminos_declarados_fw2025.csv` | Google Trends y listas de FW2025 (20 tendencias) | Google Trends; Who What Wear, CBC Life, Yahoo Lifestyle |
| `app/datos/brief_temporada.json`, `brief_ss2025.json`, `brief_fw2025.json` | Veredictos que usa la página | `brief_temporada.py`, `brief_ss2025.py`, `brief_fw2025.py` |

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
- Fotos de los desfiles que muestra la app: solo en la versión publicada, no en el repo (lista en `prototipo/FOTOS.md`).
- Datos crudos del Lyst Index (Lyst no permite redistribuirlos); en la repo solo hay agregados (`analisis/lyst_*.csv`).
- Claves de API: nunca se suben. Para clasificar con Gemini hace falta una propia (`export GEMINI_API_KEY=...`).

## Estructura

| Carpeta / archivo | Qué hay |
|---|---|
| `prototipo/` | La app (publicada en Netlify) y `armar_datos.py`, que arma sus datos |
| `netlify/functions/` | La función de la IA y su prompt |
| `trazabilidad/` | Verificación de cada número de la app desde lo crudo |
| `hipotesis.md` | La hipótesis, definiciones, resultados y límites |
| `analisis/hipotesis/` | Prueba con datos nuevos 2016-2018: reglas, datos, `c1.py`, `salida_c1.txt` |
| `analisis/microtendencias/` | Tendencias 2019-2023: reglas, datos, `m1.py`, `m2.py`, salidas |
| `analisis/brief_2026/`, `brief_2025/`, `brief_fw2025/` | Veredictos de cada temporada: reglas, datos y scripts |
| `analisis/persistencia/` | Búsquedas por categoría, Shopping, Argentina y predicción congelada |
| `analisis/` | Cruce pasarela-búsquedas, marcas, casos, Lyst, backtest y validación de Gemini |
| `runway_gemini/` | Scripts para bajar y clasificar fotos de pasarela |
| `datasets/`, `datasets_procesados/` | Datos de entrada y clasificación |
| `app/` | Versión anterior de la página ("informe") y los scripts que arman los datos base |
| `entrega3/`, `entregas/` | Material de las entregas |
| `decisiones.md` | Registro de decisiones con fecha |
