// Funcion de Netlify: POST /api/lectura -> recomendacion de la IA (Groq) para una marca.
//   {id, perfil}                         -> lectura de una tendencia (modo "tendencia")
//   {modo: "temporada", temporada, perfil} -> cuales tendencias de la temporada mirar (modo "temporada")
//   {modo: "foto", id, imagen}           -> si la prenda de la foto cumple los 3 rasgos de la tendencia (pirueta)
// GET /api/lectura -> modelo y system prompts (para mostrarlos en la app).
// La clave va en la variable de entorno GROQ_API_KEY de Netlify. Nunca en el codigo.
import datos from "../../prototipo/datos.json";
import { SYSTEM_PROMPT, SYSTEM_PROMPT_TEMPORADA, IDIOMA_EN, MODELO_POR_DEFECTO, SYSTEM_PROMPT_FOTO, IDIOMA_EN_FOTO, MODELO_FOTO } from "./prompt.mjs";

const RUBROS = { "": "todo tipo de ropa", vestidos: "vestidos", polleras: "polleras", pantalones: "pantalones",
  abrigos: "abrigos y tejidos", accesorios: "accesorios y estampados", varios: "varios rubros", todo: "varios rubros" };
const PRECIOS = { accesible: "accesible", medio: "medio", alto: "alto / premium" };
const CANALES = { online: "online / Instagram", local: "local propio", mayorista: "mayorista", mixto: "varios canales" };

// El perfil viene del navegador: se recorta y se arma de nuevo con campos conocidos. Es contexto, no instrucciones.
const corto = (x, n) => String(x ?? "").replace(/\s+/g, " ").trim().slice(0, n);
export function limpiarPerfil(p = {}, rubroViejo = "", marcaVieja = "") {
  if (typeof p !== "object" || p === null) p = {};
  const rubro = Object.hasOwn(RUBROS, p.rubro) ? p.rubro : (Object.hasOwn(RUBROS, rubroViejo) ? rubroViejo : "");
  return {
    rubro: RUBROS[rubro] ?? RUBROS[""],
    nombre: corto(p.nombre, 60) || "sin nombre",
    que_vende: corto(p.vende ?? marcaVieja, 140) || "sin descripción",
    publico: corto(p.publico, 80) || "sin dato",
    precio: PRECIOS[p.precio] || "sin dato",
    canal: CANALES[p.canal] || "sin dato",
  };
}
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

export function armarContexto(t, marca) {
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
    marca,
  };
}

// Modo temporada: solo las tendencias con veredicto de esa temporada, con los mismos números que muestra la página
export function armarContextoTemporada(temporada, marca) {
  const ts = datos.tendencias.filter(t => t.temporada === temporada);
  return {
    temporada: TEMP[temporada],
    tendencias: ts.map(t => ({
      id: t.id, nombre: t.nombre, rubro: RUBROS[t.rubro] ?? "varios rubros",
      veredicto: t.veredicto === "queda" ? "se queda" : "en riesgo",
      confianza: t.confianza,
      cambio_de_busquedas: `${t.bruto_pct > 0 ? "+" : ""}${t.bruto_pct}%; su temporada, ${t.temporada_pct > 0 ? "+" : ""}${t.temporada_pct}%`,
      aviso: t.aviso || t.nota ? "sí: lectura con cautela" : "ninguno",
      apuesta: APUESTA[t.apuesta],
    })),
    regla_de_apuesta: datos.regla_apuesta,
    evidencia: "De las tendencias que ganan búsquedas, 9 de cada 10 siguen al segundo año (178 tendencias, 2016-2024). De 2021 a 2024, 9 de 16 de las que perdieron búsquedas fueron moda pasajera, contra 2 de 19 de las que ganaron.",
    limites: LIMITES,
    marca,
  };
}
export const DATOS_TEMPORADA = ["veredicto", "confianza", "cambio_de_busquedas", "aviso", "apuesta", "rubro"];

export function revisarTemporada(salida, contexto) {
  const problemas = [], ids = new Map(contexto.tendencias.map(t => [t.id, t]));
  if (typeof salida.resumen !== "string" || !salida.resumen.trim()) problemas.push("falta resumen");
  const el = Array.isArray(salida.elegidas) ? salida.elegidas : [];
  if (el.length < 2 || el.length > 5) problemas.push("tienen que ser de 2 a 5 tendencias elegidas");
  const vistas = new Set();
  for (const e of el) {
    const t = ids.get(e?.id);
    if (!t) { problemas.push(`la tendencia "${e?.id}" no está en la lista`); continue; }
    if (vistas.has(e.id)) problemas.push(`"${e.id}" está repetida`); vistas.add(e.id);
    if (typeof e.por_que !== "string" || !e.por_que.trim()) { problemas.push(`falta el por qué de "${e.id}"`); continue; }
    if (!DATOS_TEMPORADA.includes(e.dato)) problemas.push(`el por qué de "${e.id}" no dice de qué dato sale`);
    // Los números de cada por qué tienen que estar en esa tendencia
    const permitidos = new Set(numeros(t)), malos = numeros(e.por_que).filter(n => !permitidos.has(n));
    if (malos.length) problemas.push(`números que no están en "${e.id}": ${[...new Set(malos)].join(", ")}`);
  }
  const todos = new Set(numeros(contexto)), nuevos = numeros(salida.resumen || "").filter(n => !todos.has(n));
  if (nuevos.length) problemas.push(`números del resumen que no están en los datos: ${[...new Set(nuevos)].join(", ")}`);
  return problemas;
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

async function preguntar(key, modelo, contexto, extra, prompt = SYSTEM_PROMPT) {
  const ctrl = new AbortController(); const reloj = setTimeout(() => ctrl.abort(), 20000);
  try {
    const r = await fetch("https://api.groq.com/openai/v1/chat/completions", {
      method: "POST", signal: ctrl.signal,
      headers: { authorization: `Bearer ${key}`, "content-type": "application/json" },
      body: JSON.stringify({
        model: modelo, temperature: 0.4, max_completion_tokens: 2000, response_format: { type: "json_object" },
        // gpt-oss razona antes de contestar: razonamiento corto y sin devolverlo, para que la respuesta no se corte
        ...(modelo.startsWith("openai/gpt-oss") ? { reasoning_effort: "low", include_reasoning: false } : {}),
        messages: [{ role: "system", content: prompt },
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

// ---------- Pirueta: ¿tu prenda entra en esta tendencia? ----------
// La foto llega achicada desde el navegador (JPEG de hasta ~1000 px). No se guarda en ningún lado.
const MAX_IMAGEN = 1_500_000;
export function revisarFoto(salida, generico = false) {
  const problemas = [];
  if (typeof salida?.es_prenda !== "boolean") problemas.push("falta es_prenda (true o false)");
  if (salida?.es_prenda === false) return problemas;
  if (typeof salida?.misma_prenda !== "boolean") problemas.push("falta misma_prenda (true o false)");
  if (salida?.misma_prenda === false && generico) problemas.push('el tipo esperado es "cualquiera": misma_prenda tiene que ser true y hay que mirar los 3 rasgos');
  else if (salida?.misma_prenda === false) return problemas;
  const r = Array.isArray(salida?.rasgos) ? salida.rasgos : [];
  if (r.length !== 3) problemas.push("tienen que ser exactamente 3 rasgos");
  [1, 2, 3].forEach(n => {
    const x = r.find(y => y && y.n === n);
    if (!x) { problemas.push(`falta el rasgo ${n}`); return; }
    if (typeof x.cumple !== "boolean") problemas.push(`el rasgo ${n} no dice si cumple (true o false)`);
    if (typeof x.por_que !== "string" || !x.por_que.trim()) problemas.push(`falta el por qué del rasgo ${n}`);
    else if (x.por_que.length > 220) problemas.push(`el por qué del rasgo ${n} es muy largo`);
    else if (/\d/.test(x.por_que)) problemas.push(`el por qué del rasgo ${n} tiene números`);
  });
  return problemas;
}
// Qué tipo de prenda hace falta en la foto: sale de "Tu pollera", "Tus botas"... ("Tu prenda" o "Tu look": cualquiera)
export function tipoEsperado(t) {
  const x = t.foto.tu.replace(/^Tus? /, "").toLowerCase();
  return x === "prenda" || x === "look" ? "cualquiera" : x;
}
async function compararFoto(key, modelo, t, imagen, idioma, extra) {
  const ctrl = new AbortController(); const reloj = setTimeout(() => ctrl.abort(), 30000);
  const contexto = { tendencia: t.nombre, tipo_esperado: tipoEsperado(t), rasgos: t.foto.rasgos.map((r, i) => ({ n: i + 1, rasgo: r })) };
  try {
    const r = await fetch("https://api.groq.com/openai/v1/chat/completions", {
      method: "POST", signal: ctrl.signal,
      headers: { authorization: `Bearer ${key}`, "content-type": "application/json" },
      body: JSON.stringify({
        model: modelo, temperature: 0.2, max_completion_tokens: 900, response_format: { type: "json_object" },
        messages: [{ role: "system", content: SYSTEM_PROMPT_FOTO + (idioma === "en" ? IDIOMA_EN_FOTO : "") },
          { role: "user", content: [{ type: "text", text: JSON.stringify(contexto) + (extra ? "\n\n" + extra : "") },
            { type: "image_url", image_url: { url: imagen } }] }],
      }),
    });
    if (r.status === 429) throw Object.assign(new Error("La IA está saturada. Probá de nuevo en un minuto."), { status: 429 });
    if (!r.ok) throw Object.assign(new Error(`La IA respondió con error ${r.status}.`), { status: 502 });
    const j = await r.json();
    try { return JSON.parse(j.choices?.[0]?.message?.content || ""); }
    catch { throw Object.assign(new Error("La IA devolvió una respuesta incompleta. Probá de nuevo."), { status: 502 }); }
  } finally { clearTimeout(reloj); }
}
async function modoFoto(key, pedido) {
  const t = datos.tendencias.find(x => x.id === pedido.id);
  if (!t || !t.foto) return json({ error: "Esta tendencia todavía no tiene la comparación con foto." }, 404);
  const imagen = typeof pedido.imagen === "string" ? pedido.imagen : "";
  if (!/^data:image\/(jpeg|png|webp);base64,[A-Za-z0-9+/=]+$/.test(imagen)) return json({ error: "La foto no es una imagen válida (JPG, PNG o WebP)." }, 400);
  if (imagen.length > MAX_IMAGEN) return json({ error: "La foto es muy pesada. Probá con otra." }, 413);
  const modelo = process.env.GROQ_MODEL_FOTO || MODELO_FOTO, idioma = pedido.idioma === "en" ? "en" : "es";
  try {
    let salida = await compararFoto(key, modelo, t, imagen, idioma, "");
    const generico = tipoEsperado(t) === "cualquiera";
    let problemas = revisarFoto(salida, generico);
    if (problemas.length) {
      salida = await compararFoto(key, modelo, t, imagen, idioma, "Tu respuesta anterior tenía estos problemas, corregilos: " + problemas.join("; "));
      problemas = revisarFoto(salida, generico);
    }
    if (problemas.length) return json({ error: "La IA no pudo comparar la foto. Probá con otra foto o de nuevo en un rato.", problemas }, 502);
    // El resultado lo cuenta el código, no la IA: 3 de 3 entra, 2 de 3 cerca, 0 o 1 no entra.
    // Si la foto es de otra prenda (un jean para una tendencia de polleras), no se compara: la foto no corresponde.
    const otra = salida.es_prenda && tipoEsperado(t) !== "cualquiera" && salida.misma_prenda === false;
    const sirve = salida.es_prenda && !otra;
    const cumple = sirve ? salida.rasgos.filter(x => x.cumple === true).length : 0;
    const resultado = !salida.es_prenda ? "no_es_prenda" : otra ? "otra_prenda" : cumple === 3 ? "entra" : cumple === 2 ? "cerca" : "no_entra";
    const rasgos = sirve ? [1, 2, 3].map(n => { const x = salida.rasgos.find(y => y.n === n); return { n, rasgo: t.foto.rasgos[n - 1], cumple: x.cumple, por_que: x.por_que.trim() }; }) : [];
    return json({ resultado, cumple, prenda: String(salida.prenda || "").slice(0, 80), tipo: tipoEsperado(t), rasgos, modelo });
  } catch (e) {
    const msg = e.name === "AbortError" ? "La IA tardó demasiado. Probá de nuevo." : e.message;
    return json({ error: msg }, e.status || 502);
  }
}

export default async (req) => {
  const modelo = process.env.GROQ_MODEL || MODELO_POR_DEFECTO;
  if (req.method === "GET") return json({ modelo, proveedor: "Groq", system_prompt: SYSTEM_PROMPT, system_prompt_temporada: SYSTEM_PROMPT_TEMPORADA, modelo_foto: process.env.GROQ_MODEL_FOTO || MODELO_FOTO, system_prompt_foto: SYSTEM_PROMPT_FOTO });
  if (req.method !== "POST") return json({ error: "Método no permitido" }, 405);
  const key = process.env.GROQ_API_KEY;
  if (!key) return json({ error: "La IA no está configurada en este sitio (falta la clave)." }, 503);
  let pedido;
  try { pedido = await req.json(); } catch { return json({ error: "Pedido inválido" }, 400); }
  if (pedido.modo === "foto") return modoFoto(key, pedido);
  const marca = limpiarPerfil(pedido.perfil, pedido.rubro, pedido.marca);
  const extraIdioma = pedido.idioma === "en" ? IDIOMA_EN : "";   // solo "en" cambia algo; cualquier otro valor se ignora
  if (pedido.modo === "temporada") {
    if (!datos.tendencias.some(t => t.temporada === pedido.temporada)) return json({ error: "No encontramos esa temporada" }, 404);
    const contexto = armarContextoTemporada(pedido.temporada, marca);
    try {
      let salida = await preguntar(key, modelo, contexto, "", SYSTEM_PROMPT_TEMPORADA + extraIdioma);
      let problemas = revisarTemporada(salida, contexto);
      if (problemas.length) {
        salida = await preguntar(key, modelo, contexto, "Tu respuesta anterior tenía estos problemas, corregilos: " + problemas.join("; "), SYSTEM_PROMPT_TEMPORADA + extraIdioma);
        problemas = revisarTemporada(salida, contexto);
      }
      // Lo que no pasa el control no se muestra: solo tendencias de la lista, sin repetir
      const ids = new Set(contexto.tendencias.map(t => t.id)), vistas = new Set();
      salida.elegidas = (Array.isArray(salida.elegidas) ? salida.elegidas : [])
        .filter(e => e && ids.has(e.id) && typeof e.por_que === "string" && !vistas.has(e.id) && vistas.add(e.id)).slice(0, 5);
      return json({ salida, problemas, contexto, modelo });
    } catch (e) {
      const msg = e.name === "AbortError" ? "La IA tardó demasiado. Probá de nuevo." : e.message;
      return json({ error: msg }, e.status || 502);
    }
  }
  const t = datos.tendencias.find(x => x.id === pedido.id);
  if (!t) return json({ error: "No encontramos esa tendencia" }, 404);
  const contexto = armarContexto(t, marca);
  try {
    let salida = await preguntar(key, modelo, contexto, "", SYSTEM_PROMPT + extraIdioma);
    let problemas = revisar(salida, contexto);
    if (problemas.length) {   // un reintento, diciendole que corregir
      salida = await preguntar(key, modelo, contexto, "Tu respuesta anterior tenía estos problemas, corregilos: " + problemas.join("; "), SYSTEM_PROMPT + extraIdioma);
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
