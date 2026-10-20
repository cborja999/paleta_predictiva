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

## Lyst Index (octubre 2026)
- Usamos el Lyst Index (via CICLO) como segunda medida de relevancia de marcas, solo como contexto y chequeo de cobertura.
- No se hizo cruce ponderado: cubre solo 2018-2026 (~17 temporadas) y tiene un corte de formula en Q1-26.
- Datos crudos de Lyst fuera del repo (`datasets/lyst/` ignorado): Lyst no permite redistribuir el informe. Se suben solo agregados.
- Los demas datos de CICLO son anuales y procesados (detrend + normalizados, 2025 excluido): no sirven para el cruce de 12-18 meses. Los mensuales crudos los tiene Zoe Dottori Greco.

## Reorganizacion de carpetas (octubre 2026)
- `datasets/muestra_vogue_para_gemini.csv`: la muestra de Vogue Runway (sin imagenes) que se le paso a Gemini.
- `datasets_procesados/resultados_gemini.csv`: la clasificacion que armamos (color, prenda, silueta, largo).
- Los scripts de `analisis/` y `runway_gemini/` ya apuntan a las nuevas rutas.

## Backtest y validación (octubre 2026)
- Regla de predicción fijada antes de calcular (señal >= 3 pts; Alta >= 6). Resultado: la pasarela sola acierta como el azar (47% Alta, 53% Media); la inercia de Trends acierta 63%. No se ajustó nada para mejorar el resultado.
- Validación de Gemini en 40 fotos: largo 90%, color 82%, prenda 70%, silueta 58%. Silueta no se presenta como dato duro. La columna "confianza" de Gemini es "alta" en casi todo y no se usa.
- Foco propuesto para la próxima entrega: una marca, una temporada, tres atributos (color, largo, prenda). Pendiente de decisión del grupo.
- Conocido: `analisis/chequeo_adelante.py` necesita los CSV crudos de Trends que no están en el repo; el resultado (7 de 14) está en `chequeo_adelante.csv`.

## Corpus de medios y marcas (octubre 2026) - piloto
- Idea de Borja: reunir a mano notas, reseñas y videos de medios y marcas (incluidos argentinos) para tener datos de Argentina y otra medida de repercusión. Se hace como corpus con protocolo, no como entrenamiento de un modelo.
- Pregunta, muestreo y período fijados antes de cargar (ver `datasets/corpus_medios/PROTOCOLO.md`). Se reporta el resultado sea cual sea.
- Pendiente: el grupo confirma la lista de fuentes (`fuentes.md`).

## Persistencia en busquedas, Argentina y prensa (20 de octubre de 2026)
- Decision: dejar de buscar que la pasarela prediga las busquedas (51%, azar) y probar si lo que gana interes en busquedas se queda. Usamos solo datos reales de la web; sin entrevistas ni ventas.
- Reglas escritas antes de correr cada prueba (`analisis/persistencia/REGLAS_*.txt`). Se reporta el resultado sea cual sea.
- Resultado: en el mundo, +14 puntos con el test limpio (84% contra 70%). El +45 de la primera version estaba inflado por la base compartida. En Argentina (busquedas generales y Shopping) no se sostiene (-7 puntos). No hay retraso de 12 a 18 meses entre el mundo y Argentina.
- Producto: la senal principal es la busqueda; la pasarela es contexto visual; la prensa argentina es contexto local con confianza menor. En Argentina no se ofrece nivel de confianza.
- Prediccion congelada el 19/10/2026 (63 filas, sha256 en `SHA256_prediccion_congelada.txt`). Chequeo principal: octubre de 2028; intermedio exploratorio: octubre de 2027.
- Prensa: 83 filas cargadas por el grupo, 70 de medios aprobados. Se guardan sin corregir y se listan los problemas de carga (`datasets/prensa_argentina/README.md`). Pendiente revisar 5 notas automaticas.
- Ventas: no hay datos publicos de ventas argentinas por color o prenda; Shopping Argentina mide busquedas de compra, no compras.

## 20 de octubre de 2026 (tarde): réplica en 2022-2023
El profesor pidió repetir con 2022-2023 lo que mostrábamos para 2023-2024. Se escribieron las reglas antes de correr (`analisis/persistencia/REGLAS_REPLICA_2022_2023.txt`) y se corrió la misma regla del brief en tres ciclos (oct-2022, oct-2021, oct-2020). Resultado: mixto en el ciclo principal, a favor en el mundo al sumar los tres, sin efecto en Argentina; la prensa no se pudo evaluar por falta de notas de 2021-2022. Detalle en `analisis/persistencia/resumen.md`.

## 20 de octubre de 2026 (mediodía): el brief pasa a ser de fashion weeks, no solo de Argentina
Como Argentina se mueve casi a la par que el mundo (sin retraso de 12 a 18 meses) y la regla no se confirmó con búsquedas argentinas, la página se presenta como un brief de las fashion weeks con lectura de búsquedas globales (qué ganó interés y tiende a quedarse), pensado para marcas argentinas pero sin decir que está validado en Argentina. La prensa argentina sale de la señal (queda como contexto en `datasets/prensa_argentina/`). El veredicto "ganó interés" exige que las dos formas de buscar coincidan.

## 20 de octubre de 2026 (tarde): tendencias puntuales (prendas, detalles, estéticas)
- Pregunta de Borja: ¿las prendas que aumentan después de aparecer en las fashion weeks persisten, y las que caen o quedan planas son pasajeras?
- Se usaron tendencias **elegidas por medios en su momento** (no por nosotros): Who What Wear SS2019-SS2023 (68 términos, M1) y, como réplica decidida después de ver M1, Sandra's Closet SS2020-SS2023 (54 términos nuevos, M2). Reglas escritas antes de bajar cada tanda de datos (`analisis/microtendencias/REGLAS_*.txt`, huellas sha256).
- Resultado: en las dos muestras las que subieron el primer año se quedaron 88% (M1 +22 pts, p=0,12; M2 +15 pts, p=0,30). Ninguna sola pasa el criterio. Juntas: +19 pts, p=0,037 (descriptivo). Las planas se quedan 73%: **la segunda mitad de la hipótesis no se sostiene**. El riesgo de pasajera está en lo que cae (41% contra 12%).
- Hipótesis reformulada: lo que gana búsquedas en su primer año rara vez se desploma en el segundo; lo que las pierde tiene más del triple de chances de ser pasajero.
- Página: nueva sección "Tendencias puntuales" con las 122 curvas y filtros (`app/armar_microtendencias.py`).

## 20 de octubre de 2026 (tarde): la hipótesis pasa a ser la del proyecto y se prueba con datos nuevos
- Borja decide reestructurar el proyecto alrededor de: "Una tendencia de pasarela que gana búsquedas en su primer año rara vez se desploma en el segundo. Las que las pierden tienen más del triple de chances de ser pasajeras".
- Como la frase salió de mirar 2019-2023, se probó con una muestra nueva: 57 tendencias de 2016-2018 (Sandra's Closet, W Magazine, Fashionista). Reglas y criterios fijados antes de bajar los datos (`analisis/hipotesis/REGLAS_HIPOTESIS_C1.txt`, sha256).
- Resultado: CONFIRMA EN PARTE. Las que subieron: 1/17 pasajeras (6%, criterio ≤ 20%). Las que cayeron: 2/11 (18%), no llega al triple con p < 0,05 (p = 0,54). En los 8 ciclos 2016-2024 las que subieron nunca pasaron de 20% de pasajeras.
- La hipótesis queda con una parte principal (confirmada) y una secundaria (no confirmada). Documento central: `hipotesis.md`. La página se reordenó con la hipótesis al frente.
