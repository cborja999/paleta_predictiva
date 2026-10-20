# Fuentes candidatas para probar la hipótesis con datos de ventas o demanda (20/10/2026)
Relevamiento hecho leyendo las páginas de cada fuente. Lo que no pude confirmar está marcado.

| Fuente | Qué mide | Cobertura | Acceso | Para qué sirve | Falta confirmar |
|---|---|---|---|---|---|
| Visuelle 2.0 (Nuna Lie, Italia) | Ventas semanales por producto y tienda; color dominante (10 colores) y categoría (27); Google Trends por etiqueta; clima | Nov 2016 a dic 2019, 6 temporadas, 5.355 productos, 110 tiendas | Formulario de Google en https://humaticslab.github.io/forecasting/visuelle (código en GitHub: HumaticsLAB/visuelle2.0-code) | Probar "lo que gana interés se queda" y pasarela contra ventas reales de una marca chica | Licencia y esquema exacto de columnas |
| H&M Personalized Fashion Recommendations (Kaggle) | Transacciones con fecha; color (colour_group_name), tipo de producto, apariencia gráfica | Cientos de millones de transacciones (cobertura exacta no confirmada en la página leída) | Cuenta de Kaggle y aceptar las reglas de la competencia | Ventas reales de una cadena masiva por color y prenda | Período exacto y condiciones de uso |
| Amazon Reviews 2023 (McAuley Lab, Hugging Face) | Reseñas con fecha y metadatos de producto (título, características, detalles) | 1996 a sep 2023; ropa: 66 millones de calificaciones, 7,2 millones de productos | Hugging Face | Serie larga de demanda aproximada (reseñas por color o prenda en el título) | Licencia; es un proxy de compras, no ventas |
| Pantone Fashion Color Trend Report | Colores de cada semana de la moda (NY, Londres), por temporada | Desde 2012 | Reportes públicos | Chequear de forma independiente la capa de pasarela por color | Archivo completo y formato |
| Mercado Libre Argentina (API oficial) | Búsquedas en alza, ahora (foto) | Sin histórico | API (parte puede pedir token) | Arrancar una serie propia desde hoy | Si el endpoint de tendencias es libre |
| CAME (ventas minoristas pyme) | Ventas del sector textil e indumentaria, agregado mensual | Años de informes | Informes públicos | Contexto macro de ventas argentinas | No hay color ni prenda |
| Trabajos académicos (GeoStyle, FIT, Runway to Realway) | Fotos de Instagram, Flickr y calle contra pasarela | 2000 a 2019 según el trabajo | No confirmé que los datos sean públicos | Antecedentes para citar | Disponibilidad |

No encontré datos públicos de ventas argentinas por color o prenda.
