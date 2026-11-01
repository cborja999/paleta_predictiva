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
- **Tendencias de la temporada:** tarjetas de las tendencias puntuales con su veredicto ("tiende a quedarse" / "riesgo de moda pasajera" / "sin señal clara"), su confianza y la curva de búsquedas. Aparte, lo que se vio en 2026, sin veredicto.
- **Detalle de una tendencia:** qué se vio en pasarela, cómo se movieron las búsquedas y qué tan confiable es la lectura (nivel de confianza).
- **Cómo lo sabemos:** la evidencia en un formato visual simple (los porcentajes y los ciclos), con link al detalle técnico.

## Estado (Entrega 3)

- La app es `index.html` (versión editorial). `wrapped.html` queda como alternativa de diseño.
- Los datos los arma `armar_datos.py` en `datos.js` (página) y `datos.json` (lo lee la IA): SS2024, FW2024 y SS2025 con veredicto, y 2026 sin veredicto.
- La IA está en `../netlify/functions/` y se documenta en `../entrega3/IA.md`.
- Para probar la IA en local hace falta Netlify CLI (`netlify dev`) y la variable `GROQ_API_KEY`. Si abrís el HTML como archivo, la página anda pero la IA avisa que funciona en la versión online.

## Datos

- `../app/datos/brief_temporada.json` (**el brief principal**):
  - `items`: 31 tendencias puntuales de SS2024 y FW2024 (las listas de Who What Wear, CBC Life y Yahoo Lifestyle). Cada una tiene `termino`, `tendencia_fuente`, `medio`, `url_fuente`, `veredicto` ("Tiende a quedarse" / "Riesgo de moda pasajera" / "Sin señal clara"), `confianza` ("Alta" / "Media"), `g1` (cuánto se movieron las búsquedas, descontando la temporada), `aviso` (si la lectura depende de un pico de un mes) y `serie` mensual desde 2019 (alineada con `meta.meses`; `null` donde no hay dato).
  - `vistas_2026`: 36 tendencias de SS2026 y FW2026, **sin veredicto**. Van como "lo que se vio en la última temporada" porque los datos de Google desde mediados de 2025 no son comparables.
  - `meta`: la regla, los niveles de confianza y la evidencia en palabras para la página.
  - Resultado: SS2024 da 4 que se quedan, 4 con riesgo y 8 sin señal; FW2024 da 4, 7 y 4.
- `../app/datos/brief.json`: 21 categorías (11 colores, 8 prendas, 2 largos). Por categoría: participación en pasarela reciente y previa, color medido (`hex`), lectura de búsquedas en dos formas de buscar (`nueva`, `original`, con `inercia`, `pred` y `confianza`) y serie mensual de búsquedas desde 2019 (`serie_mundo`).
- `../app/datos/microtendencias.json`: 178 tendencias puntuales con su curva 2015-2024, el grupo del primer año (`SUBE`, `PLANO`, `CAE`) y si se quedó (`se_queda`). También el resumen por muestra y la tabla por ciclo.
- Usar `brief.json` para los colores (hex, participación en pasarela), no para veredictos: solo 3 de 21 categorías tienen.
- Veredicto de una categoría: "tiende a quedarse" si las dos formas de buscar dicen que ganó interés (inercia ≥ 0,10); "riesgo de moda pasajera" si las dos dicen que lo perdió (≤ −0,10); si no, sin veredicto. Es la misma regla de `app/index.html`.

## Diseño

- Referencias del grupo: The Lyst Index (rankings), Spotify Wrapped (relato visual por pantallas), TradingView (curvas), Pantone Color of the Year (el color como protagonista).
- Lo que pidieron los profes: más visual, criterios de la IA y niveles de confianza a la vista, y alternativas de diseño.
- Tiene que verse bien en celular.

## Para seguir editando el diseño en Claude Code

- **La que se edita es la versión editorial: `prototipo/index.html`.** `wrapped.html` es la alternativa descartada; queda solo como registro para la entrega (no tocarla).
- `index.html` tiene todo adentro (HTML, CSS y JavaScript). Lee los datos de `datos.js`.
- `datos.js` y `datos.json` no se editan a mano: los arma `python3 prototipo/armar_datos.py` desde `app/datos/`. Los nombres en castellano y el rubro de cada tendencia están en ese script.
- No cambiar textos de números, veredictos ni límites sin chequearlos contra `hipotesis.md` y las salidas de `analisis/`.
- Mantener lo que pide la entrega: etiquetas "Calculado" e "Inferencia de la IA", estados de la IA (cargando, error, sin servidor, aviso del control), responsive a 390 px y accesibilidad. Si cambia algo de diseño importante, anotarlo en `entrega3/DISENO.md` (la entrega pide documentar decisiones y diferencias).
- Para ver la página: abrirla en el panel de navegador, o `python3 -m http.server` desde la raíz del repo y entrar a `http://localhost:8000/prototipo/`. La IA solo responde en la versión online (Netlify).
- Trabajar en la rama `entrega-3`. Cada push a esa rama actualiza la página online.

Prompt para arrancar una sesión:

> Leé `CLAUDE.md` y `prototipo/README.md`. Vamos a seguir con el diseño de la versión editorial (`prototipo/index.html`), en la rama `entrega-3`. Abrila en el panel de navegador, mirala en escritorio y en celular, y decime qué mejorarías antes de cambiar nada.
