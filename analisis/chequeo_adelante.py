"""
Chequeo hacia adelante: lo que los reportes dijeron de FW25 y SS26, ya se ve en las busquedas de 2026?
Prediccion fijada antes de calcular (segun la tabla de reportes):
  SUBE: brown outfit (cocoa), wide leg jeans (+9,4 ppt), yellow, ecru, salmon, charcoal,
        polka dot dress, duster coat, tailored trousers, tailored blazer, harem pants, crop top
  NO SUBE (cambio ~0 o negativo en el reporte): flare pants (-1,3), bootcut jeans (-0,5)
Medida: log( promedio ene-sep 2026 / promedio ene-sep 2025 ), menos la mediana de los mismos
cambios en 25 terminos 'neutros' (los de la prueba historica). Mide cambio relativo al resto.
"""
import csv, math, os, glob
from statistics import median
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(AQUI)
TD = os.path.join(RAIZ, "datasets", "trends")
def am(y, m): return y * 12 + m - 1
SUBE = ["brown outfit", "wide leg jeans", "yellow outfit", "ecru outfit", "salmon outfit", "charcoal outfit",
        "polka dot dress", "duster coat", "tailored trousers", "tailored blazer", "harem pants", "crop top"]
NOSUBE = ["flare pants", "bootcut jeans"]
series = {}
for f in sorted(glob.glob(os.path.join(TD, "trends_*.csv"))):
    if f.endswith("unificado.csv"): continue
    rows = list(csv.reader(open(f, encoding="utf-8")))
    for j, h in enumerate(rows[2][1:], 1):
        t = h.split(":")[0].strip(); s = {}
        for r in rows[3:]:
            y, m = r[0].split("-"); s[am(int(y), int(m))] = float(r[j].replace("<1", "0.5"))
        if t not in series or max(s.values()) > max(series[t].values()): series[t] = s
def prom(s, a, b): v = [s[k] for k in range(a, b + 1) if k in s]; return sum(v) / len(v)
def g(s, anio):
    a = prom(s, am(anio, 1), am(anio, 9)); b = prom(s, am(anio - 1, 1), am(anio - 1, 9))
    return math.log(max(a, 0.3) / max(b, 0.3))
reportes = set(SUBE + NOSUBE)
neutros = [t for t in series if t not in reportes and max(series[t].values()) >= 8 and t not in ("bodycon", "flowy")]
base26 = median(g(series[t], 2026) for t in neutros)
base25 = median(g(series[t], 2025) for t in neutros)
out = []
for t in SUBE + NOSUBE:
    s = series[t]
    e26 = g(s, 2026) - base26; e25 = g(s, 2025) - base25
    pred = "sube" if t in SUBE else "no sube"
    ok = (e26 > 0) if t in SUBE else (e26 <= 0)
    out.append((t, pred, round(max(s.values()), 0), round(e25, 2), round(e26, 2), "si" if ok else "no"))
with open(os.path.join(AQUI, "chequeo_adelante.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(["termino", "prediccion_reporte", "volumen_max", "cambio_2025_vs_resto", "cambio_2026_vs_resto", "acierta"]); w.writerows(out)
print("Mediana de cambio 2026 vs 2025 en %d terminos neutros: %+.2f (log)" % (len(neutros), base26))
print("%-20s %-8s %5s %10s %10s %s" % ("termino", "predice", "vol", "2025", "2026", "acierta"))
for r in out: print("%-20s %-8s %5s %+10.2f %+10.2f %s" % r)
n = len(out); k = sum(1 for r in out if r[5] == "si")
# prob. de >=k aciertos de n al azar (50%)
from math import comb
p = sum(comb(n, i) for i in range(k, n + 1)) / 2 ** n
print("\nAciertos: %d de %d. Probabilidad de tantos aciertos tirando una moneda: %.3f" % (k, n, p))
