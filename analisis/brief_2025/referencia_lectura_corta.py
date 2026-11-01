# Referencia limpia (datos hasta 2024) para la sensibilidad de SS2025: cuanto coincide la lectura corta
# (oct-dic despues del desfile contra oct-dic del anio anterior) con la lectura de 12 meses, en temporadas SS sin el problema de Google.
# Se corre ANTES de bajar datos de SS2025. Uso: python3 -I referencia_lectura_corta.py
import csv, math, os, statistics as st, sys
AQUI = os.path.dirname(os.path.abspath(__file__)); A = os.path.join(AQUI, "..")
sys.path.insert(0, os.path.join(A, "microtendencias")); import m1  # noqa: E402
def am(s): y, m = s.split("-"); return int(y) * 12 + int(m) - 1
def serie(p):
    s = {}
    for r in csv.DictReader(open(p, encoding="utf-8")):
        if r.get("geo", "MUNDO") in ("MUNDO", "", None): s.setdefault(r["termino"], {})[am(r["mes"])] = float(r["valor"])
    return s
def terms(p): return [t for t in csv.DictReader(open(p, encoding="utf-8")) if t["termino"]]
MUESTRAS = [("C1", "hipotesis/datos/trends_c1_web.csv", "hipotesis/terminos_declarados_c1.csv"),
            ("M1", "microtendencias/datos/trends_microtendencias_web.csv", "microtendencias/terminos_declarados.csv"),
            ("M2", "microtendencias/datos/trends_microtendencias_web_m2.csv", "microtendencias/terminos_declarados_m2.csv"),
            ("B24", "brief_2026/datos/trends_2024_web.csv", "brief_2026/terminos_declarados_2024.csv")]
def ver(g): return "Q" if g >= 0.10 else ("P" if g <= -0.10 else "N")
res = []
for nom, fs, ft in MUESTRAS:
    S = serie(os.path.join(A, fs)); T = terms(os.path.join(A, ft))
    for tem in sorted({t["temporada"] for t in T if t["temporada"].startswith("SS")}):
        filas = []
        for t in T:
            if t["temporada"] != tem or t["termino"] not in S: continue
            s, e = S[t["termino"]], am(t["mes_desfile"])
            if any(k not in s for k in range(e - 12, e + 12)): continue
            w = [s[k] for k in range(e - 12, e + 12)]
            B0, B1, c0, c1 = st.mean(w[:12]), st.mean(w[12:]), st.mean(w[:3]), st.mean(w[12:15])
            if sum(1 for x in w if x == 0) > 8 or min(B0, B1, c0, c1) <= 0: continue
            filas.append((math.log(B1 / B0), math.log(c1 / c0)))
        if len(filas) < 6: continue
        m12, m3 = st.median(f[0] for f in filas), st.median(f[1] for f in filas)
        g = [f[0] - m12 for f in filas]; q = [f[1] - m3 for f in filas]
        rho, _ = m1.spearman(g, q)
        con = [(ver(a), ver(b)) for a, b in zip(g, q)]
        igual = sum(1 for a, b in con if a == b) / len(con)
        contra = sum(1 for a, b in con if {a, b} == {"Q", "P"})
        res.append((nom, tem, len(filas), rho, igual, contra))
        print(f"{nom} {tem}: n={len(filas):2d}  Spearman 12m vs oct-dic = {rho:+.2f}  mismo veredicto {igual:.0%}  opuestos {contra}")
print(f"MINIMO Spearman en temporadas SS limpias: {min(r[3] for r in res):+.2f} | mediana {st.median(r[3] for r in res):+.2f}")
print(f"Mismo veredicto: minimo {min(r[4] for r in res):.0%} | mediana {st.median(r[4] for r in res):.0%}")
