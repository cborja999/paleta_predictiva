# Arma los datos de la seccion "Tendencias puntuales" de app/index.html a partir de analisis/microtendencias/.
# No inventa datos: lee los detalles calculados por m1.py / m2.py y las series de Google Trends.
# Uso: python3 -I app/armar_microtendencias.py   (despues de correr m1.py y m2.py)
import csv, json, os, re, sys
A = os.path.dirname(os.path.abspath(__file__))
M = os.path.join(A, "..", "analisis", "microtendencias")
sys.path.insert(0, M)
import m1  # noqa: E402

def am(s): y, mm = s.split("-"); return int(y) * 12 + int(mm) - 1
desde, hasta = am("2015-01"), am("2024-12")

H = os.path.join(A, "..", "analisis", "hipotesis")
def cargar_c1():
    from collections import defaultdict
    ser = defaultdict(dict)
    for r in csv.DictReader(open(os.path.join(H, "datos", "trends_c1_web.csv"), encoding="utf-8")):
        ser[r["termino"]][m1.am(r["mes"])] = float(r["valor"])
    return ser

def bloque(muestra, terms_file, datos_file, detalle_file, base=M):
    ser = cargar_c1() if muestra == "C1" else m1.cargar(datos_file)
    det = {r["termino"]: r for r in csv.DictReader(open(os.path.join(base, detalle_file), encoding="utf-8"))}
    terms = [t for t in csv.DictReader(open(os.path.join(base, terms_file), encoding="utf-8")) if t["termino"]]
    out = []
    for t in terms:
        d = det[t["termino"]]
        if d["usable"] != "si": continue
        s = ser[t["termino"]]
        out.append({
            "muestra": muestra, "temporada": t["temporada"], "termino": t["termino"], "tipo": t["tipo"],
            "fuente": t["tendencia_fuente"], "e": t["mes_desfile"],
            "g1": round(float(d["g1"]), 3), "c2": round(float(d["c2"]), 3), "grupo": d["grupo"],
            "se_queda": d["se_queda"] == "si",
            "serie": [int(s.get(k, 0)) for k in range(desde, hasta + 1)],
        })
    return out

items = bloque("M1", "terminos_declarados.csv", "trends_microtendencias_web.csv", "m1_detalle.csv")
if os.path.exists(os.path.join(M, "m2_detalle.csv")):
    items += bloque("M2", "terminos_declarados_m2.csv", "trends_microtendencias_web_m2.csv", "m2_detalle.csv")
items += bloque("C1", "terminos_declarados_c1.csv", None, "c1_detalle.csv", base=H)
ciclos = list(csv.DictReader(open(os.path.join(H, "ciclos.csv"), encoding="utf-8")))

def resumen(sub):
    r = {}
    for g in ("SUBE", "PLANO", "CAE"):
        x = [i for i in sub if i["grupo"] == g]
        r[g] = {"n": len(x), "quedan": sum(i["se_queda"] for i in x)}
    a, n1 = r["SUBE"]["quedan"], r["SUBE"]["n"]
    c = r["PLANO"]["quedan"] + r["CAE"]["quedan"]; n2 = r["PLANO"]["n"] + r["CAE"]["n"]
    r["p_fisher"] = round(m1.fisher(a, n1 - a, c, n2 - c), 3)
    pc, nc = r["CAE"]["n"] - r["CAE"]["quedan"], r["CAE"]["n"]; ps = n1 - a
    r["p_cae_vs_sube"] = round(m1.fisher(pc, nc - pc, ps, n1 - ps), 3)
    rho, p = m1.spearman([i["g1"] for i in sub], [i["c2"] for i in sub])
    r["spearman"] = [round(rho, 2), round(p, 3)]
    return r

D = {"meta": {"desde": "2015-01", "hasta": "2024-12",
              "generado_de": ["analisis/hipotesis/c1_detalle.csv", "analisis/hipotesis/ciclos.csv", "analisis/microtendencias/m1_detalle.csv", "analisis/microtendencias/m2_detalle.csv",
                              "analisis/microtendencias/datos/"]},
     "resumen": {k: resumen([i for i in items if k == "todo" or i["muestra"] == k]) for k in ("C1", "M1", "M2", "todo")
                 if any(k == "todo" or i["muestra"] == k for i in items)},
     "ciclos": ciclos, "items": items}
js = json.dumps(D, ensure_ascii=False, separators=(",", ":"))
open(os.path.join(A, "datos", "microtendencias.json"), "w", encoding="utf-8").write(js)
html = open(os.path.join(A, "index.html"), encoding="utf-8").read()
nuevo, n = re.subn(r'(<script id="micro" type="application/json">).*?(</script>)', lambda m_: m_.group(1) + js + m_.group(2), html, flags=re.S)
assert n == 1, "no encontre el bloque <script id=micro> en index.html"
open(os.path.join(A, "index.html"), "w", encoding="utf-8").write(nuevo)
print(len(items), "tendencias;", json.dumps(D["resumen"]))
