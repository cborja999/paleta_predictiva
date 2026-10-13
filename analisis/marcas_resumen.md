# Marcas mas buscadas y ponderacion del cruce

Fuente: Google Trends, busqueda web, mensual 2004 - sep 2026, 8 consultas en datasets/trends_marcas.
Cada consulta de Trends se reescala sola. Para poder comparar marcas entre consultas se encadenan con una marca ancla
(Gucci para el lujo; Zara para venta masiva, enlazada a Gucci con una consulta puente; Zara de Argentina para las marcas locales).
Los indices de Argentina estan en su propia escala y **no** son comparables con los globales.

## Marcas mas buscadas en los ultimos 12 meses (oct 2025 - sep 2026)

### Casas de lujo de pasarela (indice global, Gucci de la primera consulta como referencia)

| Marca | Indice promedio | Avisos |
|---|---|---|
| prada | 33.7 |  |
| gucci | 32.2 |  |
| dior | 32.1 |  |
| chanel | 31.0 |  |
| louis vuitton | 28.5 |  |
| hermes | 24.7 | termino ambiguo |
| ralph lauren | 19.9 |  |
| calvin klein | 16.8 |  |
| valentino | 11.8 | termino ambiguo |
| versace | 10.3 |  |
| saint laurent | 8.1 |  |
| balenciaga | 7.9 |  |
| fendi | 3.7 | volumen bajo |
| alexander mcqueen | 1.5 |  |

### Venta masiva (indice global)

| Marca | Indice promedio | Avisos |
|---|---|---|
| zara | 77.8 |  |
| shein | 55.3 |  |
| mango | 45.8 | termino ambiguo |
| h&m | 31.2 |  |
| uniqlo | 25.1 |  |
| cos | 18.1 | termino ambiguo |
| bershka | 11.0 |  |
| stradivarius | 7.8 |  |
| pull and bear | 5.1 | volumen bajo |

### Marcas argentinas y Zara (indice de Argentina; Zara = referencia)

| Marca | Indice promedio | Avisos |
|---|---|---|
| vitamina | 91.9 | termino ambiguo |
| zara | 79.0 |  |
| mimo | 23.2 | termino ambiguo |
| 47 street | 18.3 |  |
| rapsodia | 11.3 |  |
| awada | 8.3 | termino ambiguo |
| kosiuko | 8.0 |  |
| ayres | 6.3 | termino ambiguo |
| cardon | 6.2 | volumen bajo |
Vitamina, Mimo, Awada y Ayres son palabras o apellidos comunes: su indice mezcla otras busquedas y **no** debe leerse como ranking de marcas. Los mas confiables de esta lista son Zara, 47 Street, Rapsodia y Kosiuko.

## Relevancia de las casas de pasarela

Para cada temporada se mide cuanto se buscaba cada casa en los 12 meses anteriores al desfile (`marcas_relevancia_por_temporada.csv`). Es un indicador de cuanto mira el publico a esa casa, no de cuanto vende.

## Cruce ponderado vs sin ponderar

Cada foto pesa segun la relevancia de busqueda de su casa en esa temporada (peso medio = 1). Comparacion declarada de antemano: correlacion promedio a 12 y 15 meses.

| Demora (meses) | Sin ponderar | Ponderada | Positivas signif. sin pond. | Positivas signif. pond. |
|---|---|---|---|---|
| 0 | 0.005 | -0.008 | 1 | 1 |
| 3 | -0.064 | -0.048 | 0 | 0 |
| 6 | -0.002 | -0.003 | 1 | 2 |
| 9 | -0.000 | -0.010 | 0 | 0 |
| 12 | 0.029 | 0.033 | 1 | 0 |
| 15 | 0.037 | 0.013 | 1 | 1 |
| 18 | -0.037 | -0.029 | 0 | 0 |
| 21 | -0.030 | -0.018 | 1 | 1 |
| 24 | -0.008 | -0.014 | 0 | 0 |

**Promedio a 12 y 15 meses:** sin ponderar 0.033, ponderada 0.023.

La diferencia es chica (-0.010): ponderar por relevancia de la casa **no cambia** el resultado. La hipotesis sigue sin confirmarse ni refutarse.

## Limitaciones

- Buscar mucho una marca no es comprarla. Es una medida de atencion.
- Terminos ambiguos (hermes, cos, mimo, vitamina, ayres, awada, mango, valentino) pueden mezclar otras busquedas.
- Fendi, Cardon y Pull and Bear tienen volumen muy bajo (maximo menor a 12 sobre 100): el ruido es grande.
- Alexander McQueen y Fendi se buscan poco hoy en la escala del lujo: su relevancia reciente es ruidosa.
- Las marcas argentinas se miden solo con busquedas de Argentina y en escala propia.
- Las 15 casas de pasarela son de lujo; Zara, H&M, etc. no aparecen en las fotos.
