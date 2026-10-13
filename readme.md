# paleta_predictiva

Paleta predictiva para marcas locales: una web app que arma un brief de tendencias de moda (colores, siluetas y prendas) para marcas de indumentaria chicas y medianas que no pueden ir a fashion weeks ni pagar un servicio de forecasting.

Proyecto de la materia K576 - IA Aplicada al diseno de productos digitales (Universidad de San Andres).

## Integrantes

Beltran Martinez, Borja Centeno y Luigi Bonomi.

## Hipotesis de trabajo

Los colores, siluetas y tipos de prenda dominantes en las pasarelas de las principales fashion weeks (Nueva York, Londres, Milan, Paris) anticipan los colores, siluetas y prendas mas vendidas en retail de moda masivo, con un desfasaje de entre 12 y 18 meses.

## Sitio

Link al sitio: pendiente (se publica en Netlify desde la carpeta app/). Captura: pendiente.

## Fuentes de datos

Pendiente: los datasets se estan redefiniendo. Al definirlos, anotar para cada uno: nombre, link de descarga, fecha de descarga, licencia y atribucion.

## Resultados del cruce pasarela - busquedas (octubre 2026)

Se clasificaron con Gemini 2.430 fotos de Vogue Runway (15 casas, FW2011 a SS2024, 90 por temporada) y se cruzaron con Google Trends mensual (sin tendencia ni estacionalidad), con desfases de 0 a 24 meses y p-valores por permutacion. Ademas se hizo un estudio de eventos y un chequeo contra 2026.

**Resultado: plano.** El perfil de correlacion por desfase promedia cerca de cero (0,03 a 12 meses y 0,04 a 15 meses) y los mejores casos individuales no coinciden en un mismo desfase, algo compatible con azar. El estudio de eventos (24 eventos) no sale de la banda aleatoria y el chequeo contra 2026 acierta 7 de 14 (p = 0,6). La hipotesis ni se confirma ni se refuta. Detalle en `analisis/resumen.md` y `analisis/evento_resumen.md`.

**Limitaciones:** solo 15 casas de lujo; Trends mide busquedas, no ventas; correlacion no es causa; los reportes 2025-2026 son resumenes publicos secundarios; los terminos de poco volumen en Trends no se pueden usar; no hay datos publicos de ventas argentinas por color o prenda.

**Como repetirlo:** las fotos no estan en el repo (derechos y tamano). `runway_gemini/bajar_fotos_vogue.py` las descarga. Para clasificar hace falta una clave propia de Gemini exportada como `GEMINI_API_KEY`; nunca se sube al repo. Los scripts de `analisis/` reproducen los resultados.

Carpetas agregadas: `runway_gemini/` (scripts, muestra y `resultados_gemini.csv`), `analisis/` (scripts y resultados), `datasets/runway_reportes_2025_2026.csv` y `datasets/trends/trends_unificado.csv`.

## Fuentes agregadas

- Vogue Runway via Hugging Face: `tonyassi/vogue-runway-top15-512px` (fotos y metadatos).
- Google Trends: exportaciones mensuales por termino.
- T-Fashion y reportes publicos de WGSN: crecimientos de presencia en pasarela 2025-2026 (resumenes secundarios).
