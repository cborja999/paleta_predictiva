"""Le pide a Gemini que mire cada foto de la muestra y anote color, prenda y silueta.

Uso (en la Terminal, dentro de esta carpeta):
    export GEMINI_API_KEY="tu_clave"          # se saca en https://aistudio.google.com/apikey
    python3 extraer_color_silueta.py --prueba  # prueba con 3 fotos
    python3 extraer_color_silueta.py           # corre todas; si se corta, volvé a correrlo y sigue donde quedó
"""
import argparse, csv, json, os, sys, time
import requests
from google import genai
from google.genai import types

MODELOS = ["gemini-3.5-flash-lite", "gemini-3.1-flash-lite"]  # si uno está saturado, prueba el siguiente
MODELO = MODELOS[0]   # si da error de modelo, poné el Flash vigente que figure en aistudio.google.com

PROMPT = """Mirá esta foto de un look de desfile de moda y devolvé SOLO un JSON con estos campos.
Elegí siempre UNA opcion de cada lista, tal como esta escrita. Si hay varios looks o no se ve una persona, usá "no_aplica".

color_dominante: el color que mas superficie ocupa en la ropa (no fondo, no zapatos, no accesorios).
  Opciones: Negro, Blanco, Gris, Beige/Crema, Marron, Rojo, Burdeos/Vino, Rosa, Naranja, Amarillo, Verde, Oliva/Caqui, Azul, Celeste, Turquesa, Violeta, Metalizado, Multicolor/Estampado, no_aplica
color_secundario: el segundo color mas presente, con las mismas opciones, o "ninguno".
prenda_principal: la prenda mas protagonista del look.
  Opciones: Vestido, Pantalon, Falda, Blazer/Saco, Abrigo/Campera, Mono, Top/Blusa/Camisa, Tejido/Sweater, Conjunto de dos piezas, Otro, no_aplica
silueta: la forma general del look sobre el cuerpo.
  Opciones: Ajustada, Recta, Amplia/Oversized, Acampanada/Evase, Estructurada, Fluida/Drapeada, no_aplica
largo: Mini, Midi, Maxi, No aplica
confianza: alta, media o baja (baja si la foto es borrosa, oscura o el look es dificil de clasificar)

Formato exacto: {"color_dominante": "...", "color_secundario": "...", "prenda_principal": "...", "silueta": "...", "largo": "...", "confianza": "..."}"""

CAMPOS = ["color_dominante", "color_secundario", "prenda_principal", "silueta", "largo", "confianza"]

ap = argparse.ArgumentParser()
ap.add_argument("--entrada", default="muestra_vogue_reducida.csv")
ap.add_argument("--salida", default="../datasets_procesados/resultados_gemini.csv")
ap.add_argument("--prueba", action="store_true", help="procesa solo 3 fotos")
ap.add_argument("--pausa", type=float, default=0.5, help="segundos entre fotos")
ap.add_argument("--hilos", type=int, default=5, help="fotos en paralelo")
args = ap.parse_args()

clave = os.environ.get("GEMINI_API_KEY")
if not clave:
    sys.exit("Falta la clave. Corré primero:  export GEMINI_API_KEY=\"tu_clave\"")
cliente = genai.Client(api_key=clave)

with open(args.entrada, newline="", encoding="utf-8") as f:
    filas = list(csv.DictReader(f))

hechas = set()
if os.path.exists(args.salida):
    with open(args.salida, newline="", encoding="utf-8") as f:
        hechas = {r["id"] for r in csv.DictReader(f) if not r.get("error")}
pendientes = [r for r in filas if r["id"] not in hechas]
if args.prueba:
    pendientes = pendientes[:3]
print(f"{len(filas)} fotos en total | {len(hechas)} ya hechas | {len(pendientes)} por hacer")

nuevo = not os.path.exists(args.salida)
out = open(args.salida, "a", newline="", encoding="utf-8")
w = csv.DictWriter(out, fieldnames=["id", "temporada", "anio", "ciudad", "marca", "look"] + CAMPOS + ["error"], lineterminator="\n")
if nuevo:
    w.writeheader()

def analizar(r):
    with open(r["ruta_local"], "rb") as fh:
        datos_img = fh.read()
    for intento in range(6):
        try:
            resp = cliente.models.generate_content(
                model=MODELOS[intento % len(MODELOS)],
                contents=[types.Part.from_bytes(data=datos_img, mime_type="image/jpeg"), PROMPT],
                config=types.GenerateContentConfig(response_mime_type="application/json", temperature=0),
            )
            return json.loads(resp.text)
        except Exception as e:
            saturado = any(x in str(e) for x in ("503", "429", "404", "NOT_FOUND", "UNAVAILABLE", "RESOURCE_EXHAUSTED"))
            cuota = "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e)
            if not saturado or intento == 5 or (cuota and intento >= 1):
                raise
            espera = 5 * (intento + 1)
            print(f"  Gemini saturado, espero {espera}s y reintento...", flush=True)
            time.sleep(espera)

import threading, logging
from concurrent.futures import ThreadPoolExecutor
logging.getLogger("google_genai.types").setLevel(logging.ERROR)
lock = threading.Lock()
estado = {"hechas": 0, "fallos": 0}
CLAVES = ["id", "temporada", "anio", "ciudad", "marca", "look"]

def trabajar(r):
    if estado["fallos"] >= 8:
        return
    try:
        datos = analizar(r)
        if isinstance(datos, list):
            datos = datos[0] if datos else {}
    except Exception as e:
        with lock:
            estado["fallos"] += 1
            print(f"  error en id {r['id']}: {str(e)[:150]}", flush=True)
        return
    fila = {k: r[k] for k in CLAVES}
    fila.update({c: datos.get(c, "") for c in CAMPOS})
    fila["error"] = ""
    with lock:
        estado["fallos"] = 0
        w.writerow(fila)
        out.flush()
        estado["hechas"] += 1
        if estado["hechas"] % 25 == 0:
            print(f"  {estado['hechas']}/{len(pendientes)}", flush=True)
    time.sleep(args.pausa)

with ThreadPoolExecutor(args.hilos) as ex:
    list(ex.map(trabajar, pendientes))

out.close()
if estado["fallos"] >= 8:
    print("Muchos errores seguidos: paré. Si es cuota o saturación, esperá un rato y volvé a correrlo (sigue donde quedó).")
else:
    print("Listo. Resultados en", args.salida)
