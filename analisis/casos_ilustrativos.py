"""
Tres casos ilustrativos: tendencias que la prensa atribuye a un desfile, y como se movieron las busquedas despues.

IMPORTANTE: son ejemplos elegidos por regla (el origen esta atribuido a un desfile en fuentes de moda), NO una prueba.
Se muestran los tres casos aunque no todos sigan el patron.

Para evitar la estacionalidad se comparan ventanas de 12 meses completos:
  base = promedio de los 12 meses ANTES del desfile
  +1..+12, +13..+24, +25..+36 = promedio de cada ano siguiente
Usa solo la libreria estandar. Salidas en esta carpeta:
  casos_resumen.csv, casos_pasarela.csv, casos_<nombre>.svg
"""
import csv, os, glob
from collections import defaultdict

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
CASOS_DIR = os.path.join(RAIZ, "datasets", "trends_casos")
RES = os.path.join(RAIZ, "runway_gemini", "resultados_gemini.csv")
ULTIMO_MES = 2026 * 12 + 8     # sep-2026

def absmes(y, m): return y * 12 + (m - 1)
def mes_txt(a): return "%04d-%02d" % (a // 12, a % 12 + 1)
def num(x):
    x = x.strip()
    if x.startswith("<"): return 0.5
    try: return float(x)
    except ValueError: return 0.0

CASOS = [
    # nombre, archivo, casa, desfile (a, m), otro hito, terminos a mostrar, contexto
    ("triple_s", "CASO__balenciaga-triple-s_dad-shoes_chunky-sneakers.csv", "Balenciaga Triple S",
     (2017, 1), ("salida a tiendas", (2017, 9)), ["balenciaga triple s", "dad shoes", "chunky sneakers"],
     "Debut en pasarela en enero de 2017; llegada a tiendas en septiembre de 2017."),
    ("rosa_valentino", "CASO__barbiecore_hot-pink_pink-dress.csv", "Rosa de Valentino (Pink PP)",
     (2022, 3), ("pelicula Barbie", (2023, 7)), ["pink dress", "hot pink"],
     "Desfile Pink PP de Valentino, otono-invierno 2022, en marzo de 2022 (Paris). La pelicula Barbie (jul 2023) contamina la senal."),
    ("minifalda_miu_miu", "CASO__mini-skirt_low-rise-skirt_miu-miu.csv", "Minifalda de tiro bajo (Miu Miu)",
     (2021, 10), None, ["mini skirt", "miu miu"],
     "Miu Miu primavera-verano 2022, mostrado el 5 de octubre de 2021. Miu Miu NO esta entre las 14 casas de nuestras fotos."),
]

def leer(path):
    rows = list(csv.reader(open(path, encoding="utf-8")))
    i = [k for k, r in enumerate(rows) if r and r[0] == "Mes"][0]
    terminos = [c.split(":")[0].strip() for c in rows[i][1:]]
    ser = {t: {} for t in terminos}
    for r in rows[i + 1:]:
        if len(r) < len(terminos) + 1 or not r[0]: continue
        y, m = r[0].split("-"); a = absmes(int(y), int(m))
        if a > ULTIMO_MES: continue
        for j, t in enumerate(terminos): ser[t][a] = num(r[j + 1])
    return ser

def prom(s, desde, hasta):
    v = [s[a] for a in range(desde, hasta + 1) if a in s]
    return sum(v) / len(v) if len(v) == hasta - desde + 1 else None

def media_movil(s, k=12):
    out = {}
    for a in sorted(s):
        v = [s[b] for b in range(a - k + 1, a + 1) if b in s]
        if len(v) == k: out[a] = sum(v) / k
    return out

def svg(nombre, titulo, serie_por_term, desfile, hito, nota, crudas=None):
    W, H, ML, MR, MT, MB = 900, 380, 56, 24, 100, 44
    meses = sorted({a for s in serie_por_term.values() for a in s})
    a0, a1 = meses[0], meses[-1]
    # recorte: desde 3 anos antes del desfile
    a0 = max(a0, desfile - 36)
    a1 = min(a1, desfile + 48)      # 4 anos despues; mas alla no se interpreta
    ymax = max(v for s in serie_por_term.values() for a, v in s.items() if a0 <= a <= a1)
    ymax = max(ymax * 1.25, 1)
    X = lambda a: ML + (a - a0) / (a1 - a0) * (W - ML - MR)
    Y = lambda v: H - MB - v / ymax * (H - MT - MB)
    colores = ["#6E2B2B", "#2F5238", "#B58A1B"]
    o = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d" role="img" aria-label="%s" font-family="sans-serif">' % (W, H, W, H, titulo),
         '<rect width="%d" height="%d" fill="#FFFFFF"/>' % (W, H),
         '<text x="%d" y="24" font-size="16" font-weight="600" fill="#1B1A18">%s</text>' % (ML, titulo),
         '<text x="%d" y="42" font-size="11" fill="#5E5850">Linea gruesa: promedio movil de 12 meses. Linea fina: dato mensual. Indice de Google Trends (mundo), todos los terminos en la misma escala.</text>' % ML,
         '<text x="%d" y="58" font-size="11" fill="#5E5850">%s</text>' % (ML, nota)]
    for g in range(0, 5):
        v = ymax * g / 4
        o.append('<line x1="%d" y1="%.1f" x2="%d" y2="%.1f" stroke="#E3DDD3"/>' % (ML, Y(v), W - MR, Y(v)))
        o.append('<text x="%d" y="%.1f" font-size="10" fill="#5E5850" text-anchor="end">%d</text>' % (ML - 6, Y(v) + 3, round(v)))
    for yy in range(a0 // 12 + 1, a1 // 12 + 1):
        x = X(yy * 12)
        o.append('<text x="%.1f" y="%d" font-size="10" fill="#5E5850" text-anchor="middle">%d</text>' % (x, H - MB + 16, yy))
    marcas = [(desfile, "desfile", "#1B1A18"), (desfile + 12, "+12 meses", "#8A8176")] + ([(hito[0], hito[1], "#2F5238")] if hito else [])
    for i, (a, et, col) in enumerate(marcas):
        if a0 <= a <= a1:
            o.append('<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="%s" stroke-dasharray="4 3"/>' % (X(a), MT, X(a), H - MB, col))
            o.append('<text x="%.1f" y="%d" font-size="10" fill="%s" text-anchor="%s">%s</text>' % (X(a), MT - 6 - 11 * (i % 3), col, "start" if i % 2 == 0 else "end", et))
    for i, (t, s) in enumerate(serie_por_term.items()):
        if crudas:
            cr = " ".join("%.1f,%.1f" % (X(a), Y(min(v, ymax))) for a, v in sorted(crudas[t].items()) if a0 <= a <= a1)
            o.append('<polyline points="%s" fill="none" stroke="%s" stroke-opacity="0.3" stroke-width="1"/>' % (cr, colores[i % 3]))
        pts = " ".join("%.1f,%.1f" % (X(a), Y(v)) for a, v in sorted(s.items()) if a0 <= a <= a1)
        o.append('<polyline points="%s" fill="none" stroke="%s" stroke-width="2.2"/>' % (pts, colores[i % 3]))
        o.append('<text x="%d" y="%d" font-size="11" fill="%s">%s</text>' % (ML + 8 + i * 190, H - 8, colores[i % 3], "— " + t))
    o.append("</svg>")
    open(os.path.join(AQUI, "casos_%s.svg" % nombre), "w", encoding="utf-8").write("\n".join(o))

filas = []
for nombre, arch, titulo, (dy, dm), hito, terminos, ctx in CASOS:
    ser = leer(os.path.join(CASOS_DIR, arch))
    d = absmes(dy, dm)
    mm_todas = {}; crudas = {}
    for t in terminos:
        s = ser[t]
        base = prom(s, d - 12, d - 1)
        w1 = prom(s, d + 1, d + 12); w2 = prom(s, d + 13, d + 24); w3 = prom(s, d + 25, d + 36)
        mm = media_movil(s); mm_todas[t] = mm; crudas[t] = s
        pico = max(((a, v) for a, v in mm.items() if a > d), key=lambda x: x[1])
        filas.append([nombre, t, mes_txt(d), round(base, 2), round(w1, 2) if w1 is not None else "",
                      round(w2, 2) if w2 is not None else "", round(w3, 2) if w3 is not None else "",
                      mes_txt(pico[0]), round(pico[0] - d), round(pico[1], 1)])
    hito_arg = (absmes(*hito[1]), hito[0]) if hito else None
    svg(nombre, titulo, mm_todas, d, hito_arg, ctx, crudas)

with open(os.path.join(AQUI, "casos_resumen.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["caso", "termino", "mes_desfile", "base_12m_previos", "ano_1_(+1..+12)", "ano_2_(+13..+24)", "ano_3_(+25..+36)",
                "mes_pico_media_movil", "meses_hasta_pico", "valor_pico_media_movil"])
    w.writerows(filas)

# --- que mostraban nuestras fotos
filas_f = [r for r in csv.DictReader(open(RES, encoding="utf-8")) if not (r.get("error") or "").strip()]
por = defaultdict(list)
for r in filas_f: por[(r["temporada"], int(r["anio"]))].append(r)
sal = []
def pct(k, f):
    L = por[k]; return 100.0 * sum(1 for x in L if f(x)) / len(L), len(L)
rosa = {k: pct(k, lambda x: x["color_dominante"] == "Rosa")[0] for k in por}
fw_prev = [rosa[k] for k in rosa if k[0] == "FW" and k[1] < 2022]
sal.append(["rosa", "FW2022", round(rosa[("FW", 2022)], 1), round(sum(fw_prev) / len(fw_prev), 1), len(fw_prev),
            "otono-invierno 2022 vs promedio de otono-invierno 2011-2021"])
casas_rosa = [x["marca"] for x in por[("FW", 2022)] if x["color_dominante"] == "Rosa"]
sal.append(["rosa", "FW2022_casas_con_rosa", "; ".join("%s=%d" % (c, casas_rosa.count(c)) for c in sorted(set(casas_rosa))), "", "", ""])
mini = {k: pct(k, lambda x: x["largo"] == "Mini")[0] for k in por}
ss_prev = [mini[k] for k in mini if k[0] == "SS" and k[1] != 2022]
sal.append(["mini", "SS2022", round(mini[("SS", 2022)], 1), round(sum(ss_prev) / len(ss_prev), 1), len(ss_prev),
            "primavera-verano 2022 vs promedio de las otras primavera-verano"])
with open(os.path.join(AQUI, "casos_pasarela.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["caso", "temporada_o_dato", "valor_%_o_detalle", "promedio_resto_%", "n_temporadas_resto", "nota"])
    w.writerows(sal)

for r in filas: print(r)
for r in sal: print(r)
