import os, sys
from google import genai
clave = os.environ.get("GEMINI_API_KEY")
if not clave:
    sys.exit("Falta la clave: export GEMINI_API_KEY=TU_CLAVE")
c = genai.Client(api_key=clave)
for m in c.models.list():
    acc = getattr(m, "supported_actions", None) or []
    if "generateContent" in acc:
        print(m.name)
