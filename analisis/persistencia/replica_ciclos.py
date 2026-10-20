# Replica del brief en ciclos anteriores. Reglas: REGLAS_REPLICA_2022_2023.txt (fijadas antes de correr).
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import io, contextlib
with contextlib.redirect_stdout(io.StringIO()):
    from fase2 import *
from scipy.stats import fisher_exact
CICLOS=[(('SS',2023),'oct-2022 (PRINCIPAL, 2022-2023)'),(('SS',2022),'oct-2021 (secundario)'),(('SS',2021),'oct-2020 (secundario)')]
def pas_senal(key,d0):
    t=[k for k in temps if mes_desfile(*k)<=d0]
    rec,ant=t[-3:],t[-6:-3]
    sh=share.get(key,{})
    f=lambda ts: sum(sh.get(k,0) for k in ts)/3
    return f(rec)-f(ant)>=1.0, round(f(rec)-f(ant),1), rec
def fx(a,b,c,d):
    # a,b = (si,no) del grupo 1 ; c,d = (si,no) del grupo 2
    if min(a+b,c+d)==0: return float('nan')
    return fisher_exact([[a,b],[c,d]])[1]
def pct(a,n): return '%d/%d = %s'%(a,n,('%.0f%%'%(100*a/n)) if n else 'n/a')
casos_f={fn:casos(fam[fn]) for fn in ('original','nueva','AR')}
print('Las series de busqueda tienen datos limpios hasta dic-2024; ciclo d0=oct-2023 no se evalua (resultado cae en 2025).\n')
tot={fn:[] for fn in casos_f}
for k,nom in CICLOS:
    d0=mes_desfile(*k)
    print('='*78); print('CICLO d0 =',nom,'| resultado = cambio oct-%d a sep-%d vs oct-%d a sep-%d'%(d0//12+1,d0//12+2,d0//12-1,d0//12))
    filas=[]
    for fn,C in casos_f.items():
        for f in C:
            if f['k']!=k: continue
            ps,dif,rec=pas_senal(f['key'],d0)
            filas.append(dict(fn=fn,key=f['key'],busq=f['inercia']>0,pas=ps,dif=dif,sube=f['y']>0,y=f['y']))
    tot_ciclo=filas
    print('temporadas "recientes" de pasarela:',[a+str(b) for a,b in rec])
    for fn in ('original','nueva','AR'):
        R=[r for r in filas if r['fn']==fn]
        a=[r for r in R if r['busq']]; b=[r for r in R if not r['busq']]
        print('\n  [%s] pares: %d'%(fn,len(R)))
        print('   P1 busquedas "sube" -> sube: %s | busquedas "no sube" -> sube: %s | Fisher p=%.3f'%(pct(sum(r['sube'] for r in a),len(a)),pct(sum(r['sube'] for r in b),len(b)),fx(sum(r['sube'] for r in a),sum(not r['sube'] for r in a),sum(r['sube'] for r in b),sum(not r['sube'] for r in b))))
        if fn!='AR':
            a1=[r for r in a if r['pas']]; a0=[r for r in a if not r['pas']]
            print('   P2 dentro de "sube": con pasarela -> sube: %s | sin pasarela -> sube: %s | Fisher p=%.3f'%(pct(sum(r['sube'] for r in a1),len(a1)),pct(sum(r['sube'] for r in a0),len(a0)),fx(sum(r['sube'] for r in a1),sum(not r['sube'] for r in a1),sum(r['sube'] for r in a0),sum(not r['sube'] for r in a0))))
            allp=[r for r in R if r['pas']]; nop=[r for r in R if not r['pas']]
            print('      pasarela sola (todos los pares): con pasarela -> sube %s | sin -> sube %s'%(pct(sum(r['sube'] for r in allp),len(allp)),pct(sum(r['sube'] for r in nop),len(nop))))
        tot[fn]+= [dict(r,ciclo=nom) for r in R]
    # P3 acuerdo entre familias
    O={r['key']:r for r in filas if r['fn']=='original'}; N={r['key']:r for r in filas if r['fn']=='nueva'}
    com=[k2 for k2 in O if k2 in N]
    ac=[k2 for k2 in com if O[k2]['busq'] and N[k2]['busq']]; de=[k2 for k2 in com if not(O[k2]['busq'] and N[k2]['busq'])]
    sub=lambda L: sum(O[x]['sube'] and N[x]['sube'] for x in L)
    print('\n  P3 categorias en ambas familias: %d | las dos "sube" -> las dos suben: %s | resto -> las dos suben: %s | Fisher p=%.3f'%(len(com),pct(sub(ac),len(ac)),pct(sub(de),len(de)),fx(sub(ac),len(ac)-sub(ac),sub(de),len(de)-sub(de))))
    print('     categorias con las dos "sube":',[x[1] for x in ac])
print('\n'+'='*78); print('TOTAL de los 3 ciclos (descriptivo; los pares de un mismo ciclo no son independientes)')
for fn in ('original','nueva','AR'):
    R=tot[fn]; a=[r for r in R if r['busq']]; b=[r for r in R if not r['busq']]
    print(' [%s] P1: "sube"->sube %s | "no sube"->sube %s | Fisher p=%.3f'%(fn,pct(sum(r['sube'] for r in a),len(a)),pct(sum(r['sube'] for r in b),len(b)),fx(sum(r['sube'] for r in a),sum(not r['sube'] for r in a),sum(r['sube'] for r in b),sum(not r['sube'] for r in b))))
    if fn!='AR':
        a1=[r for r in a if r['pas']]; a0=[r for r in a if not r['pas']]
        print('       P2: con pasarela %s | sin pasarela %s | Fisher p=%.3f'%(pct(sum(r['sube'] for r in a1),len(a1)),pct(sum(r['sube'] for r in a0),len(a0)),fx(sum(r['sube'] for r in a1),sum(not r['sube'] for r in a1),sum(r['sube'] for r in a0),sum(not r['sube'] for r in a0))))
