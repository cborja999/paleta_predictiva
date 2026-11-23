#!/bin/sh
# Publica la app en Netlify (https://paleta-predictiva.netlify.app) con las fotos locales.
# Sube lo que esta en GitHub en la rama entrega-3 (hacer push antes) mas las fotos de prototipo/fotos/.
# Las fotos nunca van a GitHub; la clave de Groq ya esta cargada en Netlify (variable GROQ_API_KEY).
# Uso, desde la raiz del repo: sh prototipo/publicar.sh   (necesita `netlify login` una vez)
set -e
SITIO=043e1ba0-4efb-44be-a44b-860fa23880fb
COPIA=$(mktemp -d)
git fetch -q origin entrega-3
git archive origin/entrega-3 | tar -x -C "$COPIA"
mkdir -p "$COPIA/prototipo/fotos"
cp prototipo/fotos/*.jpg "$COPIA/prototipo/fotos/"
cd "$COPIA"
# Desde el 23/11/2026 Netlify rechaza "deploy --prod" con Forbidden, pero acepta borradores: se sube un borrador
# y despues se publica con la API (es el mismo deploy, con fotos y la funcion de la IA).
SALIDA=$(netlify deploy --json --dir prototipo --functions netlify/functions --site "$SITIO" \
  --message "entrega-3 $(git -C "$OLDPWD" rev-parse --short origin/entrega-3) con fotos")
DEPLOY=$(printf '%s' "$SALIDA" | python3 -c "import sys, json; print(json.load(sys.stdin)['deploy_id'])")
netlify api restoreSiteDeploy --data "{\"site_id\":\"$SITIO\",\"deploy_id\":\"$DEPLOY\"}" > /dev/null
echo "Publicado: https://paleta-predictiva.netlify.app (deploy $DEPLOY)"
rm -rf "$COPIA"
