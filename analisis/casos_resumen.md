# Tres casos ilustrativos (octubre 2026)

**Que son:** tres tendencias que la prensa de moda atribuye a un desfile puntual. Miramos como se movieron las busquedas en Google Trends (mundo) en los 3 años siguientes.
**Que NO son:** una prueba de la hipotesis. Los casos los elegimos porque ya sabiamos que "funcionaron" (sesgo de seleccion). Sirven para ilustrar, no para confirmar.

Como se mide: ventanas de 12 meses completos (evita estacionalidad). Base = 12 meses antes del desfile; luego año 1 (+1..+12), año 2 (+13..+24), año 3 (+25..+36). Indice de Trends 0-100, todos los terminos de un caso en la misma escala. Datos: `datasets/trends_casos/`. Calculo: `analisis/casos_ilustrativos.py`. Cifras: `casos_resumen.csv` y `casos_pasarela.csv`.

| Caso | Termino | Base | Año 1 | Año 2 | Año 3 |
|---|---|---|---|---|---|
| Balenciaga Triple S (desfile ene 2017) | balenciaga triple s | 0,0 | 10,8 | 53,3 | 53,8 |
| | dad shoes | 3,3 | 4,5 | 11,8 | 9,8 |
| | chunky sneakers | 0,5 | 0,7 | 5,0 | 10,5 |
| Rosa Valentino (desfile mar 2022) | pink dress | 23,9 | 29,7 | 32,8 | 33,9 |
| | hot pink | 15,4 | 19,0 | 21,4 | 19,8 |
| Minifalda Miu Miu (desfile oct 2021) | mini skirt | 6,0 | 7,8 | 9,3 | 12,6 |
| | miu miu | 12,3 | 15,3 | 20,7 | 34,3 |

Lo que mostraban nuestras fotos (Gemini): rosa dominante en otoño-invierno 2022 = 8,9% de las fotos vs 2,3% promedio de los 11 otoño-invierno anteriores (Valentino 6 fotos, Chanel 2). Mini en primavera-verano 2022 = 33,3% vs 26,2% promedio de las otras 13 primavera-verano.

## Lectura honesta caso por caso
- **Triple S:** las busquedas despegan despues de la salida a tiendas (sep 2017), no del desfile. Hay un retraso de 1-2 años, pero el lanzamiento comercial confunde: no podemos separar "efecto pasarela" de "efecto producto a la venta".
- **Rosa Valentino:** el rosa ya venia subiendo antes del desfile y sigue subiendo gradualmente, sin quiebre en la fecha. Ademas la pelicula Barbie (jul 2023) contamina la señal. Ambiguo.
- **Minifalda:** es el caso mas limpio: suba gradual de "mini skirt" (6 → 12,6, se duplica en 3 años). Pero Miu Miu no esta entre las 14 casas de nuestras fotos, y la busqueda "miu miu" es crecimiento de la marca, no de la prenda.

## Limites
- Sesgo de seleccion (elegimos casos conocidos). No hay casos "que no funcionaron" para comparar.
- Con un solo desfile no hay forma de decir que la causa fue la pasarela y no otra cosa (redes, pelicula, lanzamiento).
- Los valores 2025-2026 de varios terminos saltan de forma rara; no los interpretamos. Por eso las ventanas llegan hasta +36 meses y los graficos hasta +48. (Los "meses hasta el pico" de varios terminos caen en 2026: no son un pico real, no usarlos.)
- Trends es mundo, no Argentina.

## Fuentes (origen atribuido al desfile)
Balenciaga Triple S: Sneaker Freaker y Fashion Magazine. Rosa Valentino (Pink PP): L'Officiel India. Miu Miu low-rise / minifalda: Rebag y L'Officiel India. (Las URLs exactas estan por completar en `decisiones.md`; no las dejamos aca para no citar de memoria.)

## Conclusion
Los casos son compatibles con un retraso de 1-3 años entre pasarela y busqueda masiva, pero no lo prueban. La hipotesis sigue **sin confirmar ni refutar**.

Graficos: `casos_triple_s.svg`, `casos_rosa_valentino.svg`, `casos_minifalda_miu_miu.svg`.
