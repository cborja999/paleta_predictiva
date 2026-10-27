# Reproduce DIAGNOSTICO_2026.md: el salto de Google Trends en 2025-2026 y por que la lectura 2026 no se usa.
# Uso: python3 -I diagnostico_2026.py  (desde esta carpeta)
import csv, math, os, statistics as st, sys
AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, "..", "microtendencias"))
import m1  # noqa: E402

ser = {}
for r in csv.DictReader(open(os.path.join(AQUI, "datos", "trends_2026_web.csv"), encoding="utf-8")):
    ser.setdefault(r["termino"], {})[r["mes"]] = float(r["valor"])
terms = [t for t in csv.DictReader(open(os.path.join(AQUI, "terminos_declarados_2026.csv"), encoding="utf-8")) if t["termino"]]
def prom(t, a, b): return st.mean(v for k, v in ser[t].items() if a <= k <= b)

print("Nivel de cada mes contra el promedio 2024 del mismo termino (36 terminos):")
base = {t["termino"]: prom(t["termino"], "2024-01", "2024-12") for t in terms}
for m in sorted(k for k in ser[terms[0]["termino"]] if k >= "2024-10"):
    r = [ser[t][m] / base[t] for t in base if base[t] > 0]
    print(f"  {m}  mediana x{st.median(r):.2f}  max x{max(r):.2f}")

VENT = {"SS2026": ("2024-10", "2025-09", "2025-10", "2026-09"), "FW2026": ("2025-03", "2025-09", "2026-03", "2026-09")}
for tem, (a0, b0, a1, b1) in VENT.items():
    T = [t["termino"] for t in terms if t["temporada"] == tem]
    r1 = {t: math.log(prom(t, a1, b1) / prom(t, a0, b0)) for t in T}
    med = st.median(r1.values())
    g1 = [r1[t] - med for t in T]
    salto = [math.log(prom(t, "2026-02", "2026-05") / prom(t, "2025-02", "2025-05")) for t in T]
    nivel = [prom(t, "2024-01", "2024-12") for t in T]
    rho, p = m1.spearman(salto, g1)
    rho2, p2 = m1.spearman(nivel, salto)
    print(f"{tem}: Spearman g1 vs salto feb-may 2026 = {rho:.2f} (p={p:.3f}); nivel 2024 vs salto = {rho2:.2f} (p={p2:.3f})")
