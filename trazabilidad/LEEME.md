# De dónde sale cada número de la página

Respuesta a la devolución de la Entrega 3 (Rigor): "cada número en pantalla tiene que poder explicarse y replicarse desde los datasets".

## Cómo replicarlo

```bash
python3 trazabilidad/verificar_numeros.py
```

El script **no usa** los JSON de la app ni los `*_detalle.csv` de los análisis. Parte de los CSV crudos de Google Trends y de la clasificación de Gemini (una fila por look), aplica las reglas escritas antes de bajar los datos y compara cada resultado con lo que muestra la página (`prototipo/datos.json` y el texto de `prototipo/index.html`).

Genera dos archivos:
- `numeros_de_la_pagina.csv`: una fila por número, con el valor en la página, el recalculado, si coincide, el archivo crudo del que sale y el cálculo.
- `salida_verificacion.txt`: el resumen.

**Resultado: 574 chequeos, 569 coinciden.** Los 5 que no coinciden se explican más abajo.

## Los números, uno por uno

### 1. Las tendencias con veredicto (las tarjetas)
**Fuente cruda:** Google Trends mensual, búsqueda web, todo el mundo. Un CSV por temporada:

| Temporada | Archivo de búsquedas | Archivo de tendencias |
|---|---|---|
| SS2024 y FW2024 | `analisis/brief_2026/datos/trends_2024_web.csv` | `analisis/brief_2026/terminos_declarados_2024.csv` |
| SS2025 | `analisis/brief_2025/datos/trends_A_2011_2025-09.csv` | `analisis/brief_2025/terminos_declarados_2025.csv` |
| FW2025 | `trends_A` más `trends_B` de `analisis/brief_fw2025/datos/` | `analisis/brief_fw2025/terminos_declarados_fw2025.csv` |

Los archivos de tendencias dicen qué medio nombró cada una y con qué término se buscó en Google.

FW2025 usa dos descargas: la A hasta septiembre de 2025 y la B desde octubre, llevada a la escala de la A. El empalme está fijado en la regla, no se decidió después.

| En la página | Cálculo |
|---|---|
| "Se buscó X% más/menos" | B1/B0 − 1. B0 es el promedio de los 12 meses antes del desfile y B1 el de los 12 meses desde el desfile. |
| "Las demás tendencias de la temporada, Y%" | La mediana de log(B1/B0) de todas las tendencias de esa temporada. Da +11% en SS2024, +19% en FW2024, +23% en SS2025 y +34% en FW2025. |
| Veredicto | g1 = log(B1/B0) − la mediana de la temporada.<br>Si g1 ≥ +0,10, se queda.<br>Si g1 ≤ −0,10, en riesgo.<br>En el medio, sin señal clara. |
| Confianza | Alta si \|g1\| ≥ 0,30. Media si no. |
| La curva | Los 24 valores mensuales tal como los da Google Trends. |
| Totales | 77 tendencias: 45 con veredicto (23 se quedan y 22 en riesgo) y 32 sin señal. Ninguna se descartó por volumen. |

**Reglas firmadas antes de bajar los datos:**
- `analisis/brief_2026/REGLAS_BRIEF_2024.txt`
- `analisis/brief_2025/REGLAS_BRIEF_2025.txt`
- `analisis/brief_fw2025/REGLAS_BRIEF_FW2025.txt`

Cada una tiene su huella sha256 en un archivo `SHA256_*.txt` de la misma carpeta.

### 2. La evidencia ("9 de cada 10", "2 de 19 contra 9 de 16")
**Fuente cruda:** las búsquedas de 178 tendencias de 2016 a 2024, en tres muestras:
- **M1:** 68 tendencias de Who What Wear. Búsquedas en `analisis/microtendencias/datos/trends_microtendencias_web.csv`.
- **M2:** 54 de Sandra's Closet. Búsquedas en `analisis/microtendencias/datos/trends_microtendencias_web_m2.csv`.
- **C1:** 56 de 2016 a 2018. Búsquedas en `analisis/hipotesis/datos/trends_c1_web.csv`.

| En la página | Cálculo |
|---|---|
| Grupo de cada tendencia (sube, plana o baja) | Igual que el veredicto, con 36 meses: el año antes, el primero y el segundo. |
| Se quedó | El segundo año, descontando la mediana de su temporada, no cayó más de 10%. |
| 9 de cada 10 | De las 50 que subieron, 45 se quedaron (90%). |
| 2 de 19 contra 9 de 16 | Ciclos 2021-2022, 2022-2023 y 2023-2024: las que subieron contra las que bajaron. |
| "Unas 5 veces más" | (9/16) / (2/19) = 5,3. |
| 1 de 17 | La prueba con datos nuevos (C1): de las 17 que subieron, 1 fue pasajera. |
| 73% contra 88% | Solo M1 y M2, las 122 tendencias de donde salió la idea. Con las 178 da 76% contra 90%. |
| Gráfico ciclo por ciclo | Las mismas cuentas, por año de la temporada. La línea del 20% es el peor ciclo de las que suben: 1 de 5. |

### 3. Los colores de la pasarela
**Fuente cruda:** `datasets_procesados/resultados_gemini.csv`. Son 2.430 looks de 15 casas de Vogue Runway; Gemini clasificó cada look por color dominante, prenda, silueta y largo.

| En la página | Cálculo |
|---|---|
| "1 de cada N looks" | 100 / (% de looks con ese color dominante, promedio de SS2023, FW2023 y SS2024). |
| ↑ / ↓ | Ese promedio contra el de FW2021, SS2022 y FW2022. |

**Qué tan confiable es Gemini:** se revisaron a mano 40 fotos (`analisis/validacion_gemini_muestra.csv`). Coincidió en:
- color, 33 de 40;
- largo, 36 de 40;
- prenda, 28 de 40;
- silueta, 23 de 40.

Por eso la página usa solo el color.

### 4. El método ("7 de 14", "2.430 looks")
- **2.430 looks:** las filas de `resultados_gemini.csv`, todas sin error.
- **7 de 14:** es la prueba de la Entrega 2 (¿la pasarela anticipa las búsquedas?). Sale de `analisis/chequeo_adelante.csv`, la cuenta de `acierta = si`. Es el único número que **no se puede rehacer desde lo crudo**: los CSV de Trends de esa prueba no están en el repo.

## Lo que no coincide (y qué hacemos)

1. **"1 de cada N looks" en 5 colores** (Gris, Naranja, Verde, Azul y Metalizado) está corrido en 1 o 2.
   - **Por qué:** la página divide por el porcentaje ya redondeado a un decimal. Por ejemplo, Gris: 100 / 7,4 = 14, cuando el porcentaje exacto da 13.
   - **Cómo se arregla:** calcularlo con el porcentaje sin redondear en `prototipo/armar_datos.py`.
2. **"73% contra 88%"** coincide, pero hay que aclarar que son 122 tendencias (M1 + M2) y no las 178 del resto de la página.
3. **"7 de 14"** se puede rehacer desde el CSV intermedio, pero no desde lo crudo. Hay que bajar de nuevo esas búsquedas o sacarlo de la página.

## Datos que juntamos y la página no usa

Lo que muestra la página sale de una parte chica de los datasets: Google Trends de las tendencias y la clasificación de Gemini. Esto quedó afuera:

| Dataset | Qué es | Posible uso |
|---|---|---|
| `datasets/prensa_argentina/` (83 notas) | Notas de prensa argentina sobre tendencias, con fecha y etiquetas | Cuántos días tarda la prensa local en hablar de una tendencia después del desfile. Es lo más cercano a la decisión de la marca argentina. |
| Google Trends **Argentina** (`analisis/persistencia/`) | Las mismas búsquedas, en Argentina | Cuánto tarda en llegar a Argentina lo que se busca en el mundo. Con la regla tal cual no se confirmó, y la página lo dice. |
| Google **Shopping** (`trends_microtendencias_shopping.csv`, `persistencia/`) | Búsquedas con intención de compra | Ver si el veredicto se repite en Shopping, para separar interés de compra. |
| Gemini: prenda, silueta, largo | Ya clasificado | Poco confiable (ver la validación). Mejor no mostrarlo, o mostrarlo con la validación al lado. |
| `datasets/trends_marcas/`, `analisis/lyst_*` | Búsquedas de marcas y el ranking Lyst | Contexto de qué casas pesan más; no cambia veredictos. |
| `datasets/trends_casos/` | Triple S, rosa Barbie, minifalda Miu Miu | Ejemplos para contar la historia. |
| `datasets/runway_reportes_2025_2026.csv` (110 datos) | Presencia en pasarela según resúmenes públicos de WGSN, T-Fashion y Heuritech | Contexto; no cubre las tendencias con veredicto (ver abajo). |

### Por qué no usamos los reportes de pasarela (WGSN, T-Fashion, Heuritech)

Los datos del archivo no cubren las tendencias que tienen veredicto en la página.

| Temporada | Datos en el archivo | Coinciden con nuestras tendencias |
|---|---|---|
| SS2025 | 4. Azul oscuro, neutros y la cuota de vestidos: categorías amplias. | Ninguna |
| FW2025 | 7. Marrón cacao, tonos oscuros, jeans bootcut, flare y wide-leg. | Ninguna. Wide-leg jeans está en nuestra lista de SS2025, no de FW2025. |
| SS2026, SS2027 | 99 | 2026 no puede llevar veredicto porque Google Trends cambió la forma de medir. Solo serviría para decir "también lo vio otra fuente", no para probar nada. |

Además son resúmenes de terceros, no datos crudos:
- los reportes completos son pagos;
- muchas filas dicen que la fuente no informa contra qué compara el crecimiento.

Por eso el archivo queda en el repo como dato juntado, sin usarse en la página. Ningún número de la página sale de él.
