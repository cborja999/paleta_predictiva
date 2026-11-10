// Funcion de Netlify: POST /api/lectura -> recomendacion de la IA (Groq) para una tendencia y una marca.
// GET /api/lectura -> modelo y system prompt (para mostrarlos en la app).
// La clave va en la variable de entorno GROQ_API_KEY de Netlify. Nunca en el codigo.
import datos from "../../prototipo/datos.json";
import { SYSTEM_PROMPT, MODELO_POR_DEFECTO } from "./prompt.mjs";

const RUBROS = { "": "todo tipo de ropa", vestidos: "vestidos", polleras: "polleras", pantalones: "pantalones",
  abrigos: "abrigos y tejidos", accesorios: "accesorios y estampados" };
const TEMP = { SS2024: "primavera-verano 2024 (desfiles de octubre de 2023, hemisferio norte)",
  FW2024: "otoño-invierno 2024 (desfiles de marzo de 2024, hemisferio norte)",
  SS2025: "primavera-verano 2025 (desfiles de septiembre y octubre de 2024, hemisferio norte)",
  FW2025: "otoño-invierno 2025 (desfiles de febrero y marzo de 2025, hemisferio norte)" };
const LIMITES = [
  "Google mide búsquedas en todo el mundo, es decir interés, no ventas.",
  "Con búsquedas solo de Argentina la regla no se confirmó.",
  "Las tendencias las eligieron medios de moda en inglés.",
  "El veredicto es la lectura del primer año después del desfile; todavía no se midió el segundo año de estas tendencias.",
];

const json = (cuerpo, status = 200) => new Response(JSON.stringify(cuerpo), {
  status, headers: { "content-type": "application/json; charset=utf-8", "cache-control": "no-store" } });

const APUESTA = { baja: "probar poco", media: "apuesta moderada", alta: "apostar fuerte" };
// De dónde puede salir cada frase de "lectura": un campo de "tendencia" o de la raíz del contexto
export const DATOS = ["veredicto", "confianza", "cambio_de_busquedas", "busquedas_promedio_0_a_100", "aviso", "apuesta", "evidencia", "limites"];

export function armarContexto(t, rubro, marca) {
  const s = t.serie, prom = a => Math.round(a.reduce((x, y) => x + y, 0) / a.length);
  return {
    tendencia: {
      nombre: t.nombre, busqueda_en_google: t.termino, temporada: TEMP[t.temporada],
      la_nombro: `${t.medio}, como "${t.tendencia_fuente}"`,
      veredicto: t.veredicto === "queda" ? "se queda (tiende a quedarse)" : "en riesgo de ser moda pasajera",
      confianza: t.confianza,
      // Los mismos números que muestra la página: cuánto cambió esta tendencia y cuánto su temporada
      cambio_de_busquedas: `${t.bruto_pct > 0 ? "+" : ""}${t.bruto_pct}% el año después del desfile contra el año anterior; las demás tendencias de su temporada, ${t.temporada_pct > 0 ? "+" : ""}${t.temporada_pct}%`,
      busquedas_promedio_0_a_100: { anio_antes: prom(s.slice(0, 12)), anio_despues: prom(s.slice(12)) },
      aviso: [t.aviso, t.nota].filter(Boolean).join(" ") || "ninguno",
      // La apuesta la fija una regla del código (prototipo/armar_datos.py), no la IA
      apuesta: `${APUESTA[t.apuesta]} (regla fija: ${datos.regla_apuesta})`,
    },
    evidencia: t.veredicto === "queda"
      ? "De las tendencias que ganan búsquedas así, 9 de cada 10 siguen vigentes al segundo año (178 tendencias, 2016-2024)."
      : "De 2021 a 2024, 9 de 16 tendencias que perdieron búsquedas fueron moda pasajera, contra 2 de 19 de las que ganaron.",
    limites: t.temporada === "SS2025"
      ? [...LIMITES, "El primer año de primavera 2025 incluye meses de 2025 en que Google empezó a medir distinto. La lectura pasó un chequeo fijado de antemano, pero conviene tomarla con más cuidado que las de 2024."]
      : t.temporada === "FW2025"
      ? [...LIMITES, "El primer año de otoño 2025 cae en buena parte en el período en que Google empezó a medir distinto. La lectura pasó un chequeo más estricto fijado de antemano, pero conviene tomarla con más cuidado que las de 2024."]
      : LIMITES,
    marca: { rubro: RUBROS[rubro] ?? RUBROS[""], descripcion: marca || "sin descripción" },
  };
}

// El valor de un campo del contexto, como texto (para ver qué números contiene)
const valor = (contexto, k) => JSON.stringify(k in contexto.tendencia ? contexto.tendencia[k] : contexto[k] ?? "");
const numeros = x => JSON.stringify(x).match(/\d+/g) || [];

export function revisar(salida, contexto) {
  const problemas = [];
  if (!Array.isArray(salida.lectura) || !salida.lectura.length) problemas.push("falta lectura");
  else if (salida.lectura.length > 4) problemas.push("la lectura tiene más de 4 frases");
  if (contexto.tendencia.aviso !== "ninguno" && Array.isArray(salida.lectura) && !salida.lectura.some(f => f?.dato === "aviso"))
    problemas.push("la tendencia tiene un aviso y la lectura no lo cuenta");
  for (const f of Array.isArray(salida.lectura) ? salida.lectura : []) {
    if (typeof f?.texto !== "string" || !f.texto.trim()) { problemas.push("una frase de lectura está vacía"); continue; }
    if (!DATOS.includes(f.dato)) { problemas.push(`la frase "${f.texto.slice(0, 40)}…" no dice de qué dato sale`); continue; }
    // Cada número de una frase tiene que estar en el dato que dice usar
    const permitidos = new Set(numeros(valor(contexto, f.dato)));
    const malos = numeros(f.texto).filter(n => !permitidos.has(n));
    if (malos.length) problemas.push(`números que no están en "${f.dato}": ${[...new Set(malos)].join(", ")}`);
  }
  if (typeof salida.para_tu_marca !== "string" || !salida.para_tu_marca.trim()) problemas.push("falta para_tu_marca");
  if (!Array.isArray(salida.ideas) || salida.ideas.length < 2) problemas.push("faltan ideas");
  // Lo que es inferencia no puede traer números que no estén en ningún lado del contexto
  const todos = new Set(numeros(contexto));
  const nuevos = numeros([salida.para_tu_marca, salida.ideas]).filter(n => !todos.has(n));
  if (nuevos.length) problemas.push(`números que no están en los datos: ${[...new Set(nuevos)].join(", ")}`);
  return problemas;
}

async function preguntar(key, modelo, contexto, extra) {
  const ctrl = new AbortController(); const reloj = setTimeout(() => ctrl.abort(), 20000);
  try {
    const r = await fetch("https://api.groq.com/openai/v1/chat/completions", {
      method: "POST", signal: ctrl.signal,
      headers: { authorization: `Bearer ${key}`, "content-type": "application/json" },
      body: JSON.stringify({
        model: modelo, temperature: 0.4, max_completion_tokens: 2000, response_format: { type: "json_object" },
        // gpt-oss razona antes de contestar: razonamiento corto y sin devolverlo, para que la respuesta no se corte
        ...(modelo.startsWith("openai/gpt-oss") ? { reasoning_effort: "low", include_reasoning: false } : {}),
        messages: [{ role: "system", content: SYSTEM_PROMPT },
          { role: "user", content: JSON.stringify(contexto) + (extra ? "\n\n" + extra : "") }],
      }),
    });
    if (r.status === 429) throw Object.assign(new Error("La IA está saturada. Probá de nuevo en un minuto."), { status: 429 });
    if (!r.ok) throw Object.assign(new Error(`La IA respondió con error ${r.status}.`), { status: 502 });
    const j = await r.json();
    try { return JSON.parse(j.choices?.[0]?.message?.content || ""); }
    catch { throw Object.assign(new Error("La IA devolvió una respuesta incompleta. Probá de nuevo."), { status: 502 }); }
  } finally { clearTimeout(reloj); }
}

export default async (req) => {
  const modelo = process.env.GROQ_MODEL || MODELO_POR_DEFECTO;
  if (req.method === "GET") return json({ modelo, proveedor: "Groq", system_prompt: SYSTEM_PROMPT });
  if (req.method !== "POST") return json({ error: "Método no permitido" }, 405);
  const key = process.env.GROQ_API_KEY;
  if (!key) return json({ error: "La IA no está configurada en este sitio (falta la clave)." }, 503);
  let pedido;
  try { pedido = await req.json(); } catch { return json({ error: "Pedido inválido" }, 400); }
  const t = datos.tendencias.find(x => x.id === pedido.id);
  if (!t) return json({ error: "No encontramos esa tendencia" }, 404);
  const rubro = Object.hasOwn(RUBROS, pedido.rubro) ? pedido.rubro : "";
  const marca = String(pedido.marca || "").replace(/\s+/g, " ").trim().slice(0, 280);
  const contexto = armarContexto(t, rubro, marca);
  try {
    let salida = await preguntar(key, modelo, contexto);
    let problemas = revisar(salida, contexto);
    if (problemas.length) {   // un reintento, diciendole que corregir
      salida = await preguntar(key, modelo, contexto, "Tu respuesta anterior tenía estos problemas, corregilos: " + problemas.join("; "));
      problemas = revisar(salida, contexto);
    }
    salida.lectura = (salida.lectura || []).filter(f => f && typeof f.texto === "string");
    return json({ salida, problemas, contexto, modelo, apuesta: t.apuesta });
  } catch (e) {
    const msg = e.name === "AbortError" ? "La IA tardó demasiado. Probá de nuevo." : e.message;
    return json({ error: msg }, e.status || 502);
  }
};

export const config = { path: "/api/lectura" };
