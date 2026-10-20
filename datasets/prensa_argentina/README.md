# Prensa argentina sobre tendencias

`planilla_prensa_notas_2026-10-20.csv` es la hoja **Notas** de la planilla compartida del grupo, exportada el 20/10/2026 (83 filas, 70 de medios aprobados). La versión viva está en el Google Sheets `planilla_prensa`. Se guarda **tal cual la cargó el grupo**; no se corrigió nada. Solo etiquetas, fecha, título y link: no se copia texto de las notas.

Reglas de carga y de cobertura: `REGLAS_COBERTURA.txt`. Medios aprobados: Infobae, La Nación, Clarín (Elle y Viva), La Gaceta, Diario de Cuyo, Marie Claire Argentina.

## Cobertura (medios aprobados, `aprobado = si`)
| Temporada | Notas |
|---|---|
| SS2022 (fuera de ventana) | 1 |
| SS2023 | 6 |
| FW2023 | 6 |
| SS2024 | 6 |
| FW2024 | 5 |
| SS2025 | 3 |
| FW2025 | 8 |
| SS2026 | 12 |
| FW2026 | 14 |
| SS2027 | 9 |

Las temporadas viejas tienen pocas notas. Estado de lectura: 12 leídas por una persona, 64 con etiquetas automáticas sin revisar, 6 solo con título, 1 sin estado. **Antes de usar los datos hay que revisar al azar 5 notas "leída (auto)".**

## Problemas de carga detectados
`python3 revisar_calidad.py` lista todo; no modifica el archivo. Resumen:
- Etiquetas fuera de la lista (colores, prendas, largos) y listas con "/" en vez de ";" (ej. `Morado/Azul/Estampado`, `Chaqueta/Jersey`, `Ropa de Playa`).
- Fila 77: los nombres de prendas están en la columna de colores.
- Fecha inválida en la fila 74 (`2023-17-09`).
- Cuatro links apuntan a `staging.clarin.com` (servidor de pruebas): hay que reemplazarlos por el link público.
- Medio escrito como `Clarin` (5 filas) y no `Clarín / Elle`, lo que hace que el resumen por medio no las cuente.
- Cinco notas dicen en observaciones que no se apoyan en desfiles internacionales (celebridades, playa, desfile argentino): no deberían entrar al cruce con pasarela.
- Una fila sin estado; una nota de SS2022 fuera de ventana; dos notas de OHLALA (La Nación) con `aprobado = no` hasta que se decida si cuentan.

## Uso
Es contexto local. Con esta muestra no se hacen pruebas estadísticas: mide lo que publica la prensa, no lo que compra la gente.
