"""Revisa la planilla de prensa contra las reglas de la hoja Instrucciones. No modifica nada, solo lista problemas."""
import csv, os, re, sys
from collections import Counter
AQUI = os.path.dirname(os.path.abspath(__file__))
ARCH = sys.argv[1] if len(sys.argv) > 1 else os.path.join(AQUI, 'planilla_prensa_notas_2026-10-20.csv')
COLORES = {'Negro','Blanco','Gris','Beige/Crema','Marron','Rojo','Burdeos/Vino','Rosa','Naranja','Amarillo','Verde','Oliva/Caqui','Azul','Celeste','Turquesa','Violeta','Metalizado','Estampado'}
PRENDAS = {'Vestido','Pantalon','Falda','Blazer','Abrigo','Mono','Top/Camisa','Sweater'}
LARGOS = {'Mini','Midi','Largo'}
APROBADOS = {'Infobae','La Nacion','Clarín / Elle','La Gaceta','Diario de Cuyo','Marie Claire Argentina'}
filas = list(csv.DictReader(open(ARCH, encoding='utf-8')))
prob = Counter(); det = []
def marca(i, tipo, txt):
    prob[tipo] += 1; det.append((i + 2, tipo, txt))
for i, r in enumerate(filas):
    if r['aprobado'] == 'si' and r['medio'] not in APROBADOS: marca(i, 'medio con nombre distinto al de la lista', r['medio'])
    if not re.fullmatch(r'\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])', r['fecha_nota']): marca(i, 'fecha invalida', r['fecha_nota'])
    for col, ok in (('colores', COLORES), ('prendas', PRENDAS), ('largos', LARGOS)):
        for v in [x for x in r[col].split(';') if x]:
            base = re.sub(r'\(.*\)', '', v)
            if base not in ok: marca(i, 'etiqueta fuera de la lista (%s)' % col, v)
    if 'staging.' in r['url']: marca(i, 'url de un servidor de pruebas (staging)', r['url'])
    if r['estado'] == '': marca(i, 'sin estado', r['titulo'][:50])
    t = r['temporada_mundial']; a = int(t[2:]) if re.fullmatch(r'(SS|FW)\d{4}', t) else 0
    if a and (a < 2023 or a > 2027): marca(i, 'fuera de la ventana SS2023-SS2027', t)
    if re.search(r'no (tiene una )?conexi|no se confirma|no confirma|no en tendencias derivadas', r['observaciones']): marca(i, 'la nota no se apoya en desfiles internacionales', r['titulo'][:50])
print('Filas:', len(filas), '| aprobadas:', sum(r['aprobado'] == 'si' for r in filas))
print('Estado:', dict(Counter(r['estado'] for r in filas)))
print('\nProblemas por tipo:')
for k, v in prob.most_common(): print('  %3d  %s' % (v, k))
print('\nDetalle (fila de la hoja, tipo, dato):')
for f, t, x in det: print('  fila %d | %s | %s' % (f, t, x))
