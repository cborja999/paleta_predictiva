# Cruce: prensa internacional + pasarela + busquedas, ciclo d0=oct-2022. Reglas: REGLAS_PRENSA_INTERNACIONAL_2022.txt
import sys, os, io, contextlib, csv
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
with contextlib.redirect_stdout(io.StringIO()):
    from fase2 import *
from scipy.stats import fisher_exact
notas=list(csv.DictReader(open(REPO+'datasets/prensa_internacional/notas_2022.csv',encoding='utf-8')))
def pct(a,n): return '%d/%d = %s'%(a,n,('%.0f%%'%(100*a/n)) if n else 'n/a')
def fx(a,b,c,d):
    if min(a+b,c+d)==0: return float('nan')
    return fisher_exact([[a,b],[c,d]])[1]
k=('SS',2023); d0=mes_desfile(*k)
def pas(key):
    t=[x for x in temps if mes_desfile(*x)<=d0]; rec,ant=t[-3:],t[-6:-3]; sh=share.get(key,{})
    f=lambda ts: sum(sh.get(x,0) for x in ts)/3
    return f(rec)-f(ant)>=1.0
def corrida(NN,nombre):
    n=len(NN); porT={}
    for x in NN: porT[x['temporada']]=porT.get(x['temporada'],0)+1
    print('\n'+'='*70); print(nombre,'| notas:',n,porT)
    if n<12 or min(porT.values())<3 or len(porT)<3: print('COBERTURA INSUFICIENTE'); return
    col={'color':'colores','prenda':'prendas','largo':'largos'}
    def pr(key):
        c=sum(1 for x in NN if key[1] in x[col[key[0]]].split(';')); return c/n
    filas=[]
    for fn in ('original','nueva'):
        for f in casos(fam[fn]):
            if f['k']!=k or f['key'][0] not in col: continue  # siluetas: la prensa no se etiqueto por silueta
            p=pr(f['key']); filas.append(dict(fn=fn,key=f['key'],busq=f['inercia']>0,prensa=p>=0.25,pas=pas(f['key']),sube=f['y']>0,p=p))
    # C1
    a=[r for r in filas if r['busq']]
    a1=[r for r in a if r['prensa']]; a0=[r for r in a if not r['prensa']]
    s=lambda L:sum(r['sube'] for r in L)
    print('C1 busquedas "sube": con prensa -> sube %s | sin prensa -> sube %s | Fisher p=%.3f'%(pct(s(a1),len(a1)),pct(s(a0),len(a0)),fx(s(a1),len(a1)-s(a1),s(a0),len(a0)-s(a0))))
    full=[r for r in filas if r['busq'] and r['prensa'] and r['pas']]; rest=[r for r in filas if r not in full]
    print('C2 coincidencia completa (prensa+pasarela+busquedas) -> sube %s | resto -> sube %s | Fisher p=%.3f'%(pct(s(full),len(full)),pct(s(rest),len(rest)),fx(s(full),len(full)-s(full),s(rest),len(rest)-s(rest))))
    print('   pares con coincidencia completa:',[(r['fn'],r['key'][1],'sube' if r['sube'] else 'no sube') for r in full])
    print('   categorias con prensa (>=25%%): %s'%sorted({r['key'][1] for r in filas if r['prensa']}))
    print('   categorias SIN prensa: %s'%sorted({r['key'][1] for r in filas if not r['prensa']}))
    return filas
corrida(notas,'PRINCIPAL (todas las notas)')
corrida([x for x in notas if x['tipo']!='galeria'],'SENSIBILIDAD (sin las 2 galerias de Vogue Scandinavia)')
# detalle por categoria
print('\nDetalle por categoria (principal): % de notas que la nombran')
n=len(notas)
for tp,colname in (('color','colores'),('prenda','prendas'),('largo','largos')):
    cats=sorted({c for x in notas for c in x[colname].split(';') if c})
    print(' ',tp,{c:'%d%%'%round(100*sum(1 for x in notas if c in x[colname].split(';'))/n) for c in cats})
