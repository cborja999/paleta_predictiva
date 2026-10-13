"""
Backtest: si en cada temporada pasada hubieramos dicho "esto sube", cuantas veces acertamos?

REGLA (fijada ANTES de mirar resultados, sin ajustes posteriores):
  Señal  = porcentaje de fotos de la categoria en la temporada  -  promedio de las 4 temporadas anteriores del mismo tipo (SS o FW).
  Prediccion: SUBE si señal >= +3 puntos; BAJA si señal <= -3 puntos; si no, sin señal.
  Confianza:  Media = 3 a 6 puntos;  Alta = 6 puntos o mas.
Resultado real:
  cambio = log( busquedas promedio de los meses +12..+23 despues del desfile / promedio de los 12 meses ANTES del desfile ).
  Se resta la mediana del cambio de todas las categorias de esa misma temporada (asi se saca la suba general de Google).
  Acierta si: SUBE y cambio relativo > 0, o BAJA y cambio relativo < 0.
Comparaciones:
  - Azar: se mezclan los resultados entre categorias de la misma temporada 2000 veces (p-valor).
  - Inercia de Trends: "lo que ya venia subiendo en las busquedas antes del desfile sigue subiendo" (no usa la pasarela).
Ventana limpia: solo temporadas cuya ventana de resultado termina antes de 2025 (Google tuvo un salto de medicion en 2025).
Solo libreria estandar. Salidas: backtest_predicciones.csv, backtest_resumen.md
"""
import csv, math, os, random
from collections import defaultdict
from statistics import median

AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(AQUI)
TRE = os.path.join(RAIZ, "datasets", "trends", "trends_unificado.csv")
PART = os.path.join(AQUI, "participacion_por_temporada.csv")
ULTIMO = 2026 * 12 + 8
LIMPIO_HASTA = 2024 * 12 + 11          # la ventana de resultado debe terminar en dic-2024 o antes
UMBRAL, ALTA, PREV, PERMS = 3.0, 6.0, 4, 2000
random.seed(11)

def am(y, m): return y * 12 + m - 1
def mes_desfile(tem, anio): return am(anio, 3) if tem == "FW" else am(anio - 1, 10)

# --- trends
tr, meta = {}, {}
for r in csv.DictReader(open(TRE, encoding="utf-8")):
    y, m = r["mes"].split("-"); a = am(int(y), int(m))
    if a > ULTIMO: continue
    tr.setdefault(r["termino"], {})[a] = float(r["valor"])
    meta[r["termino"]] = (r["tipo"], r["categoria_gemini"], r["usable"], float(r["max_serie"]))
elegido = {}
for t, (tipo, cat, us, mx) in meta.items():
    if not tipo or us != "si": continue
    if (tipo, cat) not in elegido or mx > meta[elegido[(tipo, cat)]][3]: elegido[(tipo, cat)] = t

def prom(s, a, b):
    v = [s[k] for k in range(a, b + 1) if k in s]
    return sum(v) / len(v) if len(v) == b - a + 1 else None
def lg(x, y): return math.log(max(x, 0.3) / max(y, 0.3))

# --- pasarela
share = defaultdict(dict)          # (tipo,cat) -> {(tem,anio): pct}
for r in csv.DictReader(open(PART, encoding="utf-8")):
    k = (r["temporada"][:2], int(r["temporada"][2:]))
    share[(r["tipo"], r["categoria"])][k] = float(r["porcentaje"])
temps = sorted({k for d in share.values() for k in d}, key=lambda k: mes_desfile(*k))
for key, d in share.items():            # ceros donde la categoria no aparecio
    for k in temps: d.setdefault(k, 0.0)

filas = []
for k in temps:
    d0 = mes_desfile(*k)
    if d0 + 23 > ULTIMO: continue
    previas = [p for p in temps if p[0] == k[0] and mes_desfile(*p) < d0][-PREV:]
    if len(previas) < 2: continue
    bloque = []
    for key, term in elegido.items():
        if key not in share: continue
        s = tr[term]
        antes, desp, antes2 = prom(s, d0 - 12, d0 - 1), prom(s, d0 + 12, d0 + 23), prom(s, d0 - 24, d0 - 13)
        if antes is None or desp is None or antes2 is None: continue
        señal = share[key][k] - sum(share[key][p] for p in previas) / len(previas)
        bloque.append([k, key, term, round(señal, 2), lg(desp, antes), lg(antes, antes2)])
    if len(bloque) < 8: continue
    med = median(b[4] for b in bloque); medm = median(b[5] for b in bloque)
    for b in bloque:
        b[4] = round(b[4] - med, 3); b[5] = round(b[5] - medm, 3)
        filas.append(b)

def evaluar(sel, pred):
    """sel: filas; pred(fila)-> +1/-1/0. Devuelve (n, aciertos)."""
    n = a = 0
    for f in sel:
        p = pred(f)
        if p == 0: continue
        n += 1
        if (p > 0 and f[4] > 0) or (p < 0 and f[4] < 0): a += 1
    return n, a

def p_azar(sel, pred):
    n0, a0 = evaluar(sel, pred)
    if n0 == 0: return None
    por = defaultdict(list)
    for i, f in enumerate(sel): por[f[0]].append(i)
    mayor = 0
    for _ in range(PERMS):
        res = {}
        for k, idx in por.items():
            v = [sel[i][4] for i in idx]; random.shuffle(v)
            for i, x in zip(idx, v): res[i] = x
        a = 0
        for i, f in enumerate(sel):
            p = pred(f)
            if p == 0: continue
            if (p > 0 and res[i] > 0) or (p < 0 and res[i] < 0): a += 1
        if a >= a0: mayor += 1
    return (mayor + 1) / (PERMS + 1)

reglas = {
    "Pasarela: Alta (>= 6 pts)": lambda f: 1 if f[3] >= ALTA else (-1 if f[3] <= -ALTA else 0),
    "Pasarela: Media (3 a 6 pts)": lambda f: (1 if UMBRAL <= f[3] < ALTA else (-1 if -ALTA < f[3] <= -UMBRAL else 0)),
    "Pasarela: Alta + Media (>= 3 pts)": lambda f: 1 if f[3] >= UMBRAL else (-1 if f[3] <= -UMBRAL else 0),
    "Solo 'SUBE' (>= 3 pts)": lambda f: 1 if f[3] >= UMBRAL else 0,
    "Inercia de Trends (sin pasarela)": lambda f: 1 if f[5] > 0 else -1,
}
limpio = [f for f in filas if mes_desfile(*f[0]) + 23 <= LIMPIO_HASTA]
with open(os.path.join(AQUI, "backtest_predicciones.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["temporada", "tipo", "categoria", "termino_trends", "señal_pasarela_pts", "cambio_busquedas_relativo(log)", "inercia_trends_previa(log)", "ventana_limpia"])
    for r in filas:
        w.writerow(["%s%d" % r[0], r[1][0], r[1][1], r[2], r[3], r[4], r[5], "si" if r in limpio else "no"])

L = ["# Backtest: ¿cuántas veces habríamos acertado?", "",
     "Regla fijada de antemano (ver encabezado de `backtest_confianza.py`). Resultado = cambio de búsquedas entre los 12 meses previos al desfile y los meses +12 a +23 después, relativo a la mediana de las demás categorías de esa temporada.",
     "Azar = 50%. El p-valor mezcla los resultados entre categorías de la misma temporada (2000 veces).", ""]
for nombre, sel in (("Ventana limpia (resultado antes de 2025)", limpio), ("Todas las temporadas posibles (incluye el salto de Google de 2025)", filas)):
    ts = sorted({r[0] for r in sel}, key=lambda k: mes_desfile(*k))
    L += ["## " + nombre, "", "Temporadas: %d (%s a %s). Categorías por temporada: ~%d." % (len(ts), "%s%d" % ts[0], "%s%d" % ts[-1], len(sel) // max(len(ts), 1)), "",
          "| Regla | Predicciones | Aciertos | % acierto | p vs azar |", "|---|---|---|---|---|"]
    for r, fn in reglas.items():
        n, a = evaluar(sel, fn); p = p_azar(sel, fn)
        L.append("| %s | %d | %d | %s | %s |" % (r, n, a, ("%.0f%%" % (100.0 * a / n)) if n else "-", ("%.3f" % p) if p is not None else "-"))
    L.append("")
L += ["## Cómo leerlo", "- Si 'Alta' acierta claramente más que 'Media' y que el azar, la confianza tiene sentido y la podemos mostrar como nivel en el brief.",
      "- Si no, hay que decir que la señal de pasarela por sí sola no alcanza para prometer confianza alta.",
      "- La inercia de Trends es el rival a vencer: si lo que ya sube en búsquedas acierta igual o más, la pasarela no agrega información.",
      "- Limitaciones: ~27 temporadas, 25 categorías, búsquedas en inglés y a nivel mundial; los umbrales se fijaron antes de mirar pero son arbitrarios; las categorías de una misma temporada no son independientes."]
open(os.path.join(AQUI, "backtest_resumen.md"), "w", encoding="utf-8").write("\n".join(L) + "\n")
print("\n".join(L))
