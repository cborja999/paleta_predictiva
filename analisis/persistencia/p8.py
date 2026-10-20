import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fase2 import *
def p8(series,nom):
    rows=[]
    for k in temps:
        d0=mes_desfile(*k)
        if d0+23>LIMPIO: continue
        bl=[]
        for key,s in series.items():
            L0,L1,L2=prom(s,d0-24,d0-13),prom(s,d0-12,d0-1),prom(s,d0+12,d0+23)
            if None in (L0,L1,L2): continue
            bl.append([k,key,lg(L1,L0),lg(L2,L0)])
        if len(bl)<8: continue
        m1=median(b[2] for b in bl); m2=median(b[3] for b in bl)
        for b in bl: b[2]-=m1; b[3]-=m2; rows.append(b)
    g=[r for r in rows if r[2]>=0.10]; c=[r for r in rows if abs(r[2])<0.10]
    sg=[r[3]>0 for r in g]; sc=[r[3]>0 for r in c]
    pg,pc=sum(sg)/len(sg),sum(sc)/len(sc); todos=sg+sc; ng=len(g); m=0
    for _ in range(2000):
        random.shuffle(todos); m+=(sum(todos[:ng])/ng-sum(todos[ng:])/len(c))>=pg-pc
    fuerte=sum(1 for r in g if r[3]>=0.5*r[2])/len(g); paj=sum(1 for r in g if r[3]<=0)/len(g)
    print('%-9s casos=%d | gano interes n=%d: se queda %.0f%%, se queda fuerte %.0f%%, moda pasajera %.0f%% | control n=%d: %.0f%% | dif %+.0f pts p=%.3f'%(nom,len(rows),len(g),100*pg,100*fuerte,100*paj,len(c),100*pc,100*(pg-pc),(m+1)/2001))
    return g
for fn in ('original','nueva','AR'): p8(fam[fn],fn)
# por tipo (descriptivo)
for fn in ('original','nueva'):
    ser=fam[fn]
    for tipo in ('color','prenda'):
        sub={k:v for k,v in ser.items() if k[0]==tipo or (tipo=='prenda' and k[0]=='largo')}
        if len([1 for k in sub])>=8: p8(sub,fn+'/'+tipo)
