# Paleta predictiva: paquete completo para arrancar una conversación nueva

Fecha del paquete: 20/10/2026. Autor del proyecto: Borja Centeno (grupo con Beltrán Martínez y Luigi Bonomi). Materia K576 "Sistemas generativos e IA para Diseño", Universidad de San Andrés (UdeSA).

Este archivo es el punto de entrada. Si sos una IA que recibe esta carpeta sin contexto previo: leé este archivo entero, después **`hipotesis.md`** (la hipótesis actual), `analisis/persistencia/resumen.md` y `decisiones.md`, y recién ahí preguntale a Borja qué necesita.

## 1. Qué es el proyecto

"Paleta predictiva" es una web app que arma un **brief de tendencias de las fashion weeks** (colores, prendas y largos) y dice **qué se queda y qué es moda pasajera**, para vender a marcas de indumentaria argentinas chicas y medianas que no pueden ir a fashion weeks ni pagar un servicio de forecasting.

## 2. Hipótesis actual (20/10/2026, tarde) — leer `hipotesis.md`

**"Una tendencia de pasarela que gana búsquedas en su primer año rara vez se desploma en el segundo."** Se confirma en parte: en datos nuevos de 2016-2018 solo 1 de 17 de las que subieron fue pasajera (6%); en 8 ciclos nunca pasó de 20%. La parte secundaria (las que caen tienen el triple de chances) no se confirmó en 2016-2018. Lo que sigue abajo es el camino anterior.

## 2b. Cómo cambió la hipótesis (importante para no repetir caminos)

1. **Hipótesis original (agosto 2026):** la pasarela anticipa lo más vendido en retail masivo con 12 a 18 meses de desfasaje. **No se sostuvo**: la pasarela sola acierta 51% (azar). Se presentó como resultado nulo, sin forzar nada.
2. **Hipótesis actual (19-20/10/2026):** los colores, prendas y largos cuyas **búsquedas en Google ganan interés** tienden a **quedarse** más que los que no se movieron.
   - Mundo: **84% contra 70% (+14 puntos)** con el test limpio, en las dos familias de términos (p=0,001 y p=0,003).
   - Argentina (búsquedas generales y Shopping): **no se sostiene** (67% contra 73%; 69% contra 76%).
   - **No hay retraso de 12 a 18 meses** entre el mundo y Argentina: se mueven casi a la par.
3. **Reencuadre del 20/10/2026 (mediodía):** como Argentina se mueve a la par que el mundo, la página es un brief de fashion weeks con lectura de búsquedas globales, **pensado para marcas argentinas pero sin decir que está validado en Argentina**. La prensa argentina sale de la señal (queda como contexto). Las notas argentinas se arman a partir de informes de las fashion weeks, no de lo que se usa acá, así que mirar el mundo es equivalente.
4. **Pedido del profesor (20/10/2026):** le interesó el proyecto y pidió replicar con 2022-2023, para que no sea solo 2023-2024. Se hizo (ver abajo).

## 3. Resultados actuales (todos con reglas escritas antes de correr)

| Qué | Resultado |
|---|---|
| Persistencia en búsquedas, mundo (limpio) | 84% vs 70%, +14 pts, en las dos familias |
| Persistencia en Argentina / Shopping Argentina | 67% vs 73% / 69% vs 76%: no se sostiene |
| Retraso Argentina vs mundo | No hay a 12-18 meses |
| Pasarela -> búsquedas | 51%, azar. Queda como contexto visual |
| Réplica ciclo principal oct-2022 | Mixto: a favor en forma 2 del mundo (67% vs 31%, p=0,12), en contra en forma 1 (40% vs 60%) |
| Réplica sumando oct-2022, 2021 y 2020 | A favor en el mundo (60% vs 40%, p=0,20; 61% vs 36%, p=0,04); en Argentina no aparece (44% vs 56%) |
| Pasarela agregada a búsquedas que suben | 73% vs 52% y 77% vs 47%: va en la dirección esperada, no se distingue del azar |
| Prensa internacional 2022 (15 notas) | Parece a favor (67% vs 17%, p=0,06) pero **se da vuelta** al sacar 2 notas (43% vs 57%). No robusta |
| Prensa argentina 2021-2022 | No evaluable: no hay notas suficientes |
| Ciclo oct-2023 | No evaluable limpio: su resultado cae en 2025, cuando Google cambió cómo mide |

**Predicción congelada:** `analisis/persistencia/prediccion_congelada_2026-10-19.csv` (63 filas, tres familias: original, nueva y Argentina), huella sha256 `3b022ec2c78b9f93…` en `SHA256_prediccion_congelada.txt`. Chequeo principal en **octubre de 2028**, intermedio exploratorio en octubre de 2027. En Argentina no se ofrece nivel de confianza.

## 4. Cómo se mide (para no confundirse)

- Ventana limpia de Google Trends: datos hasta dic-2024.
- Inercia = log(promedio meses d-12..d-1 / promedio d-24..d-13), menos la mediana de la familia. "Sube" si > 0. "Ganó interés" si ≥ +0,10; "perdió" si ≤ -0,10.
- Resultado = log(promedio d+12..d+23 / promedio d-12..d-1), menos la mediana de la familia. "Sube" si > 0.
- Dos **familias de términos del mundo**: "nueva" (ej. gray dress) y "original" (ej. gray outfit). En la página son "Forma 1" y "Forma 2". El veredicto exige que las dos coincidan.
- Confianza Alta/Media/Baja = terciles de |inercia| por familia.
- Señal de pasarela en la página: promedio de participación en las 3 temporadas recientes menos las 3 anteriores; "sube" si la diferencia es ≥ 1,0 punto.
- Tests: Fisher exacto, dos colas. Pares de un mismo ciclo no son independientes.

## 5. Reglas de trabajo de Borja (respetarlas siempre)

- **Honestidad ante todo:** no ajustar datos ni reglas para forzar que la hipótesis salga. Si da mal, se informa.
- **Las reglas se escriben ANTES de correr cada prueba** (`REGLAS_*.txt`) y no se cambian después.
- Nada de entrevistas: la validación es con datos históricos de la web.
- No decir que algo está validado en Argentina.
- Nunca pegar ni mostrar claves de API (Gemini u otras).
- Pedir permiso antes de descargar archivos o publicar. No subir nada a GitHub sin que Borja diga explícitamente "subila".
- Estilo: español argentino casual, directo, paso a paso, poca teoría. Si Borja dice "no entendí", hacerlo uno mismo en vez de dar instrucciones.

## 6. Mapa de carpetas

| Carpeta o archivo | Qué hay |
|---|---|
| `01_PROMPT_PARA_ARRANCAR.md` | Texto para pegar al empezar la conversación nueva |
| `readme.md` | Readme del proyecto (hipótesis, fuentes, resultados por etapa) |
| `decisiones.md` | Registro cronológico de decisiones. Leer entero |
| `analisis/persistencia/` | **El corazón de la hipótesis actual.** `resumen.md`, todos los `REGLAS_*.txt`, scripts, salidas `salida_*.txt`, predicción congelada, `datos/` con Trends del mundo, Argentina y Shopping Argentina |
| `analisis/` (resto) | Etapa anterior (pasarela vs búsquedas): `participacion_por_temporada.csv` (la que usa la página), `color_real_por_categoria.csv/.py` (colores medidos), backtest, casos, Lyst, marcas |
| `datasets/trends/`, `trends_casos/`, `trends_marcas/` | Google Trends de etapas anteriores |
| `datasets/prensa_argentina/` | Planilla de 83 notas cargadas por el grupo + `README.md` con problemas de carga. Contexto secundario |
| `datasets/prensa_internacional/` | 15 notas de 2022 con etiquetas automáticas + README |
| `datasets/fuentes_candidatas.md` | Relevamiento de datasets posibles para validar con ventas o demanda |
| `datasets/diccionario.md` | Diccionario de categorías (colores, prendas, largos) |
| `datasets/corpus_medios/` | Protocolo del corpus de medios (piloto) |
| `datasets_procesados/resultados_gemini.csv` | 2.430 fotos de Vogue Runway clasificadas por Gemini (color, prenda, silueta, largo) |
| `app/` | La página: `plantilla.html`, `armar_datos.py` (arma `datos/brief.json` y mete todo en `index.html`), `index.html` (abre con doble clic) |
| `runway_gemini/` | Scripts para bajar fotos y clasificar con Gemini (necesita `GEMINI_API_KEY` propia) |
| `entregas/entrega_3/` | Respuesta a la devolución de los docentes, proceso y criterios, guion de pantallas |

## 7. Cómo correr las cosas

Desde la carpeta correspondiente, con Python 3 (pandas, numpy, scipy; Pillow para colores):

```
cd analisis/persistencia
python3 -I replica_ciclos.py                 # réplica 2022-2023, 2021, 2020
python3 -I prensa_internacional_2022.py      # cruce prensa internacional + búsquedas
cd ../../app
python3 armar_datos.py                       # regenera datos/brief.json e index.html
```

Verificado el 20/10/2026: `replica_ciclos.py` y `prensa_internacional_2022.py` dan salidas idénticas a las guardadas (`salida_*.txt`) dentro de este paquete.

## 8. Qué NO está en este paquete

- **Las fotos de Vogue Runway** (1.205 usadas para los colores medidos; derechos y tamaño). Están en la Mac de Borja en `UDESA/Sistemas generativos/runway_gemini/`. `runway_gemini/bajar_fotos_vogue.py` las vuelve a bajar.
- **Datos crudos del Lyst Index** (`datasets/lyst/`): Lyst no permite redistribuir el informe. Se dejaron afuera a propósito.
- **La planilla viva de prensa del grupo** (Google Sheets) y el Doc "Cómo funciona Paleta predictiva" (https://claude.ai/code/artifact/2ee6c457-20cd-4c65-9d96-a5cc3cabd123), que **tiene números viejos** (88-91%, "12 meses", "marca de ejemplo") y no refleja el reencuadre.
- Claves de API: nunca estuvieron ni deben estar en la carpeta.
- El Excel de Kaggle `fashion_data_2018_2022.xls`: se detectó como datos sintéticos y se descartó.

## 9. Pendientes conocidos

- Decidir con Borja cuál es el **próximo entregable** concreto (no está definido en estos archivos) y armar el trabajo.
- Actualizar el Doc "Cómo funciona Paleta predictiva" (números del test limpio, chequeo en oct-2028/oct-2027, sacar "marca de ejemplo", reflejar el reencuadre a fashion weeks).
- Rama `pagina-prototipo` de GitHub: la página, la réplica, la prensa internacional, los colores medidos y `fuentes_candidatas.md` están solo en commits locales, **sin subir**. `main` llega hasta la prueba de Argentina y la prensa argentina. Beltrán y Luigi no los ven hasta que Borja diga "subila".
- Validar con ventas o demanda real: pedir Visuelle 2.0 (formulario), cuenta de Kaggle para H&M. Ver `datasets/fuentes_candidatas.md`.
- Corregir errores de la planilla de prensa argentina (hoy solo contexto).
- Opcionales: volver a poner un chip exploratorio de Argentina en las tarjetas, cruzar con el reporte Pantone, actualizar Figma, decidir derechos de las fotos y de los hex.

## 10. Límites a decir siempre

- Google Trends mide **búsquedas, no ventas**. No hay datos públicos de ventas argentinas por color o prenda.
- Entre 20 y 27 temporadas; las categorías de una temporada no son independientes.
- Etiquetas de Gemini: largo 90%, color 82%, prenda 70%, silueta 58% de acierto en 40 fotos validadas. Silueta no se presenta como dato duro.
- Etiquetas de prensa internacional: automáticas, sin revisión humana.
