import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import io, contextlib
with contextlib.redirect_stdout(io.StringIO()):
    from fase2 import *
exec(open(S+'ar_test.py').read().split('# TEST 1')[0].split('random.seed(2010)')[1])
random.seed(2011)
SA=cargar_csv(S+'datos/trends_shopping_AR_2026-10-20.csv')
ser={}
for k,t in ar_map.items():
    s=SA[t]; z=sum(1 for v in s.values() if v==0)/len(s)
    print('%-18s ceros=%.0f%% %s'%(t,100*z,'' if z<=0.5 else 'NO USABLE'))
    if z<=0.5: ser[k]=s
print('usables:',len(ser))
rows=[]
for k in temps:
    d0=mes_desfile(*k)
    if d0+23>LIMPIO: continue
    bl=[]
    for key,s in ser.items():
        L0,L1,L2=prom(s,d0-24,d0-13),prom(s,d0-12,d0-1),prom(s,d0+12,d0+23)
        if None in (L0,L1,L2): continue
        bl.append([lg(L1,L0),lg(L2,L0),lg(L2,L1)])
    if len(bl)<8: continue
    m=[median(b[i] for b in bl) for i in range(3)]
    for b in bl: rows.append([b[i]-m[i] for i in range(3)])
g=[r for r in rows if r[0]>=0.10]; c=[r for r in rows if abs(r[0])<0.10]
def test(nom,f):
    sg=[f(r) for r in g]; sc=[f(r) for r in c]; pg,pc=sum(sg)/len(sg),sum(sc)/len(sc); t=sg+sc; ng=len(g); mm=0
    for _ in range(2000):
        random.shuffle(t); mm+=(sum(t[:ng])/ng-sum(t[ng:])/len(c))>=pg-pc
    print('%s: casos=%d | gano n=%d: %.0f%% | control n=%d: %.0f%% | dif %+.0f pts p=%.3f'%(nom,len(rows),len(g),100*pg,len(c),100*pc,100*(pg-pc),(mm+1)/2001))
test('T1 se queda (original, base L0)',lambda r:r[1]>0)
test('T2 se queda limpio (L2 vs L1)',lambda r:r[2]>=-0.10)
print('\nT3 retraso: suba mundial (busqueda general) vs suba Shopping AR')
for K in (0,6,12,18):
    X=[];Y=[]
    for k in temps:
        d0=mes_desfile(*k)
        if d0+K-1>LIMPIO: continue
        ok=[]
        for key,s in ser.items():
            if key not in nuevo_map: continue
            sm=Nm[nuevo_map[key]]
            a0,a1=prom(sm,d0-24,d0-13),prom(sm,d0-12,d0-1)
            b0,b1=prom(s,d0+K-24,d0+K-13),prom(s,d0+K-12,d0+K-1)
            if None in (a0,a1,b0,b1): continue
            ok.append((lg(a1,a0),lg(b1,b0)))
        if len(ok)<8: continue
        mw=median(o[0] for o in ok); ma=median(o[1] for o in ok)
        for o in ok: X.append(o[0]-mw); Y.append(o[1]-ma)
    r,p=perm(X,Y,spear)
    gx=[y>=0.10 for x,y in zip(X,Y) if x>=0.10]
    print('k=%2d | n=%d | Spearman %.3f p=%.3f | mundo gano => Shopping AR gano: %.0f%% (n=%d) vs base %.0f%%'%(K,len(X),r,p,100*sum(gx)/max(len(gx),1),len(gx),100*sum(y>=0.10 for y in Y)/len(Y)))
