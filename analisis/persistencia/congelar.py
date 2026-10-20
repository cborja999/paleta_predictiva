import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fase2 import *
import hashlib
d0=am(2026,10)
filas=[]
terms={'original':{k:el[k] for k in el},'nueva':nuevo_map,'AR':ar_map}
for fn in ('original','nueva','AR'):
    ser=fam[fn]; bl=[]
    for key,s in ser.items():
        a=prom(s,d0-12,d0-1); a2=prom(s,d0-24,d0-13)
        if a is None or a2 is None: continue
        bl.append([key,lg(a,a2)])
    m=median(b[1] for b in bl)
    if fn in ('original','nueva'):
        C=casos(ser); ab=sorted(abs(f['inercia']) for f in C); c1,c2=ab[len(ab)//3],ab[2*len(ab)//3]
    for key,x in bl:
        x-=m; niv='no se ofrece (la regla no se sostuvo en series de Argentina)' if fn=='AR' else ('Baja' if abs(x)<c1 else ('Media' if abs(x)<c2 else 'Alta'))
        filas.append(['2026-10-19',fn,key[0],key[1],terms[fn][key],round(x,3),'SUBE' if x>0 else 'NO SUBE',niv,'oct-2027 (exploratorio)','oct-2028 (principal)'])
filas.sort(key=lambda r:(r[1],-r[5]))
p=S+'prediccion_congelada_2026-10-19.csv'
if os.path.exists(p):
    print('YA EXISTE: la prediccion congelada NO se reescribe. sha256 actual:', hashlib.sha256(open(p,'rb').read()).hexdigest()); sys.exit(0)
with open(p,'w',newline='',encoding='utf-8') as f:
    w=csv.writer(f); w.writerow(['fecha_congelado','familia','tipo','categoria','termino','inercia_relativa','prediccion','confianza','chequeo_intermedio','chequeo_principal']); w.writerows(filas)
print('filas',len(filas)); print('sha256',hashlib.sha256(open(p,'rb').read()).hexdigest())
for r in filas:
    if r[1]!='AR' : print('%-9s %-7s %-17s %-22s %+.2f %-7s %s'%(r[1],r[2],r[3],r[4],r[5],r[6],r[7]))
