# Registro de decisiones

Formato: fecha, que se decidio y por que.

## 2026-08 Una sola hipotesis

Se dejo una unica hipotesis (el runway anticipa las ventas masivas con 12-18 meses de desfasaje). El buzz de busqueda por marca paso a ser una funcion de la IA (ponderar que mostrar), no una segunda hipotesis, para que sea mas facil de defender y de probar.

## 2026-09 Se excluye la alta costura

Se trabaja solo con Ready-to-Wear: la Couture casi nunca se replica tal cual en el mercado masivo y metia ruido en la hipotesis.

## 2026-09 Limite de datos de runway

El dataset de runway llega hasta 2023 y no se encontro ningun dataset abierto mas actual. Se documenta como limitacion y se compensa con Google Trends para la parte actual.

## 2026-09 Se descarta el Instagram Influencer Dataset

Pesa mas de 200 GB y el acceso es por formulario academico con espera. Se reemplaza por un dataset liviano de engagement.

## 2026-09-28 Datasets en redefinicion

El grupo esta redefiniendo la lista de datasets. Cuando quede cerrada, actualizar readme.md y datasets/diccionario.md.

## 2026-09-29 Tendencias de color, silueta y prenda

La app no trabaja solo con colores: cada tendencia puede ser un color, una silueta o un tipo de prenda, con el mismo peso en la interfaz (tres pestanas en Tendencias de la temporada). Se ajusto la redaccion de la hipotesis para nombrar los tres.

## 2026-10 Resultado plano del cruce pasarela - busquedas

Con 2.430 fotos clasificadas y Google Trends no aparece un desfase comun entre pasarela y busquedas (perfil promedio cerca de cero, estudio de eventos dentro de la banda aleatoria, 7 de 14 aciertos contra 2026). Se decidio presentarlo como resultado nulo y no forzar la hipotesis. Proximos pasos: Trends de Argentina en espanol, una segunda fuente de pasarela y datos de ventas de marcas locales.

## 2026-10 Clasificacion de fotos con Gemini

Gemini anota color dominante, prenda, silueta y largo por foto. Falta validar a mano una muestra. Las fotos no se suben al repo; el script `runway_gemini/bajar_fotos_vogue.py` las descarga.

## 2026-10 Marcas mas buscadas como ponderacion

Se descartaron los Trends sueltos de colores y prendas del Drive (8 terminos elegidos a dedo, sin relacion directa con las categorias de las fotos), y los datasets de Instagram, TikTok y Pinterest del Drive (rankings de influencers y datos de ejemplo sin fechas). En su lugar se bajaron busquedas de marcas (lujo, venta masiva y argentinas) y se uso la relevancia de cada casa para ponderar las fotos. La comparacion se declaro antes de correrla (promedio a 12 y 15 meses) y el resultado no cambio. No se ajusto ningun dato para forzar la hipotesis.

## Casos ilustrativos (octubre 2026)
- Decision: sumar 3 casos de tendencias atribuidas a un desfile, mostrando los tres aunque no todos sigan el patron.
- Compara ventanas de 12 meses completos (base, +1..+12, +13..+24, +25..+36) para evitar estacionalidad.
- Lectura: Triple S confundido por salida a tiendas; rosa ambiguo (suba previa + Barbie); minifalda es el mas limpio. No confirma la hipotesis.
- Pendiente: completar URLs de fuentes (Sneaker Freaker, Fashion Magazine, L'Officiel India, Rebag).
