# Replica M2 (reglas en REGLAS_M2_REPLICA.txt). Usa las mismas funciones de m1.py.
# Uso: python3 -I m2.py  (desde esta carpeta)
import sys, os, csv
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import m1
out = []
f2, ok2, res2 = m1.correr("trends_microtendencias_web_m2.csv", "M2 - REPLICA (Sandra's Closet), busqueda web MUNDO", out,
                          terms_file="terminos_declarados_m2.csv")
_, ok1 = m1.medir(m1.cargar("trends_microtendencias_web.csv"), m1.leer_terms("terminos_declarados.csv"))
out.append("=" * 78)
out.append("M1 + M2 JUNTOS (descriptivo; mediana de temporada calculada dentro de cada muestra)")
todos = ok1 + ok2
m1.tabla(todos, lambda f: f["c2"] >= -0.10, "PRINCIPAL: se queda = c2 >= -0.10", out)
m1.tabla(todos, lambda f: f["c2"] > 0, "SECUNDARIO 1: c2 > 0", out)
rho, p = m1.spearman([f["g1"] for f in todos], [f["c2"] for f in todos])
out.append(f"  Spearman g1 vs c2: rho={rho:.2f}, p={p:.3f}  (n={len(todos)})")
with open(os.path.join(m1.AQUI, "m2_detalle.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["temporada", "termino", "tipo", "tendencia_fuente", "usable", "B0", "B1", "B2", "g1", "c2", "grupo", "se_queda"])
    for r in f2:
        if r["usable"] == "si":
            w.writerow([r["temporada"], r["termino"], r["tipo"], r["tendencia_fuente"], "si", f"{r['B0']:.2f}", f"{r['B1']:.2f}",
                        f"{r['B2']:.2f}", f"{r['g1']:.3f}", f"{r['c2']:.3f}", r["grupo"], "si" if r["c2"] >= -0.10 else "no"])
        else:
            w.writerow([r["temporada"], r["termino"], r["tipo"], r["tendencia_fuente"], "no"] + [""] * 7)
print("\n".join(out))
