"""Arma una muestra de looks del CSV de runway para que Gemini les anote color, prenda y silueta.

Solo usa ready-to-wear (sin alta costura ni menswear) de las temporadas spring-summer y fall-winter, 2011-2023.
Por cada temporada toma N colecciones al azar (semilla fija, asi el resultado se repite) y, de cada una,
unos pocos looks repartidos a lo largo del desfile (no solo los primeros).
"""
import argparse, csv, re, random
from collections import defaultdict

ap = argparse.ArgumentParser()
ap.add_argument("--entrada", default="1. collection_images_download.csv")
ap.add_argument("--salida", default="muestra_runway_para_gemini.csv")
ap.add_argument("--colecciones", type=int, default=30, help="colecciones por temporada")
ap.add_argument("--looks", type=int, default=3, help="looks por coleccion")
ap.add_argument("--semilla", type=int, default=42)
ap.add_argument("--min_colecciones", type=int, default=10, help="descarta temporadas con menos colecciones que esto (SS2011 tiene solo 2)")
args = ap.parse_args()

PAT = re.compile(r"^(?P<marca>.+?)-ready-to-wear-(?P<temp>spring-summer|fall-winter)-(?P<anio>20\d\d)"
                 r"(?:-(?P<ciudad>paris|milan|london|new-york))?(?:-|$)")

colecciones = defaultdict(list)   # slug -> [(image_name, image_url)]
with open(args.entrada, newline="", encoding="utf-8") as f:
    for r in csv.DictReader(f):
        slug = r["collection_url"].rstrip("/").split("/")[-1]
        colecciones[slug].append((r["image_name"], r["image_url"]))

por_temporada = defaultdict(list)  # (anio, temp) -> [(slug, marca, ciudad)]
for slug in sorted(colecciones):
    m = PAT.match(slug)
    if not m:
        continue
    anio = int(m["anio"])
    if not 2011 <= anio <= 2023:
        continue
    por_temporada[(anio, m["temp"])].append((slug, m["marca"], m["ciudad"] or "sin_dato"))

filas = []
for (anio, temp) in sorted(por_temporada):
    lista = por_temporada[(anio, temp)]
    if len(lista) < args.min_colecciones:
        print(f"aviso: se descarta {temp} {anio}: solo {len(lista)} colecciones en el dataset")
        continue
    rng = random.Random(f"{args.semilla}-{anio}-{temp}")
    elegidas = sorted(rng.sample(lista, min(args.colecciones, len(lista))))
    for slug, marca, ciudad in elegidas:
        imgs = sorted(colecciones[slug])
        n = len(imgs)
        pos = list(range(n)) if n <= args.looks else sorted({min(n - 1, int((k + 1) * n / (args.looks + 1))) for k in range(args.looks)})
        for p in pos:
            filas.append({"temporada": "SS" if temp == "spring-summer" else "FW", "anio": anio, "ciudad": ciudad,
                          "marca": marca.replace("-", " ").title(), "coleccion": slug,
                          "look": imgs[p][0], "image_url": imgs[p][1]})

with open(args.salida, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=["id", "temporada", "anio", "ciudad", "marca", "coleccion", "look", "image_url"], lineterminator="\n")
    w.writeheader()
    for i, r in enumerate(filas, 1):
        w.writerow({"id": i, **r})

print(f"{len(filas)} looks en {len({(r['anio'], r['temporada']) for r in filas})} temporadas -> {args.salida}")
cont = defaultdict(int)
for r in filas:
    cont[(r["anio"], r["temporada"])] += 1
print("looks por temporada (min/max):", min(cont.values()), "/", max(cont.values()))
ciudades = defaultdict(int)
for r in filas:
    ciudades[r["ciudad"]] += 1
print("por ciudad:", dict(ciudades))
