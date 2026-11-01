# Entrega 3: guion de 15 minutos y preguntas probables

Antes de la clase:
- tener abierta la app online (link y QR en `entrega3/README.md`);
- pedir una recomendación de prueba, para que la IA no arranque en frío;
- tener a mano la captura `entrega3/capturas/4_editorial_nota.png` por si falla internet.

Los números salen de `hipotesis.md`, `analisis/brief_2026/salida_brief_2024.txt` y `analisis/brief_2025/salida_brief_ss2025.txt`. No los redondeen distinto.

---

## 0:00 a 1:00: el problema

Una marca argentina chica o mediana no puede ir a las fashion weeks ni pagar un servicio de forecasting. Se entera de las tendencias por notas que dicen "esto es tendencia", pero ninguna dice si va a durar. Si produce algo que pasa de moda en seis meses, se queda con el stock.

Paleta predictiva le dice qué tendencias de pasarela tienden a quedarse y cuáles tienen riesgo de ser pasajeras, y qué hacer con cada una en su rubro.

## 1:00 a 3:00: la hipótesis y qué cambió (punto 1)

> Una tendencia de pasarela que gana búsquedas en su primer año rara vez se desploma en el segundo, y las que las pierden tienen más del triple de chances de ser pasajeras.

1. **Entrega 1:** "la pasarela anticipa las ventas 12 a 18 meses después".
2. **Entrega 2:** lo probamos con 2.430 looks de Vogue Runway clasificados con Gemini contra Google Trends. No apareció ningún desfase: acertaba 7 de 14, como tirar una moneda. Lo presentamos como resultado nulo.
3. **Qué aprendimos:** lo que sí sirve es mirar qué pasa con las búsquedas el primer año después del desfile.
   - **Lo que sube se queda.** Lo probamos con tendencias de 2016 a 2018 que no habíamos usado, con las reglas escritas antes de bajar los datos: solo 1 de 17 fue pasajera. En 8 ciclos, de 2016 a 2024, nunca pasó del 20%.
   - **Lo que cae.** De 2021 a 2024, 9 de 16 de las que perdieron búsquedas fueron pasajeras, contra 2 de 19 de las que ganaron.
4. **Lo que descartamos:** "lo que queda plano es pasajero". No se sostuvo.

**Cómo se conecta con el usuario:** con la app, la marca decide en qué tendencia apostar fuerte y en cuál probar poco, que es justo lo que hoy no puede decidir bien.

## 3:00 a 7:00: demo en vivo

1. **Portada.** "Revisamos las 57 tendencias que nombraron Who What Wear, CBC Life y Yahoo Lifestyle. 16 tienden a quedarse y 16 pueden ser moda pasajera." Las otras 25 no dan señal clara y no las mostramos como recomendación.
2. **Rubro.** Elegir "Polleras": la página reordena las tendencias.
3. **Etiquetas.** Mostrar la leyenda: **Calculado** (recuadro negro) contra **Inferencia de la IA** (azul).
4. **Una tendencia que se queda.** Abrir "Pollera balón": +92% de búsquedas el año después del desfile, confianza alta. Mostrar la curva y la línea del desfile.
5. **Pedir recomendación.** Escribir una línea de marca, por ejemplo "Ropa de mujer, vendemos por Instagram". Mostrar:
   - la lectura y las ideas de producto;
   - la apuesta;
   - "Qué le mandamos a la IA", con el JSON exacto.
6. **Una en riesgo.** Abrir una en rojo, por ejemplo "Pantalón cigarette", −46%. La IA solo puede recomendar apuesta baja.
7. **Visto en 2026.** Explicar que hay tendencias sin veredicto y por qué (ver punto 2).
8. **Método.** Ahí están la regla, la evidencia, "Lo que no dicen" y "Ver qué le pedimos a la IA".

Si la IA no responde, decirlo tranquilos: la página lo avisa y los datos calculados siguen valiendo. Mostrar "Qué le mandamos a la IA" y seguir.

## 7:00 a 10:00: rigor con los datos (punto 2)

- **Datasets definitivos:**
  - listas de tendencias de Who What Wear, CBC Life y Yahoo Lifestyle de primavera 2024, otoño 2024 y primavera 2025;
  - Google Trends mundial y mensual.
- **El cálculo, sobre los datos:** búsquedas del año después del desfile contra el año anterior, descontando lo que se movió el resto de la temporada (la mediana).
  - "Se queda" desde +10%; "en riesgo" desde −10%.
  - Confianza alta desde ±30%.
- **Verificable:** las reglas se escribieron y se firmaron con sha256 antes de bajar los datos, y cada número sale de un script (`brief_temporada.py`, `brief_ss2025.py`, `armar_datos.py`).
- **Lo que encontramos y lo que hicimos con eso:**
  - **El problema de Google.** Desde mediados de 2025 Google Trends mide distinto: en feb-may 2026 todas las búsquedas saltan entre 3 y 4 veces, y distinto en cada término.
  - **2026 va sin veredicto.** Se muestra como "visto en pasarela".
  - **Primavera 2025 tuvo que pasar un chequeo fijado de antemano.** El veredicto no puede depender del volumen del término, ni de cuánto se infló en 2026, ni del cambio de enero de 2025. Pasó (los tres por debajo de 0,5): 8 se quedan, 5 en riesgo, 13 sin señal.
  - **Primavera 2025 tiene un cuidado.** Tres de sus "se queda" dependen de agosto y septiembre de 2025, y la app lo avisa en cada una.
  - **El segundo año no se puede medir.** Probamos corregir el salto de 2026 por volumen y no alcanza: la dispersión es 3,2 veces la de un año limpio. Todavía no sabemos si las tendencias de 2024 y 2025 se quedaron.
- **Limitaciones** (en la app, Método → "Lo que no dicen"):
  - búsquedas no son ventas;
  - es todo el mundo: con búsquedas solo de Argentina la regla no se confirmó;
  - los medios son en inglés;
  - las muestras son chicas.

## 10:00 a 12:30: la IA (punto 3)

- **Modelo:** GPT-OSS 120B, un modelo abierto de OpenAI, vía la API de Groq, en una función de Netlify. La clave está en el servidor, nunca en el navegador ni en el repo.
- **Qué pregunta responde:** "¿qué hago con esta tendencia en mi marca?".
- **Qué le mandamos:** el navegador manda solo el id de la tendencia, el rubro y la descripción de la marca. Los datos los agrega el servidor, desde los mismos archivos que la página, así que nadie le puede mandar datos inventados.
- **Qué le pedimos:** un JSON con la lectura, qué haría una marca de ese rubro, tres ideas, la apuesta, por qué y el cuidado principal.
- **Límites:**
  - no cambia veredictos;
  - no puede inventar números: un control compara cada número de la respuesta con los datos; si aparece uno nuevo, le pide que corrija una vez, y si sigue, lo marca en amarillo;
  - la apuesta la acota el código según el veredicto;
  - ignora instrucciones que vengan en la descripción de la marca.
- Mostrar el system prompt en la app (Método → "Ver qué le pedimos a la IA") o en `entrega3/IA.md`.

## 12:30 a 14:30: diseño (punto 4)

- **No hubo Figma: diseñamos en código con un agente de IA (Claude Code).** Lo decidimos así porque cada pantalla dependía de datos reales (curvas, veredictos, estados de la IA) y en código lo podíamos probar con esos datos desde el primer día.
- **Partimos de:**
  - el brief (para quién, qué preguntas tiene que responder);
  - las referencias: Lyst Index, Spotify Wrapped, TradingView y Pantone;
  - el pedido de la Entrega 2: más visual, confianza a la vista, alternativas.
- **Dos alternativas:** editorial y Wrapped (capturas 1 y 5). Elegimos la editorial porque entraban el método, los límites y la IA sin cortar el relato.
- **Decisiones que tomamos en código:**
  - **Láminas en lugar de fotos.** Las fotos de pasarela no se pueden publicar, así que el dato es la imagen: el porcentaje grande y la curva.
  - **Rojo solo para el riesgo, y sin verde**, para que "se queda" no se lea como "comprá".
  - **Estados de la IA:** cargando, error, sin servidor y control de números.
  - **Responsive** a 390 px y **accesibilidad**.
- **Contra la Entrega 2** (captura 6): antes había 21 categorías amplias con 3 veredictos; ahora son tendencias puntuales con veredicto y confianza, y la IA está adentro de la app.

Detalle en `entrega3/DISENO.md`.

## 14:30 a 15:00: cierre

La app no le dice a la marca qué está de moda; le dice qué tiene más chances de durar y cuánto apostar, con los datos y los límites a la vista. Repo: https://github.com/cborja999/paleta_predictiva

---

## Preguntas probables (las tenemos que poder contestar los tres)

**¿Por qué Google Trends y no ventas?**
No hay datos públicos de ventas de ropa en Argentina. Las búsquedas miden interés, no ventas, y eso lo decimos en la app.

**¿Qué es "descontando la temporada"?**
A cada tendencia le restamos la mediana de cómo se movieron todas las tendencias de esa temporada. Así, si Google sube para todos, no cuenta como que la tendencia creció.

**¿Por qué ±10% y ±30%?**
Son los mismos umbrales de la prueba de la hipótesis. Se fijaron antes de bajar los datos y no se cambiaron después.

**¿Cómo saben que no ajustaron las reglas para que dé bien?**
Cada archivo de reglas tiene su huella sha256 con fecha, anterior a la bajada de datos. Cuando algo dio mal (el desfase de la Entrega 2, lo plano, 2026) lo dijimos.

**¿Por qué 2026 no tiene veredicto?**
Desde mediados de 2025 Google mide distinto. En feb-may 2026 todos los términos saltan a la vez, y en 2026 el veredicto quedaba explicado por ese salto (Spearman 0,92 y 0,96). Ver `analisis/brief_2026/DIAGNOSTICO_2026.md`.

**¿Y primavera 2025, que también toca 2025?**
Antes de mirar los datos escribimos tres chequeos. El veredicto no podía depender del volumen del término, ni de cuánto se infló en 2026, ni del cambio de enero de 2025. Los tres dieron por debajo del límite (0,5). Igual, tres de sus "se queda" cambian si sacamos agosto y septiembre de 2025, y la app lo marca.

**¿Saben si las tendencias se quedaron?**
Todavía no. El segundo año cae entero en el período en que Google mide distinto. Probamos corregirlo por volumen y no alcanza. Lo decimos en la app.

**¿Por qué la IA no calcula el veredicto?**
Porque un modelo de lenguaje puede inventar. El veredicto es una cuenta con reglas fijas; la IA solo lo traduce a una recomendación para el rubro, y la interfaz separa las dos cosas.

**¿Cómo evitan que la IA invente?**
El servidor compara cada número de la respuesta con los de los datos. Si hay uno nuevo, le pide que corrija; si sigue, lo marca en amarillo. La apuesta la limita el código.

**¿Por qué Groq y GPT-OSS 120B?**
Groq es rápido y tiene capa gratuita. Empezamos con Llama 3.3 70B, pero Groq lo apagó en agosto de 2026 y recomienda GPT-OSS 120B como reemplazo: es abierto, responde bien en español y devuelve JSON. Le pedimos razonamiento corto para que conteste rápido. El modelo se cambia con una variable, sin tocar código.

**¿Qué pasa si alguien escribe instrucciones en la descripción de la marca?**
Se recorta a 280 caracteres y el prompt le dice a la IA que la tome solo como contexto. Igual, la apuesta y los números los controla el código, no la IA.

**¿Por qué no hay Figma?**
Diseñamos directamente en código con un agente de IA, porque las pantallas dependían de datos reales. Las alternativas, las decisiones y las diferencias están documentadas con capturas en `entrega3/DISENO.md`.

**¿Por qué no hay fotos de los desfiles?**
Las fotos de Vogue Runway tienen derechos y no se pueden publicar. Las reemplazamos por la curva de búsquedas.

**¿Funciona para Argentina?**
Con búsquedas solo de Argentina la regla no se confirmó. Argentina se mueve casi a la par que el mundo, así que usamos datos mundiales y lo aclaramos.

**¿Qué haría distinto con más tiempo?**
Medir el segundo año cuando Google se estabilice, sumar más medios y validar con datos de ventas si alguna marca nos los presta.
