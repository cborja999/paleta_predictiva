"""
Cruce pasarela (fotos clasificadas con Gemini) vs busquedas (Google Trends).
Pregunta: cuando un color/prenda/silueta domina una temporada de desfiles,
suben las busquedas de ese termino unos meses despues? Cuantos meses?

Usa solo la libreria estandar de Python.
Salidas en la misma carpeta:
  mapa_temporadas.csv, participacion_por_temporada.csv,
  correlaciones.csv, perfil_por_demora.csv, resumen.md
"""
import csv, math, random, os, sys
from collections import defaultdict, Counter

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
RES = os.path.join(RAIZ, "datasets_procesados", "resultados_gemini.csv")
TRE = os.path.join(RAIZ, "datasets", "trends", "trends_unificado.csv")
LAGS = [0, 3, 6, 9, 12, 15, 18, 21, 24]      # meses entre desfile y busqueda
PERMS = 2000
MIN_LOOKS = 15                              # minimo de fotos por temporada
ULTIMO_MES = 2026 * 12 + 8                  # sep-2026 (oct-2026 esta incompleto)
random.seed(7)

def absmes(y, m): return y * 12 + (m - 1)
def mes_txt(a): return "%04d-%02d" % (a // 12, a % 12 + 1)

# ---------- mapa de temporadas ----------
# FWn se muestra en feb-mar de n; SSn se muestra en sep-oct de n-1.
def mes_desfile(tem, anio):
    return absmes(anio, 3) if tem == "FW" else absmes(anio - 1, 10)

def temporada_ar(tem, anio):
    # La temporada argentina equivalente arranca ~12 meses despues del desfile.
    if tem == "SS":
        return "Primavera-Verano (arranca sep %d)" % anio
    return "Otono-Invierno (arranca mar %d)" % (anio + 1)

# ---------- carga de resultados de Gemini ----------
CAMPOS = {"color": "color_dominante", "prenda": "prenda_principal",
          "silueta": "silueta", "largo": "largo"}
INVALIDOS = {"", "no_aplica", "No aplica", "Otro", "otro"}
def norm(v):
    v = (v or "").strip()
    return "Pantalon" if v == "Pantalón" else v

filas = []
with open(RES, encoding="utf-8") as f:
    for r in csv.DictReader(f):
        if (r.get("error") or "").strip():
            continue
        filas.append(r)
print("Fotos clasificadas:", len(filas))

por_temp = defaultdict(list)
for r in filas:
    por_temp[(r["temporada"], int(r["anio"]))].append(r)

temporadas = sorted(por_temp, key=lambda k: mes_desfile(*k))
with open(os.path.join(AQUI, "mapa_temporadas.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["temporada_desfile", "mes_del_desfile", "temporada_argentina_equivalente", "fotos_clasificadas"])
    for k in temporadas:
        w.writerow(["%s%d" % k, mes_txt(mes_desfile(*k)), temporada_ar(*k), len(por_temp[k])])

# participacion por temporada
share = {}      # (tipo, categoria) -> {temporada: porcentaje}
with open(os.path.join(AQUI, "participacion_por_temporada.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(["temporada", "tipo", "categoria", "fotos", "total_validas", "porcentaje"])
    for k in temporadas:
        for tipo, col in CAMPOS.items():
            vals = [norm(r[col]) for r in por_temp[k]]
            vals = [v for v in vals if v not in INVALIDOS]
            if len(vals) < MIN_LOOKS: continue
            c = Counter(vals)
            for cat, n in c.items():
                p = 100.0 * n / len(vals)
                share.setdefault((tipo, cat), {})[k] = p
                w.writerow(["%s%d" % k, tipo, cat, n, len(vals), round(p, 2)])
            # categorias que no aparecen en la temporada valen 0
    # completar ceros
for key, d in share.items():
    for k in temporadas:
        if k not in d:
            tipo = key[0]
            vals = [norm(r[CAMPOS[tipo]]) for r in por_temp[k]]
            vals = [v for v in vals if v not in INVALIDOS]
            if len(vals) >= MIN_LOOKS: d[k] = 0.0

# ---------- carga de Trends ----------
trends = {}      # termino -> {absmes: valor}
meta = {}
with open(TRE, encoding="utf-8") as f:
    for r in csv.DictReader(f):
        y, m = r["mes"].split("-")
        a = absmes(int(y), int(m))
        if a > ULTIMO_MES: continue
        t = r["termino"]
        trends.setdefault(t, {})[a] = float(r["valor"])
        meta[t] = (r["tipo"], r["categoria_gemini"], r["usable"], float(r["max_serie"]))

def ajustar(serie):
    """Quita tendencia de largo plazo y estacionalidad del hemisferio norte."""
    meses = sorted(serie)
    x = {a: math.log1p(serie[a]) for a in meses}
    resid = {}
    for a in meses:
        vent = [x[b] for b in range(a - 6, a + 7) if b in x]
        resid[a] = x[a] - sum(vent) / len(vent)
    est = defaultdict(list)
    for a, v in resid.items(): est[a % 12].append(v)
    est = {m: sum(v) / len(v) for m, v in est.items()}
    return {a: resid[a] - est[a % 12] for a in meses}

def valor_en(serie, centro):
    v = [serie[b] for b in (centro - 1, centro, centro + 1) if b in serie]
    return sum(v) / len(v) if len(v) >= 2 else None

def pearson(a, b):
    n = len(a)
    if n < 8: return None
    ma, mb = sum(a) / n, sum(b) / n
    sa = math.sqrt(sum((x - ma) ** 2 for x in a)); sb = math.sqrt(sum((y - mb) ** 2 for y in b))
    if sa == 0 or sb == 0: return None
    return sum((x - ma) * (y - mb) for x, y in zip(a, b)) / (sa * sb)

def pval(a, b, r):
    mayor = 0
    bb = list(b)
    for _ in range(PERMS):
        random.shuffle(bb)
        rr = pearson(a, bb)
        if rr is not None and abs(rr) >= abs(r): mayor += 1
    return (mayor + 1) / (PERMS + 1)

# termino elegido por categoria (el usable de mayor volumen)
elegido = {}
for t, (tipo, cat, usable, mx) in meta.items():
    if not tipo or usable != "si": continue
    k = (tipo, cat)
    if k not in elegido or mx > meta[elegido[k]][3]: elegido[k] = t

filas_out = []
for k, t in sorted(elegido.items()):
    if k not in share: continue
    tipo, cat = k
    raw = trends[t]; adj = ajustar(raw)
    # porcentaje ajustado: resta el promedio de las temporadas del mismo tipo (FW / SS)
    d = share[k]
    prom = {}
    for ty in ("FW", "SS"):
        v = [d[s] for s in d if s[0] == ty]
        prom[ty] = sum(v) / len(v) if v else 0
    for L in LAGS:
        xs_adj, ys_adj, xs_raw, ys_raw = [], [], [], []
        for s in d:
            c = mes_desfile(*s) + L
            va = valor_en(adj, c); vr = valor_en(raw, c)
            if va is None or vr is None: continue
            xs_adj.append(d[s] - prom[s[0]]); ys_adj.append(va)
            xs_raw.append(d[s]); ys_raw.append(vr)
        r_adj = pearson(xs_adj, ys_adj)
        r_raw = pearson(xs_raw, ys_raw)
        p = pval(xs_adj, ys_adj, r_adj) if r_adj is not None else None
        filas_out.append([tipo, cat, t, L, len(xs_adj),
                          None if r_adj is None else round(r_adj, 3),
                          None if p is None else round(p, 3),
                          None if r_raw is None else round(r_raw, 3)])

with open(os.path.join(AQUI, "correlaciones.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["tipo", "categoria", "termino_trends", "demora_meses", "n_temporadas", "corr_ajustada", "p_permutacion", "corr_bruta"])
    w.writerows(filas_out)

# ---------- perfil por demora ----------
perfil = []
for L in LAGS:
    v = [r[5] for r in filas_out if r[3] == L and r[5] is not None]
    pos = sum(1 for x in v if x > 0)
    sig = sum(1 for r in filas_out if r[3] == L and r[6] is not None and r[6] < 0.05 and r[5] and r[5] > 0)
    perfil.append((L, len(v), sum(v) / len(v), pos / len(v), sig))
with open(os.path.join(AQUI, "perfil_por_demora.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(["demora_meses", "n_categorias", "corr_promedio", "proporcion_positivas", "n_positivas_significativas"])
    for L, n, m, pr, sg in perfil: w.writerow([L, n, round(m, 3), round(pr, 2), sg])

# mejor demora por categoria
mejores = []
for k in sorted(elegido):
    rs = [r for r in filas_out if (r[0], r[1]) == k and r[5] is not None]
    if not rs: continue
    b = max(rs, key=lambda r: r[5])
    mejores.append(b)
mejores.sort(key=lambda r: -r[5])

lineas = ["# Resultado del cruce pasarela vs busquedas", "",
          "Temporadas de desfile: %d (de %s a %s). Fotos clasificadas: %d." % (
              len(temporadas), "%s%d" % temporadas[0], "%s%d" % temporadas[-1], len(filas)), "",
          "## Perfil por demora (promedio de todas las categorias)", "",
          "| Demora (meses) | Categorias | Correlacion promedio | % positivas | Positivas significativas (p<0,05) |",
          "|---|---|---|---|---|"]
for L, n, m, pr, sg in perfil:
    lineas.append("| %d | %d | %.3f | %d%% | %d |" % (L, n, m, round(pr * 100), sg))
lineas += ["", "## Mejor demora por categoria (ordenado por correlacion)", "",
           "| Tipo | Categoria | Busqueda usada | Mejor demora | Correlacion | p | n |", "|---|---|---|---|---|---|---|"]
for r in mejores:
    lineas.append("| %s | %s | %s | %d m | %.2f | %.3f | %d |" % (r[0], r[1], r[2], r[3], r[5], r[6], r[4]))
lineas += ["", "Notas: la correlacion es ajustada (se saco la tendencia de largo plazo y la estacionalidad de las busquedas, y el promedio de cada tipo de temporada).",
           "El p-valor sale de mezclar las temporadas al azar %d veces. Con ~%d categorias x %d demoras, algunos resultados 'significativos' pueden darse por azar." % (PERMS, len(mejores), len(LAGS))]
open(os.path.join(AQUI, "resumen.md"), "w", encoding="utf-8").write("\n".join(lineas))
print("\n".join(lineas))
