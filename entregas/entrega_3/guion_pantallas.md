# Guion de pantallas (para armar en Figma: 2-3 alternativas por pantalla)

Principio de los docentes: **la plataforma tiene que ser visual, no textual**. Cada tendencia se muestra con imagen de silueta/look, no solo con nombre.

| # | Pantalla | Qué se ve | Datos que la alimentan |
|---|---|---|---|
| 1 | Inicio / elegir marca y temporada | Marca (rubro, rango de precio), temporada argentina objetivo | Perfil cargado por la marca |
| 2 | Brief de la temporada | **Máximo 5 tendencias**, cada una con foto de looks reales, paleta de colores y largo | `participacion_por_temporada.csv`, fotos de la muestra |
| 3 | Detalle de una tendencia | Foto de pasarela + curva de búsquedas + "la temporada argentina arranca acá (+12 meses)" | `trends_unificado.csv`, mapa de temporadas |
| 4 | Evidencia y confianza | Casos pasados parecidos (ej. minifalda, rosa) y qué pasó; nivel de confianza con su explicación | `casos_resumen.csv`, `backtest_resumen.md` |
| 5 | Cómo se calculó | Fuentes, método y límites en lenguaje simple; cuánto acertamos antes | `proceso_y_criterios.md` |
| 6 | Mi paleta / exportar | Armar y guardar la selección de la marca | — |

Para validar (pedido de los docentes): hablar con **2 o más** marcas locales o coolhunters y preguntarles qué decisión toman hoy con esta información, qué usan y cuánto pagan. Guardar las respuestas en `entregas/entrega_3/entrevistas.md`.
