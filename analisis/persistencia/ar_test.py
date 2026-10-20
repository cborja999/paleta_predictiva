import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import io, contextlib
with contextlib.redirect_stdout(io.StringIO()):
    from fase2 import *
random.seed(2010)
def perm(x,y,stat,n=2000):
    obs=stat(x,y); m=0; y=list(y)
    for _ in range(n):
        random.shuffle(y); m+= stat(x,y)>=obs
    return obs,(m+1)/(n+1)
def rank(v):
    o=sorted(range(len(v)),key=lambda i:v[i]); r=[0]*len(v)
    for p,i in enumerate(o): r[i]=p
    return r
def spear(x,y):
    a,b=rank(x),rank(y); ma,mb=mean(a),mean(b)
    num=sum((i-ma)*(j-mb) for i,j in zip(a,b)); den=math.sqrt(sum((i-ma)**2 for i in a)*sum((j-mb)**2 for j in b))
    return num/den if den else 0
# TEST 1
print('TEST 1 - se queda LIMPIO (h=log(L2/L1)-mediana; no retrocede si h>=-0.10)')
for fn in ('original','nueva','AR'):
    rows=[]
    for k in temps:
        d0=mes_desfile(*k)
        if d0+23>LIMPIO: continue
        bl=[]
        for key,s in fam[fn].items():
            L0,L1,L2=prom(s,d0-24,d0-13),prom(s,d0-12,d0-1),prom(s,d0+12,d0+23)
            if None in (L0,L1,L2): continue
            bl.append([lg(L1,L0),lg(L2,L1)])
        if len(bl)<8: continue
        m=[median(b[i] for b in bl) for i in (0,1)]
        for b in bl: rows.append([b[0]-m[0],b[1]-m[1]])
    g=[r for r in rows if r[0]>=0.10]; c=[r for r in rows if abs(r[0])<0.10]
    sg=[r[1]>=-0.10 for r in g]; sc=[r[1]>=-0.10 for r in c]
    pg,pc=sum(sg)/len(sg),sum(sc)/len(sc); t=sg+sc; ng=len(g); mm=0
    for _ in range(2000):
        random.shuffle(t); mm+=(sum(t[:ng])/ng-sum(t[ng:])/len(c))>=pg-pc
    print('%-9s gano n=%d: no retrocede %.0f%% | control n=%d: %.0f%% | dif %+.0f pts p=%.3f | mediana h gano %+.2f'%(fn,len(g),100*pg,len(c),100*pc,100*(pg-pc),(mm+1)/2001,median(r[1] for r in g)))
# TEST 2
print('\nTEST 2 - Argentina vs mundo, retraso k meses')
comun=[k for k in nuevo_map if k in ar_map]
print('categorias comunes:',len(comun))
for K in (0,6,12,18):
    X=[];Y=[]
    for k in temps:
        d0=mes_desfile(*k)
        if d0+K-1>LIMPIO: continue
        bw=[];ba=[]
        ok=[]
        for key in comun:
            sm=Nm[nuevo_map[key]]; sa=Nar[ar_map[key]]
            a0,a1=prom(sm,d0-24,d0-13),prom(sm,d0-12,d0-1)
            b0,b1=prom(sa,d0+K-24,d0+K-13),prom(sa,d0+K-12,d0+K-1)
            if None in (a0,a1,b0,b1): continue
            ok.append((lg(a1,a0),lg(b1,b0)))
        if len(ok)<8: continue
        mw=median(o[0] for o in ok); ma=median(o[1] for o in ok)
        for o in ok: X.append(o[0]-mw); Y.append(o[1]-ma)
    r,p=perm(X,Y,spear)
    base=sum(y>=0.10 for y in Y)/len(Y)
    gx=[y>=0.10 for x,y in zip(X,Y) if x>=0.10]
    print('k=%2d meses | n=%d | Spearman %.3f p=%.3f | mundo gano => AR gano: %.0f%% (n=%d) vs base AR %.0f%%'%(K,len(X),r,p,100*sum(gx)/max(len(gx),1),len(gx),100*base))
