# Diseño: del brief al código

## Cómo se hizo

No hubo diseño en Figma: decidimos diseñar directamente en código con un agente de IA (Claude Code). Cada pantalla depende de datos reales (curvas de búsquedas, veredictos, confianza, respuestas de la IA con sus estados de carga y error) y en código las podíamos probar con esos datos desde el primer día, en celular y en escritorio. Lo que en un flujo con Figma sería "el diseño original" acá son el brief, las referencias y las dos alternativas que armó el agente (capturas abajo).

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

- Antes la página tenía colores, prendas y largos amplios; solo 3 de 21 tenían veredicto. Ahora son 19 tendencias puntuales con veredicto, que es lo que la marca puede producir.
- Antes no había IA dentro de la app. Ahora hay una recomendación por tendencia, separada de los datos.
- Antes no se veía la confianza; ahora cada tarjeta dice "Confianza alta" o "media" y la nota explica qué significa.

## Capturas

En `entrega3/capturas/`:

1. `1_editorial_escritorio.png`: portada de la versión elegida.
2. `2_editorial_celular.png`: la misma portada a 390 px.
3. `3_editorial_grilla.png`: filtro por rubro, leyenda Calculado / Inferencia de la IA y grilla de "Lo que se queda".
4. `4_editorial_nota.png`: nota de una tendencia, con la lámina y la curva.
5. `5_alternativa_wrapped_celular.png`: la alternativa descartada. Se capturó sin la tipografía de la web, por eso el título se corta.
6. `6_entrega2_informe.png`: la página de la Entrega 2, para comparar.
