# Aplica REGLAS_BRIEF_2025.txt: veredicto de SS2025, chequeo de validez (V1, V2, V3), sensibilidades (S1, S2)
# y prueba de factibilidad del segundo anio. Uso: python3 -I brief_ss2025.py > salida_brief_ss2025.txt
# Escribe brief_ss2025_detalle.csv y ../../app/datos/brief_ss2025.json
import csv, json, math, os, statistics as st, sys
AQUI = os.path.dirname(os.path.abspath(__file__))
B26 = os.path.join(AQUI, "..", "brief_2026")
sys.path.insert(0, os.path.join(AQUI, "..", "microtendencias"))
import m1  # noqa: E402

def am(s): y, m = s.split("-"); return int(y) * 12 + int(m) - 1
def ma(i): return f"{i // 12}-{i % 12 + 1:02d}"
def leer(p):
    ser = {}
    for r in csv.DictReader(open(p, encoding="utf-8")):
        ser.setdefault(r["termino"], {})[am(r["mes"])] = float(r["valor"])
    return ser
def rows(p): return list(csv.DictReader(open(p, encoding="utf-8")))
def prom(s, a, b):
    v = [s[k] for k in range(am(a), am(b) + 1) if k in s]
    return st.mean(v) if len(v) == am(b) - am(a) + 1 else None
def lr(a, b): return math.log(a / b) if a and b and a > 0 and b > 0 else None
def sp(x, y):
    par = [(a, b) for a, b in zip(x, y) if a is not None and b is not None]
    if len(par) < 6: return None, None, len(par)
    r, p = m1.spearman([a for a, _ in par], [b for _, b in par]); return r, p, len(par)
def fmt(r): return "n/d" if r[0] is None else f"{r[0]:+.2f} (p={r[1]:.3f}, n={r[2]})"
def ver(g): return "Tiende a quedarse" if g >= 0.10 else ("Riesgo de moda pasajera" if g <= -0.10 else "Sin señal clara")
def sd_res(xs, ys):
    mx, my = st.mean(xs), st.mean(ys)
    b = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sum((x - mx) ** 2 for x in xs)
    return st.stdev([y - (my + b * (x - mx)) for x, y in zip(xs, ys)]), b

D = os.path.join(AQUI, "datos")
A = leer(os.path.join(D, "trends_A_2011_2025-09.csv"))
A24 = leer(os.path.join(B26, "datos", "trends_2024_web.csv"))
B = leer(os.path.join(D, "trends_B_2024_2026.csv"))
VOL = {r["termino"]: (float(r["volumen"]) if r["volumen"] != "" else None) for r in rows(os.path.join(D, "volumen_ancla.csv"))}
T25 = [t for t in rows(os.path.join(AQUI, "terminos_declarados_2025.csv")) if t["termino"]]
T24 = [t for t in rows(os.path.join(B26, "terminos_declarados_2024.csv")) if t["termino"]]
T26 = [t for t in rows(os.path.join(B26, "terminos_declarados_2026.csv")) if t["termino"]]
FU = {f["medio"]: f for f in rows(os.path.join(AQUI, "fuentes_listas_2025.csv"))}
DET24 = [r for r in rows(os.path.join(B26, "brief_2024_detalle.csv")) if r["usable"] == "si"]
out = ["BRIEF SS2025 (reglas en REGLAS_BRIEF_2025.txt)", ""]

# Lectura principal
filas = []
for t in T25:
    s, e = A[t["termino"]], am(t["mes_desfile"])
    falta = [ma(k) for k in range(e - 12, e + 12) if k not in s]
    if falta: sys.exit(f"Faltan meses para {t['termino']}: {falta}")
    w = [s[k] for k in range(e - 12, e + 12)]
    B0, B1 = st.mean(w[:12]), st.mean(w[12:])
    ceros = sum(1 for x in w if x == 0)
    picos = []
    for lab, ww, a in (("año previo", w[:12], e - 12), ("primer año", w[12:], e)):
        md = st.median(ww)
        if md > 0 and max(ww) >= 5 * md: picos.append(f"{lab}: {ma(a + ww.index(max(ww)))}")
    f = dict(t, B0=B0, B1=B1, ceros=ceros, usable=ceros <= 8 and B0 > 0 and B1 > 0,
             aviso=("Lectura apoyada en un pico de un solo mes (" + "; ".join(picos) + ")") if picos else "",
             vol=VOL.get(t["termino"]))
    if f["usable"]:
        f["r1"] = math.log(B1 / B0)
        f["s1"] = lr(prom(s, "2024-10", "2024-12"), prom(s, "2023-10", "2023-12"))
        f["s2"] = lr(prom(s, "2024-10", "2025-07"), prom(s, "2023-10", "2024-07"))
        f["paso"] = None
        x, y = lr(prom(s, "2025-01", "2025-03"), prom(s, "2024-10", "2024-12")), lr(prom(s, "2024-01", "2024-03"), prom(s, "2023-10", "2023-12"))
        if x is not None and y is not None: f["paso"] = x - y
        f["salto"] = lr(prom(B[t["termino"]], "2026-02", "2026-05"), prom(B[t["termino"]], "2025-10", "2026-01"))
    filas.append(f)
ok = [f for f in filas if f["usable"]]
med = st.median(f["r1"] for f in ok)
for k in ("s1", "s2"):
    mk = st.median(f[k] for f in ok if f[k] is not None)
    for f in ok: f["g" + k] = None if f[k] is None else f[k] - mk
for f in ok:
    f["g1"] = f["r1"] - med; f["veredicto"] = ver(f["g1"])
    f["confianza"] = "" if abs(f["g1"]) < 0.10 else ("Alta" if abs(f["g1"]) >= 0.30 else "Media")
    if f["gs1"] is not None and ((f["g1"] >= 0.10 and f["gs1"] <= -0.10) or (f["g1"] <= -0.10 and f["gs1"] >= 0.10)):
        f["aviso"] = (f["aviso"] + " | " if f["aviso"] else "") + "La lectura de oct-dic va en sentido contrario"
out.append(f"SS2025: {len(filas)} terminos, {len(ok)} usables")
for f in filas:
    if not f["usable"]: out.append(f"   descartado por volumen: {f['termino']} ({f['ceros']} meses en cero)")
for f in sorted(ok, key=lambda f: -f["g1"]):
    v = "n/d" if f["vol"] is None else f"{f['vol']:.3f}"
    out.append(f"   {f['termino']:20s} g1 {f['g1']:+.2f}  {f['veredicto']:24s} {f['confianza']:6s} vol {v:>7s}  {f['aviso']}")
cnt = {}
for f in ok: cnt[f["veredicto"]] = cnt.get(f["veredicto"], 0) + 1
out.append("   total: " + " | ".join(f"{k}: {v}" for k, v in sorted(cnt.items())))

# Chequeo de validez
out += ["", "CHEQUEO DE VALIDEZ (falla si |rho| >= 0.5)"]
g = [f["g1"] for f in ok]
v1 = sp(g, [f["vol"] for f in ok])
v2 = sp(g, [f["salto"] for f in ok])
v3 = sp([f["paso"] for f in ok], [f["vol"] for f in ok])
d24 = {r["termino"]: float(r["g1"]) for r in DET24}
r24 = [(d24[t], VOL.get(t), lr(prom(B[t], "2026-02", "2026-05"), prom(B[t], "2025-10", "2026-01"))) for t in d24 if t in B]
v1r = sp([a for a, _, _ in r24], [b for _, b, _ in r24])
v2r = sp([a for a, _, _ in r24], [c for _, _, c in r24])
paso24 = []
for t in d24:
    s = A24[t]; x = lr(prom(s, "2024-01", "2024-03"), prom(s, "2023-10", "2023-12")); y = lr(prom(s, "2023-01", "2023-03"), prom(s, "2022-10", "2022-12"))
    paso24.append((None if x is None or y is None else x - y, VOL.get(t)))
v3r = sp([a for a, _ in paso24], [b for _, b in paso24])
pasos_todos = []
for t in {x["termino"] for x in T25 + T26}:
    s = A.get(t, {}); x = lr(prom(s, "2025-01", "2025-03"), prom(s, "2024-10", "2024-12")); y = lr(prom(s, "2024-01", "2024-03"), prom(s, "2023-10", "2023-12"))
    if x is not None and y is not None: pasos_todos.append((x - y, VOL.get(t)))
v3t = sp([a for a, _ in pasos_todos], [b for _, b in pasos_todos])
falla1 = v1[0] is not None and abs(v1[0]) >= 0.5
v2_sirve = not (v2r[0] is not None and abs(v2r[0]) >= 0.5)
falla2 = v2_sirve and v2[0] is not None and abs(v2[0]) >= 0.5
falla3 = v3[0] is not None and abs(v3[0]) >= 0.5
out.append(f"   V1 g1 vs volumen:            SS2025 {fmt(v1)}  -> {'FALLA' if falla1 else 'pasa'}   | referencia 2024 {fmt(v1r)}")
out.append(f"   V2 g1 vs salto feb-may 2026: SS2025 {fmt(v2)}  -> {'FALLA' if falla2 else ('pasa' if v2_sirve else 'no concluyente (la referencia 2024 tambien correlaciona)')}   | referencia 2024 {fmt(v2r)}")
out.append(f"   V3 paso ene-2025 vs volumen: SS2025 {fmt(v3)}  -> {'FALLA' if falla3 else 'pasa'}   | pase ene-2024 (2024) {fmt(v3r)} | todos los terminos con A {fmt(v3t)}")
mp = [f["paso"] for f in ok if f["paso"] is not None]
out.append(f"   mediana del paso ene-2025 (contra el pase del anio anterior): {st.median(mp):+.2f} (lo descuenta la mediana de la temporada)")
pasa = not (falla1 or falla2 or falla3)
out.append(f"   RESULTADO: {'PASA: SS2025 lleva veredicto' if pasa else 'NO PASA: SS2025 va sin veredicto'}")

# Sensibilidades
out += ["", "SENSIBILIDADES (descriptivas)"]
s1 = sp(g, [f["gs1"] for f in ok]); s2 = sp(g, [f["gs2"] for f in ok])
cambia2 = sum(1 for f in ok if f["gs2"] is not None and ver(f["gs2"]) != f["veredicto"])
contra1 = [f["termino"] for f in ok if "sentido contrario" in f["aviso"]]
out.append(f"   S1 oct-dic (no cruza ene-2025): Spearman con g1 {fmt(s1)} (referencia limpia: mediana +0.68, minimo -0.03); en sentido contrario: {', '.join(contra1) or 'ninguno'}")
out.append(f"   S2 oct-jul (sin la suba de ago-2025): Spearman con g1 {fmt(s2)}; veredictos que cambian: {cambia2} de {len(ok)}")

# Segundo anio
out += ["", "SEGUNDO ANIO: factibilidad de corregir por volumen"]
def a_de(t): return A[t] if t in A else A24.get(t, {})
pts26, pts24 = [], []
for t in sorted({x["termino"] for x in T25 + T24 + T26}):
    vol = VOL.get(t)
    if not vol: continue
    j26 = lr(prom(B.get(t, {}), "2026-02", "2026-05"), prom(B.get(t, {}), "2025-02", "2025-05"))
    j24 = lr(prom(a_de(t), "2024-02", "2024-05"), prom(a_de(t), "2023-02", "2023-05"))
    if j26 is not None: pts26.append((math.log(vol), j26))
    if j24 is not None: pts24.append((math.log(vol), j24))
sd26, b26 = sd_res([x for x, _ in pts26], [y for _, y in pts26])
sd24, b24 = sd_res([x for x, _ in pts24], [y for _, y in pts24])
fact = sd26 <= 1.25 * sd24
out.append(f"   J26 (feb-may 2026 vs 2025): n={len(pts26)}, mediana {st.median(y for _, y in pts26):+.2f}, pendiente vs log(volumen) {b26:+.2f}, desvio de residuos {sd26:.2f}")
out.append(f"   J24 (feb-may 2024 vs 2023): n={len(pts24)}, mediana {st.median(y for _, y in pts24):+.2f}, pendiente vs log(volumen) {b24:+.2f}, desvio de residuos {sd24:.2f}")
out.append(f"   cociente {sd26 / sd24:.2f} (limite 1.25) -> {'FACTIBLE' if fact else 'NO FACTIBLE: el segundo anio no se puede chequear limpio con Google Trends'}")
rv = sp([x for x, _ in pts26], [y for _, y in pts26])
out.append(f"   (Spearman volumen real vs J26: {fmt(rv)})")
if fact:
    out.append("   c2 corregido por volumen (experimental):")
    fac = {}
    for f in ok:
        s, b = A[f["termino"]], B[f["termino"]]
        comun = [k for k in b if k in s]
        fac[f["termino"]] = sum(s[k] for k in comun) / sum(b[k] for k in comun) if sum(b[k] for k in comun) > 0 else None
    raw = []
    for f in ok:
        b2 = prom(B[f["termino"]], "2025-10", "2026-09")
        raw.append((f, None if not f["vol"] or not fac[f["termino"]] or not b2 else math.log(b2 * fac[f["termino"]] / f["B1"])))
    xs = [(math.log(f["vol"]), c) for f, c in raw if c is not None]
    _, bb = sd_res([x for x, _ in xs], [y for _, y in xs]); mx, my = st.mean(x for x, _ in xs), st.mean(y for _, y in xs)
    for f, c in raw:
        if c is None: continue
        f["c2_corr"] = c - (my + bb * (math.log(f["vol"]) - mx))
        out.append(f"      {f['termino']:20s} {f['veredicto']:24s} c2 corregido {f['c2_corr']:+.2f}  {'se quedo' if f['c2_corr'] >= -0.10 else 'pasajera'}")

# Archivos
with open(os.path.join(AQUI, "brief_ss2025_detalle.csv"), "w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh)
    w.writerow(["medio", "tendencia_fuente", "termino", "tipo", "usable", "B0", "B1", "g1", "veredicto", "confianza", "aviso", "volumen", "salto_2026", "paso_ene2025", "g1_octdic", "g1_octjul", "c2_corregido"])
    for f in filas:
        n = lambda k, d=3: "" if f.get(k) is None else f"{f[k]:.{d}f}"
        w.writerow([f["medio"], f["tendencia_fuente"], f["termino"], f["tipo"], "si" if f["usable"] else "no", n("B0", 2), n("B1", 2), n("g1"),
                    f.get("veredicto", ""), f.get("confianza", ""), f["aviso"], n("vol", 5), n("salto"), n("paso"), n("gs1"), n("gs2"), n("c2_corr")])
desde, hasta = am("2019-01"), am("2026-09")
motivo = "" if pasa else "Sin veredicto: la lectura de SS2025 no pasó el chequeo de validez fijado de antemano (ver analisis/brief_2025/salida_brief_ss2025.txt)."
items = []
for f in filas:
    if not f["usable"]: continue
    fu = FU[f["medio"]]
    d = {"temporada": "SS2025", "termino": f["termino"], "tipo": f["tipo"], "tendencia_fuente": f["tendencia_fuente"], "medio": f["medio"],
         "url_fuente": fu["url"], "fecha_fuente": fu["fecha_publicacion"], "mes_desfile": f["mes_desfile"],
         "serie": [None if k not in A[f["termino"]] else int(A[f["termino"]][k]) for k in range(desde, hasta + 1)]}
    if pasa: d.update(g1=round(f["g1"], 3), veredicto=f["veredicto"], confianza=f["confianza"], aviso=f["aviso"],
                      sin_ago_sep_2025=None if f["gs2"] is None else ver(f["gs2"]))  # descriptivo (S2), agregado despues de ver los resultados
    else: d.update(veredicto=None, nota=motivo)
    items.append(d)
meta = {"meses": [ma(k) for k in range(desde, hasta + 1)], "temporada": "SS2025", "con_veredicto": pasa,
        "chequeo": {"V1_volumen": v1[0], "V2_salto_2026": v2[0], "V3_paso_ene2025": v3[0], "limite": 0.5},
        "segundo_anio_factible": fact, "serie_nota": "Serie 0-100 de la bajada ene-2011 a sep-2025; null después.",
        "fuentes": list(FU.values()), "generado_de": "analisis/brief_2025/"}
json.dump({"meta": meta, "items": items}, open(os.path.join(AQUI, "..", "..", "app", "datos", "brief_ss2025.json"), "w", encoding="utf-8"),
          ensure_ascii=False, separators=(",", ":"))
print("\n".join(out))
