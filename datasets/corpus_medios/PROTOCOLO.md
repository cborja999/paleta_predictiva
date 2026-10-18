# Corpus de medios y marcas: protocolo de carga (piloto)

**Para qué:** tener una segunda medida de "repercusión" (cuántas piezas de prensa y de marcas mencionan un color, y cuándo) y cubrir Argentina, donde no tenemos datos. No es "entrenar" un modelo: es un dataset hecho a mano con un método fijo.

**Pregunta del piloto (fijada antes de cargar):** los colores que ganan presencia en pasarela (señal Alta o Media del backtest) ¿aparecen más en prensa y marcas en los 6 a 18 meses siguientes que los demás colores?
**Cómo se mide:** para cada color y mes, porcentaje de piezas del mes que lo mencionan. Se compara el grupo "ganó presencia en pasarela" contra el resto, relativo al mes. Se reporta el resultado sea cual sea, junto con cuántas piezas hay.

## Reglas (no se cambian después de cargar)
1. **Lista de fuentes cerrada antes de empezar** (ver `fuentes.md`). No se agregan fuentes si el resultado no gusta.
2. **Muestreo sin mirar el color:** en cada fuente y cada mes, las **primeras 5 piezas** de moda/tendencias que muestra su buscador o archivo ordenado por fecha. Si hay menos de 5, se cargan las que haya. No se eligen piezas por el color que mencionan.
3. **Período del piloto:** enero 2023 a junio 2025 (cubre los desfiles de otoño-invierno 2023 y primavera-verano 2024, y los 12 a 18 meses siguientes).
4. **Qué se guarda:** link, fecha, título y los datos extraídos. **No** se guarda el texto completo ni se copian fotos (derechos de autor y términos de uso). De los videos, solo título, descripción y fecha.
5. **Vocabulario cerrado** para colores, prendas y largos (mismas listas que `datasets_procesados/resultados_gemini.csv`). Un color cuenta solo si la pieza lo presenta como tendencia o como parte del look principal, no por una mención suelta.
6. **Sin scraping automático** de sitios que lo prohíben ni de redes sociales: se carga a mano o con ayuda de IA leyendo páginas públicas.
7. **Dos personas cargan las mismas 20 piezas** al inicio para medir cuánto coinciden (acuerdo mínimo 80%; si no llega, se ajustan las definiciones antes de seguir).

## Columnas de `plantilla_corpus.csv`
`id` | `fuente` | `tipo_fuente` (medio / marca / coolhunter) | `pais` | `url` | `fecha_publicacion` (AAAA-MM-DD) | `titulo` | `tipo_pieza` (nota / reseña de desfile / video / newsletter) | `temporada_referida` (ej. FW2023) | `colores_mencionados` (separados por `;`) | `prendas_mencionadas` | `largos_mencionados` | `presenta_como_novedad` (si/no) | `cargado_por` | `fecha_carga` | `nota`

## Límites que hay que decir
- Muestra chica y no aleatoria de verdad: depende de lo que muestre cada buscador.
- Hay un solo período; los medios repiten el mismo color por cobertura de desfiles, no solo por adopción.
- Que un color aparezca en prensa no significa que se vendió.
