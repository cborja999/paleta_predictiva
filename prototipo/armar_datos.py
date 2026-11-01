"""Arma prototipo/datos.js (y datos.json, para la funcion de la IA) a partir de app/datos/brief_temporada.json
y app/datos/brief_ss2025.json.

Uso (desde la raíz del repo):
    python3 prototipo/armar_datos.py

Toma las tendencias de SS2024 y FW2024 con veredicto (se queda / riesgo) y los
nombres de lo que se vio en SS2026 y FW2026 (sin veredicto). No cambia ningún dato:
solo traduce los nombres y recorta la curva a 12 meses antes y 12 después del desfile.
"""
import json
import math
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
ENTRADA = RAIZ / "app" / "datos" / "brief_temporada.json"
SALIDA = RAIZ / "prototipo" / "datos.js"

# Nombre en castellano y rubro de cada tendencia (para ordenar según lo que hace la marca)
NOMBRES = {
    "halter dress": ("Vestido halter", "vestidos"),
    "slip skirt": ("Pollera lencera", "polleras"),
    "sheer skirt": ("Pollera transparente", "polleras"),
    "mini dress": ("Minivestido", "vestidos"),
    "pencil skirt": ("Pollera lápiz", "polleras"),
    "hot pants": ("Hot pants", "pantalones"),
    "fringe jacket": ("Campera con flecos", "abrigos"),
    "lavender dress": ("Vestido lavanda", "vestidos"),
    "pillbox hat": ("Sombrero pillbox", "accesorios"),
    "leopard print": ("Animal print leopardo", "todo"),
    "tailored trousers": ("Pantalón sastre", "pantalones"),
    "cashmere pants": ("Pantalón de cashmere", "pantalones"),
    "cigarette pants": ("Pantalón cigarette", "pantalones"),
    "faux fur coat": ("Tapado de piel sintética", "abrigos"),
    "leather dress": ("Vestido de cuero", "vestidos"),
    "turtleneck": ("Polera", "abrigos"),
    "feather dress": ("Vestido con plumas", "vestidos"),
    "green dress": ("Vestido verde", "vestidos"),
    "tea length dress": ("Vestido a media pierna", "vestidos"),
    # SS2025
    "statement sunglasses": ("Anteojos de sol protagonistas", "accesorios"),
    "bubble skirt": ("Pollera balón", "polleras"),
    "polka dot": ("Lunares", "todo"),
    "chiffon cape": ("Capa de gasa", "abrigos"),
    "wide leg jeans": ("Jean de pierna ancha", "pantalones"),
    "one leg pants": ("Pantalón de una sola pierna", "pantalones"),
    "dress over pants": ("Vestido sobre pantalón", "vestidos"),
    "tutu skirt": ("Pollera tutú", "polleras"),
    "breton sweater": ("Sweater marinero a rayas", "abrigos"),
    "sequin dress": ("Vestido de lentejuelas", "vestidos"),
    "80s blazer": ("Blazer ochentoso", "abrigos"),
}
VISTAS = {
    "leather mini skirt": "Minifalda de cuero", "satin scarf": "Pañuelo de satén", "floral print": "Estampado floral",
    "poplin shirt": "Camisa de popelín", "trench coat": "Trench", "80s fashion": "Estilo ochentas",
    "lilac dress": "Vestido lila", "preppy outfit": "Estilo preppy", "tweed suit": "Traje de tweed",
    "bell sleeve": "Manga campana", "feather skirt": "Pollera con plumas", "yellow dress": "Vestido amarillo",
    "chainmail dress": "Vestido de malla metálica", "ruffle dress": "Vestido con volados", "flapper dress": "Vestido charleston",
    "spaghetti strap top": "Top de breteles finos", "low rise pants": "Pantalón tiro bajo", "power shoulders": "Hombros marcados",
    "fair isle sweater": "Sweater fair isle", "brocade": "Brocado", "tailored coat": "Tapado sastre",
    "statement coat": "Tapado protagonista", "polo shirt": "Chomba", "satin dress": "Vestido de satén",
    "silk shirt": "Camisa de seda", "fur coat": "Tapado de piel", "brooch": "Broche", "check shirt": "Camisa a cuadros",
    "purple dress": "Vestido violeta", "skirt suit": "Trajecito de pollera", "chunky scarf": "Bufanda gruesa",
    "shearling coat": "Campera de corderito", "lace dress": "Vestido de encaje", "fringe jacket": "Campera con flecos",
    "sheer dress": "Vestido transparente", "pink dress": "Vestido rosa",
}

d = json.loads(ENTRADA.read_text(encoding="utf-8"))
d25 = json.loads((RAIZ / "app" / "datos" / "brief_ss2025.json").read_text(encoding="utf-8"))
assert d25["meta"]["meses"] == d["meta"]["meses"]
items = d["items"] + (d25["items"] if d25["meta"]["con_veredicto"] else [])
meses = d["meta"]["meses"]
tendencias = []
for it in items:
    if it["veredicto"] == "Sin señal clara":
        continue
    nombre, rubro = NOMBRES[it["termino"]]
    j = meses.index(it["mes_desfile"])
    sin = it.get("sin_ago_sep_2025")
    tendencias.append({
        "id": it["termino"].replace(" ", "-") + ("-ss2025" if it["temporada"] == "SS2025" else ""),
        "nota": (f"Sin agosto y septiembre de 2025, cuando Google empezó a medir distinto, la lectura da “{sin.lower()}”."
                 if sin and sin != it["veredicto"] else ""),
        "nombre": nombre,
        "termino": it["termino"],
        "rubro": rubro,
        "temporada": it["temporada"],
        "veredicto": "queda" if it["veredicto"] == "Tiende a quedarse" else "riesgo",
        "confianza": it["confianza"],
        "g1": it["g1"],
        "cambio_pct": round((math.exp(it["g1"]) - 1) * 100),
        "aviso": it.get("aviso") or "",
        "medio": it["medio"],
        "tendencia_fuente": it["tendencia_fuente"],
        "url_fuente": it["url_fuente"],
        "mes_desfile": it["mes_desfile"],
        "desde": meses[j - 12],
        "serie": it["serie"][j - 12:j + 12],
    })
vistas = [{"nombre": VISTAS[v["termino"]], "temporada": v["temporada"]} for v in d["vistas_2026"]]

# Ciclo por ciclo: pasajeras entre las que ganaron y entre las que perdieron búsquedas (hipotesis.md)
micro = json.loads((RAIZ / "app" / "datos" / "microtendencias.json").read_text(encoding="utf-8"))
ciclos = [{"ciclo": c["ciclo"], "sube_pasajeras": int(c["sube_pasajeras"]), "sube_n": int(c["sube_n"]),
           "cae_pasajeras": int(c["cae_pasajeras"]), "cae_n": int(c["cae_n"])} for c in micro["ciclos"]]

sin_senal = sum(1 for it in items if it["veredicto"] == "Sin señal clara")
medios = sorted({it["medio"] for it in items})

datos = {"tendencias": tendencias, "vistas_2026": vistas, "sin_senal": sin_senal, "medios": medios, "ciclos": ciclos,
         "regla": d["meta"]["regla"], "confianza": d["meta"]["confianza"], "evidencia": d["meta"]["evidencia"]}
(RAIZ / "prototipo" / "datos.json").write_text(json.dumps(datos, ensure_ascii=False), encoding="utf-8")  # lo lee la funcion de la IA
SALIDA.write_text("// Generado por prototipo/armar_datos.py. No editar a mano.\nwindow.DATOS = "
                  + json.dumps(datos, ensure_ascii=False) + ";\n", encoding="utf-8")
print(f"{len(tendencias)} tendencias con veredicto y {len(vistas)} vistas en 2026 -> {SALIDA.relative_to(RAIZ)}")
