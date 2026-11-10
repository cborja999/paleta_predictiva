# Verificacion independiente: recalcula cada numero que muestra la pagina
# (prototipo/index.html + prototipo/datos.json) desde los CSV crudos, sin usar
# los JSON ni los *_detalle.csv intermedios, y dice si coincide.
#
# Uso (desde la raiz del repo):  python3 trazabilidad/verificar_numeros.py
# Escribe trazabilidad/numeros_de_la_pagina.csv y trazabilidad/salida_verificacion.txt
import csv, json, math, os, re, statistics as st
from collections import Counter, defaultdict

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AQUI = os.path.join(R, "trazabilidad")
def p(*a): return os.path.join(R, *a)
def filas(ruta): return list(csv.DictReader(open(p(ruta), encoding="utf-8")))
def am(s): y, m = s.split("-"); return int(y) * 12 + int(m) - 1

def serie(ruta):
    s = defaultdict(dict)
    for r in filas(ruta): s[r["termino"]][am(r["mes"])] = float(r["valor"])
    return s

pagina = json.load(open(p("prototipo", "datos.json"), encoding="utf-8"))
html = open(p("prototipo", "index.html"), encoding="utf-8").read()
texto = re.sub(r"<[^>]+>", " ", html)          # el texto de la pagina sin etiquetas

tabla, salida, fallas = [], [], []
def chequear(seccion, que, calculado, en_pagina, fuente, calculo, tol=0):
    ok = (calculado == en_pagina) if tol == 0 else abs(calculado - en_pagina) <= tol
    tabla.append([seccion, que, en_pagina, calculado, "si" if ok else "NO", fuente, calculo])
    if not ok: fallas.append(f"{seccion} | {que}: pagina {en_pagina}, recalculado {calculado}")
    return ok
def en_texto(frase): return frase in texto

# =====================================================================
# 1. TENDENCIAS CON Y SIN VEREDICTO (77): Google Trends crudo
# =====================================================================
FUENTES = {
    "SS2024": ("analisis/brief_2026/datos/trends_2024_web.csv", "analisis/brief_2026/terminos_declarados_2024.csv"),
    "FW2024": ("analisis/brief_2026/datos/trends_2024_web.csv", "analisis/brief_2026/terminos_declarados_2024.csv"),
    "SS2025": ("analisis/brief_2025/datos/trends_A_2011_2025-09.csv", "analisis/brief_2025/terminos_declarados_2025.csv"),
    "FW2025": ("analisis/brief_fw2025/datos/trends_A_2011_2025-09.csv", "analisis/brief_fw2025/terminos_declarados_fw2025.csv"),
}
calc = {}            # (temporada, termino) -> dict
medianas = {}
def empalmar(A, B):
    # FW2025 (regla fijada en REGLAS_BRIEF_FW2025.txt): descarga A hasta sep-2025 y, despues, descarga B
    # llevada a la escala de A con el cociente de sumas de ene-2024 a sep-2025
    S = {}
    for k, a in A.items():
        b = B.get(k, {}); comun = [m for m in range(am("2024-01"), am("2025-09") + 1) if m in a and m in b]
        sb = sum(b[m] for m in comun); s = dict(a)
        if sb > 0:
            fac = sum(a[m] for m in comun) / sb
            for m, v in b.items():
                if m > am("2025-09"): s[m] = v * fac
        S[k] = s
    return S

for tem, (rt, rterm) in FUENTES.items():
    S = serie(rt) if tem != "FW2025" else empalmar(serie(rt), serie("analisis/brief_fw2025/datos/trends_B_2024_2026.csv"))
    terms = [t for t in filas(rterm) if t["termino"] and t["temporada"] == tem]
    ok = []
    for t in terms:
        e = am(t["mes_desfile"]); s = S[t["termino"]]
        w = [s[k] for k in range(e - 12, e + 12)]           # 12 meses antes y 12 despues del desfile
        B0, B1 = st.mean(w[:12]), st.mean(w[12:])
        usable = sum(x == 0 for x in w) <= 8 and B0 > 0 and B1 > 0
        d = dict(B0=B0, B1=B1, usable=usable, ventana=w, mes=t["mes_desfile"])
        calc[(tem, t["termino"])] = d
        if usable: d["r1"] = math.log(B1 / B0); ok.append(d)
    med = st.median(d["r1"] for d in ok)
    medianas[tem] = med
    for d in ok:
        g = d["r1"] - med
        d["g1"] = g
        d["veredicto"] = "queda" if g >= 0.10 else ("riesgo" if g <= -0.10 else "sin")
        d["confianza"] = "" if abs(g) < 0.10 else ("Alta" if abs(g) >= 0.30 else "Media")
    salida.append(f"{tem}: {len(terms)} terminos declarados, {len(ok)} usables, mediana de la temporada {med:+.3f} "
                  f"(= {round((math.exp(med) - 1) * 100):+d}%)")

for t in pagina["tendencias"] + pagina["sin_senal_items"]:
    tem, term = t["temporada"], t["termino"]
    d = calc.get((tem, term))
    src = FUENTES[tem][0]
    if d is None or not d["usable"]:
        fallas.append(f"{tem} {term}: no esta entre los terminos usables del CSV crudo"); continue
    sec = f"Tendencia {tem} · {term}"
    chequear(sec, "veredicto", d["veredicto"], t["veredicto"], src, "g1 >= +0.10 queda; <= -0.10 riesgo; si no, sin señal")
    chequear(sec, "g1", round(d["g1"], 3), t["g1"], src, "log(B1/B0) - mediana de la temporada", tol=0.001)
    chequear(sec, "cambio descontando la temporada (%)", round((math.exp(d["g1"]) - 1) * 100), t["cambio_pct"], src, "exp(g1) - 1", tol=1)
    if t in pagina["tendencias"]:
        chequear(sec, "confianza", d["confianza"], t["confianza"], src, "Alta si |g1| >= 0.30; Media si no")
        ap = "baja" if d["veredicto"] == "riesgo" else ("alta" if d["confianza"] == "Alta" and not t["aviso"] and not t["nota"] else "media")
        chequear(sec, "cuánto apostar", ap, t["apuesta"], src, "riesgo: baja; queda, Alta y sin avisos: alta; si no: media")
        chequear(sec, "B0 (promedio 12 meses antes)", round(d["B0"], 2), t["b0"], src, "promedio de los 12 meses antes del desfile", tol=0.06)
        chequear(sec, "B1 (promedio 12 meses despues)", round(d["B1"], 2), t["b1"], src, "promedio de los 12 meses desde el desfile", tol=0.06)
        chequear(sec, "busquedas: cambio sin descontar (%)", round((d["B1"] / d["B0"] - 1) * 100), t["bruto_pct"], src, "B1/B0 - 1", tol=1)
        chequear(sec, "busquedas: cambio de la temporada (%)", round((math.exp(medianas[tem]) - 1) * 100), t["temporada_pct"], src,
                 "exp(mediana de log(B1/B0) de la temporada) - 1")
        # la curva dibujada: los 24 meses de la ventana tienen que ser los del CSV crudo
        serie_pag = t["serie"][-24:] if len(t["serie"]) >= 24 else t["serie"]
        dif = max(abs(a - b) for a, b in zip(serie_pag, d["ventana"]))
        chequear(sec, "curva (max diferencia mes a mes)", round(dif, 1), 0.0, src, "24 valores mensuales de Google Trends", tol=0.5)

tend, sin = pagina["tendencias"], pagina["sin_senal_items"]
chequear("Totales", "tendencias con veredicto", sum(1 for d in calc.values() if d.get("veredicto") in ("queda", "riesgo")), len(tend),
         "los 4 CSV de Trends + terminos_declarados", "cuenta")
chequear("Totales", "se quedan", sum(1 for d in calc.values() if d.get("veredicto") == "queda"), sum(t["veredicto"] == "queda" for t in tend),
         "idem", "cuenta")
chequear("Totales", "en riesgo", sum(1 for d in calc.values() if d.get("veredicto") == "riesgo"), sum(t["veredicto"] == "riesgo" for t in tend),
         "idem", "cuenta")
chequear("Totales", "sin señal clara", sum(1 for d in calc.values() if d.get("veredicto") == "sin"), pagina["sin_senal"], "idem", "cuenta")
descartadas = [f"{k[0]} {k[1]}" for k, d in calc.items() if not d["usable"]]
salida.append(f"Terminos declarados que no se usaron por poco volumen: {', '.join(descartadas) or 'ninguno'}")

# =====================================================================
# 2. EVIDENCIA (178 tendencias 2016-2024): Google Trends crudo
# =====================================================================
MUESTRAS = {
    "M1": ("analisis/microtendencias/datos/trends_microtendencias_web.csv", "analisis/microtendencias/terminos_declarados.csv"),
    "M2": ("analisis/microtendencias/datos/trends_microtendencias_web_m2.csv", "analisis/microtendencias/terminos_declarados_m2.csv"),
    "C1": ("analisis/hipotesis/datos/trends_c1_web.csv", "analisis/hipotesis/terminos_declarados_c1.csv"),
}
ev = []
for mu, (rt, rterm) in MUESTRAS.items():
    S = serie(rt); por_t = defaultdict(list)
    for t in filas(rterm):
        if not t["termino"] or t["termino"] not in S: continue
        e = am(t["mes_desfile"]); s = S[t["termino"]]
        w = [s.get(e + k, 0.0) for k in range(-12, 24)]       # 12 antes, 12 despues (1er anio), 12 mas (2do anio)
        B0, B1, B2 = st.mean(w[:12]), st.mean(w[12:24]), st.mean(w[24:])
        if sum(x == 0 for x in w) > 12 or min(B0, B1, B2) <= 0: continue
        por_t[t["temporada"]].append(dict(muestra=mu, temporada=t["temporada"], r1=math.log(B1 / B0), r2=math.log(B2 / B1)))
    for tem, fs in por_t.items():
        m1, m2 = st.median(f["r1"] for f in fs), st.median(f["r2"] for f in fs)
        for f in fs:
            g, c = f["r1"] - m1, f["r2"] - m2
            f["grupo"] = "SUBE" if g >= 0.10 else ("CAE" if g <= -0.10 else "PLANO")
            f["queda"] = c >= -0.10
            f["anio"] = int(tem[2:])
            ev.append(f)

FEV = "analisis/microtendencias/datos/*.csv + analisis/hipotesis/datos/trends_c1_web.csv"
def grupo(g, cond=lambda f: True): return [f for f in ev if f["grupo"] == g and cond(f)]
sube = grupo("SUBE")
chequear("Evidencia", "tendencias en la prueba", len(ev), len(json.load(open(p("app/datos/microtendencias.json")))["items"]), FEV,
         "terminos usables de M1+M2+C1")
salida.append(f"Evidencia: {len(ev)} tendencias; suben {len(sube)}, se quedan {sum(f['queda'] for f in sube)} "
              f"({100 * sum(f['queda'] for f in sube) / len(sube):.0f}%)")
chequear("Evidencia", "'9 de cada 10' que suben se quedan", round(10 * sum(f["queda"] for f in sube) / len(sube)), 9, FEV,
         "se queda = 2do anio (descontando la temporada) no cae mas de 10%")
reciente = lambda f: 2021 <= f["anio"] <= 2023          # ciclos 2021-2022, 2022-2023 y 2023-2024
s21, c21 = grupo("SUBE", reciente), grupo("CAE", reciente)
chequear("Evidencia", "suben 2021-2024: pasajeras / total", f"{sum(not f['queda'] for f in s21)} de {len(s21)}", "2 de 19", FEV, "ciclos 2021-2024")
chequear("Evidencia", "bajan 2021-2024: pasajeras / total", f"{sum(not f['queda'] for f in c21)} de {len(c21)}", "9 de 16", FEV, "ciclos 2021-2024")
ratio = (sum(not f["queda"] for f in c21) / len(c21)) / (sum(not f["queda"] for f in s21) / len(s21))
salida.append(f"Riesgo de las que bajan sobre las que suben (2021-2024): {ratio:.2f} veces")
chequear("Evidencia", "'unas 5 veces más' riesgo", round(ratio), 5, FEV, "(9/16) / (2/19)")
c1s = [f for f in sube if f["muestra"] == "C1"]
chequear("Método", "'1 de 17' pasajera (prueba nueva 2016-2018)", f"{sum(not f['queda'] for f in c1s)} de {len(c1s)}", "1 de 17", MUESTRAS["C1"][0], "C1, grupo SUBE")
mm = [f for f in ev if f["muestra"] in ("M1", "M2")]
pq = lambda L: round(100 * sum(f["queda"] for f in L) / len(L))
chequear("Método", "planas que se quedan (%)", pq([f for f in mm if f["grupo"] == "PLANO"]), 73, "M1 + M2", "PLANO que se quedan / PLANO")
chequear("Método", "suben que se quedan (%)", pq([f for f in mm if f["grupo"] == "SUBE"]), 88, "M1 + M2", "SUBE que se quedan / SUBE")
salida.append(f"   (con las 178, no solo M1+M2: planas {pq(grupo('PLANO'))}%, suben {pq(sube)}%)")
# ciclo por ciclo (grafico de barras de Metodo)
for c in pagina["ciclos"]:
    y = int(c["ciclo"][:4]); s_, c_ = grupo("SUBE", lambda f: f["anio"] == y), grupo("CAE", lambda f: f["anio"] == y)
    chequear("Método · ciclos", f"{c['ciclo']} suben pasajeras", f"{sum(not f['queda'] for f in s_)}/{len(s_)}",
             f"{c['sube_pasajeras']}/{c['sube_n']}", FEV, "anio de la temporada -> anio siguiente")
    chequear("Método · ciclos", f"{c['ciclo']} bajan pasajeras", f"{sum(not f['queda'] for f in c_)}/{len(c_)}",
             f"{c['cae_pasajeras']}/{c['cae_n']}", FEV, "idem")
peor = max(sum(not f["queda"] for f in grupo("SUBE", lambda f, y=y: f["anio"] == y)) / max(1, len(grupo("SUBE", lambda f, y=y: f["anio"] == y)))
           for y in range(2016, 2024))
salida.append(f"Peor ciclo de las que suben: {100 * peor:.0f}% pasajeras (la linea del grafico marca 20%)")
tam = {mu: sum(f["muestra"] == mu for f in ev) for mu in MUESTRAS}
salida.append(f"Tamanio de cada muestra: {tam}; temporadas del brief: " +
              ", ".join(f"{t} {sum(1 for k, d in calc.items() if k[0] == t and d['usable'])}" for t in FUENTES))

# =====================================================================
# 3. PASARELA Y COLORES: clasificaciones de Gemini (fila por look)
# =====================================================================
G = [r for r in filas("datasets_procesados/resultados_gemini.csv") if not r["error"].strip()]
chequear("Método", "looks de Vogue Runway clasificados", len(G), 2430, "datasets_procesados/resultados_gemini.csv", "filas sin error")
salida.append(f"Casas: {len({r['marca'] for r in G})}; temporadas: {len({(r['temporada'], r['anio']) for r in G})}")
INV = {"", "no_aplica", "No aplica", "Otro", "otro"}
por_t = defaultdict(list)
for r in G: por_t[f"{r['temporada']}{r['anio']}"].append(r["color_dominante"].strip())
def share(cat, temps):
    v = []
    for t in temps:
        vals = [x for x in por_t[t] if x not in INV]
        v.append(100 * vals.count(cat) / len(vals) if len(vals) >= 15 else 0)
    return sum(v) / len(v)
meta = pagina["colores_meta"]
for c in pagina["colores"]:
    cat = {"Marrón": "Marron", "Beige y crema": "Beige/Crema"}.get(c["nombre"], c["nombre"])   # nombre en el CSV
    rec, pre = share(cat, meta["recientes"]), share(cat, meta["previas"])
    sec = f"Color · {c['nombre']}"
    chequear(sec, "% de looks (3 temporadas recientes)", round(rec, 1), c["reciente"], "resultados_gemini.csv (color_dominante)",
             "promedio de " + "+".join(meta["recientes"]), tol=0.1)
    chequear(sec, "1 de cada N looks", round(100 / rec), c["cada"], "idem", "100 / % exacto")
    chequear(sec, "cambio (puntos)", round(rec - pre, 1), c["cambio_pts"], "idem", "reciente - " + "+".join(meta["previas"]))

# =====================================================================
# 4. NUMEROS ESCRITOS A MANO EN EL HTML: que esten y que coincidan
# =====================================================================
for frase in ["9 de cada 10", "178 tendencias", "2 de 19", "9 de 16", "unas 5 veces", "2.430 looks", "1 de 17", "73%", "88%", "122 tendencias"]:
    chequear("Texto de la página", f"'{frase}' aparece", en_texto(frase), True, "prototipo/index.html", "busqueda de texto")
# "7 de 14" (Entrega 2) se saco de la pagina: sus CSV crudos no estan en el repo y media 2026, cuando Google cambio la forma de medir
chequear("Método", "'7 de 14' ya no esta en la pagina", en_texto("7 de 14"), False, "prototipo/index.html", "busqueda de texto")
chequear("Método", "'122 tendencias' (M1 + M2)", len(mm), 122, "M1 + M2", "terminos usables")

# =====================================================================
os.makedirs(AQUI, exist_ok=True)
with open(os.path.join(AQUI, "numeros_de_la_pagina.csv"), "w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh)
    w.writerow(["seccion", "numero", "en_la_pagina", "recalculado", "coincide", "fuente_cruda", "calculo"])
    w.writerows(tabla)
n_ok = sum(1 for x in tabla if x[4] == "si")
salida = ["VERIFICACION INDEPENDIENTE DE LOS NUMEROS DE LA PAGINA",
          f"{len(tabla)} chequeos: {n_ok} coinciden, {len(tabla) - n_ok} no", ""] + salida + ["", "NO COINCIDEN:"] + (fallas or ["ninguno"])
open(os.path.join(AQUI, "salida_verificacion.txt"), "w", encoding="utf-8").write("\n".join(salida) + "\n")
print("\n".join(salida))
