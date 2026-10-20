# Color medido de las fotos de pasarela por etiqueta de color de Gemini.
# Uso: python3 -I color_real_por_categoria.py <carpeta runway_gemini>   (las fotos NO se suben al repo)
# Por foto: recorte central (x 30-70%, y 15-85%) -> 4 grupos de color (k-means) -> se queda el grupo (>=8% de pixeles)
# mas cercano en Lab al color de referencia de la etiqueta. Por etiqueta: mediana de las fotos. Seed fija.
import sys, os, csv, collections
import numpy as np
from PIL import Image
B=sys.argv[1]
REF={'Negro':'1a1a1a','Blanco':'f4f1ea','Gris':'8a8d91','Beige/Crema':'d9c6a5','Marron':'6b4a35','Rojo':'b3202a','Rosa':'e8a3b8','Naranja':'e07a2d','Verde':'3f7d4e','Azul':'2f4f8f','Metalizado':'b8bcc2','Amarillo':'e6c229','Oliva/Caqui':'6b6b3a','Celeste':'9fc5e8','Burdeos/Vino':'5e1a2b','Violeta':'6a4c93','Turquesa':'2aa6a0'}
def lab(rgb):
    c=np.asarray(rgb,float)/255.0
    c=np.where(c>0.04045,((c+0.055)/1.055)**2.4,c/12.92)
    M=np.array([[0.4124,0.3576,0.1805],[0.2126,0.7152,0.0722],[0.0193,0.1192,0.9505]])
    xyz=c@M.T/np.array([0.9505,1,1.089])
    f=np.where(xyz>0.008856,np.cbrt(xyz),7.787*xyz+16/116)
    return np.stack([116*f[...,1]-16,500*(f[...,0]-f[...,1]),200*(f[...,1]-f[...,2])],-1)
def hx(h): return [int(h[i:i+2],16) for i in (0,2,4)]
def kmeans(X,k=4,it=15):
    rng=np.random.default_rng(0); C=X[rng.choice(len(X),k,replace=False)].astype(float)
    for _ in range(it):
        d=((X[:,None,:]-C[None])**2).sum(-1); a=d.argmin(1)
        for j in range(k):
            if (a==j).any(): C[j]=X[a==j].mean(0)
    return C,np.bincount(a,minlength=k)/len(X)
res=list(csv.DictReader(open(os.path.join(B,'resultados_gemini.csv'),encoding='utf-8')))
mu={x['look']+'|'+x['marca']+'|'+x['temporada']+x['anio']:x['ruta_local'] for x in csv.DictReader(open(os.path.join(B,'muestra_vogue_400_para_gemini.csv'),encoding='utf-8'))}
got=collections.defaultdict(list)
for x in res:
    k=x['look']+'|'+x['marca']+'|'+x['temporada']+x['anio']
    if x['color_dominante'] not in REF or k not in mu: continue
    p=os.path.join(B,mu[k])
    if not os.path.exists(p): continue
    im=Image.open(p).convert('RGB'); im=im.resize((120,int(120*im.height/im.width)))
    a=np.asarray(im); h,w,_=a.shape
    X=a[int(.15*h):int(.85*h),int(.30*w):int(.70*w)].reshape(-1,3)
    C,s=kmeans(X.astype(float))
    ok=np.where(s>=0.08)[0]; L=lab(C[ok]); r=lab(np.array(hx(REF[x['color_dominante']])))
    j=ok[((L-r)**2).sum(1).argmin()]; got[x['color_dominante']].append(C[j])
rows=[]
for c,v in got.items():
    v=np.array(v); m=np.median(v,0).round().astype(int); q1=np.percentile(v,25,0); q3=np.percentile(v,75,0)
    rows.append([c,len(v),'%02x%02x%02x'%tuple(m),'|'.join(str(int(t)) for t in (q3-q1))])
rows.sort(key=lambda r:-r[1])
w=csv.writer(sys.stdout); w.writerow(['etiqueta','fotos','hex_mediana','rango_intercuartil_RGB'])
for r in rows: w.writerow(r)
