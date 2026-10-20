# Hipótesis del proyecto

> **Una tendencia de pasarela que gana búsquedas en su primer año rara vez se desploma en el segundo.**

Estado: **confirmada con datos nuevos** (tendencias de 2016 a 2018 que no se usaron para formularla, con reglas y criterios fijados antes de bajar los datos).

## Qué significa cada palabra

| Palabra | Cómo se mide |
|---|---|
| Tendencia de pasarela | Una prenda, detalle, color o estética que un medio de moda nombró entre las principales de una fashion week (listas elegidas por el medio en su momento). |
| Búsquedas | Google Trends, búsqueda web, mundo, mensual. Un término por tendencia, literal. |
| Primer año / segundo año | Los 12 meses desde el mes del desfile / los 12 siguientes (SS = octubre del año anterior, FW = marzo). |
| Gana búsquedas | El primer año subió al menos 10% (0,10 en log) contra el año previo, descontando lo que se movió el resto de esa temporada. |
| Se desploma (moda pasajera) | En el segundo año pierde más de ~10% contra el resto de la temporada. |
| Rara vez | Como máximo 20% de pasajeras. |

## Cómo se probó

1. **Exploración (donde nació la frase):** 122 tendencias de Who What Wear (SS2019-SS2023) y Sandra's Closet (SS2020-SS2023). `analisis/microtendencias/`.
2. **Prueba con datos nuevos:** 57 tendencias de 2016-2018 (Sandra's Closet, W Magazine, Fashionista). Reglas en `analisis/hipotesis/REGLAS_HIPOTESIS_C1.txt`, con huella sha256 en `SHA256_reglas_c1.txt`.

## Resultado

| Muestra | Pasajeras entre las que ganaron búsquedas | Resto (planas o en baja) |
|---|---|---|
| **2016-2018 (prueba, 56 usables)** | **1 de 17 = 6%** | 7 de 39 = 18% |
| 2019-2023 Who What Wear | 2 de 16 = 12% | 18 de 52 = 35% |
| 2020-2023 Sandra's Closet | 2 de 17 = 12% | 10 de 37 = 27% |
| Las tres juntas | 5 de 50 = 10% | 35 de 128 = 27% |

**Ciclo por ciclo** (`analisis/hipotesis/ciclos.csv`): en los 8 ciclos, de 2016→2017 a 2023→2024, las pasajeras entre las tendencias que ganaron búsquedas nunca pasaron del 20%.

| Colecciones | Pasajeras entre las que ganaron búsquedas |
|---|---|
| 2016 → 2017 | 0 de 4 |
| 2017 → 2018 | 1 de 9 |
| 2018 → 2019 | 0 de 4 |
| 2019 → 2020 | 0 de 2 |
| 2020 → 2021 | 2 de 12 |
| 2021 → 2022 | 1 de 9 |
| 2022 → 2023 | 0 de 5 |
| 2023 → 2024 | 1 de 5 |

**En una frase:** 9 de cada 10 tendencias de pasarela que ganan búsquedas en su primer año siguen ahí al segundo.

## Lo que muestran los últimos años: las que pierden búsquedas (2021 a 2024)

> **Los datos de 2021 a 2024 muestran que las tendencias que pierden búsquedas en su primer año tienen más del triple de chances de ser pasajeras que las que las ganan.**

| Colecciones | Pasajeras entre las que perdieron búsquedas | Pasajeras entre las que las ganaron |
|---|---|---|
| 2021 → 2022 | 5 de 8 | 1 de 9 |
| 2022 → 2023 | 2 de 5 | 0 de 5 |
| 2023 → 2024 | 2 de 3 | 1 de 5 |
| **Total** | **9 de 16 = 56%** | **2 de 19 = 11%** |

Más de la mitad de las que perdieron búsquedas fueron pasajeras, contra 1 de cada 10 de las que las ganaron (unas 5 veces más; Fisher p = 0,009). Datos: `analisis/hipotesis/ciclos.csv`. Se sigue midiendo con cada temporada nueva.

## Cómo lo usa el producto

- **Ganó búsquedas el primer año** → "tiende a quedarse".
- **Perdió búsquedas el primer año** → "riesgo de moda pasajera" (en 2021-2024, más de la mitad lo fueron).
- **Sin cambio claro** → no se da veredicto.
- La pasarela muestra qué se vio en cada fashion week; la señal para el veredicto son las búsquedas.

## Límites

- Mide búsquedas en Google (interés), no ventas.
- Listas de medios en inglés: refleja el interés global.
- El paso de tendencia a término de búsqueda es una decisión documentada fila por fila (`terminos_declarados_*.csv`).
- Las tendencias de una misma temporada no son independientes.
