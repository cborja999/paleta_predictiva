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

## El prototipo (tarea actual)

- Va en la carpeta `prototipo/`. Ver `prototipo/README.md` para el brief.
- La página actual (`app/index.html`) es la versión "informe": sirve como base de datos y textos, no como diseño final.
- Los datos listos para usar están en `app/datos/brief.json` (colores, prendas y largos con su lectura de búsquedas) y `app/datos/microtendencias.json` (las 178 tendencias con su curva, grupo y si se quedó).
- Para verla: abrir el HTML en el panel de navegador de la app (o `python3 -m http.server` desde la raíz y entrar a `http://localhost:8000/prototipo/`).
- Pedido de los profes en la Entrega 2: interfaz más visual, criterios de la IA y niveles de confianza explícitos, y alternativas de diseño (Figma).
- Referencias de diseño elegidas por el grupo: The Lyst Index, Spotify Wrapped, TradingView y Pantone Color of the Year.

## Mapa del repo

| Carpeta / archivo | Qué hay |
|---|---|
| `hipotesis.md` | Hipótesis, definiciones, resultados y límites |
| `readme.md` | Resumen del proyecto y lista completa de datasets con fuentes |
| `app/` | Página actual y scripts que arman sus datos (`armar_datos.py`, `armar_microtendencias.py`) |
| `prototipo/` | El prototipo nuevo |
| `analisis/` | Pruebas, reglas (`REGLAS_*.txt`) y salidas |
| `datasets/`, `datasets_procesados/` | Datos de entrada |
| `decisiones.md` | Registro de decisiones con fecha |
