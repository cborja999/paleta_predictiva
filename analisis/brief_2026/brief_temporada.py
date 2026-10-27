# Brief de la ultima temporada limpia (SS2024 y FW2024) con el metodo de la hipotesis,
# mas las tendencias de SS2026 y FW2026 como "lo que se vio" (sin veredicto: ver DIAGNOSTICO_2026.md).
# Reglas: REGLAS_BRIEF_2024.txt (fijadas antes de bajar los datos).
# Uso: python3 -I brief_temporada.py  (desde esta carpeta). Escribe salida_brief_2024.txt (por stdout),
#      brief_2024_detalle.csv y ../../app/datos/brief_temporada.json
import csv, json, math, os, statistics as st, sys
AQUI = os.path.dirname(os.path.abspath(__file__))
APP = os.path.join(AQUI, "..", "..", "app", "datos")
sys.path.insert(0, os.path.join(AQUI, "..", "microtendencias"))
import m1  # noqa: E402

def am(s): y, m = s.split("-"); return int(y) * 12 + int(m) - 1
def ma(i): return f"{i // 12}-{i % 12 + 1:02d}"
def leer(nombre):
    ser = {}
    for r in csv.DictReader(open(os.path.join(AQUI, "datos", nombre), encoding="utf-8")):
        ser.setdefault(r["termino"], {})[am(r["mes"])] = float(r["valor"])
    return ser
def rows(nombre): return list(csv.DictReader(open(os.path.join(AQUI, nombre), encoding="utf-8")))

ser24, ser26 = leer("trends_2024_web.csv"), leer("trends_2026_web.csv")
t24 = [t for t in rows("terminos_declarados_2024.csv") if t["termino"]]
t26 = [t for t in rows("terminos_declarados_2026.csv") if t["termino"]]
f24 = {(f["temporada"], f["medio"]): f for f in rows("fuentes_listas_2024.csv")}
f26 = {(f["temporada"], f["medio"]): f for f in rows("fuentes_listas_2026.csv")}

filas = []
for t in t24:
    s, e = ser24[t["termino"]], am(t["mes_desfile"])
    falta = [ma(k) for k in range(e - 12, e + 12) if k not in s]
    if falta: sys.exit(f"Faltan meses de la ventana para {t['termino']}: {falta}")
    w = [s[k] for k in range(e - 12, e + 12)]
    B0, B1 = st.mean(w[:12]), st.mean(w[12:])
    ceros = sum(1 for x in w if x == 0)
    picos = []
    for lab, ww, a in (("año previo", w[:12], e - 12), ("primer año", w[12:], e)):
        md = st.median(ww)
        if md > 0 and max(ww) >= 5 * md: picos.append(f"{lab}: {ma(a + ww.index(max(ww)))}")
    f = dict(t, B0=B0, B1=B1, ceros=ceros, usable=ceros <= 8 and B0 > 0 and B1 > 0,
             aviso=("Lectura apoyada en un pico de un solo mes (" + "; ".join(picos) + ")") if picos else "")
    if f["usable"]: f["r1"] = math.log(B1 / B0)
    filas.append(f)

out = ["BRIEF ULTIMA TEMPORADA LIMPIA (reglas en REGLAS_BRIEF_2024.txt)"]
for tem in ("SS2024", "FW2024"):
    ok = [f for f in filas if f["temporada"] == tem and f["usable"]]
    med = st.median(f["r1"] for f in ok)
    for f in ok:
        g = f["r1"] - med
        f["g1"] = g
        f["veredicto"] = "Tiende a quedarse" if g >= 0.10 else ("Riesgo de moda pasajera" if g <= -0.10 else "Sin señal clara")
        f["confianza"] = "" if abs(g) < 0.10 else ("Alta" if abs(g) >= 0.30 else "Media")
    out.append("=" * 70)
    fs = [f for f in filas if f["temporada"] == tem]
    out.append(f"{tem}: {len(fs)} terminos, {len(ok)} usables")
    for f in fs:
        if not f["usable"]: out.append(f"   descartado por volumen: {f['termino']} ({f['ceros']} meses en cero)")
    for f in sorted(ok, key=lambda f: -f["g1"]):
        out.append(f"   {f['termino']:20s} g1 {f['g1']:+.2f}  {f['veredicto']:24s} {f['confianza']:6s} {f['aviso']}")
    cnt = {}
    for f in ok: cnt[f["veredicto"]] = cnt.get(f["veredicto"], 0) + 1
    out.append("   total: " + " | ".join(f"{k}: {v}" for k, v in sorted(cnt.items())))
    rho, p = m1.spearman([f["B0"] for f in ok], [f["g1"] for f in ok])
    aviso = "  -> AVISO: posible sesgo por volumen" if abs(rho) >= 0.5 else "  -> sin sesgo por volumen"
    out.append(f"   control: Spearman nivel B0 vs g1 = {rho:.2f} (p={p:.3f}){aviso}")

with open(os.path.join(AQUI, "brief_2024_detalle.csv"), "w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh)
    w.writerow(["temporada", "medio", "tendencia_fuente", "termino", "tipo", "usable", "B0", "B1", "g1", "veredicto", "confianza", "aviso"])
    for f in filas:
        w.writerow([f["temporada"], f["medio"], f["tendencia_fuente"], f["termino"], f["tipo"], "si" if f["usable"] else "no",
                    f"{f['B0']:.2f}", f"{f['B1']:.2f}", f"{f['g1']:.3f}" if "g1" in f else "", f.get("veredicto", ""), f.get("confianza", ""), f["aviso"]])

desde, hasta = am("2019-01"), am("2026-09")
def item(t, ser, fuentes, extra):
    fu = fuentes[(t["temporada"], t["medio"])]
    d = {"temporada": t["temporada"], "termino": t["termino"], "tipo": t["tipo"], "tendencia_fuente": t["tendencia_fuente"],
         "medio": t["medio"], "url_fuente": fu["url"], "fecha_fuente": fu["fecha_publicacion"], "mes_desfile": t["mes_desfile"],
         "serie": [None if ser[t["termino"]].get(k) is None else int(ser[t["termino"]][k]) for k in range(desde, hasta + 1)]}
    d.update(extra)
    return d

items = [item(f, ser24, f24, {"g1": round(f["g1"], 3), "veredicto": f["veredicto"], "confianza": f["confianza"], "aviso": f["aviso"]})
         for f in filas if f["usable"]]
vistas = [item(t, ser26, f26, {"veredicto": None, "nota": "Sin veredicto: los datos de Google desde mediados de 2025 no son comparables."})
          for t in t26]
meta = {
    "meses": [ma(k) for k in range(desde, hasta + 1)],
    "corte_google": "2025-01",
    "serie_nota": "Cada serie va de 0 a 100 dentro de su propia bajada. Las de 2024 llegan hasta feb-2025 (null después); las de 2026 hasta sep-2026, con el problema de medición de Google desde mediados de 2025.",
    "temporada_con_veredicto": ["SS2024", "FW2024"],
    "temporada_vista": ["SS2026", "FW2026"],
    "regla": "Tiende a quedarse si las búsquedas del primer año después del desfile subieron al menos 10% contra el año previo, descontando lo que se movió el resto de la temporada; riesgo de moda pasajera si bajaron 10% o más; si no, sin señal clara.",
    "confianza": "Alta si el movimiento es de 30% o más; Media entre 10% y 30%.",
    "aviso": "Si un solo mes vale 5 veces o más la mediana de su año, la lectura se apoya en un pico aislado (aviso agregado después de ver los datos; no cambia el veredicto).",
    "segundo_anio": "El segundo año de estas tendencias (2025-2026) no se puede medir limpio: los veredictos son la lectura del primer año, como pide la hipótesis.",
    "evidencia": "9 de cada 10 tendencias que ganan búsquedas en su primer año siguen al segundo (178 tendencias, 2016-2024). Los datos de 2021 a 2024 muestran que las que pierden búsquedas tienen más del triple de chances de ser pasajeras (9 de 16 contra 2 de 19).",
    "fuentes": list(f24.values()) + list(f26.values()),
    "generado_de": "analisis/brief_2026/",
}
json.dump({"meta": meta, "items": items, "vistas_2026": vistas},
          open(os.path.join(APP, "brief_temporada.json"), "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
print("\n".join(out))
