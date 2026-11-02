# Entrega 3: dónde está cada cosa

App online: **(link de Netlify, pendiente)** · Repo: https://github.com/cborja999/paleta_predictiva

## 1. Hipótesis y foco

> Una tendencia de pasarela que gana búsquedas en su primer año rara vez se desploma en el segundo, y las que las pierden tienen más del triple de chances de ser pasajeras.

**Qué cambió y por qué**
1. **Entrega 1:** "la pasarela anticipa las ventas masivas 12 a 18 meses después".
2. **Entrega 2:** lo probamos con 2.430 looks de Vogue Runway clasificados con Gemini contra Google Trends. No apareció ningún desfase: acertaba 7 de 14, como una moneda. Lo presentamos como resultado nulo.
3. **Lo que sí funcionó:** mirar las búsquedas del primer año después del desfile. Lo que sube se queda: lo probamos con tendencias nuevas de 2016 a 2018, con reglas escritas antes de bajar los datos, y solo 1 de 17 fue pasajera. En 8 ciclos de 2016 a 2024 nunca pasó del 20%.
4. **Lo que descartamos:** "lo que queda plano es pasajero". No se sostuvo (las planas se quedan 73%). El riesgo está en lo que cae: de 2021 a 2024, 9 de 16 pasajeras, contra 2 de 19 de las que suben.

**La decisión del usuario.** Una marca argentina chica o mediana no puede ir a las fashion weeks ni pagar forecasting. Con la app decide en qué tendencia apostar fuerte y en cuál probar poco, según su rubro. Antes se guiaba por notas de medios que dicen "esto es tendencia" sin decir si va a durar.

Detalle: `hipotesis.md`. En la app: Método → "Qué cambió y por qué".

## 2. Rigor con los datos

- **Datos de la app:** 77 tendencias que nombraron Who What Wear, CBC Life y Yahoo Lifestyle después de las fashion weeks de primavera 2024, otoño 2024, primavera 2025 y otoño 2025: 45 con veredicto (23 se quedan, 22 en riesgo) y 32 sin señal clara. Además, 36 de 2026 sin veredicto y los colores de la pasarela (15 casas en Vogue Runway, clasificados con Gemini). Las búsquedas son de Google Trends, en todo el mundo, mensuales.
- **Cálculos sobre los datos:** búsquedas del año después del desfile contra el año anterior, descontando la mediana de la temporada. Umbral de ±10% y confianza alta desde ±30%. Las reglas se escribieron y se firmaron con sha256 antes de bajar los datos:
  - `analisis/brief_2026/REGLAS_BRIEF_2024.txt`
  - `analisis/brief_2025/REGLAS_BRIEF_2025.txt`
  - `analisis/brief_fw2025/REGLAS_BRIEF_FW2025.txt` (con un chequeo más estricto; si no pasaba, otoño 2025 no iba a la página)
- **Verificable por el grupo:** cada número sale de un script.
  - `analisis/brief_2026/brief_temporada.py`
  - `analisis/brief_2025/brief_ss2025.py`
  - `analisis/brief_fw2025/brief_fw2025.py`
  - `prototipo/armar_datos.py`
- **Calculado contra IA en la interfaz:** etiqueta **Calculado** (veredictos, confianza, curvas, porcentajes) y etiqueta azul **Inferencia de la IA** (recomendaciones), en bloques separados.
- **Limitaciones** (también en la app, Método → "Lo que no dicen"):
  - búsquedas no son ventas;
  - son búsquedas de todo el mundo, y con Argentina la regla no se confirmó;
  - las listas son de medios en inglés;
  - el segundo año no se puede medir: desde 2025 Google mide distinto y se probó que no se puede corregir;
  - las muestras son chicas;
  - primavera 2025 pasó un chequeo, pero 3 de sus 8 "se queda" dependen de ago-sep 2025, y está marcado;
  - otoño 2025 pasó un chequeo más estricto, pero en 8 de sus 13 veredictos la lectura con solo marzo a julio de 2025 da "sin señal clara", y está marcado.

## 3. Integración de IA

GPT-OSS 120B (modelo abierto de OpenAI) vía la API de Groq, en una función de Netlify. Responde "¿qué hago con esta tendencia en mi marca?". System prompt, contexto que se envía, salida y controles: `entrega3/IA.md`. En la app: botón "Pedir recomendación" en cada tendencia y "Ver qué le pedimos a la IA" en Método.

## 4. Diseño / UX

No hubo Figma: el diseño se hizo en código con un agente de IA (Claude Code), a partir del brief y las referencias. Se hicieron dos alternativas (editorial y Wrapped) y elegimos la editorial. La página abre con un home y un índice por temporada al estilo de las notas de análisis de WGSN (foto del desfile, veredicto y el número en la frase), con dos fotos por tendencia de dos desfiles distintos. Las decisiones de código (el gráfico que muestra lo que compara la regla, estados de carga y error de la IA, responsive, accesibilidad, fotos solo en la presentación) y las capturas están en `entrega3/DISENO.md`.

## 5. Comunicación

Guion de 15 minutos y preguntas probables: `entrega3/GUION.md`.
