# Proceso, datos y criterios (respuesta a la devolución de la Entrega 2)

## 1. Qué datos usamos y cómo entran (todo está en el repo)

| Dato | Cómo se obtuvo | Archivo | Para qué sirve |
|---|---|---|---|
| Fotos de pasarela | Banco Vogue Runway (Hugging Face, `tonyassi/vogue-runway-top15-512px`). Se tomó una muestra de 90 fotos por temporada (SS2011 a SS2024; 14 casas) vía su API pública. | `datasets/muestra_vogue_para_gemini.csv` | Qué se mostró en pasarela |
| Clasificación de las fotos | **API de Gemini**: a cada foto se le pide color, prenda, silueta y largo, con listas cerradas de opciones. | `datasets_procesados/resultados_gemini.csv` (2.430 fotos) | Convertir fotos en atributos medibles |
| Reportes de pasarela 2025-26 | **Carga manual** de reportes públicos: T-Fashion (89 filas), WGSN (17, de sus notas públicas de Fashion Week Data) y Heuritech (4). No hay API ni scraping. | `datasets/runway_reportes_2025_2026.csv` | Pronósticos recientes para chequear hacia adelante |
| Búsquedas | Google Trends, web, mensual. Descarga manual desde la web. | `datasets/trends/`, `trends_marcas/`, `trends_casos/` | Qué buscó la gente después |
| Relevancia de marcas | Trends de marcas + Lyst Index (del grupo CICLO) | `analisis/marcas_*`, `analisis/lyst_*` | Qué casas pesan más |

**¿Cómo se convierten fotos en siluetas?** Gemini mira cada foto y elige **una** opción de una lista cerrada (Recta, Estructurada, Amplia/Oversized, Fluida/Drapeada, Ajustada, Acampanada/Evase). Después se cuenta qué porcentaje de las fotos de cada temporada cae en cada opción. No hay "creatividad" de la IA: es una clasificación con vocabulario fijo.

**¿Qué tan bien clasifica?** Validamos 40 fotos con una segunda lectura: largo 90%, color 82%, prenda 70%, **silueta 58%**. Silueta es el atributo débil y subjetivo; no hay que presentarlo como dato duro (ver `analisis/validacion_gemini_resumen.md`).

## 2. Qué decide la IA y qué deciden reglas fijas

| Paso | Quién | Criterio |
|---|---|---|
| Etiquetar la foto | IA (Gemini) | Lista cerrada de opciones; validada en muestra |
| Calcular % por temporada | Código | Conteo simple |
| Detectar "sube en pasarela" | **Regla fija** | % de la temporada menos promedio de las 4 temporadas anteriores del mismo tipo (SS o FW) |
| Nivel de confianza | **Regla fija** | Media: +3 a +6 puntos. Alta: +6 o más. Menos de 3: sin señal |
| Resultado real | Código | Cambio de búsquedas entre los 12 meses previos al desfile y los meses +12 a +23 después, relativo a las demás categorías |
| Redactar el brief | IA (Claude) | Solo redacta a partir de los indicadores; no decide qué tendencia sube |

## 3. Qué nos dice el backtest (acierto histórico de la regla)
Resultados en `analisis/backtest_resumen.md`. En la ventana limpia (20 temporadas, FW2013 a SS2023):
- Confianza **Alta** de pasarela: 47% de acierto (91 predicciones). **Media**: 53% (124). Azar: 50%. Ninguna es distinta del azar.
- Rival: la **inercia de Trends** (lo que ya venía subiendo en búsquedas) acierta 63% y sí es distinta del azar.
- Chequeo exploratorio: sumar la señal de pasarela a la inercia de Trends no mejora (61% vs 65%).
- Chequeo hacia adelante con los reportes 2025-26: 7 aciertos en 14 predicciones.

**Qué significa para el producto:** hoy, con estos datos, **no podemos prometer confianza alta** a partir de la pasarela sola. Lo honesto es mostrar el nivel de confianza como "baja a media" y explicar por qué. Lo que sí tiene respaldo es mostrar la **evidencia concreta** de casos (ver `analisis/casos_resumen.md`) y combinar con la inercia de búsquedas.

## 4. Límites que hay que decir en voz alta
- Argentina: la regla "lo que gana interés se queda" vale en búsquedas del mundo (+14 puntos con el test limpio), pero no se confirmó en búsquedas de Argentina ni en Shopping Argentina (`analisis/persistencia/resumen.md`).
- Los umbrales (3 y 6 puntos) se fijaron antes de calcular, pero son arbitrarios.
- 20 a 27 temporadas es poco; las categorías de una temporada no son independientes entre sí.
- Los casos ilustrativos fueron elegidos porque ya sabíamos que "funcionaron" (sesgo de selección).
- Google Trends tuvo un salto de medición en 2025; los análisis principales lo evitan.


## 5. Segunda etapa (20/10/2026)
El producto ahora combina tres señales: se vio en pasarela, la prensa argentina lo nombra y las búsquedas suben. La señal principal es la búsqueda. Resultados, reglas y la predicción congelada están en `analisis/persistencia/`; la prensa, en `datasets/prensa_argentina/`.
