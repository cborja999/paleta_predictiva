import csv, math, random
from collections import defaultdict
from statistics import median, mean
random.seed(19)
import os
REPO=os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..'))+'/'
S=os.path.dirname(os.path.abspath(__file__))+'/'
def am(y,m): return y*12+m-1
ULT=am(2026,9); LIMPIO=am(2024,12)
def mes_desfile(t,a): return am(a,3) if t=='FW' else am(a-1,10)
def prom(s,a,b):
    v=[s[k] for k in range(a,b+1) if k in s]; return sum(v)/len(v) if len(v)==b-a+1 else None
def lg(x,y): return math.log(max(x,0.3)/max(y,0.3))
# nuevos
N={}
for r in csv.DictReader(open(S+'datos/trends_nuevos_2026-10-19.csv')):
    y,m=r['mes'].split('-'); N.setdefault((r['geo'],r['termino']),{})[am(int(y),int(m))]=float(r['valor'])
# originales
O={};meta={}
for r in csv.DictReader(open(REPO+'datasets/trends/trends_unificado.csv',encoding='utf-8')):
    y,m=r['mes'].split('-');a=am(int(y),int(m))
    if a>ULT: continue
    O.setdefault(r['termino'],{})[a]=float(r['valor']); meta[r['termino']]=(r['tipo'],r['categoria_gemini'],r['usable'],float(r['max_serie']))
el={}
for t,(tp,c,u,mx) in meta.items():
    if not tp or u!='si': continue
    if (tp,c) not in el or mx>meta[el[(tp,c)]][3]: el[(tp,c)]=t
nuevo_map={('color','Rosa'):'pink dress',('color','Rojo'):'red dress',('color','Negro'):'black dress',('color','Blanco'):'white dress',('color','Azul'):'blue dress',('color','Verde'):'green dress',('color','Marron'):'brown dress',('color','Beige/Crema'):'beige dress',('color','Naranja'):'orange dress',('color','Gris'):'gray dress',('color','Metalizado'):'silver dress',
 ('prenda','Falda'):'skirt outfit',('largo','Midi'):'midi skirt outfit',('largo','Mini'):'mini skirt outfit',('prenda','Blazer/Saco'):'blazer outfit',('prenda','Pantalon'):'trousers outfit',('prenda','Abrigo/Campera'):'coat outfit',('prenda','Tejido/Sweater'):'sweater outfit',('prenda','Mono'):'jumpsuit outfit',('prenda','Top/Blusa/Camisa'):'blouse outfit'}
nuevo={k:N[('MUNDO',t)] for k,t in nuevo_map.items()}
orig={k:O[t] for k,t in el.items()}
share=defaultdict(dict)
for r in csv.DictReader(open(REPO+'analisis/participacion_por_temporada.csv',encoding='utf-8')):
    share[(r['tipo'],r['categoria'])][(r['temporada'][:2],int(r['temporada'][2:]))]=float(r['porcentaje'])
temps=sorted({k for d in share.values() for k in d},key=lambda k:mes_desfile(*k))
for d in share.values():
    for k in temps: d.setdefault(k,0.0)
def filas(series):
    out=[]
    for k in temps:
        d0=mes_desfile(*k)
        if d0+23>LIMPIO: continue
        prev=[p for p in temps if p[0]==k[0] and mes_desfile(*p)<d0][-4:]
        if len(prev)<2: continue
        bl=[]
        for key,s in series.items():
            if key not in share: continue
            a,d,a2=prom(s,d0-12,d0-1),prom(s,d0+12,d0+23),prom(s,d0-24,d0-13)
            if None in (a,d,a2): continue
            sen=share[key][k]-sum(share[key][p] for p in prev)/len(prev)
            bl.append([k,key,sen,lg(d,a),lg(a,a2)])
        if len(bl)<8: continue
        m1=median(b[3] for b in bl); m2=median(b[4] for b in bl)
        for b in bl: b[3]-=m1; b[4]-=m2; out.append(b)
    return out
def hit(f): p=f[4]>0; return (p and f[3]>0) or ((not p) and f[3]<=0)
def p_azar(sel,n=2000):
    a0=sum(hit(f) for f in sel); por=defaultdict(list)
    for i,f in enumerate(sel): por[f[0]].append(i)
    m=0
    for _ in range(n):
        res={}
        for k,idx in por.items():
            v=[sel[i][3] for i in idx]; random.shuffle(v)
            for i,x in zip(idx,v): res[i]=x
        a=0
        for i,f in enumerate(sel):
            p=f[4]>0; y=res[i]; a+=(p and y>0) or ((not p) and y<=0)
        m+=a>=a0
    return (m+1)/(n+1)
print('=== PRUEBA A2: traccion con familia nueva (X dress / X outfit)')
F=filas(nuevo); a=sum(hit(f) for f in F); print('Total: %d de %d = %.0f%%  p=%.3f'%(a,len(F),100*a/len(F),p_azar(F)))
temp=sorted({f[0] for f in F},key=lambda k:mes_desfile(*k)); h=len(temp)//2
for nom,sel in (('mitad vieja',[f for f in F if f[0] in temp[:h]]),('mitad nueva',[f for f in F if f[0] in temp[h:]])):
    print('  %s: %d de %d = %.0f%%'%(nom,sum(hit(f) for f in sel),len(sel),100*sum(hit(f) for f in sel)/len(sel)))
for nom,tp in (('colores',['color']),('prendas+largos',['prenda','largo'])):
    sel=[f for f in F if f[1][0] in tp]; print('  solo %s: %d de %d = %.0f%%'%(nom,sum(hit(f) for f in sel),len(sel),100*sum(hit(f) for f in sel)/len(sel)))
# referencia: misma regla con familia original en las MISMAS categorias
Fo=filas({k:v for k,v in orig.items() if k in nuevo}); ao=sum(hit(f) for f in Fo); print('Referencia familia original (mismas categorias): %d de %d = %.0f%%'%(ao,len(Fo),100*ao/len(Fo)))
print('\n=== PRUEBA B2: gano presencia en pasarela -> exito en busquedas (cambio relativo>0), vs control')
def b2(series,nom):
    F=filas(series); g=[f[3]>0 for f in F if f[2]>=3]; c=[f[3]>0 for f in F if -3<f[2]<3]
    pg,pc=sum(g)/len(g),sum(c)/len(c); todos=g+c; ng=len(g); m=0
    for _ in range(2000):
        random.shuffle(todos); m+=(sum(todos[:ng])/ng-sum(todos[ng:])/len(c))>=pg-pc
    print('%s: gano %d casos, exito %.0f%% | control %d casos, exito %.0f%% | dif %+.0f pts | p=%.3f'%(nom,len(g),100*pg,len(c),100*pc,100*(pg-pc),(m+1)/2001))
b2(orig,'terminos originales'); b2(nuevo,'terminos nuevos')
print('\n=== PRUEBA C0: Argentina vs mundo (desfase)')
pares=[('vestido rosa','pink dress'),('vestido rojo','red dress'),('vestido negro','black dress'),('vestido blanco','white dress'),('vestido azul','blue dress'),('vestido verde','green dress'),('vestido marron','brown dress'),('vestido beige','beige dress'),('vestido naranja','orange dress'),('vestido gris','gray dress'),('vestido plateado','silver dress'),
 ('pollera','skirt outfit'),('pollera midi','midi skirt outfit'),('pollera mini','mini skirt outfit'),('blazer','blazer outfit'),('pantalon','trousers outfit'),('sweater','sweater outfit'),('tapado','coat outfit'),('camisa','blouse outfit'),('enterito','jumpsuit outfit')]
def ajust(s,a,b):
    xs=[math.log1p(s[k]) for k in range(a,b+1)]
    n=len(xs); r=[]
    for i in range(n):
        lo,hi=max(0,i-6),min(n,i+7)
        if i<6 or i>n-7: r.append(None)
        else: r.append(xs[i]-sum(xs[lo:hi])/(hi-lo))
    mm=defaultdict(list)
    for i,v in enumerate(r):
        if v is not None: mm[(a+i)%12].append(v)
    mu={k:sum(v)/len(v) for k,v in mm.items()}
    return [None if v is None else v-mu[(a+i)%12] for i,v in enumerate(r)]
def corr(x,y):
    p=[(a,b) for a,b in zip(x,y) if a is not None and b is not None]
    if len(p)<30: return None
    mx=sum(a for a,_ in p)/len(p); my=sum(b for _,b in p)/len(p)
    sxy=sum((a-mx)*(b-my) for a,b in p); sxx=sum((a-mx)**2 for a,_ in p); syy=sum((b-my)**2 for _,b in p)
    return sxy/math.sqrt(sxx*syy) if sxx>0 and syy>0 else None
a0,b0=am(2011,1),LIMPIO
perfil=defaultdict(list); mejor={}; excl=[]
for ar,mu in pares:
    sar=N[('AR',ar)]; z=sum(1 for k in range(a0,b0+1) if sar[k]==0)/(b0-a0+1)
    if z>0.5: excl.append((ar,round(z,2))); continue
    A=ajust(sar,a0,b0); M=ajust(N[('MUNDO',mu)],a0,b0); n=len(A); cs={}
    for L in range(-12,13):
        # AR(t) vs MUNDO(t-L)
        x=[A[i] if 0<=i-L<n else None for i in range(n)]; y=[M[i-L] if 0<=i-L<n else None for i in range(n)]
        c=corr(x,y)
        if c is not None: cs[L]=c; perfil[L].append(c)
    mejor[ar]=max(cs,key=cs.get)
print('Excluidos (>50%% de meses en cero): %s'%excl)
print('Pares usados:',len(mejor))
for L in range(-12,13): print('  L=%+3d  corr media=%+.3f'%(L,mean(perfil[L])))
pico=max(perfil,key=lambda L:mean(perfil[L])); print('Pico del perfil promedio en L=%+d (corr %.3f); L=0: %.3f'%(pico,mean(perfil[pico]),mean(perfil[0])))
pos=sum(1 for v in mejor.values() if v>0); neg=sum(1 for v in mejor.values() if v<0); cer=sum(1 for v in mejor.values() if v==0)
from math import comb
n=pos+neg; p=sum(comb(n,k) for k in range(max(pos,neg),n+1))*2/2**n if n else 1
print('L optimo >0: %d | <0: %d | =0: %d | prueba de signos bilateral p=%.3f'%(pos,neg,cer,min(1,p)))
for k,v in mejor.items(): print('   %-18s L optimo=%+d'%(k,v))
