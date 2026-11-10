# Diseño: del brief al código

## Cómo se hizo

Maquetas en baja en Figma: https://www.figma.com/design/T9rjlTSq9BcnjynoK2gRoU (alternativa editorial: home, índice y nota; alternativa Wrapped: tres pantallas de celular; con notas cortas que explican las decisiones). Muestran la estructura de cada alternativa.

El diseño en sí no se hizo en Figma: decidimos diseñar directamente en código con un agente de IA (Claude Code). Cada pantalla depende de datos reales (curvas de búsquedas, veredictos, confianza, respuestas de la IA con sus estados de carga y error) y en código las podíamos probar con esos datos desde el primer día, en celular y en escritorio. Lo que en un flujo con Figma sería "el diseño original" acá son el brief, las referencias y las dos alternativas que armó el agente (capturas abajo).

El diseño partió de:

- el brief de `prototipo/README.md`: para quién es, qué preguntas tiene que responder la página y qué pantallas sugerimos;
- las referencias del grupo: The Lyst Index (rankings), Spotify Wrapped (relato por pantallas), TradingView (curvas) y Pantone Color of the Year (el color como protagonista);
- el pedido de la Entrega 2: más visual, criterios de la IA y niveles de confianza a la vista, y alternativas de diseño.

El agente propuso **dos alternativas** y elegimos una:

| Alternativa | Archivo | Idea | Por qué sí o no |
|---|---|---|---|
| Editorial (elegida) | `prototipo/index.html` | Revista de moda: tipografía Didone, blanco y negro, rojo para lo que está en riesgo, grilla tipo Lyst | Entra todo: portada, rubros, evidencia, método y detalle de cada tendencia. Se lee como un informe que una marca guarda. |
| Wrapped | `prototipo/wrapped.html` | Relato en pantallas tipo Spotify Wrapped, azul y amarillo | Muy visual en celular, pero no entraban el método, los límites ni la IA sin cortar el relato. |

## Qué se decidió en código (y no estaba en ningún diseño)

- **Las fotos de pasarela se reemplazaron por "láminas" con la curva de búsquedas.** Las fotos de Vogue Runway no se pueden publicar. En su lugar, cada tendencia muestra el cambio calculado en grande (por ejemplo "+68%") y su curva de 24 meses con una línea punteada en el mes del desfile. Así el dato pasa a ser la imagen, como en TradingView.
- **La lámina dibuja lo que compara la regla (1/11/2026).** Al revisar la página vimos que la curva sola podía contradecir el veredicto: el blazer ochentoso sale "en riesgo, −17%" pero su curva termina arriba, porque sus búsquedas subieron 3% mientras la temporada subió 23%. Ahora, sobre la curva (más tenue), van tres líneas: el promedio del año antes, el del año después y, punteada, dónde estaría si se hubiera movido como la temporada. El número grande es la distancia entre las dos últimas. La nota de cada tendencia lo dice con sus números ("se buscó 3% más, pero la temporada subió 23%: quedó atrás"). Los tres números salen de la misma curva y del cambio que ya se calculaba (`armar_datos.py`); no cambia ningún veredicto.
- **Una sola explicación y una sola curva.** La leyenda "cómo leer cada lámina" aparece una vez, arriba de la grilla, en lugar de repetirse en cada tarjeta. Se sacó la curva chica del pie de cada tarjeta y el segundo gráfico de la nota, que repetían la misma curva.
- **Cinco grandes y el resto en lista.** Cada sección muestra 5 tendencias como láminas y las demás en una lista compacta tipo índice de Lyst (curva chica, nombre, temporada, confianza y número). La página bajó de unos 11.000 a 9.700 px de alto en escritorio y de 17.500 a 15.300 en celular.
- **La tapa no se repite.** La tendencia de la portada ya no abre la grilla de "Lo que se queda": pasa al segundo lugar.
- **Filtro por temporada.** Además del rubro, la marca puede ver solo primavera 2025 (marcada como "la más nueva"), otoño 2024 o primavera 2024. El sumario de la portada y la lista de 2026 muestran la temporada con el año.
- **Anterior / siguiente en la nota.** Se pasa de una tendencia a otra sin cerrar la nota, con botones o con las flechas del teclado, en el mismo orden de la página y respetando los filtros ("3 de 13").
- **Cabecera más chica en celular.** Se saca la línea de arriba y se achica el nombre: pasa de 122 a 81 px de alto. Los filtros se deslizan de costado en una línea por grupo.
- **Leyenda "Calculado / Inferencia de la IA" en una línea**, con textos más cortos, debajo de los filtros.
- **Índice con fotos, como las notas de análisis de WGSN (1/11/2026).** Mirando la nota de WGSN sobre los desfiles S/S 27 de Nueva York vimos que no usan gráficos grandes: cada tendencia es una foto del desfile, un título y una frase con el número adentro ("rose by +1.4ppt"). Reemplazamos las láminas con curvas por eso:
  - **La foto vuelve a ser la imagen.** La página muestra la foto del look si está en `prototipo/fotos/` y, si no, deja el lugar con el nombre del archivo. Esa carpeta no se sube a GitHub porque el repo es público y las fotos tienen derechos; la lista de fotos está en `prototipo/FOTOS.md` (las 52 de 2025, dos por tendencia, ya están). La versión online (https://paleta-predictiva.netlify.app) sí las muestra: Borja decidió publicarla abierta y con fotos (2/11/2026). Se suben con `prototipo/publicar.sh` desde su compu, nunca por GitHub.
  - **Un solo índice por temporada** (primavera 2025, otoño 2024, primavera 2024) en lugar de "Lo que se queda" y "Lo que puede pasar". Cada ficha: foto, veredicto, nombre y la frase "Se buscó +137% el año después del desfile; su temporada, +23%". Se agrega un filtro por veredicto.
  - **Todos los datos.** Entran las 45 con veredicto y las 36 de 2026. Las 32 "sin señal clara" estuvieron en una lista corta debajo de cada temporada; el 2/11/2026 Borja decidió sacarla para que el índice muestre solo veredictos. Siguen contadas en Método ("En el medio no damos veredicto (32 quedaron así)").
  - **Los colores de la pasarela**, como los colores de WGSN: la muestra del color medido en las fotos, qué parte de los looks lo tuvo y cuántos puntos cambió (de `app/datos/brief.json`). Se aclara que lo clasificó Gemini (82% de acierto en color en una prueba de 40 fotos) y que dice qué se vio, no qué se queda.
  - **El gráfico queda solo en la nota de cada tendencia,** chico y con su leyenda, debajo del texto.
- **Un home y la temporada más nueva primero.** Al entrar, la página muestra el nombre, la frase "Qué se queda y qué se va", una línea con los números de primavera 2025 y dos botones: "Ver primavera 2025" y "Temporadas anteriores". Abajo, una franja con los 11 colores de la pasarela, cada uno del ancho de cuánto se vio (es la paleta del nombre, y se aclara de qué temporadas sale). Al bajar, el índice muestra solo primavera 2025; otoño 2024 y primavera 2024 se eligen arriba del índice, como "temporadas anteriores". La cabecera aparece recién después del home y queda fija arriba.
- **Otoño 2025 (2/11/2026).** Pasó su chequeo (ver `analisis/brief_fw2025/LEEME.md`) y pasa a ser la temporada que abre la página; primavera 2025, otoño 2024 y primavera 2024 quedan como anteriores. Las 8 tendencias cuya lectura cambia con solo marzo a julio de 2025 llevan el aviso en su nota.
- **Menos texto y gráficos más simples (2/11/2026).** Borja: la página explicaba demasiado y los gráficos no se entendían. La nota ahora tiene una línea ("se buscó 132% más; las demás tendencias de la temporada subieron 34%") y dos barras con esa misma comparación, en lugar de la curva con cuatro líneas. El aviso largo pasa a una etiqueta "Con cuidado" que se abre con una frase. Las tres cifras de evidencia (con el "≤ 20%" que no se entendía) pasan a dos datos con puntitos. Los colores dicen "1 de cada 3 looks" y "más que antes", sin códigos ni explicación técnica.
- **¿Volvieron en 2026?** En la sección de 2026 se cruza cada tendencia de 2025 con las listas de 2026 (mismo término de búsqueda): volvieron 3 de 15 de las que se quedan, 0 de 11 de las que están en riesgo y 6 de 20 de las sin señal. Se mostró como pista, no como prueba: volver a la pasarela no es lo que mide la hipótesis, y las sin señal volvieron más. El 2/11/2026 se sacó de la página porque confundía más de lo que sumaba (se sacó el bloque entero, no solo la columna que no convenía).
- **Home sin texto, nombre que se pinta y aparición al bajar (2/11/2026).** Se sacó la línea explicativa del home. Al pasar el cursor por "Paleta Predictiva", cada letra toma un color de la pasarela (en celular, al tocar el nombre, se pintan en ola). Al bajar, cada bloque aparece cuando entra en pantalla; si el sistema pide menos movimiento, no hay efecto.
- **Dos desfiles por tendencia.** Para respaldar que una tendencia se vio en más de una pasarela, cada una lleva dos fotos de dos marcas distintas de esa temporada (`<id>-1.jpg` y `<id>-2.jpg`). La tarjeta del índice muestra la primera; la nota muestra las dos, cada una con su crédito ("Chloé · Primavera 2025"). Las marcas salen de la nota del medio que nombró la tendencia; cuando esa nota no se pudo abrir (CBC Life) o no nombra marcas (The Impression y parte de Marie Claire y Who What Wear), salen de otras notas de la misma temporada, y `prototipo/FOTOS.md` lo marca como "otra". Para el vestido rosa de otoño 2026 ninguna nota nombra marcas.
- **Calculado contra IA.** Dos etiquetas: "Calculado" (recuadro negro) e "Inferencia de la IA" (azul). Todo lo que escribe la IA vive en un bloque azul aparte, nunca mezclado con los veredictos.
- **Rojo solo para el riesgo.** Lo que se queda va en negro; lo que puede pasar, en rojo. Sin verde: no queremos que "se queda" se lea como "comprá".
- **Filtro por rubro.** La marca elige su rubro y la página reordena las tendencias; el mismo rubro pasa como contexto a la IA.
- **Estados de la IA:**
  - cargando: el botón se desactiva y aparecen tres líneas que titilan;
  - error (saturada, sin clave, más de 45 segundos sin respuesta, sin conexión): mensaje en rojo y aclaración de que los datos calculados siguen valiendo;
  - abierta como archivo local, sin servidor: avisa que la IA funciona en la versión online;
  - control automático: si la respuesta tuvo números que no estaban en los datos, aviso amarillo.
- **Transparencia.** Debajo de cada respuesta, "Qué le mandamos a la IA" muestra el JSON exacto. En Método, "Ver qué le pedimos a la IA" muestra el system prompt.
- **Responsive.** En celular la grilla pasa de 4 columnas a 2, la nota de detalle pasa a una columna con la lámina arriba, la navegación se desplaza de costado y la cabecera se achica al bajar. Se probó a 390 px de ancho sin desplazamiento horizontal.
- **Accesibilidad.** Foco visible, cierre de la nota con Escape, texto alternativo en las láminas, respuesta de la IA anunciada con `aria-live` y animaciones apagadas si el sistema pide menos movimiento.

## Qué hizo el agente y qué hicimos nosotros

- **Agente de IA (Claude Code):** armó las dos alternativas a partir del brief y las referencias, escribió el HTML, CSS y JavaScript, el script que arma los datos (`prototipo/armar_datos.py`), la función de la IA y las pruebas en celular y escritorio.
- **Nosotros:** definimos el brief y las referencias, elegimos la alternativa editorial, decidimos qué se muestra con veredicto y qué no (2026 sin veredicto), los textos y las reglas de la IA (qué puede y qué no puede decir).

## Diferencias entre el prototipo de la Entrega 2 y esta versión

- Antes la página tenía colores, prendas y largos amplios; solo 3 de 21 tenían veredicto. Ahora son 45 tendencias puntuales con veredicto en cuatro temporadas (de primavera 2024 a otoño 2025), que es lo que la marca puede producir, con foto de dos desfiles cada una.
- Antes no había IA dentro de la app. Ahora hay una recomendación por tendencia, separada de los datos.
- Antes no se veía la confianza; ahora cada tarjeta dice "Confianza alta" o "media" y la nota explica qué significa.

## Capturas

En `entrega3/capturas/` (2/11/2026, antes de tener las fotos: los recuadros grises son donde van):

1. `1_home_escritorio.png`: el home, con la paleta de la pasarela abajo.
2. `2_home_celular.png`: el mismo home a 390 px.
3. `3_indice.png`: el índice de otoño 2025, con las temporadas anteriores, los filtros y la leyenda Calculado / Inferencia de la IA.
4. `4_colores.png`: los colores de la pasarela.
5. `5_nota.png`: la nota de una tendencia (Lunares, otoño 2025): las dos fotos con su desfile, la frase con los números y las dos barras (la tendencia contra su temporada).
6. `6_alternativa_wrapped_celular.png`: la alternativa descartada. Se capturó sin la tipografía de la web, por eso el título se corta.
7. `7_entrega2_informe.png`: la página de la Entrega 2, para comparar.

Las mismas capturas con las fotos de los desfiles (índice, Lunares en escritorio y celular, Pollera balón de primavera 2025) están en `entrega3/capturas/con_fotos/`, solo en la compu de Borja: no van al repo porque es público.
