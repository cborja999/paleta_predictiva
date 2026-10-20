# ¿Lo que gana interés en búsquedas se queda? (20/10/2026)

Pregunta nueva del proyecto: de los colores, prendas y largos que **ganan interés** en Google, ¿cuáles se quedan y cuáles son moda pasajera? Todas las reglas se escribieron **antes** de correr cada prueba (`REGLAS_*.txt`) y no se cambiaron después. Los scripts corren desde esta carpeta (`python3 -I p8.py`) y dan los mismos números que las salidas guardadas (`salida_*.txt`).

## Cómo se mide
- Fecha `d` = mes del desfile de cada temporada (FW2013 a SS2023, ventana limpia: los datos terminan en dic-2024 porque Google cambió cómo mide en 2025).
- `L0` = promedio de los meses d-24 a d-13; `L1` = d-12 a d-1; `L2` = d+12 a d+23. Siempre 12 meses completos, así la estación (verano/invierno) se cancela.
- "Ganó interés" = subió al menos 0,10 (en log) respecto de la mediana de todas las categorías de esa temporada. Control = las que no se movieron (entre -0,10 y 0,10).

## Resultados
| Prueba | Búsquedas | Ganó interés | Control | Diferencia |
|---|---|---|---|---|
| "Se queda" original (compara contra L0) | Mundo, familia original | 88% | 43% | +45 pts |
| | Mundo, familia nueva | 91% | 42% | +48 pts |
| | Argentina | 86% | 45% | +41 pts |
| | Shopping Argentina | 89% | 44% | +44 pts |
| **"Se queda" limpio (L2 contra L1)** | **Mundo, familia original** | **84%** | **70%** | **+14 pts (p=0,001)** |
| | **Mundo, familia nueva** | **84%** | **69%** | **+14 pts (p=0,003)** |
| | Argentina | 67% | 73% | -7 pts (p=0,91) |
| | Shopping Argentina | 69% | 76% | -7 pts (p=0,89) |

**Lectura honesta:** la versión original compara contra el mismo período base con el que se mide la suba (`L0`), y eso infla la diferencia. Con el test limpio, en el mundo la ventaja es de unos **14 puntos** y se sostiene en las dos familias de términos. En Argentina (búsquedas generales y de Shopping) **no se sostiene**.

## Argentina contra el mundo, con retraso
Spearman entre la suba mundial (búsqueda general) en `d` y la suba argentina medida con la ventana corrida `k` meses.

| k (meses) | Argentina general | Shopping Argentina |
|---|---|---|
| 0 | 0,09 (p=0,03) | 0,27 (p<0,001) |
| 6 | 0,06 (p=0,11) | 0,19 (p=0,001) |
| 12 | -0,02 (p=0,65) | 0,04 (p=0,25) |
| 18 | -0,02 (p=0,66) | 0,06 (p=0,17) |

No hay evidencia de que Argentina siga al mundo con 12 a 18 meses de demora. Se mueven casi a la par; con Shopping la relación es más clara pero modesta (si el mundo ganó interés, Shopping Argentina también en 32% de los casos, contra 22% en general).

## Otras pruebas del mismo marco (`salida_fase2.txt`, `salida.txt`)
- Tracción ("lo que sube sigue subiendo"): 64 a 69% en el mundo, 61% en Shopping mundo, **49% en Argentina** (azar).
- Pasarela -> búsquedas: 51% (azar). La pasarela queda como contexto visual, no como predictor.

## Predicción congelada
`prediccion_congelada_2026-10-19.csv` (63 filas, tres familias: original, nueva y Argentina) con huella `SHA256_prediccion_congelada.txt`. `congelar.py` **no** reescribe el archivo si ya existe. Chequeo principal: **octubre de 2028**; chequeo intermedio exploratorio: octubre de 2027. En Argentina no se ofrece nivel de confianza.

## Límites
- 20 a 27 temporadas; las categorías de una temporada no son independientes.
- Términos en búsquedas: 14 de 18 términos de Shopping Argentina fueron usables (beige, naranja, plateado y pollera mini tienen más de 50% de meses en cero y se descartaron sin reemplazo). Marrón y pollera midi se bajaron pero no entran en el mapeo.
- Trends mide búsquedas, no ventas. No hay datos públicos de ventas argentinas por color o prenda.
- Los datos de Shopping Argentina se bajaron el 20/10/2026 con la categoría Compras (18) de Google Trends.
