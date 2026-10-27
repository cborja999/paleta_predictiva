# Diagnóstico de los datos de Google Trends 2025-2026 (27/10/2026)

Al aplicar `REGLAS_BRIEF_2026.txt` a 36 tendencias de SS2026 y FW2026 (datos en `datos/trends_2026_web.csv`, bajados el 27/10/2026, checksum verificado) apareció un problema de medición:

- Entre febrero y mayo de 2026 las 36 búsquedas, que no tienen relación entre sí, se multiplican a la vez: en la mediana, entre 3 y 5 veces su nivel de 2024; en algunos términos, más de 20 veces. Desde agosto de 2025 ya hay una suba general menor (entre 1,3 y 1,6 veces).
- El salto es más grande cuanto menos búsquedas tenía el término (Spearman −0,84 entre el nivel de 2024 y el tamaño del salto).
- El veredicto de cada tendencia queda explicado casi entero por ese salto: Spearman 0,96 (SS2026) y 0,92 (FW2026) entre g1 y el tamaño del salto feb-may 2026.
- El mismo salto aparece en datos semanales, en Estados Unidos y en Google Shopping: es de la fuente, no de nuestra consulta.

Conclusión: con Google Trends, las comparaciones entre antes y después de mediados de 2025 favorecen a los términos de poco volumen. La lectura de SS2026 y FW2026 con estas reglas **no se usa ni se congela**. Los datos de la hipótesis (hasta diciembre de 2024) no están afectados.
