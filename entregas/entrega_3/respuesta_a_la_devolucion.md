# Devolución de la Entrega 2 (promedio 5/10) y qué hicimos

| Observación de los docentes | Qué hicimos | Dónde está | Qué falta |
|---|---|---|---|
| **Foco muy amplio** ("TODO"); hay que explicar qué es una silueta y mostrar ejemplos visuales | Propuesta de foco abajo. Silueta validada solo al 58%: la bajamos de protagonista. | este archivo | Decidir el foco entre los 3 |
| **Evidencia real** de runways pasados que se dispararon (runways, ventas, Trends) y **niveles de confianza** | 3 casos con Trends + backtest de 20 temporadas con tasa de acierto por nivel | `analisis/casos_resumen.md`, `analisis/backtest_resumen.md` | Fotos de runway de cada caso al lado de la curva (para la presentación) |
| **No mostraron datasets/atributos**; ¿T-Fashion es API o manual?; ¿cómo se convierten datos en siluetas? | Inventario de datasets con fuente y método; T-Fashion = carga manual de reportes públicos; siluetas = Gemini con lista cerrada | `entregas/entrega_3/proceso_y_criterios.md`, `datasets/diccionario.md` | Mostrar 1 tabla de datos en pantalla en la presentación |
| **IA sin criterios** ni indicadores | Tabla de qué decide la IA y qué decide una regla fija, con umbrales | `proceso_y_criterios.md`, sección 2 | Que el equipo valide los umbrales |
| **Diseño/UX visual**, Figma con alternativas, validar con coolhunters o empresas | Guion de pantallas con contenido visual por pantalla | `guion_pantallas.md` | **Figma con 2-3 alternativas (lo hace el equipo)**; hablar con al menos 2 marcas o coolhunters |
| **Comunicación**: estructura, sub-instancias, más pantallas | El guion propone el flujo completo | `guion_pantallas.md` | Ensayar |

## Propuesta de foco (para decidir)
**Recomendación:** un solo recorrido, de punta a punta, para **una marca argentina de ropa de mujer** y **una temporada** (primavera-verano 2027 en Argentina, que arranca ~sep 2027 y cuyos desfiles de referencia fueron en oct 2026), con **tres atributos**: color, largo y prenda. Se deja afuera la silueta hasta validarla mejor.
Por qué: son los atributos con mejor clasificación (largo 90%, color 82%, prenda 70%) y los que se pueden ilustrar con fotos y con casos reales (rosa, minifalda).

## Dos cosas que cambian el mensaje
1. **El backtest no confirma la hipótesis.** La pasarela sola acierta como el azar. Hay que presentarlo así y proponer el producto como **brief con evidencia y confianza explícita**, no como "predicción".
2. **Lo que sí predice es la inercia de búsquedas** (63%). Una versión honesta del producto combina "lo que ya viene subiendo en búsquedas" con la pasarela como contexto visual.
