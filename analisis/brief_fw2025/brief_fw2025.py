# Aplica REGLAS_BRIEF_FW2025.txt: veredicto de FW2025 y chequeo de validez (V1, V3, V4; V2 solo se informa).
# Uso: python3 -I brief_fw2025.py > salida_brief_fw2025.txt
# Escribe brief_fw2025_detalle.csv y ../../app/datos/brief_fw2025.json
import csv, json, math, os, statistics as st, sys
AQUI = os.path.dirname(os.path.abspath(__file__))
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

D = os.path.join(AQUI, "datos")
A = leer(os.path.join(D, "trends_A_2011_2025-09.csv"))
B = leer(os.path.join(D, "trends_B_2024_2026.csv"))
VOL = {r["termino"]: (float(r["volumen"]) if r["volumen"] != "" else None) for r in rows(os.path.join(D, "volumen_ancla.csv"))}
TF = [t for t in rows(os.path.join(AQUI, "terminos_declarados_fw2025.csv")) if t["termino"]]
FU = {f["medio"]: f for f in rows(os.path.join(AQUI, "fuentes_listas_fw2025.csv"))}
out = ["BRIEF FW2025 (reglas en REGLAS_BRIEF_FW2025.txt)", ""]

# Serie mensual: A hasta sep-2025 y, despues, B llevada a la escala de A con el cociente de sumas en ene-2024 a sep-2025
UNION = {}
for t in TF:
    k = t["termino"]; a, b = A[k], B[k]
    comun = [m for m in range(am("2024-01"), am("2025-09") + 1) if m in a and m in b]
    sb = sum(b[m] for m in comun)
    fac = sum(a[m] for m in comun) / sb if sb > 0 else None
    s = dict(a)
    if fac is not None:
        for m, v in b.items():
            if m > am("2025-09"): s[m] = v * fac
    UNION[k] = s

filas = []
e = am("2025-03")
for t in TF:
    s = UNION[t["termino"]]
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
        f["corto"] = lr(prom(s, "2025-03", "2025-07"), prom(s, "2024-03", "2024-07"))
        x, y = lr(prom(s, "2025-01", "2025-02"), prom(s, "2024-10", "2024-12")), lr(prom(s, "2024-01", "2024-02"), prom(s, "2023-10", "2023-12"))
        f["paso"] = None if x is None or y is None else x - y
        f["salto"] = lr(prom(B[t["termino"]], "2026-02", "2026-05"), prom(B[t["termino"]], "2025-10", "2026-01"))
    filas.append(f)
ok = [f for f in filas if f["usable"]]
med = st.median(f["r1"] for f in ok)
mc = st.median(f["corto"] for f in ok if f["corto"] is not None)
for f in ok:
    f["g1"] = f["r1"] - med; f["veredicto"] = ver(f["g1"])
    f["confianza"] = "" if abs(f["g1"]) < 0.10 else ("Alta" if abs(f["g1"]) >= 0.30 else "Media")
    f["gc"] = None if f["corto"] is None else f["corto"] - mc
out.append(f"FW2025: {len(filas)} terminos, {len(ok)} usables")
for f in filas:
    if not f["usable"]: out.append(f"   descartado por volumen: {f['termino']} ({f['ceros']} meses en cero)")
for f in sorted(ok, key=lambda f: -f["g1"]):
    v = "n/d" if f["vol"] is None else f"{f['vol']:.3f}"
    c = "n/d" if f["gc"] is None else f"{f['gc']:+.2f}"
    out.append(f"   {f['termino']:18s} g1 {f['g1']:+.2f}  {f['veredicto']:24s} {f['confianza']:6s} mar-jul {c:>6s}  vol {v:>7s}  {f['aviso']}")
cnt = {}
for f in ok: cnt[f["veredicto"]] = cnt.get(f["veredicto"], 0) + 1
out.append("   total: " + " | ".join(f"{k}: {v}" for k, v in sorted(cnt.items())))

# Chequeo de validez
out += ["", "CHEQUEO DE VALIDEZ"]
g = [f["g1"] for f in ok]
v1 = sp(g, [f["vol"] for f in ok])
v3 = sp([f["paso"] for f in ok], [f["vol"] for f in ok])
v4 = sp(g, [f["gc"] for f in ok])
opuestos = [f["termino"] for f in ok if f["gc"] is not None and {ver(f["g1"]), ver(f["gc"])} == {"Tiende a quedarse", "Riesgo de moda pasajera"}]
v2 = sp(g, [f["salto"] for f in ok])
falla1 = v1[0] is not None and abs(v1[0]) >= 0.5
falla3 = v3[0] is not None and abs(v3[0]) >= 0.5
falla4 = v4[0] is None or v4[0] < 0.50 or len(opuestos) > 1
out.append(f"   V1 g1 vs volumen (falla si |rho| >= 0.5):          {fmt(v1)}  -> {'FALLA' if falla1 else 'pasa'}")
out.append(f"   V3 paso ene-2025 vs volumen (falla si |rho| >= 0.5): {fmt(v3)}  -> {'FALLA' if falla3 else 'pasa'}")
out.append(f"   V4 12 meses vs mar-jul (falla si rho < 0.50 o mas de 1 opuesto): {fmt(v4)}; opuestos: {', '.join(opuestos) or 'ninguno'}  -> {'FALLA' if falla4 else 'pasa'}")
out.append(f"      referencia limpia (temporadas FW 2016-2024): mediana +0.75, minimo +0.05; 8 de 9 dan +0.50 o mas")
out.append(f"   V2 g1 vs salto feb-may 2026 (solo se informa, no decide): {fmt(v2)}")
pasa = not (falla1 or falla3 or falla4)
out.append(f"   RESULTADO: {'PASA: FW2025 lleva veredicto' if pasa else 'NO PASA: FW2025 no va a la pagina'}")

# Archivos
with open(os.path.join(AQUI, "brief_fw2025_detalle.csv"), "w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh)
    w.writerow(["medio", "tendencia_fuente", "termino", "tipo", "usable", "B0", "B1", "g1", "veredicto", "confianza", "aviso", "volumen", "paso_ene2025", "g1_marjul", "salto_2026"])
    for f in filas:
        n = lambda k, d=3: "" if f.get(k) is None else f"{f[k]:.{d}f}"
        w.writerow([f["medio"], f["tendencia_fuente"], f["termino"], f["tipo"], "si" if f["usable"] else "no", n("B0", 2), n("B1", 2), n("g1"),
                    f.get("veredicto", ""), f.get("confianza", ""), f["aviso"], n("vol", 5), n("paso"), n("gc"), n("salto")])
desde, hasta = am("2019-01"), am("2026-09")
motivo = "" if pasa else "FW2025 no pasó el chequeo de validez fijado de antemano (ver analisis/brief_fw2025/salida_brief_fw2025.txt): no va a la página."
items = []
if pasa:
    for f in ok:
        fu = FU[f["medio"]]
        items.append({"temporada": "FW2025", "termino": f["termino"], "tipo": f["tipo"], "tendencia_fuente": f["tendencia_fuente"], "medio": f["medio"],
                      "url_fuente": fu["url"], "fecha_fuente": fu["fecha_publicacion"], "mes_desfile": f["mes_desfile"],
                      "serie": [None if k not in UNION[f["termino"]] else round(UNION[f["termino"]][k], 1) for k in range(desde, hasta + 1)],
                      "g1": round(f["g1"], 3), "veredicto": f["veredicto"], "confianza": f["confianza"], "aviso": f["aviso"],
                      # descriptivo, agregado despues de ver los resultados (no cambia el veredicto): la lectura con solo mar-jul
                      "lectura_marjul": None if f["gc"] is None else ver(f["gc"])})
meta = {"meses": [ma(k) for k in range(desde, hasta + 1)], "temporada": "FW2025", "con_veredicto": pasa, "motivo": motivo,
        "chequeo": {"V1_volumen": v1[0], "V3_paso_ene2025": v3[0], "V4_marjul": v4[0], "V4_opuestos": opuestos, "V2_salto_2026_informativo": v2[0]},
        "serie_nota": "Serie 0-100 de la bajada ene-2011 a sep-2025; desde oct-2025, la bajada semanal 2024-2026 llevada a esa escala.",
        "fuentes": list(FU.values()), "generado_de": "analisis/brief_fw2025/"}
json.dump({"meta": meta, "items": items}, open(os.path.join(AQUI, "..", "..", "app", "datos", "brief_fw2025.json"), "w", encoding="utf-8"),
          ensure_ascii=False, separators=(",", ":"))
print("\n".join(out))
