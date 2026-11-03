# Paleta predictiva — instrucciones para Claude Code

Proyecto de la materia K576 (UdeSA) de Beltrán Martínez, Borja Centeno y Luigi Bonomi. Una web app que arma un brief de las fashion weeks para marcas de ropa argentinas chicas y medianas y les dice qué tendencias tienden a quedarse y cuáles tienen riesgo de ser pasajeras.

## Hipótesis (leer `hipotesis.md` para el detalle)

> Una tendencia de pasarela que gana búsquedas en su primer año rara vez se desploma en el segundo, y las que las pierden tienen más del triple de chances de ser pasajeras.

- Lo que sube se queda: probado con tendencias nuevas de 2016-2018 (1 de 17 pasajeras); en 8 ciclos 2016-2024 nunca más de 20%.
- Lo que cae: los datos de 2021 a 2024 muestran 9 de 16 pasajeras contra 2 de 19 de las que suben.
- Los números salen de `analisis/hipotesis/` y `analisis/microtendencias/`. No inventar ni redondear distinto: usar los de esos archivos.

## Cómo trabajar con Borja

- Español argentino, casual, directo, paso a paso. Poca teoría.
- Si Borja dice "no entendí", hacelo vos en vez de darle instrucciones.
- Nunca ajustar datos ni reglas para que la hipótesis salga bien. Si algo da mal, se dice.
- No tocar `analisis/`, `datasets/` ni `datasets_procesados/` salvo que Borja lo pida.
- No subir nada a GitHub (commit/push) sin que Borja lo pida. Trabajar en una rama, no en `main`.
- Nunca pegar ni subir claves de API.

## El prototipo (Entrega 3: ver `entrega3/`)

- Va en la carpeta `prototipo/`. Ver `prototipo/README.md` para el brief y cómo seguir.
- **El diseño que se edita es el editorial (`prototipo/index.html`).** `prototipo/wrapped.html` es la alternativa descartada: no tocarla.
- Se trabaja en la rama `entrega-3`. Online: https://paleta-predictiva.netlify.app, abierta y con fotos (decisión de Borja). No se actualiza sola con el push: se publica con `sh prototipo/publicar.sh` (lo de GitHub más las fotos locales). Pasar a `main` solo cuando el diseño esté terminado y Borja lo pida.
- La página actual (`app/index.html`) es la versión "informe": sirve como base de datos y textos, no como diseño final.
- Los datos listos para usar:
  - `app/datos/brief_temporada.json` (**el brief principal**): 31 tendencias puntuales de SS2024 y FW2024 con veredicto, confianza, aviso y curva (`items`), más 36 de SS2026 y FW2026 sin veredicto, como "lo que se vio" (`vistas_2026`). Detalle en `analisis/brief_2026/LEEME.md`.
  - `app/datos/brief_ss2025.json`: 26 tendencias de SS2025 con veredicto (pasaron el chequeo de `analisis/brief_2025/`), con la nota de las que cambian sin ago-sep 2025.
  - `app/datos/brief_fw2025.json`: 20 tendencias de FW2025 con veredicto (pasaron el chequeo más estricto de `analisis/brief_fw2025/`), con la nota de las que cambian con solo mar-jul 2025. Si no pasara, no va a la página.
  - `prototipo/armar_datos.py` junta todo en `prototipo/datos.js` (página) y `prototipo/datos.json` (lo lee la IA).
  - `app/datos/microtendencias.json`: las 178 tendencias de la prueba con su curva, grupo y si se quedó (para la pantalla de evidencia).
  - `app/datos/brief.json`: colores, prendas y largos amplios. Solo 3 de 21 tienen veredicto; sirve para la paleta de colores y los hex, no para veredictos.
- Desde mediados de 2025 Google Trends mide distinto (salto de 3 a 4 veces en feb-may 2026, distinto en cada término). Nunca mostrar veredicto para 2026 ni medir el segundo año de 2024-2025 con Google: se probó y no se puede.
- La IA: `netlify/functions/lectura.mjs` (Groq, clave en la variable `GROQ_API_KEY` de Netlify) y su prompt en `netlify/functions/prompt.mjs`. Documentado en `entrega3/IA.md`. La IA no calcula ni cambia veredictos.
- Para verla: abrir el HTML en el panel de navegador de la app (o `python3 -m http.server` desde la raíz y entrar a `http://localhost:8000/prototipo/`).
- Pedido de los profes en la Entrega 2: interfaz más visual, criterios de la IA y niveles de confianza explícitos, y alternativas de diseño (Figma).
- Referencias de diseño elegidas por el grupo: The Lyst Index, Spotify Wrapped, TradingView y Pantone Color of the Year.

## Mapa del repo

| Carpeta / archivo | Qué hay |
|---|---|
| `hipotesis.md` | Hipótesis, definiciones, resultados y límites |
| `readme.md` | Resumen del proyecto y lista completa de datasets con fuentes |
| `app/` | Página actual y scripts que arman sus datos (`armar_datos.py`, `armar_microtendencias.py`) |
| `prototipo/` | La app (publicada en Netlify) |
| `netlify/`, `netlify.toml` | Función de la IA y configuración de Netlify |
| `entrega3/` | Documentación de la Entrega 3 (IA, diseño, guion) |
| `analisis/` | Pruebas, reglas (`REGLAS_*.txt`) y salidas |
| `datasets/`, `datasets_procesados/` | Datos de entrada |
| `decisiones.md` | Registro de decisiones con fecha |
