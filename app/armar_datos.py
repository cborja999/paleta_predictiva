# Arma app/datos/brief.json a partir de los archivos de la repo. No inventa datos:
# pasarela (participacion_por_temporada.csv), prensa (planilla aprobada), busquedas (prediccion congelada + series de Trends).
import csv, json, os, collections, statistics, math
A=os.path.dirname(os.path.abspath(__file__)); R=os.path.join(A,'..')
def rd(p): return list(csv.DictReader(open(os.path.join(R,p),encoding='utf-8')))
part=rd('analisis/participacion_por_temporada.csv')
fro=rd('analisis/persistencia/prediccion_congelada_2026-10-19.csv')
prensa=[x for x in rd('datasets/prensa_argentina/planilla_prensa_notas_2026-10-20.csv') if x['aprobado']=='si']
tr=rd('analisis/persistencia/datos/trends_nuevos_2026-10-19.csv')

# --- pasarela: promedio de participacion en las 3 ultimas temporadas vs las 3 anteriores (orden cronologico del desfile)
def fecha(t): y=int(t[2:]); return y-1+0.75 if t.startswith('SS') else y+0.15
temps=sorted({x['temporada'] for x in part}, key=fecha)
rec, ant = temps[-3:], temps[-6:-3]
def share(tipo,cat,ts):
    v=[float(x['porcentaje']) for x in part if x['tipo']==tipo and x['categoria']==cat and x['temporada'] in ts]
    d={x['temporada']:float(x['porcentaje']) for x in part if x['tipo']==tipo and x['categoria']==cat}
    return round(sum(d.get(t,0) for t in ts)/len(ts),1)

# --- prensa: % de notas aprobadas de las 3 ultimas temporadas que nombran la categoria
PRE=['SS2026','FW2026','SS2027']
notas=[x for x in prensa if x['temporada_mundial'] in PRE]
alias={'colores':{'Estampado':'Multicolor/Estampado'},
       'prendas':{'Abrigo':'Abrigo/Campera','Top/Camisa':'Top/Blusa/Camisa','Sweater':'Tejido/Sweater'},
       'largos':{'Largo':'Maxi'}}
def prensa_pct(col,cat):
    n=0
    for x in notas:
        labs=[alias[col].get(k.split('(')[0].strip(),k.split('(')[0].strip()) for k in x[col].split(';')]
        if cat in labs: n+=1
    return round(100*n/len(notas),0)

# --- busquedas: prediccion congelada
F=collections.defaultdict(dict)
for x in fro: F[(x['tipo'],x['categoria'])][x['familia']]=x
ser=collections.defaultdict(dict)
for x in tr: ser[(x['geo'],x['termino'])][x['mes']]=int(x['valor'])
meses=sorted({x['mes'] for x in tr if x['mes']>='2019-01'})
def serie(geo,term): return [ser[(geo,term)].get(m,0) for m in meses]

cats=[('color',k) for k in ['Negro','Blanco','Gris','Beige/Crema','Marron','Rojo','Rosa','Naranja','Verde','Azul','Metalizado']]+\
     [('prenda',k) for k in ['Vestido','Falda','Pantalon','Blazer/Saco','Abrigo/Campera','Tejido/Sweater','Top/Blusa/Camisa','Mono']]+\
     [('largo',k) for k in ['Mini','Midi']]
colmap={'color':'colores','prenda':'prendas','largo':'largos'}
out=[]
for tipo,cat in cats:
    f=F.get((tipo,cat),{})
    item={'tipo':tipo,'categoria':cat,
          'pasarela_reciente':share(tipo,cat,rec),'pasarela_previo':share(tipo,cat,ant),
          'prensa_pct':prensa_pct(colmap[tipo],cat)}
    for fam in ('nueva','original','AR'):
        if fam in f:
            g=f[fam]
            item[fam]={'termino':g['termino'],'inercia':float(g['inercia_relativa']),'pred':g['prediccion'],'confianza':None if fam=='AR' else g['confianza']}
    if 'nueva' in f: item['serie_mundo']=serie('MUNDO',f['nueva']['termino'])
    if 'AR' in f:    item['serie_ar']=serie('AR',f['AR']['termino'])
    out.append(item)
# regla del tablero (descriptiva, no es una prueba): señales que coinciden
for tp in ('color','prenda','largo'):
    for i in out:
        if i['tipo']!=tp: continue
        s1 = i['pasarela_reciente']-i['pasarela_previo']>=1.0  # sube = al menos 1 punto mas
        s2 = i['prensa_pct']>=25  # nombrado en al menos 1 de cada 4 notas recientes
        fams=[i[k]['pred'] for k in ('nueva','original') if k in i]
        s3 = (len(fams)>0 and all(p=='SUBE' for p in fams))
        i['senales']={'pasarela':s1,'prensa':s2,'busquedas_mundo':s3}
        i['n_senales']=sum([s1,s2,s3])
        i['busquedas_mundo_acuerdo']= 'sin dato' if not fams else ('acuerdan' if len(set(fams))==1 else 'discrepan')
COL={x['etiqueta']:x for x in rd('analisis/color_real_por_categoria.csv')}
for i in out:
    c=COL.get(i['categoria'])
    if i['tipo']=='color' and c: i['hex']='#'+c['hex_mediana']; i['fotos_color']=int(c['fotos'])
meta={'meses':meses,'pasarela_recientes':rec,'pasarela_previas':ant,'prensa_temporadas':PRE,'prensa_notas':len(notas),
      'generado_de':['analisis/participacion_por_temporada.csv','analisis/persistencia/prediccion_congelada_2026-10-19.csv',
                     'analisis/persistencia/datos/trends_nuevos_2026-10-19.csv','datasets/prensa_argentina/planilla_prensa_notas_2026-10-20.csv','analisis/color_real_por_categoria.csv']}
os.makedirs(os.path.join(A,'datos'),exist_ok=True)
json.dump({'meta':meta,'items':out},open(os.path.join(A,'datos','brief.json'),'w',encoding='utf-8'),ensure_ascii=False,separators=(',',':'))
for i in out: print(i['tipo'],i['categoria'],i['pasarela_previo'],'->',i['pasarela_reciente'],'prensa',i['prensa_pct'],{k:i[k]['pred'] for k in ('nueva','original','AR') if k in i},i['n_senales'])
print(meta['pasarela_recientes'],meta['pasarela_previas'],meta['prensa_notas'])

# --- incrusta los datos en la pagina para que se abra con doble click (sin servidor)
plantilla=open(os.path.join(A,'plantilla.html'),encoding='utf-8').read()
datos=open(os.path.join(A,'datos','brief.json'),encoding='utf-8').read().replace('</','<\\/')
sha=open(os.path.join(R,'analisis','persistencia','SHA256_prediccion_congelada.txt'),encoding='utf-8').read().strip().split()
sha=[t for t in sha if len(t)==64]
open(os.path.join(A,'index.html'),'w',encoding='utf-8').write(plantilla.replace('/*DATOS*/null',datos).replace('{{SHA}}',sha[0] if sha else 'ver SHA256_prediccion_congelada.txt'))
print('index.html listo')
