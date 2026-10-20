# paleta_predictiva

Paleta predictiva para marcas locales: una web app que arma un brief de tendencias de moda (colores, siluetas y prendas) para marcas de indumentaria chicas y medianas que no pueden ir a fashion weeks ni pagar un servicio de forecasting.

Proyecto de la materia K576 - IA Aplicada al diseno de productos digitales (Universidad de San Andres).

## Integrantes

Beltran Martinez, Borja Centeno y Luigi Bonomi.

## Hipotesis de trabajo

Los colores, siluetas y tipos de prenda dominantes en las pasarelas de las principales fashion weeks (Nueva York, Londres, Milan, Paris) anticipan los colores, siluetas y prendas mas vendidas en retail de moda masivo, con un desfasaje de entre 12 y 18 meses.

**Hipotesis original: no se sostuvo** (la pasarela sola acierta 51%, como el azar). Ver mas abajo.

## Hipotesis actual (20/10/2026)

Los colores, prendas y largos cuyas busquedas **ganan interes** tienden a **quedarse** mas que los que no se movieron. En busquedas del mundo la ventaja es de unos 14 puntos con el test limpio (84% contra 70%). **En Argentina no se confirmo** (busquedas generales y de Shopping). Argentina se mueve casi a la par que el mundo; no hay evidencia de un retraso de 12 a 18 meses. La pasarela queda como contexto visual y la prensa argentina como contexto local. Recorrido del producto: se vio en pasarela, la prensa lo nombra y las busquedas suben. Detalle en `analisis/persistencia/resumen.md`. La prediccion quedo congelada el 19/10/2026 (`analisis/persistencia/prediccion_congelada_2026-10-19.csv`, con huella sha256); chequeo principal en octubre de 2028.

## Sitio

Link al sitio: pendiente (se publica en Netlify desde la carpeta app/). Captura: pendiente.

## Fuentes de datos

Pendiente: los datasets se estan redefiniendo. Al definirlos, anotar para cada uno: nombre, link de descarga, fecha de descarga, licencia y atribucion.

## Resultados del cruce pasarela - busquedas (octubre 2026)

Se clasificaron con Gemini 2.430 fotos de Vogue Runway (15 casas, FW2011 a SS2024, 90 por temporada) y se cruzaron con Google Trends mensual (sin tendencia ni estacionalidad), con desfases de 0 a 24 meses y p-valores por permutacion. Ademas se hizo un estudio de eventos y un chequeo contra 2026.

**Resultado: plano.** El perfil de correlacion por desfase promedia cerca de cero (0,03 a 12 meses y 0,04 a 15 meses) y los mejores casos individuales no coinciden en un mismo desfase, algo compatible con azar. El estudio de eventos (24 eventos) no sale de la banda aleatoria y el chequeo contra 2026 acierta 7 de 14 (p = 0,6). La hipotesis ni se confirma ni se refuta. Detalle en `analisis/resumen.md` y `analisis/evento_resumen.md`.

**Limitaciones:** solo 15 casas de lujo; Trends mide busquedas, no ventas; correlacion no es causa; los reportes 2025-2026 son resumenes publicos secundarios; los terminos de poco volumen en Trends no se pueden usar; no hay datos publicos de ventas argentinas por color o prenda.

**Como repetirlo:** las fotos no estan en el repo (derechos y tamano). `runway_gemini/bajar_fotos_vogue.py` las descarga. Para clasificar hace falta una clave propia de Gemini exportada como `GEMINI_API_KEY`; nunca se sube al repo. Los scripts de `analisis/` reproducen los resultados.

Carpetas agregadas: `runway_gemini/` (scripts), `datasets/muestra_vogue_para_gemini.csv` (muestra de Vogue) y `datasets_procesados/resultados_gemini.csv` (clasificacion con Gemini), `analisis/` (scripts y resultados), `datasets/runway_reportes_2025_2026.csv` y `datasets/trends/trends_unificado.csv`.

## Fuentes agregadas

- Vogue Runway via Hugging Face: `tonyassi/vogue-runway-top15-512px` (fotos y metadatos).
- Google Trends: exportaciones mensuales por termino.
- T-Fashion y reportes publicos de WGSN: crecimientos de presencia en pasarela 2025-2026 (resumenes secundarios).

## Marcas mas buscadas (octubre 2026)

Se bajaron de Google Trends (busqueda web, mensual 2004 a sep 2026) 8 consultas de marcas: casas de lujo de las fotos de pasarela, marcas de venta masiva y marcas argentinas (con busquedas de Argentina). Como Trends reescala cada consulta, se encadenan con una marca ancla (Gucci, Zara). Archivos en `datasets/trends_marcas/` y analisis en `analisis/marcas_trends.py` y `analisis/marcas_resumen.md`.

- **Lujo (ultimos 12 meses, indice global):** Prada, Gucci, Dior, Chanel y Louis Vuitton lideran con indices entre 28 y 34.
- **Venta masiva:** Zara (78) esta muy arriba, seguida de Shein (55) y H&M (31).
- **Argentina (escala propia):** Zara (79) se busca mucho mas que las marcas locales: 47 Street (18), Rapsodia (11) y Kosiuko (8). Vitamina, Mimo, Awada y Ayres son palabras comunes y no se leen como ranking.
- **Ponderacion del cruce:** cada foto se peso por la relevancia de busqueda de su casa. El promedio de correlaciones a 12 y 15 meses fue 0,033 sin ponderar y 0,023 ponderado: no cambia el resultado. La hipotesis sigue sin confirmarse ni refutarse.

Limitaciones: buscar una marca no es comprarla; hay terminos ambiguos (hermes, cos, mango, valentino, etc.) y marcas con volumen muy bajo (Fendi, Cardon, Pull and Bear).

## Tres casos ilustrativos (octubre 2026)
Triple S de Balenciaga, rosa de Valentino y minifalda de Miu Miu: como se movieron las busquedas en los 3 años despues del desfile. Son ejemplos elegidos (sesgo de seleccion), **no prueba**. Detalle, tabla y limites en `analisis/casos_resumen.md`; datos en `datasets/trends_casos/`; codigo `analisis/casos_ilustrativos.py`.

## Lyst Index como segunda medida de relevancia (octubre 2026)
Dataset del proyecto CICLO (Berney, Dobler, Dottori Greco). Las casas que tenemos en las fotos ocupan en promedio 42% del ranking Lyst; faltan Moncler, Bottega Veneta, Loewe, Burberry, Jacquemus y Miu Miu (puesto promedio 3,8). Acuerdo con Trends entre las 12 casas comunes: Spearman 0,45 (no significativo). Detalle: `analisis/lyst_resumen.md`. Los datos crudos de Lyst no estan en el repo (licencia).

## Respuesta a la devolución de la Entrega 2 (octubre 2026)
Carpeta `entregas/entrega_3/`: qué observaron los docentes, qué hicimos (`respuesta_a_la_devolucion.md`), proceso y criterios (`proceso_y_criterios.md`) y guion de pantallas (`guion_pantallas.md`). Nuevos análisis: `analisis/backtest_resumen.md` (acierto histórico por nivel de confianza) y `analisis/validacion_gemini_resumen.md` (validación de 40 fotos).


## Persistencia en busquedas y prensa argentina (octubre 2026)
- `analisis/persistencia/`: reglas fijadas antes de correr, scripts, resultados y prediccion congelada. Los datos nuevos de Google Trends (mundo, Argentina y Shopping, mensual 2011 a sep 2026) estan en `analisis/persistencia/datos/`.
- `datasets/prensa_argentina/`: planilla de notas de prensa argentina cargada por el grupo (83 filas) con la lista de problemas de carga detectados.
- Limites: Trends mide busquedas y no ventas; 20 a 27 temporadas; la muestra de prensa es chica y desigual entre temporadas.
