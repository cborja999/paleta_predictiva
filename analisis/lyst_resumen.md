# Lyst Index como segunda medida de relevancia

Fuente: Lyst Index, ranking trimestral de marcas (Q1-18 a Q2-26), transcripto por el grupo CICLO. Datos crudos fuera del repo por licencia.
Los 2018 son top 10 y desde Q1-19 top 20; en Q1-26 Lyst recalibro la formula (corte en la serie).

## Cobertura: cuanto del ranking Lyst esta en nuestras fotos
Tenemos 12 de las casas que aparecen en Lyst (Hermes y Calvin Klein estan en nuestras fotos pero no en el ranking).
Promedio de puestos del ranking ocupados por casas que tenemos: 42%.
Por año: 2018=48%; 2019=38%; 2020=39%; 2021=50%; 2022=46%; 2023=45%; 2024=36%; 2025=34%; 2026=38%

## Marcas que mas aparecen en Lyst y NO estan en nuestras fotos

| Marca | Trimestres en el ranking (de 34) | Puesto promedio |
|---|---|---|
| Moncler | 32 | 9.3 |
| Bottega Veneta | 28 | 8.9 |
| Loewe | 28 | 10.4 |
| Burberry | 28 | 11.8 |
| Jacquemus | 24 | 14.7 |
| Nike | 21 | 9.8 |
| Miu Miu | 19 | 3.8 |
| Off-White | 18 | 6.1 |
| Dolce & Gabbana | 15 | 13.4 |
| Stone Island | 14 | 13.6 |

## Acuerdo con Google Trends

Entre las 12 casas que estan en ambos, correlacion de rangos (Spearman) entre puntos Lyst (ultimos 4 trimestres) e indice de Trends (ultimos 12 meses): **0.45**.
Con 12 casas esa correlacion no es estadisticamente significativa (p aprox. 0,14): es una referencia, no una prueba. Detalle en `lyst_vs_trends.csv`.

## Lectura
- Lyst y Trends miden cosas parecidas pero no iguales (Lyst combina busquedas, ventas y clics en su plataforma).
- Lo mas util: Lyst muestra que marcas dominan la conversacion y no estan en nuestra muestra (ver tabla), asi que la muestra de pasarela puede estar subrepresentando a las marcas que mueven la busqueda. Es una hipotesis, no esta probado.
- No se hizo cruce ponderado con Lyst: solo cubre 2018 en adelante (~17 temporadas), muy poco para correlaciones con retraso.
