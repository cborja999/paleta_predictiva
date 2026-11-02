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
# Las que no se movieron lo suficiente ("Sin señal clara"): van al índice sin veredicto
SIN_SENAL = {
    "burgundy dress": ("Vestido bordó", "vestidos"), "oversized bag": ("Cartera grande", "accesorios"),
    "satin coat": ("Tapado de satén", "abrigos"), "statement belt": ("Cinturón protagonista", "accesorios"),
    "rose print": ("Estampado de rosas", "todo"), "sheer dress": ("Vestido transparente", "vestidos"),
    "shorts suit": ("Traje con short", "pantalones"), "dress over pants": ("Vestido sobre pantalón", "vestidos"),
    "funnel neck coat": ("Tapado de cuello alto", "abrigos"), "scarf coat": ("Tapado bufanda", "abrigos"),
    "peacoat": ("Saco marinero", "abrigos"), "balloon pants": ("Pantalón globo", "pantalones"),
    "trench coat": ("Trench", "abrigos"), "light pink dress": ("Vestido rosa claro", "vestidos"),
    "brocade jacket": ("Saco de brocado", "abrigos"), "peep toe heels": ("Zapatos peep toe", "accesorios"),
    "fringe jacket": ("Campera con flecos", "abrigos"), "mini dress": ("Minivestido", "vestidos"),
    "utility jacket": ("Campera utilitaria", "abrigos"), "bow blouse": ("Blusa con moño", "abrigos"),
    "floral dress": ("Vestido floreado", "vestidos"), "lace dress": ("Vestido de encaje", "vestidos"),
    "ruffle skirt": ("Pollera con volados", "polleras"), "plaid jacket": ("Saco escocés", "abrigos"),
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
# Lo que compara la regla, para dibujarlo: promedio del año antes (b0) y del año después (b1) en la escala de la
# curva, y cuánto se movió la temporada. g1 = log(b1/b0) - mediana de la temporada, así que la mediana sale de cada
# curva como log(b1/b0) - g1 (da lo mismo en toda la temporada, salvo redondeo de g1).
def promedio(xs):
    xs = [x for x in xs if x is not None]
    return sum(xs) / len(xs)
med_temp = {}
for t in tendencias:
    t["b0"], t["b1"] = round(promedio(t["serie"][:12]), 2), round(promedio(t["serie"][12:]), 2)
    med_temp.setdefault(t["temporada"], []).append(math.log(t["b1"] / t["b0"]) - t["g1"])
for t in tendencias:
    med = sum(med_temp[t["temporada"]]) / len(med_temp[t["temporada"]])
    t["bruto_pct"] = round((t["b1"] / t["b0"] - 1) * 100)        # cuánto cambiaron sus búsquedas, sin descontar nada
    t["temporada_pct"] = round((math.exp(med) - 1) * 100)         # cuánto se movió la temporada (mediana)
    t["esperado"] = round(t["b0"] * math.exp(med), 2)             # dónde estaría si se hubiera movido como la temporada

def fid(termino, temporada):
    # Mismo id que usan las fotos: prototipo/fotos/<id>.jpg
    return termino.replace(" ", "-") + ("" if temporada in ("SS2024", "FW2024") else "-" + temporada.lower())

# Sin señal clara: nombre, rubro, fuente y cuánto se movió frente a la temporada (no alcanza para veredicto)
sin_senal_items = [{
    "id": fid(it["termino"], it["temporada"]), "nombre": SIN_SENAL[it["termino"]][0], "rubro": SIN_SENAL[it["termino"]][1],
    "termino": it["termino"], "temporada": it["temporada"], "veredicto": "sin", "g1": it["g1"],
    "cambio_pct": round((math.exp(it["g1"]) - 1) * 100), "medio": it["medio"], "tendencia_fuente": it["tendencia_fuente"],
    "url_fuente": it["url_fuente"], "mes_desfile": it["mes_desfile"],
} for it in items if it["veredicto"] == "Sin señal clara"]

vistas = [{"id": fid(v["termino"], v["temporada"]), "nombre": VISTAS[v["termino"]], "termino": v["termino"],
           "temporada": v["temporada"], "medio": v.get("medio", ""), "tendencia_fuente": v.get("tendencia_fuente", ""),
           "url_fuente": v.get("url_fuente", "")} for v in d["vistas_2026"]]

# Colores de pasarela (brief.json): % de looks con ese color, temporadas recientes contra previas, y el color medido
NOM_COLOR = {"Marron": "Marrón", "Beige/Crema": "Beige y crema"}
b = json.loads((RAIZ / "app" / "datos" / "brief.json").read_text(encoding="utf-8"))
colores = [{"nombre": NOM_COLOR.get(c["categoria"], c["categoria"]), "hex": c["hex"],
            "reciente": c["pasarela_reciente"], "previo": c["pasarela_previo"],
            "cambio_pts": round(c["pasarela_reciente"] - c["pasarela_previo"], 1)}
           for c in b["items"] if c["tipo"] == "color"]
colores_meta = {"recientes": b["meta"]["pasarela_recientes"], "previas": b["meta"]["pasarela_previas"]}

# Ciclo por ciclo: pasajeras entre las que ganaron y entre las que perdieron búsquedas (hipotesis.md)
micro = json.loads((RAIZ / "app" / "datos" / "microtendencias.json").read_text(encoding="utf-8"))
ciclos = [{"ciclo": c["ciclo"], "sube_pasajeras": int(c["sube_pasajeras"]), "sube_n": int(c["sube_n"]),
           "cae_pasajeras": int(c["cae_pasajeras"]), "cae_n": int(c["cae_n"])} for c in micro["ciclos"]]

sin_senal = sum(1 for it in items if it["veredicto"] == "Sin señal clara")
medios = sorted({it["medio"] for it in items})

datos = {"tendencias": tendencias, "sin_senal_items": sin_senal_items, "vistas_2026": vistas, "sin_senal": sin_senal,
         "colores": colores, "colores_meta": colores_meta, "medios": medios, "ciclos": ciclos,
         "regla": d["meta"]["regla"], "confianza": d["meta"]["confianza"], "evidencia": d["meta"]["evidencia"]}
(RAIZ / "prototipo" / "datos.json").write_text(json.dumps(datos, ensure_ascii=False), encoding="utf-8")  # lo lee la funcion de la IA
SALIDA.write_text("// Generado por prototipo/armar_datos.py. No editar a mano.\nwindow.DATOS = "
                  + json.dumps(datos, ensure_ascii=False) + ";\n", encoding="utf-8")
print(f"{len(tendencias)} tendencias con veredicto y {len(vistas)} vistas en 2026 -> {SALIDA.relative_to(RAIZ)}")

# Lista de fotos que hacen falta (prototipo/FOTOS.md). Las fotos van en prototipo/fotos/, que no se sube a GitHub.
TEMP = {"SS2024": ("Primavera 2024", "spring 2024"), "FW2024": ("Otoño 2024", "fall 2024"), "SS2025": ("Primavera 2025", "spring 2025"),
        "SS2026": ("Primavera 2026", "spring 2026"), "FW2026": ("Otoño 2026", "fall 2026")}
lineas = ["# Fotos para el prototipo", "",
          "Las fotos van en `prototipo/fotos/` con el nombre exacto de la columna **Archivo** (en `.jpg`). Esa carpeta está en "
          "`.gitignore`: **no se sube a GitHub** (el repo es público y las fotos tienen derechos). La página muestra la foto si "
          "está y, si no, deja el lugar vacío con el nombre del archivo.", "",
          "Cómo elegir: un look de desfile de esa temporada, vertical y de cuerpo entero, donde la prenda se vea clara. La nota "
          "del medio que nombró la tendencia suele tener la foto justa.", "",
          "Este archivo lo arma `prototipo/armar_datos.py`: no editarlo a mano.", ""]
for titulo, lista in ((f"Con veredicto ({len(tendencias)})", tendencias), (f"Visto en 2026 ({len(vistas)})", vistas)):
    lineas += [f"## {titulo}", "", "| Archivo | Tendencia | Temporada | Buscar en Google Imágenes | Nota del medio |", "|---|---|---|---|---|"]
    lineas += [f"| `{t['id']}.jpg` | {t['nombre']} | {TEMP[t['temporada']][0]} | {t['termino']} runway {TEMP[t['temporada']][1]} "
               f"| [{t['medio']}]({t['url_fuente']}) |" for t in lista]
    lineas.append("")
(RAIZ / "prototipo" / "FOTOS.md").write_text("\n".join(lineas), encoding="utf-8")
