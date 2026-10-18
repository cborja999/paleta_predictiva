"""
Cuenta, para cada color y mes, el porcentaje de piezas del corpus que lo mencionan (separado en Argentina y resto).
Lee datasets/corpus_medios/corpus.csv (mismo formato que plantilla_corpus.csv).
Salida: analisis/corpus_menciones_por_mes.csv
Solo libreria estandar.
"""
import csv, os
from collections import defaultdict
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(AQUI)
SRC = os.path.join(RAIZ, "datasets", "corpus_medios", "corpus.csv")
if not os.path.exists(SRC):
    raise SystemExit("Falta datasets/corpus_medios/corpus.csv (copiar plantilla_corpus.csv y cargar piezas)")
piezas = defaultdict(int); cuenta = defaultdict(int)
for r in csv.DictReader(open(SRC, encoding="utf-8")):
    mes = r["fecha_publicacion"][:7]; grupo = "AR" if r["pais"].strip().lower() in ("argentina", "ar") else "resto"
    piezas[(mes, grupo)] += 1
    for c in {x.strip() for x in r["colores_mencionados"].split(";") if x.strip()}:
        cuenta[(mes, grupo, c)] += 1
with open(os.path.join(AQUI, "corpus_menciones_por_mes.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(["mes", "grupo", "color", "piezas_con_el_color", "piezas_del_mes", "porcentaje"])
    for (mes, g, c), n in sorted(cuenta.items()):
        t = piezas[(mes, g)]; w.writerow([mes, g, c, n, t, round(100.0 * n / t, 1)])
