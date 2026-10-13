# Backtest: ¿cuántas veces habríamos acertado?

Regla fijada de antemano (ver encabezado de `backtest_confianza.py`). Resultado = cambio de búsquedas entre los 12 meses previos al desfile y los meses +12 a +23 después, relativo a la mediana de las demás categorías de esa temporada.
Azar = 50%. El p-valor mezcla los resultados entre categorías de la misma temporada (2000 veces).

## Ventana limpia (resultado antes de 2025)

Temporadas: 20 (FW2013 a SS2023). Categorías por temporada: ~25.

| Regla | Predicciones | Aciertos | % acierto | p vs azar |
|---|---|---|---|---|
| Pasarela: Alta (>= 6 pts) | 91 | 43 | 47% | 0.596 |
| Pasarela: Media (3 a 6 pts) | 124 | 66 | 53% | 0.142 |
| Pasarela: Alta + Media (>= 3 pts) | 215 | 109 | 51% | 0.234 |
| Solo 'SUBE' (>= 3 pts) | 101 | 45 | 45% | 0.811 |
| Inercia de Trends (sin pasarela) | 500 | 315 | 63% | 0.000 |

## Todas las temporadas posibles (incluye el salto de Google de 2025)

Temporadas: 22 (FW2013 a SS2024). Categorías por temporada: ~25.

| Regla | Predicciones | Aciertos | % acierto | p vs azar |
|---|---|---|---|---|
| Pasarela: Alta (>= 6 pts) | 96 | 45 | 47% | 0.642 |
| Pasarela: Media (3 a 6 pts) | 138 | 70 | 51% | 0.289 |
| Pasarela: Alta + Media (>= 3 pts) | 234 | 115 | 49% | 0.381 |
| Solo 'SUBE' (>= 3 pts) | 112 | 47 | 42% | 0.936 |
| Inercia de Trends (sin pasarela) | 550 | 344 | 63% | 0.000 |

## Cómo leerlo
- Si 'Alta' acierta claramente más que 'Media' y que el azar, la confianza tiene sentido y la podemos mostrar como nivel en el brief.
- Si no, hay que decir que la señal de pasarela por sí sola no alcanza para prometer confianza alta.
- La inercia de Trends es el rival a vencer: si lo que ya sube en búsquedas acierta igual o más, la pasarela no agrega información.
- Limitaciones: ~27 temporadas, 25 categorías, búsquedas en inglés y a nivel mundial; los umbrales se fijaron antes de mirar pero son arbitrarios; las categorías de una misma temporada no son independientes.

## Chequeo exploratorio (calculado después de ver los resultados; no es una prueba)
Entre las categorías cuyas búsquedas ya venían subiendo (ventana limpia): si además subían en pasarela (>= 3 pts) acertaron 61% (31 de 51); si no subían en pasarela, 65% (121 de 187). La pasarela no mejora la predicción sobre la inercia de Trends en este dataset.
