import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fase2 import *
for fn in ('original','nueva'):
    rows=[]
    for k in temps:
        d0=mes_desfile(*k)
        if d0+23>LIMPIO: continue
        bl=[]
        for key,s in fam[fn].items():
            L0,L1,L2=prom(s,d0-24,d0-13),prom(s,d0-12,d0-1),prom(s,d0+12,d0+23)
            if None in (L0,L1,L2): continue
            bl.append([lg(L1,L0),lg(L2,L0),lg(L2,L1)])
        if len(bl)<8: continue
        ms=[median(b[i] for b in bl) for i in range(3)]
        for b in bl: rows.append([b[i]-ms[i] for i in range(3)])
    g=[r for r in rows if r[0]>=0.10]; c=[r for r in rows if abs(r[0])<0.10]
    # POST-HOC (no declarado): exigencia estricta = sigue creciendo (L2 vs L1 relativo > 0)
    print(fn,'estricto (post-hoc): gano interes y sigue CRECIENDO %.0f%% (n=%d) | control %.0f%% (n=%d)'%(100*sum(r[2]>0 for r in g)/len(g),len(g),100*sum(r[2]>0 for r in c)/len(c),len(c)))
    ret=sorted(r[1]/r[0] for r in g); print('   mediana de la suba que conserva: %.0f%%; p25=%.0f%% p75=%.0f%%'%(100*ret[len(ret)//2],100*ret[len(ret)//4],100*ret[3*len(ret)//4]))
