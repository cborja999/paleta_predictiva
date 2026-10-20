import csv, math, random, hashlib, sys
from collections import defaultdict
from statistics import median, mean
random.seed(20)
import os
REPO=os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..'))+'/'
S=os.path.dirname(os.path.abspath(__file__))+'/'
def am(y,m): return y*12+m-1
ULT=am(2026,9); LIMPIO=am(2024,12)
def mes_desfile(t,a): return am(a,3) if t=='FW' else am(a-1,10)
def prom(s,a,b):
    v=[s[k] for k in range(a,b+1) if k in s]; return sum(v)/len(v) if len(v)==b-a+1 else None
def lg(x,y): return math.log(max(x,0.3)/max(y,0.3))
def cargar_csv(path,geo=None):
    N={}
    for r in csv.DictReader(open(path)):
        if geo and r['geo']!=geo: continue
        y,m=r['mes'].split('-'); N.setdefault(r['termino'],{})[am(int(y),int(m))]=float(r['valor'])
    return N
NU=csv.DictReader(open(S+'datos/trends_nuevos_2026-10-19.csv'))
Nm,Nar={},{}
for r in NU:
    y,m=r['mes'].split('-'); d=Nm if r['geo']=='MUNDO' else Nar
    d.setdefault(r['termino'],{})[am(int(y),int(m))]=float(r['valor'])
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
ar_map={('color','Rosa'):'vestido rosa',('color','Rojo'):'vestido rojo',('color','Negro'):'vestido negro',('color','Blanco'):'vestido blanco',('color','Azul'):'vestido azul',('color','Verde'):'vestido verde',('color','Beige/Crema'):'vestido beige',('color','Naranja'):'vestido naranja',('color','Gris'):'vestido gris',('color','Metalizado'):'vestido plateado',
 ('prenda','Falda'):'pollera',('largo','Mini'):'pollera mini',('prenda','Blazer/Saco'):'blazer',('prenda','Pantalon'):'pantalon',('prenda','Tejido/Sweater'):'sweater',('prenda','Abrigo/Campera'):'tapado',('prenda','Top/Blusa/Camisa'):'camisa',('prenda','Mono'):'enterito'}
fam={'original':{k:O[t] for k,t in el.items()},'nueva':{k:Nm[t] for k,t in nuevo_map.items()},'AR':{k:Nar[t] for k,t in ar_map.items()}}
# shopping (si existe)
try:
    Sh=cargar_csv(S+'datos/trends_shopping_2026-10-19.csv')
    fam['shopping']={}
    for k,t in nuevo_map.items():
        s=Sh.get(t)
        if not s: continue
        z=sum(1 for v in s.values() if v==0)/len(s)
        print('shopping %-20s ceros=%.0f%%'%(t,100*z))
        if z<=0.5: fam['shopping'][k]=s
except FileNotFoundError: print('sin shopping')
share=defaultdict(dict)
for r in csv.DictReader(open(REPO+'analisis/participacion_por_temporada.csv',encoding='utf-8')):
    share[(r['tipo'],r['categoria'])][(r['temporada'][:2],int(r['temporada'][2:]))]=float(r['porcentaje'])
temps=sorted({k for d in share.values() for k in d},key=lambda k:mes_desfile(*k))
def slope(s,d0):
    ys=[]
    for i in range(d0-36,d0):
        if i not in s: return None
        ys.append(math.log(max(s[i],0.3)))
    xm=17.5; ym=sum(ys)/36
    return sum((i-xm)*(y-ym) for i,y in enumerate(ys))/sum((i-xm)**2 for i in range(36))
def casos(series,desde36=False,limite=LIMPIO):
    out=[]
    for k in temps:
        d0=mes_desfile(*k)
        if d0+23>limite: continue
        bl=[]
        for key,s in series.items():
            a,d,a2=prom(s,d0-12,d0-1),prom(s,d0+12,d0+23),prom(s,d0-24,d0-13)
            c6,c6b=prom(s,d0-6,d0-1),prom(s,d0-12,d0-7)
            if None in (a,d,a2,c6,c6b): continue
            sl=slope(s,d0)
            if desde36 and sl is None: continue
            bl.append(dict(k=k,key=key,y=lg(d,a),inercia=lg(a,a2),nivel=a,mom=lg(c6,c6b),sl=sl))
        if len(bl)<8: continue
        for f in ('y','inercia','mom'):
            m=median(b[f] for b in bl)
            for b in bl: b[f]-=m
        mn=median(b['nivel'] for b in bl)
        for b in bl: b['nivel_rel']=b['nivel']-mn
        if desde36:
            ms=median(b['sl'] for b in bl)
            for b in bl: b['sl']-=ms
        out.append(bl)
    return [b for bl in out for b in bl]
def hit_p(p,y): return (p and y>0) or ((not p) and y<=0)
def p_azar(sel,pred,n=2000):
    a0=sum(hit_p(pred(f),f['y']) for f in sel); por=defaultdict(list)
    for i,f in enumerate(sel): por[f['k']].append(i)
    m=0
    for _ in range(n):
        res={}
        for k,idx in por.items():
            v=[sel[i]['y'] for i in idx]; random.shuffle(v)
            for i,x in zip(idx,v): res[i]=x
        m+=sum(hit_p(pred(f),res[i]) for i,f in enumerate(sel))>=a0
    return (m+1)/(n+1)
A=lambda f:f['inercia']>0
def rep(nombre,sel,pred=A):
    a=sum(hit_p(pred(f),f['y']) for f in sel); return a,len(sel)
if __name__=='__main__':
    print('=== P3 PISOS (casos desde FW2015 aprox, comun a todas las reglas; B3 pide 36 meses de historia)')
    for fn in ('original','nueva'):
        C=casos(fam[fn],desde36=True); print('\nFamilia',fn,'casos',len(C))
        reglas={'A tracción (inercia 12m)':A,'B1 popular sigue creciendo':lambda f:f['nivel_rel']>0,'B2 momentum corto (6m)':lambda f:f['mom']>0,'B3 tendencia lineal 36m':lambda f:f['sl']>0,'B4 siempre SUBE':lambda f:True}
        ra={}
        for n,p in reglas.items():
            a,t=rep(n,C,p); ra[n]=a/t; print('  %-28s %3d/%3d = %.1f%%'%(n,a,t,100*a/t))
        for n in list(reglas)[1:]:
            d=ra['A tracción (inercia 12m)']-ra[n]; print('  A vs %-26s %+.1f pts -> %s'%(n,100*d,'supera' if d>=0.03 else 'no se distingue'))
    print('\n=== P4 NIVELES DE CONFIANZA (terciles de |inercia| por familia, casos completos)')
    cortes={}
    for fn in ('original','nueva'):
        C=casos(fam[fn]); ab=sorted(abs(f['inercia']) for f in C); c1,c2=ab[len(ab)//3],ab[2*len(ab)//3]; cortes[fn]=(c1,c2)
        def niv(f): x=abs(f['inercia']); return 'Baja' if x<c1 else ('Media' if x<c2 else 'Alta')
        print('\nFamilia',fn,'cortes |inercia|: %.3f / %.3f'%(c1,c2))
        res={}
        for n in ('Baja','Media','Alta'):
            sel=[f for f in C if niv(f)==n]; a,t=rep(n,sel); res[n]=a/t
            su=[f for f in sel if f['inercia']>0]; ns=[f for f in sel if f['inercia']<=0]
            print('  %-5s %3d/%3d = %.0f%% | SUBE %3d/%3d = %.0f%% | NO SUBE %3d/%3d = %.0f%%'%(n,a,t,100*a/t,*rep('',su),100*rep('',su)[0]/len(su),*rep('',ns),100*rep('',ns)[0]/len(ns)))
        print('  creciente:',res['Baja']<res['Media']<res['Alta'],'| Alta-Baja = %+.0f pts'%(100*(res['Alta']-res['Baja'])))
    print('\n=== P5 ARGENTINA (tracción)')
    C=casos(fam['AR']); a,t=rep('',C); print('Total %d/%d = %.0f%% p=%.3f'%(a,t,100*a/t,p_azar(C,A)))
    bajo={k:s for k,s in fam['AR'].items() if sum(1 for k2 in range(am(2011,1),LIMPIO+1) if s[k2]==0)/(LIMPIO-am(2011,1)+1)<0.25}
    C2=casos(bajo); a2,t2=rep('',C2); print('Solo series con <25%% ceros (%d series): %d/%d = %.0f%% p=%.3f'%(len(bajo),a2,t2,100*a2/t2,p_azar(C2,A)))
    print('   series usadas en la sensibilidad:',sorted(k[1] for k in bajo))
    if 'shopping' in fam:
        print('\n=== P6 SHOPPING'); C=casos(fam['shopping']); print('categorias usables:',len(fam['shopping']),'casos',len(C))
        if C: a,t=rep('',C); print('Total %d/%d = %.0f%% p=%.3f'%(a,t,100*a/t,p_azar(C,A)))
        else: print('no se puede testear (menos de 8 categorias por temporada)')
