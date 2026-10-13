"""Baja una muestra de fotos de desfiles del banco 'Vogue Runway' (HuggingFace: tonyassi/vogue-runway-top15-512px)
y arma muestra_vogue_para_gemini.csv. NO baja las 87.000 fotos: solo ~90 por temporada.

Uso (Terminal, dentro de esta carpeta):
    pip3 install requests
    python3 bajar_fotos_vogue.py
Si se corta, volvelo a correr: no repite las fotos que ya bajo.
"""
import argparse, csv, os, re, sys, time
import requests

DS = "tonyassi/vogue-runway-top15-512px"
API = "https://datasets-server.huggingface.co/rows"
CIUDAD = {  # ciudad donde desfila cada casa (aproximada, para poder separar por semana de la moda)
    "alexander mcqueen": "paris", "armani": "milan", "balenciaga": "paris", "calvin klein": "new-york",
    "chanel": "paris", "dior": "paris", "fendi": "milan", "gucci": "milan", "hermes": "paris",
    "louis vuitton": "paris", "prada": "milan", "ralph lauren": "new-york", "saint laurent": "paris",
    "valentino": "paris", "versace": "milan",
}

ap = argparse.ArgumentParser()
ap.add_argument("--por_temporada", type=int, default=90)
ap.add_argument("--desde", type=int, default=2011)
ap.add_argument("--hasta", type=int, default=2025)
ap.add_argument("--carpeta", default="fotos_vogue")
ap.add_argument("--salida", default="muestra_vogue_para_gemini.csv")
args = ap.parse_args()
S = requests.Session()

def pedir(offset, largo=100, intentos=15):
    for k in range(intentos):
        try:
            r = S.get(API, params={"dataset": DS, "config": "default", "split": "train", "offset": offset, "length": largo}, timeout=60)
            if r.status_code == 200:
                return r.json()
            if r.status_code in (429, 500, 502, 503, 504):
                time.sleep(min(5 * (k + 1), 30)); continue
            r.raise_for_status()
        except requests.RequestException as e:
            if k == intentos - 1:
                sys.exit(f"No pude conectar con HuggingFace: {e}")
            time.sleep(min(5 * (k + 1), 30))
    sys.exit("HuggingFace no responde. Probá de nuevo en unos minutos.")

# Paso 1: recorrer el listado (solo texto, rapido) para saber que foto es de que coleccion
primero = pedir(0, 1)
nombres = primero["features"][1]["type"]["names"]
total = primero["num_rows_total"]
print(f"{total} fotos en el banco, {len(nombres)} colecciones. Recorriendo listado...")
from concurrent.futures import ThreadPoolExecutor
HILOS = 10
HILOS_LISTADO = 4
import json
CACHE = 'listado_cache.json'
por_temp = {}   # (anio, temp) -> [(offset, marca, url)]
cache = json.load(open(CACHE)) if os.path.exists(CACHE) else {}
def pagina(o):
    if str(o) not in cache:
        d = pedir(o, 100)
        cache[str(o)] = d
        if len(cache) % 100 == 0:
            print(f"  listado {len(cache)*100}/{total}", flush=True)
    return cache[str(o)]
with ThreadPoolExecutor(HILOS_LISTADO) as ex:
    paginas = list(ex.map(pagina, range(0, total, 100)))
json.dump(cache, open(CACHE, "w"))
print("  listado completo")
for d in paginas:
    for it in d["rows"]:
        nombre = nombres[it["row"]["label"]]            # "alexander mcqueen,fall 1996 ready to wear"
        m = re.match(r"^(.+?),(fall|spring) (\d{4}) ready to wear$", nombre)
        if not m:
            continue
        marca, est, anio = m.group(1), m.group(2), int(m.group(3))
        if not (args.desde <= anio <= args.hasta):
            continue
        temp = "FW" if est == "fall" else "SS"
        por_temp.setdefault((anio, temp), []).append((it["row_idx"], marca, it["row"]["image"]["src"]))

# Paso 2: elegir ~por_temporada fotos parejas dentro de cada temporada y bajarlas (en paralelo)
os.makedirs(args.carpeta, exist_ok=True)
tareas, n = [], 0
for (anio, temp) in sorted(por_temp):
    lst = por_temp[(anio, temp)]
    k = min(args.por_temporada, len(lst))
    for j in range(k):
        ix, marca, url = lst[int((j + 0.5) * len(lst) / k)]
        n += 1
        tareas.append((n, anio, temp, ix, marca, url, os.path.join(args.carpeta, f"{n:05d}.jpg")))
    print(f"  {temp}{anio}: {k} fotos (hay {len(lst)})")

def bajar(t):
    ruta, url = t[6], t[5]
    if os.path.exists(ruta):
        return True
    for intento in range(4):
        try:
            r = S.get(url, timeout=60)
            if r.status_code == 200 and len(r.content) > 1000:
                open(ruta, "wb").write(r.content); return True
        except requests.RequestException:
            pass
        time.sleep(3 * (intento + 1))
    return False

print(f"Bajando {len(tareas)} fotos...")
with ThreadPoolExecutor(HILOS) as ex:
    res = list(ex.map(bajar, tareas))
filas = [{"id": t[0], "temporada": t[2], "anio": t[1], "ciudad": CIUDAD.get(t[4], "sin_dato"),
          "marca": t[4], "look": f"row{t[3]}", "ruta_local": t[6]} for t, ok in zip(tareas, res) if ok]
print(f"No se pudieron bajar {res.count(False)} fotos (se saltean).")

with open(args.salida, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=["id", "temporada", "anio", "ciudad", "marca", "look", "ruta_local"], lineterminator="\n")
    w.writeheader(); w.writerows(filas)
print(f"Listo: {len(filas)} fotos en '{args.carpeta}/' y lista en {args.salida}")
