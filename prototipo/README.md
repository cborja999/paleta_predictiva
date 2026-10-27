# Prototipo de Paleta predictiva

Acá va el prototipo de la página para marcas. La versión "informe" que ya existe está en `app/index.html`; este prototipo es la versión producto: lo que ve una marca.

## Para quién

Dueños o diseñadores de marcas de ropa argentinas chicas y medianas. No saben de estadística y no pueden ir a fashion weeks. Quieren saber qué producir para la próxima temporada sin quedarse con stock de una moda pasajera.

## Qué tiene que responder la página

1. ¿Qué se vio en las últimas fashion weeks? (colores, prendas, largos)
2. ¿Qué tiende a quedarse? Lo que ganó búsquedas en su primer año.
3. ¿Qué tiene riesgo de ser pasajero? Lo que perdió búsquedas.
4. ¿Por qué le creo? La evidencia: 9 de cada 10 que ganan búsquedas siguen al segundo año; en 2021-2024, 9 de 16 de las que cayeron fueron pasajeras.

## Pantallas sugeridas (punto de partida, no obligatorio)

- **Portada:** la temporada, la hipótesis en una frase y 3 o 4 tendencias destacadas.
- **Tendencias de la temporada:** tarjetas de colores, prendas y largos con su veredicto ("tiende a quedarse" / "riesgo de moda pasajera" / sin veredicto), la muestra de color real y la curva de búsquedas.
- **Detalle de una tendencia:** qué se vio en pasarela, cómo se movieron las búsquedas y qué tan confiable es la lectura (nivel de confianza).
- **Cómo lo sabemos:** la evidencia en un formato visual simple (los porcentajes y los ciclos), con link al detalle técnico.

## Datos

- `../app/datos/brief.json`: 21 categorías (11 colores, 8 prendas, 2 largos). Por categoría: participación en pasarela reciente y previa, color medido (`hex`), lectura de búsquedas en dos formas de buscar (`nueva`, `original`, con `inercia`, `pred` y `confianza`) y serie mensual de búsquedas desde 2019 (`serie_mundo`).
- `../app/datos/microtendencias.json`: 178 tendencias puntuales con su curva 2015-2024, el grupo del primer año (`SUBE`, `PLANO`, `CAE`) y si se quedó (`se_queda`). También el resumen por muestra y la tabla por ciclo.
- Veredicto de una categoría: "tiende a quedarse" si las dos formas de buscar dicen que ganó interés (inercia ≥ 0,10); "riesgo de moda pasajera" si las dos dicen que lo perdió (≤ −0,10); si no, sin veredicto. Es la misma regla de `app/index.html`.

## Diseño

- Referencias del grupo: The Lyst Index (rankings), Spotify Wrapped (relato visual por pantallas), TradingView (curvas), Pantone Color of the Year (el color como protagonista).
- Lo que pidieron los profes: más visual, criterios de la IA y niveles de confianza a la vista, y alternativas de diseño.
- Tiene que verse bien en celular.

## Para arrancar en Claude Code

Pegá algo así en la primera sesión:

> Leé `CLAUDE.md`, `hipotesis.md` y `prototipo/README.md`. Armá una primera versión del prototipo en `prototipo/index.html` usando los datos de `app/datos/`. Mostrámelo en el panel de navegador y trabajá en una rama nueva.
