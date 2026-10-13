"""
Marcas mas buscadas (Google Trends) y su uso como ponderacion del cruce pasarela - busquedas.

Hace tres cosas:
  1. Unifica las 8 consultas de marcas de datasets/trends_marcas en una sola escala comparable
     (cada consulta de Trends se reescala sola, asi que se encadenan con una marca "ancla"
     que aparece en varias consultas: Gucci para el lujo, Zara para venta masiva).
  2. Calcula la relevancia de busqueda de cada casa de pasarela antes de cada temporada.
  3. Repite el cruce pasarela - busquedas ponderando cada foto por la relevancia de su casa,
     y lo compara con el cruce sin ponderar. UNA sola comparacion declarada de antemano
     (promedio de correlaciones a 12 y 15 meses); el resto es descriptivo.

Usa solo la libreria estandar. Salidas en esta carpeta y en datasets/trends_marcas:
  marcas_unificado.csv, marcas_relevancia_por_temporada.csv,
  marcas_perfil_ponderado.csv, marcas_resumen.md
"""
import csv, math, random, os, glob
from collections import defaultdict, Counter

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
RES = os.path.join(RAIZ, "datasets_procesados", "resultados_gemini.csv")
TRE = os.path.join(RAIZ, "datasets", "trends", "trends_unificado.csv")
MAR = os.path.join(RAIZ, "datasets", "trends_marcas")
LAGS = [0, 3, 6, 9, 12, 15, 18, 21, 24]
PERMS = 2000
MIN_LOOKS = 15
ULTIMO_MES = 2026 * 12 + 8          # sep-2026 (oct-2026 esta incompleto)
random.seed(7)

def absmes(y, m): return y * 12 + (m - 1)
def mes_txt(a): return "%04d-%02d" % (a // 12, a % 12 + 1)

# ---------------------------------------------------------------- 1. marcas
ARCHIVOS = [  # (archivo, grupo, geo, ancla, referencia_para_escala)
    ("MUNDO__gucci_chanel_dior_louis-vuitton_prada.csv", "lujo", "MUNDO", "gucci", "ref_gucci"),
    ("MUNDO__gucci_saint-laurent_versace_balenciaga_fendi.csv", "lujo", "MUNDO", "gucci", None),
    ("MUNDO__gucci_valentino_hermes_alexander-mcqueen_ralph-lauren.csv", "lujo", "MUNDO", "gucci", None),
    ("MUNDO__gucci_calvin-klein_zara.csv", "lujo", "MUNDO", "gucci", "enlace"),
    ("MUNDO__zara_h-m_shein_mango_uniqlo.csv", "masiva", "MUNDO", "zara", None),
    ("MUNDO__zara_bershka_stradivarius_pull-and-bear_cos.csv", "masiva", "MUNDO", "zara", None),
    ("AR__zara_rapsodia_cardon_kosiuko_mimo.csv", "argentina", "AR", "zara", "ref_zara_ar"),
    ("AR__zara_47-street_awada_vitamina_ayres.csv", "argentina", "AR", "zara", None),
]
AMBIGUAS = {"hermes", "cos", "mimo", "vitamina", "ayres", "awada", "mango", "valentino"}

def num(x):
    x = x.strip()
    if x.startswith("<"): return 0.5
    try: return float(x)
    except ValueError: return 0.0

def leer_trends(path):
    rows = list(csv.reader(open(path, encoding="utf-8")))
    i = [k for k, r in enumerate(rows) if r and r[0] == "Mes"][0]
    terminos = [c.split(":")[0].strip() for c in rows[i][1:]]
    ser = {t: {} for t in terminos}
    for r in rows[i + 1:]:
        if len(r) < len(terminos) + 1 or not r[0]: continue
        y, m = r[0].split("-")
        a = absmes(int(y), int(m))
        if a > ULTIMO_MES: continue
        for j, t in enumerate(terminos):
            ser[t][a] = num(r[j + 1])
    return ser

def suma(s, meses): return sum(s[a] for a in meses)

datos = {a[0]: leer_trends(os.path.join(MAR, a[0])) for a in ARCHIVOS}
base_gucci = datos[ARCHIVOS[0][0]]["gucci"]
meses_ok = sorted(base_gucci)
factor = {}
for arch, grupo, geo, ancla, rol in ARCHIVOS:
    if geo == "MUNDO" and ancla == "gucci":
        factor[arch] = suma(base_gucci, meses_ok) / suma(datos[arch]["gucci"], meses_ok)
zara_enlace = {a: v * factor[ARCHIVOS[3][0]] for a, v in datos[ARCHIVOS[3][0]]["zara"].items()}
for arch, grupo, geo, ancla, rol in ARCHIVOS:
    if geo == "MUNDO" and ancla == "zara":
        z = datos[arch]["zara"]
        factor[arch] = suma(zara_enlace, meses_ok) / suma(z, meses_ok)
zara_ar1 = datos[ARCHIVOS[6][0]]["zara"]
factor[ARCHIVOS[6][0]] = 1.0
factor[ARCHIVOS[7][0]] = suma(zara_ar1, meses_ok) / suma(datos[ARCHIVOS[7][0]]["zara"], meses_ok)

marcas = {}       # (marca, geo) -> {mes: valor normalizado}
info = {}         # (marca, geo) -> (grupo, archivo, max_crudo)
for arch, grupo, geo, ancla, rol in ARCHIVOS:
    for t, s in datos[arch].items():
        # la ancla se toma solo de su archivo de referencia
        if t == ancla and (t, geo) in marcas: continue
        marcas[(t, geo)] = {a: v * factor[arch] for a, v in s.items()}
        info[(t, geo)] = (grupo if t != "zara" else "masiva", arch, max(s.values()))
# 'zara' en el archivo de enlace gana sobre las otras (misma escala que Gucci); ya esta primero por orden
# (el archivo de enlace va antes que los de venta masiva).

with open(os.path.join(MAR, "marcas_unificado.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["marca", "grupo", "geo", "mes", "valor_normalizado", "archivo_origen", "volumen_bajo", "termino_ambiguo"])
    for (t, geo), s in sorted(marcas.items(), key=lambda kv: (kv[0][1], info[kv[0]][0], kv[0][0])):
        grupo, arch, mx = info[(t, geo)]
        for a in sorted(s):
            w.writerow([t, grupo, geo, mes_txt(a), round(s[a], 2), arch,
                        "si" if mx < 12 else "no", "si" if t in AMBIGUAS else "no"])

# ---------------------------------------------------------- 2. relevancia
CASA = {"chanel": "chanel", "valentino": "valentino", "christian dior": "dior", "gucci": "gucci",
        "saint laurent": "saint laurent", "versace": "versace", "balenciaga": "balenciaga",
        "ralph lauren": "ralph lauren", "fendi": "fendi", "hermes": "hermes", "prada": "prada",
        "louis vuitton": "louis vuitton", "alexander mcqueen": "alexander mcqueen",
        "calvin klein collection": "calvin klein", "calvin klein": "calvin klein"}

def mes_desfile(tem, anio):
    return absmes(anio, 3) if tem == "FW" else absmes(anio - 1, 10)

filas = []
with open(RES, encoding="utf-8") as f:
    for r in csv.DictReader(f):
        if (r.get("error") or "").strip(): continue
        filas.append(r)
por_temp = defaultdict(list)
for r in filas: por_temp[(r["temporada"], int(r["anio"]))].append(r)
temporadas = sorted(por_temp, key=lambda k: mes_desfile(*k))

casas = sorted(set(CASA.values()))
relev = {}        # temporada -> {casa: indice}
for k in temporadas:
    m0 = mes_desfile(*k)
    ventana = range(m0 - 12, m0)         # los 12 meses ANTES del desfile
    rel = {}
    for c in casas:
        s = marcas[(c, "MUNDO")]
        v = [s[a] for a in ventana if a in s]
        rel[c] = sum(v) / len(v) if v else 0.0
    relev[k] = rel
with open(os.path.join(AQUI, "marcas_relevancia_por_temporada.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["temporada", "casa", "indice_busqueda_12m_previos", "porcentaje_entre_casas", "fotos_de_la_casa"])
    for k in temporadas:
        tot = sum(relev[k].values())
        cnt = Counter(CASA.get((r["marca"] or "").strip().lower(), "?") for r in por_temp[k])
        for c in casas:
            w.writerow(["%s%d" % k, c, round(relev[k][c], 2), round(100 * relev[k][c] / tot, 2), cnt.get(c, 0)])

# --------------------------------------------- 3. cruce ponderado vs sin ponderar
CAMPOS = {"color": "color_dominante", "prenda": "prenda_principal", "silueta": "silueta", "largo": "largo"}
INVALIDOS = {"", "no_aplica", "No aplica", "Otro", "otro"}
def norm(v):
    v = (v or "").strip()
    return "Pantalon" if v == "Pantalón" else v

def pesos(k):
    rel = relev[k]; prom = sum(rel.values()) / len(rel)
    out = []
    for r in por_temp[k]:
        c = CASA.get((r["marca"] or "").strip().lower())
        out.append(rel[c] / prom if c else 1.0)
    return out

def participaciones(ponderar):
    share = {}
    for tipo, col in CAMPOS.items():
        for k in temporadas:
            ps = pesos(k) if ponderar else [1.0] * len(por_temp[k])
            vals = [(norm(r[col]), p) for r, p in zip(por_temp[k], ps)]
            vals = [(v, p) for v, p in vals if v not in INVALIDOS]
            if len(vals) < MIN_LOOKS: continue
            tot = sum(p for _, p in vals)
            acc = defaultdict(float)
            for v, p in vals: acc[v] += p
            for cat, x in acc.items():
                share.setdefault((tipo, cat), {})[k] = 100.0 * x / tot
            for cat in {c for (t, c) in share if t == tipo}:
                share[(tipo, cat)].setdefault(k, 0.0)
    return share

trends = {}; meta = {}
with open(TRE, encoding="utf-8") as f:
    for r in csv.DictReader(f):
        y, m = r["mes"].split("-"); a = absmes(int(y), int(m))
        if a > ULTIMO_MES: continue
        t = r["termino"]
        trends.setdefault(t, {})[a] = float(r["valor"])
        meta[t] = (r["tipo"], r["categoria_gemini"], r["usable"], float(r["max_serie"]))
elegido = {}
for t, (tipo, cat, usable, mx) in meta.items():
    if not tipo or usable != "si": continue
    k = (tipo, cat)
    if k not in elegido or mx > meta[elegido[k]][3]: elegido[k] = t

def ajustar(serie):
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
    mayor = 0; bb = list(b)
    for _ in range(PERMS):
        random.shuffle(bb)
        rr = pearson(a, bb)
        if rr is not None and abs(rr) >= abs(r): mayor += 1
    return (mayor + 1) / (PERMS + 1)

def perfil(share):
    out = {L: [] for L in LAGS}; sig = {L: 0 for L in LAGS}
    for k, t in sorted(elegido.items()):
        if k not in share: continue
        d = share[k]; adj = ajustar(trends[t]); raw = trends[t]
        prom = {}
        for ty in ("FW", "SS"):
            v = [d[s] for s in d if s[0] == ty]
            prom[ty] = sum(v) / len(v) if v else 0
        for L in LAGS:
            xs, ys = [], []
            for s in d:
                c = mes_desfile(*s) + L
                va = valor_en(adj, c); vr = valor_en(raw, c)
                if va is None or vr is None: continue
                xs.append(d[s] - prom[s[0]]); ys.append(va)
            r = pearson(xs, ys)
            if r is None: continue
            out[L].append(r)
            if r > 0 and pval(xs, ys, r) < 0.05: sig[L] += 1
    return out, sig

print("Calculando cruce sin ponderar...")
p0, s0 = perfil(participaciones(False))
print("Calculando cruce ponderado por relevancia de la casa...")
p1, s1 = perfil(participaciones(True))

def prom(v): return sum(v) / len(v) if v else float("nan")
with open(os.path.join(AQUI, "marcas_perfil_ponderado.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["demora_meses", "n_categorias", "corr_promedio_sin_ponderar", "corr_promedio_ponderada",
                "positivas_signif_sin_ponderar", "positivas_signif_ponderada"])
    for L in LAGS:
        w.writerow([L, len(p0[L]), round(prom(p0[L]), 3), round(prom(p1[L]), 3), s0[L], s1[L]])

# --------------------------------------------------------------- resumen
def media_lags(p, lags): return prom([x for L in lags for x in p[L]])
dec0 = media_lags(p0, (12, 15)); dec1 = media_lags(p1, (12, 15))

ult = range(absmes(2025, 10), ULTIMO_MES + 1)   # ultimos 12 meses
def nivel(t, geo):
    s = marcas[(t, geo)]; v = [s[a] for a in ult if a in s]
    return sum(v) / len(v)
L = ["# Marcas mas buscadas y ponderacion del cruce", "",
     "Fuente: Google Trends, busqueda web, mensual 2004 - sep 2026, 8 consultas en datasets/trends_marcas.",
     "Cada consulta de Trends se reescala sola. Para poder comparar marcas entre consultas se encadenan con una marca ancla",
     "(Gucci para el lujo; Zara para venta masiva, enlazada a Gucci con una consulta puente; Zara de Argentina para las marcas locales).",
     "Los indices de Argentina estan en su propia escala y **no** son comparables con los globales.", "",
     "## Marcas mas buscadas en los ultimos 12 meses (oct 2025 - sep 2026)", ""]
for grupo, geo, titulo in (("lujo", "MUNDO", "Casas de lujo de pasarela (indice global, Gucci de la primera consulta como referencia)"),
                           ("masiva", "MUNDO", "Venta masiva (indice global)"),
                           ("argentina", "AR", "Marcas argentinas y Zara (indice de Argentina; Zara = referencia)")):
    items = sorted(((t, nivel(t, g)) for (t, g), (gr, _, _) in info.items() if g == geo and ((gr == grupo and not (grupo == "lujo" and t == "zara")) or (grupo == "argentina" and t == "zara"))),
                   key=lambda x: -x[1])
    L += ["### " + titulo, "", "| Marca | Indice promedio | Avisos |", "|---|---|---|"]
    for t, v in items:
        av = []
        if info[(t, geo)][2] < 12: av.append("volumen bajo")
        if t in AMBIGUAS: av.append("termino ambiguo")
        L.append("| %s | %.1f | %s |" % (t, v, ", ".join(av)))
    if grupo == "argentina":
        L += ["Vitamina, Mimo, Awada y Ayres son palabras o apellidos comunes: su indice mezcla otras busquedas y **no** debe leerse "
              "como ranking de marcas. Los mas confiables de esta lista son Zara, 47 Street, Rapsodia y Kosiuko.", ""]
    else:
        L.append("")
L += ["## Relevancia de las casas de pasarela", "",
      "Para cada temporada se mide cuanto se buscaba cada casa en los 12 meses anteriores al desfile "
      "(`marcas_relevancia_por_temporada.csv`). Es un indicador de cuanto mira el publico a esa casa, no de cuanto vende.", "",
      "## Cruce ponderado vs sin ponderar", "",
      "Cada foto pesa segun la relevancia de busqueda de su casa en esa temporada (peso medio = 1). "
      "Comparacion declarada de antemano: correlacion promedio a 12 y 15 meses.", "",
      "| Demora (meses) | Sin ponderar | Ponderada | Positivas signif. sin pond. | Positivas signif. pond. |",
      "|---|---|---|---|---|"]
for l in LAGS:
    L.append("| %d | %.3f | %.3f | %d | %d |" % (l, prom(p0[l]), prom(p1[l]), s0[l], s1[l]))
L += ["", "**Promedio a 12 y 15 meses:** sin ponderar %.3f, ponderada %.3f." % (dec0, dec1), ""]
dif = dec1 - dec0
if abs(dif) < 0.03:
    L.append("La diferencia es chica (%.3f): ponderar por relevancia de la casa **no cambia** el resultado. "
             "La hipotesis sigue sin confirmarse ni refutarse." % dif)
elif dif > 0:
    L.append("La ponderada es %.3f mas alta. Es una sola comparacion y con pocas temporadas: "
             "sirve como pista para seguir probando, no como confirmacion." % dif)
else:
    L.append("La ponderada es %.3f mas baja: ponderar por relevancia no ayuda." % -dif)
L += ["", "## Limitaciones", "",
      "- Buscar mucho una marca no es comprarla. Es una medida de atencion.",
      "- Terminos ambiguos (hermes, cos, mimo, vitamina, ayres, awada, mango, valentino) pueden mezclar otras busquedas.",
      "- Fendi, Cardon y Pull and Bear tienen volumen muy bajo (maximo menor a 12 sobre 100): el ruido es grande.",
      "- Alexander McQueen y Fendi se buscan poco hoy en la escala del lujo: su relevancia reciente es ruidosa.",
      "- Las marcas argentinas se miden solo con busquedas de Argentina y en escala propia.",
      "- Las 15 casas de pasarela son de lujo; Zara, H&M, etc. no aparecen en las fotos."]
open(os.path.join(AQUI, "marcas_resumen.md"), "w", encoding="utf-8").write("\n".join(L) + "\n")
print("\n".join(L))
