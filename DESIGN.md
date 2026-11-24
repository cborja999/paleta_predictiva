---
name: Paleta predictiva
description: Qué tendencias de pasarela se quedan y cuáles están en riesgo, para marcas de ropa argentinas chicas y medianas.
colors:
  tinta: "#111713"
  verde-noche: "#071814"
  azul-noche: "#142638"
  pizarra: "#3d444c"
  mostaza: "#b68a3a"
  crema: "#f2eee6"
  pista: "#ece9e2"
  linea: "#b9b8b3"
  gris-texto: "#5b605c"
  blanco: "#ffffff"
  durazno-summer: "#faeee3"
  celeste-winter: "#eaf2f8"
  panel-summer: "#b07a55"
  panel-winter: "#3d444c"
  sello-queda: "#7fa58c"
  sello-riesgo: "#e0907e"
  sello-cautela: "#e8bd5c"
  sello-sin: "#a9b1bd"
  queda-texto: "#15573d"
  queda-fondo: "#ddeee5"
  riesgo-texto: "#902a32"
  riesgo-fondo: "#f9e1e1"
  riesgo-numero: "#8e2739"
  cautela-texto: "#684500"
  cautela-fondo: "#fff2d8"
  azul-ia: "#3b3fd6"
  fondo-ia: "#f3f3fd"
typography:
  display:
    fontFamily: "Inter, system-ui, -apple-system, Segoe UI, Roboto, sans-serif"
    fontSize: "clamp(64px, 9vw, 140px)"
    fontWeight: 700
    lineHeight: 0.86
    letterSpacing: "-0.045em"
  numero:
    fontFamily: "Inter, system-ui, sans-serif"
    fontSize: "clamp(46px, 5vw, 72px)"
    fontWeight: 700
    lineHeight: 1
    letterSpacing: "-0.035em"
    fontFeature: "tnum"
  headline:
    fontFamily: "Inter, system-ui, sans-serif"
    fontSize: "clamp(30px, 3.6vw, 46px)"
    fontWeight: 300
    lineHeight: 1.1
    letterSpacing: "0.01em"
  title:
    fontFamily: "Inter, system-ui, sans-serif"
    fontSize: "clamp(26px, 3.4vw, 40px)"
    fontWeight: 700
    lineHeight: 1
    letterSpacing: "-0.02em"
  body:
    fontFamily: "Inter, system-ui, sans-serif"
    fontSize: "16px"
    fontWeight: 500
    lineHeight: 1.4
  label:
    fontFamily: "Inter, system-ui, sans-serif"
    fontSize: "12px"
    fontWeight: 700
    lineHeight: 1.3
    letterSpacing: "0.12em"
rounded:
  none: "0px"
spacing:
  gutter-celular: "16px"
  gutter-tablet: "32px"
  gutter-compu: "72px"
components:
  boton-principal:
    backgroundColor: "{colors.azul-noche}"
    textColor: "{colors.blanco}"
    rounded: "{rounded.none}"
    padding: "11px 16px"
  boton-home:
    backgroundColor: "{colors.azul-noche}"
    textColor: "{colors.blanco}"
    rounded: "{rounded.none}"
    padding: "15px 28px"
  boton-home-hover:
    backgroundColor: "{colors.verde-noche}"
  menu-activo:
    backgroundColor: "{colors.verde-noche}"
    textColor: "{colors.blanco}"
    padding: "10px 12px"
  sello-queda:
    backgroundColor: "{colors.sello-queda}"
    textColor: "{colors.blanco}"
    rounded: "{rounded.none}"
    padding: "4px 12px"
  sello-riesgo:
    backgroundColor: "{colors.sello-riesgo}"
    textColor: "{colors.blanco}"
    rounded: "{rounded.none}"
    padding: "4px 12px"
  sello-cautela:
    backgroundColor: "{colors.sello-cautela}"
    textColor: "{colors.blanco}"
    rounded: "{rounded.none}"
    padding: "4px 12px"
  etiqueta-calculado:
    backgroundColor: "{colors.blanco}"
    textColor: "{colors.tinta}"
    typography: "{typography.label}"
    padding: "3px 8px"
  etiqueta-ia:
    backgroundColor: "{colors.azul-ia}"
    textColor: "{colors.blanco}"
    typography: "{typography.label}"
    padding: "3px 8px"
  panel-ia:
    backgroundColor: "{colors.pizarra}"
    textColor: "{colors.blanco}"
    padding: "22px 24px"
  cuerpo-ia:
    backgroundColor: "{colors.fondo-ia}"
    textColor: "{colors.tinta}"
    padding: "22px 24px"
---

# Design System: Paleta predictiva

## Overview

**Creative North Star: "El informe de pasarela"**

La app se lee como un informe de tendencias impreso, en la línea del LIVETREND que el grupo tomó de referencia. La foto de desfile manda, los números son enormes y van encima o al lado del look, un sello dice el veredicto, y cada tendencia es una doble página que alterna de lado. Es editorial en la forma y verificable en el fondo: cada número tiene su etiqueta "Calculado" y lo que dice la IA va siempre aparte y marcado.

El tono es editorial, directo y verificable. Hay una sola familia, Inter, en pesos muy distintos (300 para los títulos de sección, 700 para nombres y números) y blanco de papel con tinta casi negra. El color viene de dos fuentes: el tono de cada temporada (durazno para Summer, pizarra para Winter) y el tono sacado de cada foto. No hay sombras ni esquinas redondeadas: la profundidad sale de las fotos, los bloques de color y las líneas finas.

Lo que nunca tiene que parecer: algo "hecho por IA" o de plantilla (grillas de tarjetas iguales, gradientes decorativos, íconos genéricos) ni una tienda online de ropa.

**Key Characteristics:**
- La foto de desfile es la protagonista; los números grandes son el segundo nivel.
- Una sola tipografía (Inter), con mucho contraste de peso y tamaño.
- Bloques de color planos, esquinas rectas y líneas de 1 a 1,5 px.
- Lo calculado y lo de la IA, siempre separados y etiquetados.
- Dobles páginas que alternan de lado, nunca una grilla repetida.

## Colors

Papel blanco y tinta verde-negra, con el color tomado de la temporada y de las fotos. Los colores de veredicto son fijos y no se usan para decorar.

### Primary
- **Azul noche** (azul-noche): botones principales, el botón del home y las letras del nombre en el home.
- **Verde noche** (verde-noche): la opción activa del menú, el chip "Tu rubro" y el hover del botón del home.

### Secondary
- **Durazno Summer** y **celeste Winter** (durazno-summer, celeste-winter): fondos suaves de las cajas de temporada.
- **Panel Summer** (panel-summer, terracota) y **panel Winter** (panel-winter, pizarra): portada partida de cada temporada y cabecera del brief.
- **Mostaza** (mostaza): curva de búsquedas, la línea punteada de "dónde estaría" y la barra de la temporada.

### Tertiary
- **Sellos de veredicto** (sello-queda verde salvia, sello-riesgo salmón, sello-cautela amarillo, sello-sin gris): solo en los sellos sobre las fotos y en las columnas del top.
- **Rojo de número en riesgo** (riesgo-numero): solo para los números de tendencias "en riesgo".
- **Azul IA** (azul-ia) sobre **fondo IA** (fondo-ia): todo lo que escribe o decide la IA.

### Neutral
- **Tinta** (tinta): texto y líneas fuertes.
- **Gris texto** (gris-texto): bajadas, pies y aclaraciones.
- **Línea** (linea): separadores finos entre filas.
- **Crema** y **pista** (crema, pista): fondo de fotos que cargan, hover del menú y barras vacías.

### Named Rules
**The Veredicto Fijo Rule.** El verde, el salmón y el amarillo de los sellos significan "se queda", "en riesgo" y "con cautela". No se usan para nada más.

**The Azul IA Rule.** El azul (azul-ia) marca solo lo que viene de la IA. Lo calculado lleva la etiqueta negra "Calculado".

**The Tono de la Foto Rule.** Las columnas del top y el link "Abrir artículo" toman el color de su propia foto (en el link, con más saturación y oscurecido para que se lea sobre blanco). Ese color es diseño, no un dato.

## Typography

**Display Font:** Inter (con system-ui, -apple-system, Segoe UI, Roboto)
**Body Font:** Inter

**Character:** una sola familia que hace todo el trabajo con el contraste: nombres de temporada enormes en minúscula, títulos de sección livianos en mayúscula y números pesados con cifras tabulares.

### Hierarchy
- **Display** (700, clamp(64px, 9vw, 140px), 0,86): el nombre de la temporada en la portada ("winter 2025"), en minúscula.
- **Número** (700, clamp(46px, 5vw, 72px), 1, cifras tabulares): los porcentajes de búsquedas y contra la temporada. En la ficha llegan a 104px; en celular se achican para que entren dos lado a lado.
- **Headline** (300, clamp(30px, 3.6vw, 46px), mayúscula): títulos de sección ("Top de la temporada", "Todas las tendencias"), con una línea de 1,5px debajo.
- **Title** (700, clamp(26px, 3.4vw, 40px), mayúscula): nombres de tendencia en las dobles páginas y títulos de bloques como la pirueta.
- **Body** (500, 16px, 1,4): texto corrido. Las bajadas usan 400 y hasta 80 caracteres por línea.
- **Label** (700, 12px, espaciado 0,12em, mayúscula): rótulos chicos ("BÚSQUEDAS", "EN LA PRENSA", "LO QUE MIRAMOS"), etiquetas y la línea de "dónde estás" en la cabecera.

### Named Rules
**The Una Sola Voz Rule.** Todo es Inter. La jerarquía sale del peso, el tamaño y la caja, nunca de otra familia.

**The Número Primero Rule.** En una tendencia, lo que más se ve después de la foto son sus dos números. El texto explica, no compite.

## Layout

El contenedor va hasta 1440px, con márgenes de 72px en compu, 32px por debajo de 1000px y 16px por debajo de 700px. Todo tiene que andar a 390px de ancho.

- **Portada de temporada:** partida, con la foto a la izquierda (44%) y el panel de color a la derecha.
- **Top de la temporada:** cinco columnas altas de color, con la foto adentro, el número enorme abajo y la flecha arriba a la derecha.
- **Todas las tendencias:** una doble página por tendencia, texto y foto grande, que alterna de lado. En celular se apila con la foto arriba.
- **Ficha:** dos columnas (datos y foto alta) y debajo, a todo el ancho, el resto: la pirueta de la foto, la comparación con la temporada, la curva, los datos y la IA.
- **Cabecera:** fija arriba, de 96px en compu. En celular va en dos filas: logo y "dónde estás" con el botón del perfil, y abajo el menú con ES/EN.

Al bajar, los bloques aparecen con un desplazamiento de 28px. Si el sistema pide menos movimiento, no hay animación.

## Elevation & Depth

Es plano: no usa sombras para dar jerarquía. La profundidad sale de las fotos, de los bloques de color de temporada y de las líneas finas. La única sombra es un `text-shadow` sobre los números blancos encima de las fotos, para que se lean.

### Named Rules
**The Papel Plano Rule.** Nada flota. Si algo tiene que destacarse, cambia de color o de tamaño, no gana una sombra.

## Shapes

Esquinas rectas en todo: botones, sellos, chips, paneles y fotos (0px). Los bordes son líneas de 1px (separadores) o 1,5px (títulos de sección, bloques como la pirueta y el selector de idioma). La única forma redonda es el punto de la etiqueta de la IA.

## Components

### Buttons
- **Forma:** rectángulo recto, sin redondeo.
- **Principal:** fondo azul noche, texto blanco en 700, 11px 16px de relleno.
- **Con borde:** transparente, con borde y texto del color actual. Se usa como alternativa al lado del principal.
- **Botón del home:** azul noche, 15px 28px de relleno; al pasar el mouse, verde noche.
- **Foco:** contorno azul de 2px separado 3px.

### Sellos
- **Estilo:** bloque de color plano, texto blanco en mayúscula, peso 300, 4px 12px de relleno.
- **Uso:** sobre la esquina de la foto ("SE QUEDA", "EN RIESGO", "CON CAUTELA") y en las columnas del top. El color sale de la regla del veredicto fijo.

### Etiquetas "Calculado" e "Inferencia de la IA"
- **Calculado:** borde de tinta de 1px, texto en mayúscula, con un cuadrado negro adelante.
- **IA:** fondo azul IA, texto blanco, con un punto blanco adelante.
- **Regla:** cada bloque con datos o con IA lleva una de las dos.

### Navigation
- **Menú:** tres opciones (Temporadas, Tu brief, Racional), 16px en 500. Al pasar el mouse, fondo crema. La activa va en verde noche con texto blanco.
- **Dónde estás:** debajo del logo, en rótulo chico. Muestra la pantalla en negrita y, al bajar, la sección que estás leyendo.
- **Idioma:** selector ES/EN con borde de 1,5px; la opción activa va rellena de tinta.

### Doble página de tendencia (componente propio)
Nombre en Title con línea debajo, meta ("rubro · la nombró [medio]"), foto chica más curvita, los dos números grandes con su rótulo a la derecha, confianza y apuesta en una línea y, abajo de todo, el bloque "En la prensa". Del otro lado, la foto alta con el sello arriba y una franja blanca semitransparente abajo con la marca del desfile y el botón "Ver el análisis →" (toda la foto lleva a la ficha).

En compu (desde 761px de ancho y 560px de alto), cada doble página ocupa una pantalla menos la cabecera, con tamaños que se ajustan a la altura, y al bajar la página frena suave en cada una (scroll-snap de proximidad). En pantallas bajas (hasta 760px de alto) se oculta la foto chica y queda la curva. En celular no hay freno.

### En la prensa (componente propio)
Línea de tinta de 1,5px arriba, rótulo "EN LA PRENSA", comillas grandes y la cita en 22 a 30px, que se pinta con los colores de la pasarela al pasar el mouse. Abajo, el medio en negrita y la fecha, y el link "Abrir artículo ↗" en el tono de la foto, subrayado. Si no hay nota de prensa, va la frase de la nota que nombró la tendencia.

### Bloque de la IA
Una cabecera en pizarra con el rótulo "Para tu marca / sugerencia de IA", la etiqueta IA y el título en mayúscula, y un cuerpo en fondo IA con una línea azul de 2px arriba. Tiene estados de carga (tres barras que brillan), error y saturada.

## Do's and Don'ts

### Do:
- **Do** que la foto de desfile sea lo más grande de cada tendencia, con el número grande como segundo nivel.
- **Do** marcar cada bloque como "Calculado" o "Inferencia de la IA", y poner lo de la IA siempre aparte.
- **Do** usar el durazno para Summer y la pizarra para Winter, y el tono de cada foto para sus columnas y su link.
- **Do** mantener las esquinas rectas (0px) y las líneas de 1 a 1,5px.
- **Do** probar cada pantalla a 390px, con teclado y en inglés.

### Don't:
- **Don't** hacer que parezca "hecho por IA" o una plantilla: nada de grillas de tarjetas iguales, gradientes decorativos ni íconos genéricos.
- **Don't** hacer que parezca una tienda online: sin precios, carritos ni grillas de producto.
- **Don't** usar los colores de los sellos para decorar, ni el rojo de número fuera de "en riesgo".
- **Don't** agregar sombras, esquinas redondeadas ni una segunda tipografía.
- **Don't** mostrar un número sin su rótulo ni sin decir de dónde sale.
