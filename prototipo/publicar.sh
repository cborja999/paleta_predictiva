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
netlify deploy --prod --dir prototipo --functions netlify/functions --site "$SITIO" \
  --message "entrega-3 $(git -C "$OLDPWD" rev-parse --short origin/entrega-3) con fotos"
rm -rf "$COPIA"
