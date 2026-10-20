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

## Réplica en ciclos anteriores (20/10/2026, pedido del profesor)
Reglas fijadas antes de correr: `REGLAS_REPLICA_2022_2023.txt`. Script: `replica_ciclos.py`; salida: `salida_replica_ciclos.txt`. Se aplica la misma regla del brief (búsquedas "sube" si la inercia de los últimos 12 meses es positiva) a un brief armado en octubre de 2022 (ciclo 2022-2023, principal), octubre de 2021 y octubre de 2020, y se mira si después subió (cambio de los meses 12 a 23 contra los 12 previos). El ciclo 2023-2024 no se puede evaluar limpio porque su resultado cae en 2025.

| Ciclo (d0) | Mundo, forma 1: "sube" -> sube / "no sube" -> sube | Mundo, forma 2 | Argentina |
|---|---|---|---|
| oct-2022 (principal) | 4/10 = 40% / 6/10 = 60% | 8/12 = 67% / 4/13 = 31% (p=0,12) | 4/9 = 44% / 5/9 = 56% |
| oct-2021 | 8/10 = 80% / 2/10 = 20% (p=0,02) | 8/12 = 67% / 4/13 = 31% (p=0,12) | 4/9 / 5/9 |
| oct-2020 | 6/10 = 60% / 4/10 = 40% | 6/12 = 50% / 6/13 = 46% | 4/9 / 5/9 |
| Total (descriptivo) | 18/30 = 60% / 12/30 = 40% (p=0,20) | 22/36 = 61% / 14/39 = 36% (p=0,04) | 12/27 = 44% / 15/27 = 56% (p=0,59) |

**Lectura honesta:** el ciclo principal 2022-2023 da resultado mixto: a favor en la forma 2 del mundo, en contra en la forma 1. Sumando los tres ciclos la regla se ve en el mundo (60% contra 40% y 61% contra 36%) pero con pocos casos, y en Argentina no aparece (44% contra 56% en los tres ciclos). Agregar pasarela a las búsquedas que suben da 73% contra 52% (forma 2, p=0,30) y 77% contra 47% (forma 1, p=0,14): va en la dirección esperada pero no se distingue del azar. Los pares de un mismo ciclo no son independientes.
**Prensa:** no se puede evaluar. La planilla tiene 7 notas para SS2022, FW2022 y SS2023 (SS2022: 1, FW2022: 0, SS2023: 6) y la regla pedía al menos 10. Hace falta cargar notas de 2021-2022.

## Prensa internacional + búsquedas, ciclo 2022-2023 (20/10/2026)
Reglas fijadas antes de leer: `REGLAS_PRENSA_INTERNACIONAL_2022.txt`. Notas y etiquetas: `datasets/prensa_internacional/notas_2022.csv` (15 notas de Fashionista, Who What Wear y Vogue Scandinavia, SS2022, FW2022 y SS2023; etiquetas automáticas). Script: `prensa_internacional_2022.py`; salida: `salida_prensa_internacional_2022.txt`.

| Comparación (pares categoría x familia del mundo, brief de oct-2022) | Con prensa | Sin prensa | Fisher |
|---|---|---|---|
| Principal (15 notas): búsquedas "sube" -> sube | 10/15 = 67% | 1/6 = 17% | p=0,06 |
| Principal: coincidencia completa (prensa + pasarela + búsquedas) -> sube | 3/3 = 100% | resto 17/38 = 45% | p=0,11 |
| Sensibilidad, sin las 2 galerías de Vogue Scandinavia (13 notas): búsquedas "sube" -> sube | 3/7 = 43% | 8/14 = 57% | p=0,66 |
| Sensibilidad: coincidencia completa | 0 casos | | |

**Lectura honesta:** el resultado principal parece a favor, pero se da vuelta al sacar dos notas. Las dos galerías de looks de Vogue Scandinavia listan casi todas las categorías y por eso casi todo "tiene prensa". Con 13 notas la prensa internacional no separa lo que sube de lo que no. Con estas notas no se puede afirmar que la prensa internacional más las búsquedas coincidan con lo que después subió. Además las prendas saturan (vestido 100%, top 87%, falda y pantalón 80%), así que la señal solo discrimina en colores y largos. Los pares de un mismo ciclo no son independientes y las etiquetas no fueron revisadas por una persona.
