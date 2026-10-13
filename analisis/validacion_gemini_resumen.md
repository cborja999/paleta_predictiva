# Validación de la clasificación de Gemini (muestra de 40 fotos)

**Qué se hizo:** se sacaron 40 fotos al azar (semilla fija) de las 2.430 clasificadas. Una segunda lectura (Claude, mirando la foto) anotó color, prenda, silueta y largo **antes** de ver lo que puso Gemini. Después se compararon.
Detalle foto por foto en `validacion_gemini_muestra.csv`.

| Atributo | Coinciden | % |
|---|---|---|
| Largo | 36 de 40 | 90% |
| Color dominante | 33 de 40 | 82% |
| Prenda principal | 28 de 40 | 70% |
| Silueta | 23 de 40 | 58% |

**Cómo leerlo:**
- **Largo y color** son confiables para el análisis. Los desacuerdos de color son casos de borde (negro vs gris oscuro, blanco vs crema, looks con varios colores).
- **Prenda:** la mayoría de los desacuerdos son por "Conjunto de dos piezas" contra "Falda", "Blazer" o "Pantalón": el look tiene dos prendas y las dos etiquetas son defendibles.
- **Silueta es el atributo más flojo (58%).** Las confusiones son entre categorías vecinas (Recta / Estructurada / Acampanada / Fluida). Es subjetivo: dos personas también discreparían. **Conclusión: no afirmar nada fuerte sobre siluetas con estos datos sin una validación humana.**
- La "confianza" que declara Gemini es "alta" en 2.425 de 2.430 fotos: no sirve como indicador. Hay que usar la validación, no esa columna.

**Limitaciones:** n = 40; la segunda lectura es de otro modelo de IA, no de una persona experta, así que mide acuerdo y no "verdad". Para cerrar esto bien, que dos personas del grupo etiqueten las mismas 40 fotos sin ver ninguna de las dos lecturas y se calcule el acuerdo.
