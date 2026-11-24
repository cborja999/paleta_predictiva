# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users

La dueña o diseñadora de una marca de ropa argentina chica o mediana. No va a las fashion weeks, no paga un servicio de tendencias y decide sola qué producir para la próxima temporada. No tiene formación en estadística y trabaja desde el celular y la compu.

Su trabajo: antes de producir, decidir en qué tendencia apostar fuerte, en cuál de forma moderada y en cuál probar poco, sin quedarse con stock de una moda pasajera.

## Product Purpose

Paleta predictiva arma un brief de las fashion weeks (Nueva York, Londres, Milán y París) y dice qué tendencias tienden a quedarse y cuáles tienen riesgo de ser pasajeras.

Se apoya en esta hipótesis: una tendencia de pasarela que gana búsquedas en su primer año rara vez se desploma en el segundo, y las que las pierden tienen más del triple de chances de ser pasajeras (detalle en `hipotesis.md`).

Éxito: que la marca salga sabiendo cuánto apostar en cada tendencia de su rubro, con un brief que se puede llevar.

## Positioning

Los informes pagos (LIVETREND, WGSN) dicen cuánto se vio algo en la pasarela. Paleta predictiva mira otra cosa: si la gente buscó la tendencia en Google el año después del desfile, comparada contra el resto de su temporada. Las reglas se escribieron antes de bajar los datos y cada número de la app se puede recalcular desde los datos crudos (`trazabilidad/`).

## Operating Context

- Proyecto de la materia K576 (Universidad de San Andrés) de Beltrán Martínez, Borja Centeno y Luigi Bonomi. Se presenta con demo en vivo.
- Temporadas del hemisferio norte: Summer es primavera-verano y Winter es otoño-invierno. Con veredicto: 2024 y 2025. 2026 se muestra sin veredicto.
- La marca entra por temporada, ve el top y todas las tendencias, abre la ficha de cada una y se lleva "Tu brief" en PDF. Con su perfil (rubro, qué vende, público, precio, canal), la IA le sugiere qué mirar.
- Online en https://paleta-predictiva.netlify.app. Se publica con `sh prototipo/publicar.sh`.

## Capabilities and Constraints

- **Veredictos calculados con reglas fijas:** "se queda" o "en riesgo", con confianza alta o media y avisos de cautela. Cuánto apostar sale de una regla fija.
- **La IA explica, no decide** (regla de `CLAUDE.md`): explica cada tendencia, elige qué mirar de una temporada y compara la foto de una prenda con tres rasgos de la tendencia. No calcula ni cambia veredictos ni números.
- **Idiomas:** español e inglés. Todo tiene que andar en los dos.
- **Celular:** todo tiene que andar a 390 px de ancho y con teclado.
- **Búsquedas no son ventas:** son búsquedas de todo el mundo. Con búsquedas solo de Argentina la regla no se confirmó.
- **Sin veredicto para 2026:** desde mediados de 2025 Google Trends mide distinto.
- **Datos:** los números salen de `analisis/` y de `app/datos/`. No se ajustan datos ni reglas para que la hipótesis dé bien.
- **Fotos de desfiles:** tienen derechos y no se suben a GitHub; van solo a la versión publicada.

## Brand Commitments

- Nombre: Paleta predictiva.
- Voz: español argentino, directo y sin teoría. Se dice "temporada", no "season".

## Evidence on Hand

- Hipótesis y resultados: `hipotesis.md`, `analisis/hipotesis/`, `analisis/microtendencias/`.
- 178 tendencias de 2016 a 2024 y los briefs de 2024, 2025 y 2026 en `app/datos/`.
- Verificación de los 620 números de la app: `trazabilidad/verificar_numeros.py`.
- Citas de prensa verificadas: `prototipo/prensa_tendencias.csv`.
- Rasgos para comparar fotos: `prototipo/rasgos_tendencias.csv` (24 de 26 son borrador a revisar por el grupo).
- **No existen:** entrevistas a marcas, testimonios, clientes ni ventas. No inventarlos ni dejar lugar para ellos.

## Product Principles

1. **Lo calculado y lo de la IA, siempre separados y marcados.**
2. **Cada número se puede rastrear** hasta su dato y su regla.
3. **Decir lo que los datos no dicen**, junto con lo que dicen.
4. **La decisión de la marca primero:** cuánto apostar en cada tendencia.
5. **Nada inventado:** ni citas, ni entrevistas, ni veredictos que los datos no sostienen.

## Accessibility & Inclusion

Navegable con teclado y legible a 390 px. Respeta "reducir movimiento" del sistema.
