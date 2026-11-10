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

## 2026-10-27 Brief de la temporada con tendencias puntuales

Las categorías amplias (colores, prendas) daban veredicto en solo 3 de 21, porque las dos formas de buscar no coincidían. Se pasó a tendencias puntuales de las listas de los medios, como en la hipótesis. Al medir SS2026 y FW2026 apareció un problema de Google Trends desde mediados de 2025 que infla los términos de poco volumen (`analisis/brief_2026/DIAGNOSTICO_2026.md`), así que esas tendencias se muestran sin veredicto. Los veredictos de la página salen de SS2024 y FW2024, la última temporada limpia (`app/datos/brief_temporada.json`). Una primera corrida contó como cero ene-feb 2025 por un error en la bajada; se corrigió y quedó registrada.

## 2026-10-27 SS2025: reglas fijadas antes de bajar datos

Se arma SS2025 con los mismos tres medios (Who What Wear, CBC Life, Yahoo Lifestyle/Harper's Bazaar; 26 términos). Como el primer año (oct-2024 a sep-2025) cruza el cambio de Google de ene-2025 y la suba desde ago-2025, las reglas (`analisis/brief_2025/REGLAS_BRIEF_2025.txt`, con sha256) fijan de antemano un chequeo: si el veredicto se explica por el volumen real del término (medido contra un ancla), por cuánto le pega el salto de 2026, o si el cambio de ene-2025 depende del volumen (|Spearman| ≥ 0,5 en cualquiera), SS2025 va sin veredicto. La lectura que no cruza ene-2025 (oct-dic) queda solo como sensibilidad: en temporadas limpias coincide poco con la de 12 meses. El segundo año solo se lee si una prueba fijada de antemano muestra que corregir por volumen limpia el salto de 2026. Datos pendientes de bajar (Google Trends no es accesible desde el entorno de Claude; se baja con `descargar_trends.js` en Chrome).

## 2026-11-01 SS2025 con veredicto; el segundo año no se puede medir

SS2025 pasó el chequeo fijado de antemano (V1 −0,01, V2 −0,08, V3 +0,26, límite 0,5): 8 tienden a quedarse, 5 en riesgo, 13 sin señal. Se suma al prototipo. Como sin agosto-septiembre de 2025 cambian 3 de los 8 "se queda", la app lo muestra como nota en cada uno (agregado después de ver los resultados, no cambia veredictos). La prueba del segundo año no pasa (dispersión 3,2 veces la de un año limpio): con Google Trends no se puede saber si las tendencias de 2024-2025 se quedaron en 2026. Se corrige el diagnóstico de 2026: el efecto del volumen existe pero es más débil (−0,36, no −0,84). Detalle en `analisis/brief_2025/LEEME.md`.

## 2026-11-01 Entrega 3: IA con Groq, app en Netlify

La app principal es la versión editorial (`prototipo/index.html`); el Wrapped queda como alternativa de diseño. La IA (GPT-OSS 120B vía Groq, función de Netlify; Llama 3.3 70B se apagó en Groq el 16/08/2026) solo traduce los datos calculados a una recomendación por rubro; no calcula ni cambia veredictos, y un control revisa que no invente números. Las fotos de pasarela se reemplazan por la curva de búsquedas porque no se pueden publicar. No hubo Figma: el diseño se hizo en código (ver `entrega3/DISENO.md`).

## 2026-11-02 Otoño 2025 (FW2025) con veredicto

- Borja: sumar la colección de otoño-invierno 2025, pero solo si pasa un chequeo; si no pasa, no va a la página.
- Como 7 de los 12 meses de su primer año (mar-2025 a feb-2026) caen en el período en que Google mide distinto, se sumó al chequeo de SS2025 uno nuevo (V4): la lectura de 12 meses tiene que coincidir con la de mar-jul 2025 al menos como en temporadas FW limpias (Spearman >= 0,50, como mucho 1 veredicto opuesto). La referencia limpia y las reglas se fijaron antes de bajar datos (`analisis/brief_fw2025/`, con huellas sha256).
- Mismos medios (Who What Wear y CBC Life por copias de Wayback de marzo de 2025; Harper's Bazaar en Yahoo). 20 términos.
- Resultado: pasa (V1 −0,21, V3 −0,16, V4 +0,70 sin opuestos). 7 tienden a quedarse, 6 en riesgo, 7 sin señal clara.
- Cuidado: en 8 de los 13 veredictos la lectura con solo mar-jul da "sin señal clara" (ninguno se da vuelta), y los dos "se queda" más fuertes son términos muy chicos. La app lo marca en cada tendencia. Detalle en `analisis/brief_fw2025/LEEME.md`.
- En la página, otoño 2025 pasa a ser la temporada más nueva (la que abre por defecto).

## 2026-11-02 ¿Las tendencias de 2025 volvieron a la pasarela en 2026?

- Idea de Borja: mostrar que las que "se quedan" en 2025 también se vieron en 2026, como prueba de la hipótesis.
- Cruce: mismo término de búsqueda en las listas de SS2026 y FW2026 (regla simple, decidida al hacer el cruce, no antes). Volvieron 3 de 15 "se queda" (broche, tapado protagonista, estampado floral), 0 de 11 "en riesgo" y 6 de 20 "sin señal clara".
- No prueba la hipótesis: la hipótesis mide búsquedas, no pasarelas, y las sin señal volvieron en mayor proporción que las que se quedan. La página lo muestra como pista, con los tres números.

## 2026-11-02 App online en Netlify, abierta y con fotos

- Sitio: https://paleta-predictiva.netlify.app (cuenta de Borja). La clave de Groq está en la variable `GROQ_API_KEY` del sitio, cargada desde el `.env` sin mostrarla.
- Netlify lo creó protegido (solo miembros del equipo). Borja decidió abrirlo para que los profes entren con el link, y que muestre las fotos de los desfiles aunque tengan derechos.
- Las fotos siguen fuera de GitHub. Por eso el sitio no se conecta al repo: se publica con `prototipo/publicar.sh`, que junta la rama `entrega-3` de GitHub con las fotos locales.

## 2026-11-02 Índice solo con veredictos; sin el cruce con 2026

- Borja: sacar de la página la lista "sin señal clara" y el bloque "¿Las de 2025 volvieron a la pasarela en 2026?".
- Las 32 sin señal siguen contadas en Método. Del cruce con 2026 se sacó el bloque entero, no solo la columna que no favorecía (6 de 20 sin señal volvieron, más que 3 de 15 "se quedan"); el resultado queda en `entrega3/GUION.md` (preguntas) por si lo preguntan.
- La evidencia de "Por qué creerle" pasa a comparar: las que bajan tienen unas 5 veces más chances de pasar de moda (9 de 16 contra 2 de 19, `hipotesis.md`).

## 2026-11-10 Trazabilidad: cada número de la página se recalcula desde lo crudo

- Por la devolución de la Entrega 3 (Rigor): `trazabilidad/verificar_numeros.py` recalcula cada número de la página desde los CSV crudos de Google Trends y de Gemini y lo compara. Detalle en `trazabilidad/LEEME.md`.
- Correcciones: "1 de cada N looks" ahora usa el porcentaje exacto (estaba corrido 1 o 2 en 5 colores); el 73%/88% aclara que son 122 tendencias (M1 + M2); se sacó el "7 de 14" de la Entrega 2 porque no se puede rehacer desde lo crudo y medía 2026, cuando Google cambió la forma de medir.
- Resultado: 575 de 575 chequeos coinciden.

## 2026-11-10 La IA solo explica: la apuesta pasa a ser una regla fija

- Por la devolución de la Entrega 3 (IA: "excesiva responsabilidad en las conclusiones, sin trazabilidad"), con el acuerdo de Borja.
- Cuánto apostar lo fija `apuesta()` en `prototipo/armar_datos.py`: en riesgo, probar poco; se queda con confianza alta y sin avisos, fuerte; el resto de "se queda", moderada (es la más alta que antes permitía el código). Se ve en la ficha de cada tendencia, sin IA.
- La IA devuelve la lectura frase por frase, con el dato del que sale cada una; el servidor revisa que cada número esté en ese dato. Ya no devuelve apuesta ni "ojo". Detalle en `entrega3/IA.md`.
