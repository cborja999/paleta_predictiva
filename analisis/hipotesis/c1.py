# Prueba confirmatoria C1 de la hipotesis (reglas en REGLAS_HIPOTESIS_C1.txt, fijadas antes de bajar los datos).
# Usa las mismas medidas que analisis/microtendencias/m1.py.
# Uso: python3 -I c1.py  (desde esta carpeta)
import csv, os, random, sys
AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, "..", "microtendencias"))
import m1  # noqa: E402

def cargar(nombre):
    from collections import defaultdict
    ser = defaultdict(dict)
    for r in csv.DictReader(open(os.path.join(AQUI, "datos", nombre), encoding="utf-8")):
        ser[r["termino"]][m1.am(r["mes"])] = float(r["valor"])
    return ser

terms = [t for t in csv.DictReader(open(os.path.join(AQUI, "terminos_declarados_c1.csv"), encoding="utf-8")) if t["termino"]]
previos = {t["termino"] for f in ("terminos_declarados.csv", "terminos_declarados_m2.csv")
           for t in csv.DictReader(open(os.path.join(AQUI, "..", "microtendencias", f), encoding="utf-8")) if t["termino"]}

def pas(f): return f["c2"] < -0.10

def evaluar(ok, titulo, out):
    S = [f for f in ok if f["grupo"] == "SUBE"]; C = [f for f in ok if f["grupo"] == "CAE"]; P = [f for f in ok if f["grupo"] == "PLANO"]
    ps, pc, pp = sum(map(pas, S)), sum(map(pas, C)), sum(map(pas, P))
    rs = ps / len(S) if S else float("nan"); rc = pc / len(C) if C else float("nan")
    p = m1.fisher(pc, len(C) - pc, ps, len(S) - ps) if S and C else float("nan")
    out.append(f"  {titulo}")
    out.append(f"     usables: {len(ok)} | SUBE {len(S)} | PLANO {len(P)} | CAE {len(C)}")
    out.append(f"     pasajeras: SUBE {ps}/{len(S)} = {100*rs:.0f}% | PLANO {pp}/{len(P)} = {100*pp/max(len(P),1):.0f}% | CAE {pc}/{len(C)} = {100*rc:.0f}%")
    # cociente CAE/SUBE con bootstrap
    random.seed(1); bs = []
    for _ in range(5000):
        s = [random.choice(S) for _ in S]; c = [random.choice(C) for _ in C]
        a = sum(map(pas, s)) / len(s); b = sum(map(pas, c)) / len(c)
        bs.append(b / a if a > 0 else float("inf"))
    bs.sort(); lo, hi = bs[int(0.025 * 5000)], bs[int(0.975 * 5000) - 1]
    ratio = rc / rs if rs > 0 else float("inf")
    if ps == 0:
        out.append(f"     cociente CAE/SUBE: no se puede calcular (0 pasajeras en SUBE) | Fisher CAE vs SUBE p={p:.3f}")
    else:
        hs = "infinito" if hi == float("inf") else f"{hi:.1f}"
        out.append(f"     cociente CAE/SUBE = {ratio:.1f} (IC95% bootstrap {lo:.1f} a {hs}) | Fisher CAE vs SUBE p={p:.3f}")
    Ha = rs <= 0.20
    Hb = (rc >= 3 * rs) and p < 0.05
    if len(S) < 8 or len(C) < 8: ver = "CASOS INSUFICIENTES (menos de 8 en SUBE o CAE)"
    elif Ha and Hb: ver = "CONFIRMA"
    elif Ha and rc > rs: ver = "CONFIRMA EN PARTE"
    else: ver = "NO CONFIRMA"
    out.append(f"     H-a (SUBE pasajeras <= 20%): {'si' if Ha else 'no'} | H-b (CAE >= 3x SUBE y p<0.05): {'si' if Hb else 'no'}  ->  {ver}")
    return dict(S=(ps, len(S)), C=(pc, len(C)), P=(pp, len(P)), p=p, ratio=ratio, ic=(lo, hi), ver=ver)

out = []
filas, ok = m1.medir(cargar("trends_c1_web.csv"), terms)
out.append("=" * 78); out.append("PRUEBA CONFIRMATORIA C1 (2016-2018, muestra nueva) - Google busqueda web, MUNDO")
out.append(f"  terminos: {len(filas)} | descartados por volumen: {len(filas)-len(ok)}")
for f in filas:
    if f["usable"] != "si": out.append(f"     descartado: {f['termino']} ({f['motivo']})")
res = evaluar(ok, "PRINCIPAL", out)
evaluar([f for f in ok if f["termino"] not in previos], "SENSIBILIDAD: sin terminos que ya estaban en M1/M2", out)
out.append("  Por temporada (descriptivo):")
for tem in ["FW2016", "SS2017", "FW2017", "SS2018", "FW2018"]:
    x = [f for f in ok if f["temporada"] == tem]
    S = [f for f in x if f["grupo"] == "SUBE"]; C = [f for f in x if f["grupo"] == "CAE"]
    out.append(f"     {tem}: n={len(x)} | pasajeras SUBE {sum(map(pas,S))}/{len(S)} | CAE {sum(map(pas,C))}/{len(C)}")
with open(os.path.join(AQUI, "c1_detalle.csv"), "w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh)
    w.writerow(["temporada", "termino", "tipo", "tendencia_fuente", "usable", "B0", "B1", "B2", "g1", "c2", "grupo", "se_queda"])
    for r in filas:
        if r["usable"] == "si":
            w.writerow([r["temporada"], r["termino"], r["tipo"], r["tendencia_fuente"], "si", f"{r['B0']:.2f}", f"{r['B1']:.2f}",
                        f"{r['B2']:.2f}", f"{r['g1']:.3f}", f"{r['c2']:.3f}", r["grupo"], "si" if r["c2"] >= -0.10 else "no"])
        else:
            w.writerow([r["temporada"], r["termino"], r["tipo"], r["tendencia_fuente"], "no"] + [""] * 7)
# ---- total de las tres muestras y ciclos (descriptivo) ----
det = []
for f in ("m1_detalle.csv", "m2_detalle.csv"):
    det += [dict(r, muestra=f[:2].upper()) for r in csv.DictReader(open(os.path.join(AQUI, "..", "microtendencias", f), encoding="utf-8")) if r["usable"] == "si"]
det += [dict(r, muestra="C1") for r in csv.DictReader(open(os.path.join(AQUI, "c1_detalle.csv"), encoding="utf-8")) if r["usable"] == "si"]
out.append("=" * 78); out.append("TOTAL TRES MUESTRAS (descriptivo: M1 y M2 son de donde salio la hipotesis)")
S = [r for r in det if r["grupo"] == "SUBE"]; C = [r for r in det if r["grupo"] == "CAE"]; P = [r for r in det if r["grupo"] == "PLANO"]
q = lambda L: sum(r["se_queda"] == "no" for r in L)
out.append(f"  pasajeras: SUBE {q(S)}/{len(S)} = {100*q(S)/len(S):.0f}% | PLANO {q(P)}/{len(P)} = {100*q(P)/len(P):.0f}% | CAE {q(C)}/{len(C)} = {100*q(C)/len(C):.0f}% | Fisher CAE vs SUBE p={m1.fisher(q(C), len(C)-q(C), q(S), len(S)-q(S)):.3f}")
out.append("  Ciclos (anio de la temporada -> anio siguiente):")
with open(os.path.join(AQUI, "ciclos.csv"), "w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh); w.writerow(["ciclo", "muestras", "n", "sube_pasajeras", "sube_n", "plano_pasajeras", "plano_n", "cae_pasajeras", "cae_n"])
    for y in sorted({r["temporada"][2:] for r in det}):
        X = [r for r in det if r["temporada"][2:] == y]
        s_, p_, c_ = [[r for r in X if r["grupo"] == g] for g in ("SUBE", "PLANO", "CAE")]
        ms = "+".join(sorted({r["muestra"] for r in X}))
        w.writerow([f"{y}-{int(y)+1}", ms, len(X), q(s_), len(s_), q(p_), len(p_), q(c_), len(c_)])
        out.append(f"     {y} -> {int(y)+1} ({ms}): n={len(X)} | pasajeras SUBE {q(s_)}/{len(s_)} | PLANO {q(p_)}/{len(p_)} | CAE {q(c_)}/{len(c_)}")
print("\n".join(out))
