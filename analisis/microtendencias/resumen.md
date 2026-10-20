# Tendencias puntuales: ¿se quedan las que suben? (20/10/2026)

Hipótesis de Borja: las prendas/tendencias que **aumentan** después de aparecer en las fashion weeks persisten; las que **caen o se mantienen planas** son modas pasajeras.

Las pruebas de `analisis/persistencia/` usan ~20 categorías amplias (negro, vestido, mini). Acá probamos lo mismo con **tendencias puntuales** (bike shorts, corset top, cargo pants, y2k…) que **un medio eligió en su momento** como las más importantes de cada temporada. Así no elegimos nosotros con el diario del lunes.

## Cómo se hizo
- **M1 (principal):** listas "biggest trends" de Who What Wear, SS2019 a SS2023 (9 temporadas). 102 tendencias → 68 términos de búsqueda (`terminos_declarados.csv`; las descartadas y el motivo están fila por fila).
- **M2 (réplica):** listas "Top 20 Runway Trends" de Sandra's Closet, SS2020 a SS2023 (7 temporadas). 54 términos **nuevos** (ninguno repetido de M1). La decisión de sumar M2 se tomó **después** de ver M1 y se declara así (`REGLAS_M2_REPLICA.txt`).
- **Datos:** Google Trends, búsqueda web, mundo, mensual 2011–2024 (después de 2025 Google cambió cómo mide). Se bajaron el 20/10/2026 desde el navegador; checksum verificado contra lo que devolvió Google. En `datos/`.
- **Reglas** escritas antes de bajar los datos (`REGLAS_MICROTENDENCIAS.txt`, huellas en `SHA256_reglas.txt`):
  - `B0` = año antes del desfile, `B1` = primer año, `B2` = segundo año (12 meses completos, la estación se cancela).
  - Grupo según el primer año contra el resto de las tendencias de esa temporada: **SUBE** (≥ +0,10 en log), **PLANO**, **CAE** (≤ −0,10).
  - **Se queda** = en el segundo año no pierde más de ~10% contra el resto (`c2 ≥ −0,10`). Si no, **pasajera**.
  - Apoya si SUBE supera a PLANO+CAE por ≥ 10 puntos con Fisher p < 0,05.

## Resultados (`salida_m1.txt`, `salida_m2.txt`)
| Muestra | SUBE se queda | PLANO se queda | CAE se queda | SUBE vs resto | Fisher p | Criterio |
|---|---|---|---|---|---|---|
| M1 Who What Wear (68) | 14/16 = 88% | 26/38 = 68% | 8/14 = 57% | +22 pts | 0,12 | No apoya |
| M2 Sandra's Closet (54) | 15/17 = 88% | 19/24 = 79% | 8/13 = 62% | +15 pts | 0,30 | No apoya |
| M1 + M2 (122, descriptivo) | 29/33 = 88% | 45/62 = 73% | 16/27 = 59% | +19 pts | 0,037 | — |

- Correlación continua (cuánto subió el primer año vs. cómo le fue el segundo): Spearman 0,28 (p = 0,02) en M1; 0,24 (p = 0,09) en M2; 0,26 (p = 0,004) juntas.
- Google Shopping (M1, 52 términos usables): 92% vs 67%, +26 pts, p = 0,15. Mismo sentido, sin significancia.
- Sin restar la mediana de la temporada (secundario 2): M1 +17 pts (p = 0,10), **M2 +2 pts** (p = 1,0). El resultado depende de comparar contra el resto de la temporada.

## Lectura honesta
1. **Primera mitad de la hipótesis (las que suben se quedan): va en la dirección, sin prueba firme.** En las dos muestras, 88% de las que subieron el primer año seguían el segundo. Cada muestra sola no pasa el criterio (pocos casos: 16 y 17). Juntas pasan p < 0,05, pero juntar fue una decisión posterior, así que lo presentamos como indicio, no como confirmación.
2. **Segunda mitad (las planas son pasajeras): no se sostiene.** Las planas se quedaron 73% de las veces: la mayoría no desaparece.
3. **Lo que sí aparece claro es el escalón:** SUBE > PLANO > CAE en las dos muestras. El riesgo de moda pasajera está en **lo que cae el primer año**: 41% de esas fueron pasajeras, contra 12% de las que subieron (descriptivo, Fisher p = 0,016; comparación no declarada antes).
4. Hipótesis reformulada que sí se puede defender: *"Una tendencia de pasarela que gana búsquedas en su primer año rara vez se desploma en el segundo; las que pierden búsquedas el primer año tienen más del triple de chances de ser pasajeras."*

## Límites
- Dos fuentes de listas, en inglés: mide el interés global de habla inglesa, no Argentina.
- El paso "tendencia → término de búsqueda" es una decisión nuestra (documentada). Algunos términos son genéricos (blazer, tank top, red dress).
- Las tendencias de una misma temporada no son independientes.
- Búsquedas no son ventas.
- Conocíamos de antemano cómo les fue a algunas (y2k, bike shorts); por eso las listas las eligieron los medios y el mapeo es literal.
- Sandra's Closet es un blog y a veces publica meses después del desfile.

## Cómo repetirlo
`python3 -I m1.py` y `python3 -I m2.py` desde esta carpeta reproducen `salida_m1.txt` y `salida_m2.txt`. Después, `python3 -I app/armar_microtendencias.py` actualiza la sección de la página.
