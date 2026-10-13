"""
Estudio de eventos: que pasa con las busquedas en los meses posteriores a un
'pico' en pasarela?
Criterio (fijado ANTES de mirar resultados):
  evento = categoria con porcentaje en la temporada >= 1.5 x su promedio
           (de las temporadas del mismo tipo, FW o SS) Y >= +5 puntos sobre ese promedio.
Se promedia la serie de busquedas (sin tendencia ni estacionalidad) en los meses
-6 ... +24 alrededor del desfile y se compara contra pares categoria-temporada al
azar (2000 sorteos, banda 5%-95%).
"""
import csv, math, os, random
from collections import defaultdict, Counter
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(AQUI)
RES = os.path.join(RAIZ, "datasets_procesados", "resultados_gemini.csv")
TRE = os.path.join(RAIZ, "datasets", "trends", "trends_unificado.csv")
OFFS = list(range(-6, 25, 3)); SORTEOS = 2000; MIN_LOOKS = 15
RATIO, PUNTOS = 1.5, 5.0
ULTIMO = 2026 * 12 + 8
random.seed(11)
CAMPOS = {"color": "color_dominante", "prenda": "prenda_principal", "silueta": "silueta", "largo": "largo"}
INV = {"", "no_aplica", "No aplica", "Otro", "otro"}
def am(y, m): return y * 12 + m - 1
def mt(a): return "%04d-%02d" % (a // 12, a % 12 + 1)
def desfile(t, y): return am(y, 3) if t == "FW" else am(y - 1, 10)
def nm(v):
    v = (v or "").strip(); return "Pantalon" if v == "Pantalón" else v

filas = [r for r in csv.DictReader(open(RES, encoding="utf-8")) if not (r.get("error") or "").strip()]
pt = defaultdict(list)
for r in filas: pt[(r["temporada"], int(r["anio"]))].append(r)
temps = sorted(pt, key=lambda k: desfile(*k))
share = {}
for k in temps:
    for tipo, col in CAMPOS.items():
        v = [nm(r[col]) for r in pt[k]]; v = [x for x in v if x not in INV]
        if len(v) < MIN_LOOKS: continue
        c = Counter(v)
        for cat in set(nm(r[col]) for s in temps for r in pt[s]) - INV:
            share.setdefault((tipo, cat), {})[k] = 100.0 * c.get(cat, 0) / len(v)

trends, meta = {}, {}
for r in csv.DictReader(open(TRE, encoding="utf-8")):
    y, m = r["mes"].split("-"); a = am(int(y), int(m))
    if a > ULTIMO: continue
    trends.setdefault(r["termino"], {})[a] = float(r["valor"])
    meta[r["termino"]] = (r["tipo"], r["categoria_gemini"], r["usable"], float(r["max_serie"]))

def ajustar(s):
    x = {a: math.log1p(v) for a, v in s.items()}; res = {}
    for a in x:
        w = [x[b] for b in range(a - 6, a + 7) if b in x]; res[a] = x[a] - sum(w) / len(w)
    est = defaultdict(list)
    for a, v in res.items(): est[a % 12].append(v)
    est = {m: sum(v) / len(v) for m, v in est.items()}
    return {a: res[a] - est[a % 12] for a in res}
def val(s, c):
    v = [s[b] for b in (c - 1, c, c + 1) if b in s]; return sum(v) / len(v) if len(v) >= 2 else None

elegido = {}
for t, (tipo, cat, us, mx) in meta.items():
    if not tipo or us != "si": continue
    k = (tipo, cat)
    if k not in elegido or mx > meta[elegido[k]][3]: elegido[k] = t

# curvas por par (categoria, temporada)
pares = {}      # (k, s) -> lista de valores por offset
eventos = []
for k, t in elegido.items():
    if k not in share: continue
    adj = ajustar(trends[t]); d = share[k]
    for s in d:
        curva = [val(adj, desfile(*s) + o) for o in OFFS]
        if any(v is None for v in curva): continue
        pares[(k, s)] = curva
        prom = [d[x] for x in d if x[0] == s[0]]; prom = sum(prom) / len(prom)
        if prom > 0 and d[s] >= RATIO * prom and d[s] - prom >= PUNTOS:
            eventos.append((k, s, d[s], prom))

def media(lst): return [sum(c[i] for c in lst) / len(lst) for i in range(len(OFFS))]
ev = [pares[(k, s)] for k, s, _, _ in eventos if (k, s) in pares]
todos = list(pares.values())
m_ev = media(ev)
sim = []
for _ in range(SORTEOS): sim.append(media(random.sample(todos, len(ev))))
lo, hi, mu = [], [], []
for i in range(len(OFFS)):
    v = sorted(x[i] for x in sim); lo.append(v[int(0.05 * SORTEOS)]); hi.append(v[int(0.95 * SORTEOS)]); mu.append(sum(v) / len(v))

with open(os.path.join(AQUI, "evento_curva.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(["meses_desde_desfile", "eventos_promedio", "azar_promedio", "azar_p5", "azar_p95"])
    for i, o in enumerate(OFFS): w.writerow([o, round(m_ev[i], 4), round(mu[i], 4), round(lo[i], 4), round(hi[i], 4)])
with open(os.path.join(AQUI, "evento_eventos.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(["tipo", "categoria", "temporada", "porcentaje", "promedio_del_tipo"])
    for k, s, p, pr in sorted(eventos): w.writerow([k[0], k[1], "%s%d" % s, round(p, 1), round(pr, 1)])

# grafico SVG
W, H, L, R, T, B = 760, 380, 60, 20, 40, 60
vals = m_ev + lo + hi + mu
ymin, ymax = min(vals) - 0.02, max(vals) + 0.02
X = lambda o: L + (o - OFFS[0]) / (OFFS[-1] - OFFS[0]) * (W - L - R)
Y = lambda v: T + (ymax - v) / (ymax - ymin) * (H - T - B)
svg = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" font-family="sans-serif" font-size="12">' % (W, H),
       '<rect width="100%" height="100%" fill="#fff"/>',
       '<text x="%d" y="22" font-size="15" font-weight="600">Busquedas despues de un pico en pasarela (%d eventos)</text>' % (L, len(ev))]
band = " ".join("%.1f,%.1f" % (X(o), Y(hi[i])) for i, o in enumerate(OFFS)) + " " + " ".join("%.1f,%.1f" % (X(o), Y(lo[i])) for i, o in reversed(list(enumerate(OFFS))))
svg.append('<polygon points="%s" fill="#cfd8dc" opacity="0.7"/>' % band)
svg.append('<line x1="%d" x2="%d" y1="%.1f" y2="%.1f" stroke="#999" stroke-dasharray="3"/>' % (L, W - R, Y(0), Y(0)))
for o in OFFS:
    svg.append('<text x="%.1f" y="%d" text-anchor="middle" fill="#444">%+d</text>' % (X(o), H - B + 18, o))
svg.append('<text x="%d" y="%d" text-anchor="middle" fill="#444">meses desde el desfile (0 = desfile)</text>' % ((L + W - R) // 2, H - 12))
svg.append('<polyline fill="none" stroke="#b7410e" stroke-width="2.5" points="%s"/>' % " ".join("%.1f,%.1f" % (X(o), Y(m_ev[i])) for i, o in enumerate(OFFS)))
for i, o in enumerate(OFFS): svg.append('<circle cx="%.1f" cy="%.1f" r="3.5" fill="#b7410e"/>' % (X(o), Y(m_ev[i])))
svg.append('<rect x="%d" y="%d" width="12" height="12" fill="#cfd8dc"/><text x="%d" y="%d">rango esperable por azar (5%%-95%%)</text>' % (W - 300, T + 4, W - 282, T + 15))
svg.append('<line x1="%d" x2="%d" y1="%d" y2="%d" stroke="#b7410e" stroke-width="2.5"/><text x="%d" y="%d">promedio tras eventos</text>' % (W - 300, W - 288, T + 28, T + 28, W - 282, T + 32))
svg.append('<text x="14" y="%d" transform="rotate(-90 14 %d)" text-anchor="middle" fill="#444">busquedas (sin tendencia ni estacion)</text>' % ((T + H - B) // 2, (T + H - B) // 2))
svg.append('</svg>')
open(os.path.join(AQUI, "evento_curva.svg"), "w", encoding="utf-8").write("\n".join(svg))

fuera = [(OFFS[i], round(m_ev[i], 3), round(lo[i], 3), round(hi[i], 3)) for i in range(len(OFFS)) if m_ev[i] > hi[i] or m_ev[i] < lo[i]]
txt = ["# Estudio de eventos", "", "Eventos: %d (criterio: >= %.1fx el promedio y >= +%.0f puntos)." % (len(ev), RATIO, PUNTOS), "",
       "| Meses | Promedio tras eventos | Azar p5 | Azar p95 |", "|---|---|---|---|"]
for i, o in enumerate(OFFS): txt.append("| %+d | %.3f | %.3f | %.3f |" % (o, m_ev[i], lo[i], hi[i]))
txt += ["", "Puntos fuera del rango del azar: %s" % (fuera if fuera else "ninguno")]
open(os.path.join(AQUI, "evento_resumen.md"), "w", encoding="utf-8").write("\n".join(txt))
print("\n".join(txt)); print("\nPrimeros eventos:"); 
for k, s, p, pr in sorted(eventos)[:40]: print(k[0], k[1], "%s%d" % s, round(p, 1), "prom", round(pr, 1))
