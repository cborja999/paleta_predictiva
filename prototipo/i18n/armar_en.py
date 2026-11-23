"""Arma prototipo/en.js: el diccionario español -> inglés que usa la app cuando se elige English.
Correr: python3 prototipo/i18n/armar_en.py"""
import json, pathlib
import en_app, en_datos
aqui = pathlib.Path(__file__).resolve().parent
d = {}
for m in (en_app, en_datos):
    for k, v in m.T.items():
        if k and k != v: d[k] = v
# Control: una traducción no puede contener otra clave como palabra suelta (se traduciría dos veces)
import re
B = "0-9A-Za-zÁÉÍÓÚÜÑáéíóúüñ"
claves = sorted(d, key=len, reverse=True)
patron = re.compile("|".join(("(?<![" + B + "])" if re.match("[" + B + "]", k[0]) else "") + re.escape(k) + ("(?![" + B + "])" if re.match("[" + B + "]", k[-1]) else "") for k in claves))
malas = {k: v for k, v in d.items() if patron.search(v)}
for k, v in malas.items(): print("se traduciria dos veces:", repr(k), "->", repr(v), "contiene", repr(patron.search(v).group()))
assert not malas, "arreglar las traducciones de arriba"
(aqui.parent / "en.js").write_text("// Generado por prototipo/i18n/armar_en.py. No editar a mano.\nwindow.EN_DIC = " + json.dumps(d, ensure_ascii=False, indent=0) + ";\n", encoding="utf-8")
print(len(d), "frases")
