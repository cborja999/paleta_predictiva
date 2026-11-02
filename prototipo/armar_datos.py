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
    # FW2025
    "brooch": ("Broche", "accesorios"), "black lace": ("Encaje negro", "vestidos"),
    "statement coat": ("Tapado protagonista", "abrigos"), "cardigan": ("Cárdigan", "abrigos"),
    "thigh high boots": ("Botas bucaneras", "accesorios"), "asymmetric jacket": ("Saco asimétrico", "abrigos"),
    "ruffle collar": ("Cuello con volados", "abrigos"), "floral print": ("Estampado floral", "todo"),
    "pearl necklace": ("Collar de perlas", "accesorios"), "neon dress": ("Vestido flúor", "vestidos"),
    "jogging pants": ("Pantalón jogging", "pantalones"),
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
    "fair isle sweater": ("Sweater fair isle", "abrigos"), "peplum": ("Peplum", "abrigos"), "scarf": ("Bufanda", "accesorios"),
    "shearling jacket": ("Campera de corderito", "abrigos"), "red dress": ("Vestido rojo", "vestidos"),
    "orange dress": ("Vestido naranja", "vestidos"),
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

# Dos desfiles por tendencia para buscar las fotos (prototipo/FOTOS.md). "nota": la marca sale de la nota del medio que
# nombró la tendencia. "otra": esa nota no se pudo abrir o no nombra marcas, y salen de otras notas de la misma temporada.
DESFILES = {
    "pencil-skirt": (["Altuzarra", "Khaite"], "nota"), "hot-pants": (["Tom Ford", "Gucci"], "nota"),
    "sheer-skirt": (["Altuzarra", "Carven"], "nota"), "slip-skirt": (["Prada", "Tory Burch"], "nota"),
    "halter-dress": (["Proenza Schouler", "Bottega Veneta"], "nota"), "fringe-jacket": (["Khaite", "Gucci"], "nota"),
    "mini-dress": (["Valentino", "Marni"], "otra"), "lavender-dress": (["Michael Kors", "Phillip Lim"], "otra"),
    "pillbox-hat": (["Prada", "Altuzarra"], "nota"), "cigarette-pants": (["Altuzarra", "Khaite"], "nota"),
    "faux-fur-coat": (["Louis Vuitton", "Gucci"], "nota"), "tailored-trousers": (["Hermès", "Tory Burch"], "nota"),
    "leather-dress": (["Proenza Schouler", "Bottega Veneta"], "nota"), "turtleneck": (["Proenza Schouler", "Prada"], "nota"),
    "feather-dress": (["Givenchy", "Bottega Veneta"], "nota"), "green-dress": (["Chloé", "Saint Laurent"], "nota"),
    "leopard-print": (["Versace", "Dior"], "nota"), "tea-length-dress": (["Loro Piana", "Prada"], "nota"),
    "cashmere-pants": (["The Row", "Balmain"], "nota"),
    "pillbox-hat-ss2025": (["Prada", "Valentino"], "nota"), "pencil-skirt-ss2025": (["Max Mara", "Toteme"], "nota"),
    "chiffon-cape-ss2025": (["Chanel", "Chloé"], "nota"), "sequin-dress-ss2025": (["Prada", "Rabanne"], "nota"),
    "80s-blazer-ss2025": (["Bottega Veneta", "Rabanne"], "otra"), "bubble-skirt-ss2025": (["Chloé", "Alaïa"], "otra"),
    "wide-leg-jeans-ss2025": (["Stella McCartney", "Sacai"], "otra"), "statement-sunglasses-ss2025": (["Prada", "McQueen"], "otra"),
    "one-leg-pants-ss2025": (["Rick Owens", "Courrèges"], "nota"), "tutu-skirt-ss2025": (["Carven", "Dries Van Noten"], "nota"),
    "dress-over-pants-ss2025": (["Fendi", "Phoebe Philo"], "nota"), "polka-dot-ss2025": (["Marc Jacobs", "Nina Ricci"], "nota"),
    "breton-sweater-ss2025": (["Proenza Schouler", "Max Mara"], "nota"),
    "leather-mini-skirt-ss2026": (["Hermès", "Mugler"], "nota"), "satin-scarf-ss2026": (["Celine", "Kallmeyer"], "nota"),
    "floral-print-ss2026": (["Chanel", "Balenciaga"], "nota"), "poplin-shirt-ss2026": (["Loewe", "Prada"], "nota"),
    "trench-coat-ss2026": (["Tom Ford", "Saint Laurent"], "nota"), "80s-fashion-ss2026": (["Saint Laurent", "Versace"], "nota"),
    "lilac-dress-ss2026": (["Versace", "Loewe"], "nota"), "preppy-outfit-ss2026": (["Miu Miu", "Loewe"], "nota"),
    "tweed-suit-ss2026": (["Chanel", "Dior"], "nota"), "bell-sleeve-ss2026": (["Gucci", "Saint Laurent"], "nota"),
    "feather-skirt-ss2026": (["Chanel", "Bottega Veneta"], "nota"), "yellow-dress-ss2026": (["Fendi", "Jil Sander"], "nota"),
    "chainmail-dress-ss2026": (["Burberry", "Conner Ives"], "nota"), "ruffle-dress-ss2026": (["Chanel", "McQueen"], "nota"),
    "flapper-dress-ss2026": (["Tory Burch", "Versace"], "nota"), "spaghetti-strap-top-ss2026": (["Eckhaus Latta", "Jil Sander"], "nota"),
    "low-rise-pants-ss2026": (["McQueen", "Prada"], "nota"), "power-shoulders-ss2026": (["Versace", "Saint Laurent"], "nota"),
    "fair-isle-sweater-fw2026": (["Altuzarra", "Khaite"], "nota"), "brocade-fw2026": (["Dior", "Bottega Veneta"], "nota"),
    "tailored-coat-fw2026": (["Jil Sander", "Tod's"], "nota"), "statement-coat-fw2026": (["Bottega Veneta", "Giorgio Armani"], "otra"),
    "polo-shirt-fw2026": (["Tory Burch", "Marni"], "nota"), "satin-dress-fw2026": (["Chloé", "Prada"], "nota"),
    "silk-shirt-fw2026": (["Kallmeyer", "Dior"], "nota"), "fur-coat-fw2026": (["Louis Vuitton", "Bottega Veneta"], "nota"),
    "brooch-fw2026": (["Khaite", "Simone Rocha"], "nota"), "check-shirt-fw2026": (["Chloé", "Acne Studios"], "nota"),
    "purple-dress-fw2026": (["Loewe", "Celine"], "nota"), "skirt-suit-fw2026": (["Jil Sander", "Tom Ford"], "otra"),
    "chunky-scarf-fw2026": (["Loewe", "Celine"], "nota"), "shearling-coat-fw2026": (["Dior", "Miu Miu"], "nota"),
    "lace-dress-fw2026": (["Gabriela Hearst", "Saint Laurent"], "otra"), "fringe-jacket-fw2026": (["Altuzarra", "Akris"], "otra"),
    "sheer-dress-fw2026": (["Khaite", "Prada"], "otra"), "pink-dress-fw2026": ([], "otra"),
    "brooch-fw2025": (["Prada", "Miu Miu"], "nota"), "black-lace-fw2025": (["Alaïa", "Dior"], "nota"),
    "statement-coat-fw2025": (["Roksanda", "Altuzarra"], "nota"), "cardigan-fw2025": (["Christopher John Rogers", "Tibi"], "nota"),
    "thigh-high-boots-fw2025": (["Stella McCartney", "Balmain"], "nota"), "asymmetric-jacket-fw2025": (["Givenchy", "Sacai"], "nota"),
    "ruffle-collar-fw2025": (["McQueen", "Dior"], "nota"), "floral-print-fw2025": (["Prada", "Erdem"], "nota"),
    "pearl-necklace-fw2025": (["Chanel", "Vaquera"], "nota"), "pencil-skirt-fw2025": (["Ferragamo", "Miu Miu"], "nota"),
    "neon-dress-fw2025": (["Marni", "Saint Laurent"], "nota"), "polka-dot-fw2025": (["Dries Van Noten", "Balenciaga"], "nota"),
    "jogging-pants-fw2025": (["Miu Miu", "Tom Ford"], "nota"),
}
def desfiles(i):
    marcas, origen = DESFILES[i]
    return [{"marca": m, "archivo": f"{i}-{k}.jpg", "origen": origen} for k, m in enumerate(marcas, 1)]

d = json.loads(ENTRADA.read_text(encoding="utf-8"))
d25 = json.loads((RAIZ / "app" / "datos" / "brief_ss2025.json").read_text(encoding="utf-8"))
assert d25["meta"]["meses"] == d["meta"]["meses"]
# FW2025 entra solo si pasó su chequeo (analisis/brief_fw2025/): si no, no va a la página
dfw = json.loads((RAIZ / "app" / "datos" / "brief_fw2025.json").read_text(encoding="utf-8"))
assert dfw["meta"]["meses"] == d["meta"]["meses"]
items = d["items"] + (d25["items"] if d25["meta"]["con_veredicto"] else []) + (dfw["items"] if dfw["meta"]["con_veredicto"] else [])
meses = d["meta"]["meses"]
tendencias = []
for it in items:
    if it["veredicto"] == "Sin señal clara":
        continue
    nombre, rubro = NOMBRES[it["termino"]]
    j = meses.index(it["mes_desfile"])
    sin, mj = it.get("sin_ago_sep_2025"), it.get("lectura_marjul")
    tendencias.append({
        "id": it["termino"].replace(" ", "-") + ("" if it["temporada"] in ("SS2024", "FW2024") else "-" + it["temporada"].lower()),
        "nota": (f"Sin agosto y septiembre de 2025, cuando Google empezó a medir distinto, la lectura da “{sin.lower()}”."
                 if sin and sin != it["veredicto"] else
                 f"Con solo marzo a julio de 2025, antes de que Google empezara a medir distinto, la lectura da “{mj.lower()}”."
                 if mj and mj != it["veredicto"] else ""),
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
    t["desfiles"] = desfiles(t["id"])

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
for v in vistas:
    v["desfiles"] = desfiles(v["id"])

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
TEMP = {"SS2024": ("Primavera 2024", "Spring 2024"), "FW2024": ("Otoño 2024", "Fall 2024"), "SS2025": ("Primavera 2025", "Spring 2025"),
        "FW2025": ("Otoño 2025", "Fall 2025"),
        "SS2026": ("Primavera 2026", "Spring 2026"), "FW2026": ("Otoño 2026", "Fall 2026")}
lineas = ["# Fotos para el prototipo", "",
          "Dos fotos por tendencia, de **dos desfiles distintos** de esa temporada, para respaldar que la tendencia se vio en más "
          "de una pasarela. Van en `prototipo/fotos/` con el nombre exacto de la columna **Archivo** (en `.jpg`). Esa carpeta está en "
          "`.gitignore`: **no se sube a GitHub** (el repo es público y las fotos tienen derechos).", "",
          "Cómo buscarlas: en Vogue Runway (vogue.com/fashion-shows) entrá a la colección de la columna **Desfile** y elegí un look "
          "vertical, de cuerpo entero, donde se vea la tendencia. O buscá en Google Imágenes el texto de la columna **Buscar**.", "",
          "**De dónde sale la marca:** *nota* = la nombra la nota del medio que eligió la tendencia; *otra* = esa nota no se pudo "
          "abrir o no nombra marcas, y la marca sale de otras notas de la misma temporada.", "",
          "Este archivo lo arma `prototipo/armar_datos.py`: no editarlo a mano.", ""]
for titulo, lista in ((f"Con veredicto ({len(tendencias)} tendencias)", tendencias), (f"Visto en 2026 ({len(vistas)} tendencias)", vistas)):
    for temp in ("FW2025", "SS2025", "FW2024", "SS2024", "SS2026", "FW2026"):
        grupo = [t for t in lista if t["temporada"] == temp]
        if not grupo:
            continue
        lineas += [f"## {titulo} · {TEMP[temp][0]}", "", "| Archivo | Tendencia | Desfile | Buscar | Marca sale de |", "|---|---|---|---|---|"]
        for t in grupo:
            if not t["desfiles"]:
                lineas.append(f"| `{t['id']}-1.jpg` y `{t['id']}-2.jpg` | {t['nombre']} | Ninguna nota nombra marcas: elegí dos en Vogue Runway | "
                              f"{t['termino']} runway {TEMP[temp][1].lower()} | – |")
            for f in t["desfiles"]:
                lineas.append(f"| `{f['archivo']}` | {t['nombre']} | {f['marca']} {TEMP[temp][1]} Ready-to-Wear | "
                              f"{f['marca']} {TEMP[temp][1].lower()} {t['termino']} | {f['origen']} |")
        lineas.append("")
(RAIZ / "prototipo" / "FOTOS.md").write_text("\n".join(lineas), encoding="utf-8")
