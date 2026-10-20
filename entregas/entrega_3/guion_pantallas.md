# Guion de pantallas (para armar en Figma: 2-3 alternativas por pantalla)

Principio de los docentes: **la plataforma tiene que ser visual, no textual**. Cada tendencia se muestra con imagen de silueta/look, no solo con nombre.

| # | Pantalla | Qué se ve | Datos que la alimentan |
|---|---|---|---|
| 1 | Inicio / elegir marca y temporada | Marca (rubro, rango de precio), temporada argentina objetivo | Perfil cargado por la marca |
| 2 | Brief de la temporada | **Máximo 5 tendencias**, cada una con foto de looks reales, paleta de colores y largo | `participacion_por_temporada.csv`, fotos de la muestra |
| 3 | Detalle de una tendencia | Foto de pasarela + curva de búsquedas del mundo y de Argentina (se mueven casi a la par; no hay evidencia de retraso de 12 meses) + qué dice la prensa local | `trends_unificado.csv`, mapa de temporadas |
| 4 | Evidencia y confianza | Casos pasados parecidos (ej. minifalda, rosa) y qué pasó; nivel de confianza con su explicación | `casos_resumen.csv`, `backtest_resumen.md` |
| 5 | Cómo se calculó | Fuentes, método y límites en lenguaje simple; cuánto acertamos antes | `proceso_y_criterios.md` |
| 6 | Mi paleta / exportar | Armar y guardar la selección de la marca | — |

Para validar: no usamos entrevistas. Todo se valida con datos reales de la web y con historia: el backtest de temporadas pasadas (`backtest_resumen.md`), los casos reales (`casos_resumen.md`) y la validación de Gemini contra etiquetado humano (`validacion_gemini_resumen.md`).
