# Prueba M1 (reglas en REGLAS_MICROTENDENCIAS.txt, fijadas antes de bajar datos).
# Uso: python3 -I m1.py  (desde esta carpeta)
import csv, math, random, statistics as st
from collections import defaultdict
from math import comb

AQUI = __file__.rsplit("/", 1)[0] if "/" in __file__ else "."

def am(s):  # "2019-10" -> indice absoluto de mes
    y, m = s.split("-"); return int(y) * 12 + int(m) - 1

def cargar(nombre):
    ser = defaultdict(dict)
    with open(f"{AQUI}/datos/{nombre}", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            ser[r["termino"]][am(r["mes"])] = float(r["valor"])
    return ser

def leer_terms(archivo):
    return [t for t in csv.DictReader(open(f"{AQUI}/{archivo}", encoding="utf-8")) if t["termino"]]
terms = leer_terms("terminos_declarados.csv")

def fisher(a, b, c, d):  # dos colas
    n = a + b + c + d; r1 = a + b; c1 = a + c
    def p(x): return comb(r1, x) * comb(n - r1, c1 - x) / comb(n, c1)
    p0 = p(a); lo = max(0, c1 - (n - r1)); hi = min(r1, c1)
    return min(1.0, sum(p(x) for x in range(lo, hi + 1) if p(x) <= p0 * (1 + 1e-9)))

def spearman(x, y):
    def rk(v):
        o = sorted(range(len(v)), key=lambda i: v[i]); r = [0] * len(v); i = 0
        while i < len(v):
            j = i
            while j + 1 < len(v) and v[o[j + 1]] == v[o[i]]: j += 1
            for k in range(i, j + 1): r[o[k]] = (i + j) / 2
            i = j + 1
        return r
    a, b = rk(x), rk(y); ma, mb = st.mean(a), st.mean(b)
    num = sum((p - ma) * (q - mb) for p, q in zip(a, b))
    den = math.sqrt(sum((p - ma) ** 2 for p in a) * sum((q - mb) ** 2 for q in b))
    rho = num / den
    random.seed(1); cnt = 0; bb = b[:]
    for _ in range(5000):
        random.shuffle(bb)
        r2 = sum((p - ma) * (q - mb) for p, q in zip(a, bb)) / den
        if abs(r2) >= abs(rho) - 1e-12: cnt += 1
    return rho, (cnt + 1) / 5001

def medir(ser, terms=None):
    terms = terms or leer_terms("terminos_declarados.csv")
    filas = []
    for t in terms:
        s = ser.get(t["termino"]); e = am(t["mes_desfile"])
        if not s: filas.append(dict(t, usable="no", motivo="sin datos")); continue
        win = [s.get(e + k, 0.0) for k in range(-12, 24)]
        B0 = st.mean(win[0:12]); B1 = st.mean(win[12:24]); B2 = st.mean(win[24:36])
        ceros = sum(1 for v in win if v == 0)
        if ceros > 12 or min(B0, B1, B2) <= 0:
            filas.append(dict(t, usable="no", motivo=f"volumen bajo ({ceros} meses en cero)", B0=B0, B1=B1, B2=B2)); continue
        filas.append(dict(t, usable="si", motivo="", B0=B0, B1=B1, B2=B2,
                          r1=math.log(B1 / B0), r2=math.log(B2 / B1), ceros=ceros))
    ok = [f for f in filas if f["usable"] == "si"]
    por_t = defaultdict(list)
    for f in ok: por_t[f["temporada"]].append(f)
    for tem, fs in por_t.items():
        m1 = st.median(f["r1"] for f in fs); m2 = st.median(f["r2"] for f in fs)
        for f in fs:
            f["g1"] = f["r1"] - m1; f["c2"] = f["r2"] - m2
            f["grupo"] = "SUBE" if f["g1"] >= 0.10 else ("CAE" if f["g1"] <= -0.10 else "PLANO")
    return filas, ok

def tabla(ok, cond, etiqueta, out):
    g = {k: [f for f in ok if f["grupo"] == k] for k in ("SUBE", "PLANO", "CAE")}
    q = {k: sum(1 for f in v if cond(f)) for k, v in g.items()}
    otros_n = len(g["PLANO"]) + len(g["CAE"]); otros_q = q["PLANO"] + q["CAE"]
    ps = q["SUBE"] / len(g["SUBE"]) if g["SUBE"] else float("nan")
    po = otros_q / otros_n if otros_n else float("nan")
    p = fisher(q["SUBE"], len(g["SUBE"]) - q["SUBE"], otros_q, otros_n - otros_q)
    out.append(f"  {etiqueta}")
    for k in g:
        n = len(g[k]); out.append(f"     {k:5s}: se queda {q[k]}/{n} = {100*q[k]/n:.0f}%" if n else f"     {k}: 0 casos")
    out.append(f"     SUBE {100*ps:.0f}% vs PLANO+CAE {100*po:.0f}% -> diferencia {100*(ps-po):+.0f} pts | Fisher p={p:.3f}")
    return ps - po, p

def correr(nombre, titulo, out, principal_solo=False, terms_file="terminos_declarados.csv"):
    filas, ok = medir(cargar(nombre), leer_terms(terms_file))
    out.append("=" * 78); out.append(f"{titulo}  ({nombre})")
    out.append(f"  terminos: {len(filas)} | usables: {len(ok)} | descartados: {len(filas)-len(ok)}")
    for f in filas:
        if f["usable"] != "si": out.append(f"     descartado: {f['termino']} ({f['motivo']})")
    res = {}
    res["principal"] = tabla(ok, lambda f: f["c2"] >= -0.10, "PRINCIPAL: se queda = c2 >= -0.10", out)
    if not principal_solo:
        res["sec1"] = tabla(ok, lambda f: f["c2"] > 0, "SECUNDARIO 1: c2 > 0", out)
        res["sec2"] = tabla(ok, lambda f: f["B2"] / f["B1"] >= 0.9, "SECUNDARIO 2: B2/B1 >= 0.9 (sin restar mediana)", out)
        rho, p = spearman([f["g1"] for f in ok], [f["c2"] for f in ok])
        out.append(f"  Spearman g1 vs c2 (continuo): rho={rho:.2f}, p={p:.3f}")
        res["rho"] = (rho, p)
    d, p = res["principal"]
    out.append(f"  CRITERIO (>= +10 pts y p < 0.05): {'APOYA' if d >= 0.10 and p < 0.05 else 'NO APOYA'}")
    return filas, ok, res

if __name__ == "__main__":
    out = []
    filas, ok, res = correr("trends_microtendencias_web.csv", "M1 - Google busqueda web, MUNDO", out)
    try:
        correr("trends_microtendencias_shopping.csv", "SECUNDARIO 3 - Google Shopping, MUNDO", out, principal_solo=True)
    except FileNotFoundError:
        out.append("Shopping: archivo no disponible")
    # detalle por termino
    with open(f"{AQUI}/m1_detalle.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["temporada", "termino", "tipo", "tendencia_fuente", "usable", "B0", "B1", "B2", "g1", "c2", "grupo", "se_queda"])
        for r in filas:
            if r["usable"] == "si":
                w.writerow([r["temporada"], r["termino"], r["tipo"], r["tendencia_fuente"], "si",
                            f"{r['B0']:.2f}", f"{r['B1']:.2f}", f"{r['B2']:.2f}", f"{r['g1']:.3f}", f"{r['c2']:.3f}",
                            r["grupo"], "si" if r["c2"] >= -0.10 else "no"])
            else:
                w.writerow([r["temporada"], r["termino"], r["tipo"], r["tendencia_fuente"], "no"] + [""] * 7)
    print("\n".join(out))
