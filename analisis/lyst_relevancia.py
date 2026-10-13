"""
Lyst Index (ranking trimestral de marcas mas buscadas, Q1-18 a Q2-26) como segunda medida de relevancia de marcas.
Fuente: https://www.lyst.com/the-lyst-index/ (transcripto por el grupo CICLO; ver datasets/diccionario.md).
El CSV crudo NO se sube al repo (Lyst no autoriza redistribuir el informe): va en datasets/lyst/ (ignorado por git).
Salida (solo agregados): lyst_cobertura.csv, lyst_vs_trends.csv, lyst_resumen.md
Solo libreria estandar.
"""
import csv, os, re
from collections import defaultdict

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
LYST = os.path.join(RAIZ, "datasets", "lyst", "lyst_index__34_trimestres.csv")

# casas de nuestras fotos (nombre en Lyst -> nombre en nuestro dataset)
NUESTRAS = {"Alexander McQueen": "alexander mcqueen", "Balenciaga": "balenciaga", "Chanel": "chanel", "Dior": "dior",
            "Fendi": "fendi", "Gucci": "gucci", "Louis Vuitton": "louis vuitton", "Prada": "prada",
            "Ralph Lauren": "ralph lauren", "Saint Laurent": "saint laurent", "Valentino": "valentino", "Versace": "versace"}
# (Hermes y Calvin Klein no figuran en Lyst)

filas = list(csv.DictReader(open(LYST, encoding="utf-8")))
tri = sorted({r["trimestre"] for r in filas}, key=lambda q: (int(q[-2:]), int(q[1])))
top = {q: int(max(int(r["puesto"]) for r in filas if r["trimestre"] == q)) for q in tri}

# 1) cobertura: de los puestos del ranking, cuantos ocupan casas que tenemos en las fotos
cob = []
for q in tri:
    r = [x for x in filas if x["trimestre"] == q]
    propias = [x for x in r if x["marca"] in NUESTRAS]
    cob.append([q, len(r), len(propias), round(100.0 * len(propias) / len(r), 1)])
with open(os.path.join(AQUI, "lyst_cobertura.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(["trimestre", "puestos_ranking", "puestos_de_casas_que_tenemos", "porcentaje"]); w.writerows(cob)

# 2) marcas que mas aparecen y no tenemos
ap = defaultdict(list)
for x in filas: ap[x["marca"]].append(int(x["puesto"]))
faltan = sorted(((m, len(p), sum(p) / len(p)) for m, p in ap.items() if m not in NUESTRAS), key=lambda t: (-t[1], t[2]))[:10]

# 3) acuerdo con Trends: puntos Lyst ultimos 4 trimestres vs indice de Trends ultimos 12 meses
ult = tri[-4:]
pts = defaultdict(float)
for x in filas:
    if x["trimestre"] in ult: pts[x["marca"]] += 21 - int(x["puesto"])
tr = {}
for l in open(os.path.join(AQUI, "marcas_resumen.md"), encoding="utf-8"):
    m = re.match(r"\| ([a-z ]+) \| ([0-9.]+) \|", l)
    if m and m.group(1).strip() in NUESTRAS.values(): tr[m.group(1).strip()] = float(m.group(2))
def rangos(d):
    o = sorted(d, key=lambda k: -d[k]); return {k: i + 1 for i, k in enumerate(o)}
comun = [k for k, v in NUESTRAS.items() if v in tr]
rl = rangos({k: pts[k] for k in comun}); rt = rangos({k: tr[NUESTRAS[k]] for k in comun})
n = len(comun)
rho = 1 - 6 * sum((rl[k] - rt[k]) ** 2 for k in comun) / (n * (n * n - 1))
with open(os.path.join(AQUI, "lyst_vs_trends.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(["casa", "puntos_lyst_ult4_trim", "puesto_lyst_entre_nuestras", "indice_trends_12m", "puesto_trends_entre_nuestras"])
    for k in sorted(comun, key=lambda k: rl[k]): w.writerow([k, pts[k], rl[k], tr[NUESTRAS[k]], rt[k]])

prom_cob = sum(c[3] for c in cob) / len(cob)
pc = {y: [c[3] for c in cob if c[0].endswith(y)] for y in ("18", "19", "20", "21", "22", "23", "24", "25", "26")}
L = ["# Lyst Index como segunda medida de relevancia", "",
     "Fuente: Lyst Index, ranking trimestral de marcas (Q1-18 a Q2-26), transcripto por el grupo CICLO. Datos crudos fuera del repo por licencia.",
     "Los 2018 son top 10 y desde Q1-19 top 20; en Q1-26 Lyst recalibro la formula (corte en la serie).", "",
     "## Cobertura: cuanto del ranking Lyst esta en nuestras fotos",
     "Tenemos 12 de las casas que aparecen en Lyst (Hermes y Calvin Klein estan en nuestras fotos pero no en el ranking).",
     "Promedio de puestos del ranking ocupados por casas que tenemos: %.0f%%." % prom_cob,
     "Por año: " + "; ".join("20%s=%.0f%%" % (y, sum(v) / len(v)) for y, v in pc.items()), "",
     "## Marcas que mas aparecen en Lyst y NO estan en nuestras fotos", "",
     "| Marca | Trimestres en el ranking (de %d) | Puesto promedio |" % len(tri), "|---|---|---|"]
L += ["| %s | %d | %.1f |" % t for t in faltan]
L += ["", "## Acuerdo con Google Trends", "",
      "Entre las %d casas que estan en ambos, correlacion de rangos (Spearman) entre puntos Lyst (ultimos 4 trimestres) e indice de Trends (ultimos 12 meses): **%.2f**." % (n, rho),
      "Con 12 casas esa correlacion no es estadisticamente significativa (p aprox. 0,14): es una referencia, no una prueba. Detalle en `lyst_vs_trends.csv`.", "",
      "## Lectura",
      "- Lyst y Trends miden cosas parecidas pero no iguales (Lyst combina busquedas, ventas y clics en su plataforma).",
      "- Lo mas util: Lyst muestra que marcas dominan la conversacion y no estan en nuestra muestra (ver tabla), asi que la muestra de pasarela puede estar subrepresentando a las marcas que mueven la busqueda. Es una hipotesis, no esta probado.",
      "- No se hizo cruce ponderado con Lyst: solo cubre 2018 en adelante (~17 temporadas), muy poco para correlaciones con retraso."]
open(os.path.join(AQUI, "lyst_resumen.md"), "w", encoding="utf-8").write("\n".join(L) + "\n")
print("\n".join(L)); print(open(os.path.join(AQUI, "lyst_vs_trends.csv")).read())
