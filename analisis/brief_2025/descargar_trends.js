// Baja los datos de Google Trends que piden las reglas (REGLAS_BRIEF_2025.txt, seccion DATOS A BAJAR).
// Uso: abrir https://trends.google.com/trends/explore?q=midi%20skirt en Chrome, abrir la consola
// (Cmd+Option+J en Mac), pegar todo este archivo y Enter. Tarda unos 15-20 minutos.
// Al terminar descarga 3 archivos: trends_A_2011_2025-09.csv, trends_B_2024_2026.csv y volumen_ancla.csv.
// Ponerlos en analisis/brief_2025/datos/ (o adjuntarlos en el chat).
(async () => {
  const T25 = ["trench coat", "light pink dress", "pillbox hat", "pencil skirt", "brocade jacket", "peep toe heels", "chiffon cape", "sequin dress", "fringe jacket", "mini dress", "80s blazer", "bubble skirt", "wide leg jeans", "sheer dress", "statement sunglasses", "utility jacket", "one leg pants", "bow blouse", "tutu skirt", "floral dress", "dress over pants", "lace dress", "polka dot", "ruffle skirt", "plaid jacket", "breton sweater"];
  const T24 = ["burgundy dress", "pencil skirt", "hot pants", "sheer skirt", "slip skirt", "halter dress", "oversized bag", "fringe jacket", "satin coat", "statement belt", "mini dress", "rose print", "sheer dress", "lavender dress", "shorts suit", "dress over pants", "funnel neck coat", "pillbox hat", "scarf coat", "cigarette pants", "faux fur coat", "tailored trousers", "leather dress", "turtleneck", "peacoat", "feather dress", "green dress", "leopard print", "tea length dress", "cashmere pants", "balloon pants"];
  const T26 = ["leather mini skirt", "satin scarf", "floral print", "poplin shirt", "trench coat", "80s fashion", "lilac dress", "preppy outfit", "tweed suit", "bell sleeve", "feather skirt", "yellow dress", "chainmail dress", "ruffle dress", "flapper dress", "spaghetti strap top", "low rise pants", "power shoulders", "fair isle sweater", "brocade", "tailored coat", "statement coat", "polo shirt", "satin dress", "silk shirt", "fur coat", "brooch", "check shirt", "purple dress", "skirt suit", "chunky scarf", "shearling coat", "lace dress", "fringe jacket", "sheer dress", "pink dress"];
  const uniq = a => [...new Set(a)];
  const LA = uniq([...T25, ...T26]);            // A: ene-2011 a sep-2025, mensual
  const LB = uniq([...T25, ...T24, ...T26]);    // B y V: todos
  const ANCLA = "midi skirt";
  const pausa = ms => new Promise(r => setTimeout(r, ms));
  async function serie(kws, time) {
    const req = { comparisonItem: kws.map(k => ({ keyword: k, geo: "", time })), category: 0, property: "" };
    for (let a = 0; a < 6; a++) {
      const r = await fetch("/trends/api/explore?hl=en-US&tz=0&req=" + encodeURIComponent(JSON.stringify(req)));
      if (r.status === 429) { await pausa(15000 * (a + 1)); continue; }
      const t = await r.text(); const j = JSON.parse(t.slice(t.indexOf("{")));
      const w = j.widgets.find(x => x.id === "TIMESERIES");
      const r2 = await fetch("/trends/api/widgetdata/multiline?hl=en-US&tz=0&req=" + encodeURIComponent(JSON.stringify(w.request)) + "&token=" + w.token);
      if (r2.status === 429) { await pausa(15000 * (a + 1)); continue; }
      const t2 = await r2.text(); const j2 = JSON.parse(t2.slice(t2.indexOf("{")));
      return j2.default.timelineData.map(d => ({ mes: new Date(d.time * 1000).toISOString().slice(0, 7), v: d.value }));
    }
    throw new Error("429 repetido: " + kws.join(","));
  }
  const log = m => { console.log(m); window.ESTADO = m; };
  const A = ["geo,termino,mes,valor"], B = ["geo,termino,mes,valor,semanas"], V = ["termino,ancla,suma_termino,suma_ancla,volumen,semanas"];
  window.FALLAS = [];
  for (const [i, k] of LA.entries()) {
    try { const s = await serie([k], "2011-01-01 2025-09-30");
      if (s.length !== 177) throw new Error("A con " + s.length + " meses");
      s.forEach(d => A.push(`MUNDO,${k},${d.mes},${d.v[0]}`)); } catch (e) { FALLAS.push("A " + k + ": " + e.message); }
    log(`A ${i + 1}/${LA.length}`); await pausa(2000);
  }
  for (const [i, k] of LB.entries()) {
    try { const s = await serie([k], "2024-01-01 2026-09-30"); const m = {};
      s.forEach(d => { (m[d.mes] = m[d.mes] || []).push(d.v[0]); });
      Object.keys(m).sort().forEach(mes => B.push(`MUNDO,${k},${mes},${(m[mes].reduce((a, b) => a + b, 0) / m[mes].length).toFixed(2)},${m[mes].length}`));
    } catch (e) { FALLAS.push("B " + k + ": " + e.message); }
    log(`B ${i + 1}/${LB.length}`); await pausa(2000);
  }
  for (let i = 0; i < LB.length; i += 4) {
    const g = LB.slice(i, i + 4);
    try { const s = await serie([ANCLA, ...g], "2023-10-01 2024-09-30");
      const sa = s.reduce((a, d) => a + d.v[0], 0);
      g.forEach((k, j) => { const st = s.reduce((a, d) => a + d.v[j + 1], 0); V.push(`${k},${ANCLA},${st},${sa},${sa > 0 ? (st / sa).toFixed(5) : ""},${s.length}`); });
    } catch (e) { FALLAS.push("V " + g.join("|") + ": " + e.message); }
    log(`V ${Math.min(i + 4, LB.length)}/${LB.length}`); await pausa(2000);
  }
  const ck = txt => { let h = 0; for (let i = 0; i < txt.length; i++) h = (h * 131 + txt.charCodeAt(i)) % 1000000007; return h; };
  window.SALIDA = { A: A.join("\n") + "\n", B: B.join("\n") + "\n", V: V.join("\n") + "\n" };
  window.CK = { A: ck(SALIDA.A), B: ck(SALIDA.B), V: ck(SALIDA.V) };
  const bajar = (n, t) => { const a = document.createElement("a"); a.href = URL.createObjectURL(new Blob([t], { type: "text/csv" })); a.download = n; a.click(); };
  if (!window.NO_DESCARGAR) { bajar("trends_A_2011_2025-09.csv", SALIDA.A); bajar("trends_B_2024_2026.csv", SALIDA.B); bajar("volumen_ancla.csv", SALIDA.V); }
  log("LISTO. Fallas: " + FALLAS.length + " | checksums " + JSON.stringify(CK));
})();
