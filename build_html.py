#!/usr/bin/env python3
"""Writes ThemePulse.html with the current themes.json embedded as offline fallback."""
import json

DATA = json.load(open("themes.json"))
FALLBACK = json.dumps(DATA, separators=(",", ":"))

HTML = r"""<!DOCTYPE html>
<html lang="en" class="h-full">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>ThemePulse</title>
<meta name="description" content="Theme board + rotation — standalone, data-driven from themes.json" />
<style>
:root{
  --bg:#0a0e16; --fg:#e7edf5;
  --panel:#141b28; --panel-deep:#0f1622; --panel-2:#1a2333;
  --border:#222c3d; --border2:#2c3850;
  --muted:#93a1b5; --neutral:#5e6b7e;
  --green:#4ade80; --red:#f87171; --blue:#60a5fa; --purple:#a78bfa; --amber:#fbbf24;
  --mono:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;
  --sans:-apple-system,BlinkMacSystemFont,"Segoe UI",Inter,Roboto,Helvetica,Arial,sans-serif;
}
*{box-sizing:border-box}
html,body{height:100%}
body{margin:0;background:var(--bg);color:var(--fg);font-family:var(--sans);-webkit-font-smoothing:antialiased}
.shell{max-width:1180px;margin:0 auto;padding:22px 18px 48px}
@media(min-width:768px){.shell{padding:34px 28px 60px}}

.tp-hd{display:flex;justify-content:space-between;align-items:flex-end;flex-wrap:wrap;gap:14px;margin-bottom:18px}
.tp-title{font-size:25px;font-weight:800;letter-spacing:-.4px;display:flex;align-items:center;gap:11px}
.tp-dot{width:10px;height:10px;border-radius:50%;background:var(--green);box-shadow:0 0 12px var(--green)}
.tp-sub{color:var(--muted);font-size:13px;margin-top:4px}
.tp-asof{font-size:11px;color:var(--neutral)}
.tp-toolbar{display:flex;align-items:center;gap:8px;flex-wrap:wrap;justify-content:flex-end;margin-top:8px}
.tp-toolbar button{background:var(--panel-2);border:1px solid var(--border2);color:var(--fg);font-size:12px;font-weight:600;padding:7px 12px;border-radius:9px;cursor:pointer}
.tp-toolbar button:hover{border-color:var(--green);color:var(--green)}
.tp-trigmsg{font-size:11.5px;color:var(--muted)}
.tp-controls{display:flex;justify-content:space-between;flex-wrap:wrap;gap:12px;margin-bottom:18px}
.tp-seg{display:inline-flex;background:var(--panel);border:1px solid var(--border);border-radius:11px;padding:4px;gap:2px}
.tp-seg button{background:transparent;border:0;color:var(--muted);font-size:12.5px;font-weight:600;padding:6px 12px;border-radius:8px;cursor:pointer}
.tp-seg button:hover{color:var(--fg)}
.tp-seg button.on{background:var(--panel-2);color:var(--fg);box-shadow:inset 0 0 0 1px var(--border2)}
.tp-seg.tp-period button.on{background:var(--green);color:#0a0e16;box-shadow:none}
.tp-lbl{font-size:11px;color:var(--neutral);text-transform:uppercase;letter-spacing:.08em;margin-right:8px;align-self:center}
.tp-strip{background:var(--panel);border:1px solid var(--border);border-radius:10px;padding:10px 14px;font-size:12.5px;margin-bottom:16px;display:flex;gap:22px;flex-wrap:wrap}
.tp-strip b{color:var(--fg)}
.tp-kpis{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-bottom:22px}
@media(max-width:780px){.tp-kpis{grid-template-columns:repeat(2,1fr)}}
.tp-kpi{background:var(--panel);border:1px solid var(--border);border-radius:14px;padding:13px 15px}
.tp-kpi .k{font-size:11px;color:var(--neutral);text-transform:uppercase;letter-spacing:.07em}
.tp-kpi .v{font-size:19px;font-weight:800;margin-top:5px}
.tp-kpi .x{font-size:11px;color:var(--muted);margin-top:2px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.tp-sectitle{display:flex;align-items:center;gap:10px;margin:6px 0 14px;font-size:12px;font-weight:700;text-transform:uppercase;letter-spacing:.09em;color:var(--muted)}
.tp-sectitle::after{content:"";flex:1;height:1px;background:var(--border)}
.tp-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(168px,1fr));gap:9px}
.tp-card{position:relative;background:var(--panel);border:1px solid var(--border);border-radius:11px;padding:10px 11px 9px;cursor:pointer;transition:.14s;overflow:hidden}
.tp-card:hover{transform:translateY(-2px);border-color:var(--border2)}
.tp-card:hover .tp-open{opacity:1}
.tp-card:hover .tp-cardadmin{opacity:1}
.tp-edge{position:absolute;left:0;top:0;bottom:0;width:3px}
.tp-open{font-size:10px;color:var(--neutral);opacity:.55}
.tp-crow{display:flex;justify-content:space-between;align-items:center;min-height:18px}
.tp-rk{font-weight:800;font-size:12px;color:var(--neutral)}.tp-rk b{color:var(--fg);font-size:14px}
.tp-badges{display:flex;gap:6px}
.tp-chip{font-size:9.5px;font-weight:800;letter-spacing:.04em;padding:3px 8px;border-radius:999px;text-transform:uppercase}
.tp-chip.main{background:rgba(96,165,250,.16);color:#9cc4fb}.tp-chip.tomo{background:rgba(167,139,250,.16);color:#c2b1fb}.tp-chip.hot{background:rgba(248,113,113,.18);color:#fca5a5}
.tp-nm{font-size:12.5px;font-weight:700;margin-top:7px;min-height:32px;line-height:1.2}
.tp-big{display:flex;align-items:baseline;gap:5px;margin-top:3px}
.tp-pct{font-size:21px;font-weight:800;letter-spacing:-.5px}
.tp-arrow{font-size:13px}
.tp-periods{display:flex;gap:5px;margin-top:12px}
.tp-pcell{flex:1;text-align:center;background:var(--panel-2);border:1px solid var(--border);border-radius:8px;padding:5px 2px}
.tp-pcell .pl{font-size:8.5px;color:var(--neutral);text-transform:uppercase}.tp-pcell .pv{font-size:11px;font-weight:700;margin-top:2px}
.tp-foot{display:flex;justify-content:space-between;align-items:center;margin-top:8px;border-top:1px solid var(--border);padding-top:7px;font-size:10.5px;color:var(--muted)}
.tp-cardadmin{position:absolute;top:6px;right:8px;display:flex;gap:4px;opacity:0;transition:.14s;z-index:2}
.tp-cardadmin button{width:20px;height:20px;border:1px solid var(--border2);background:var(--panel-2);color:var(--muted);border-radius:6px;font-size:10px;cursor:pointer;line-height:1;padding:0}
.tp-cardadmin button:hover{color:#fff}
.pos{color:var(--green)} .neg{color:var(--red)} .flat{color:var(--muted)}

.tp-scrim{position:fixed;inset:0;background:rgba(4,7,12,.72);backdrop-filter:blur(3px);display:flex;align-items:flex-start;justify-content:center;padding:32px 16px;z-index:60;overflow-y:auto}
.tp-modal{width:100%;max-width:860px;background:#0f1622;border:1px solid var(--border2);border-radius:20px;box-shadow:0 30px 80px rgba(0,0,0,.6);overflow:hidden}
.tp-mhead{padding:20px 22px;border-bottom:1px solid var(--border);position:relative}
.tp-x{position:absolute;right:16px;top:16px;width:30px;height:30px;border-radius:8px;border:1px solid var(--border2);background:var(--panel-2);color:var(--muted);font-size:16px;cursor:pointer}
.tp-x:hover{color:#fff}
.tp-mtag{display:inline-flex;gap:7px;margin-bottom:8px}
.tp-mh1{font-size:21px;font-weight:800;letter-spacing:-.3px}
.tp-mdesc{font-size:13px;color:var(--muted);margin-top:7px;max-width:680px}
.tp-mmeta{display:flex;gap:16px;flex-wrap:wrap;margin-top:12px;font-size:11.5px;color:var(--muted)}.tp-mmeta b{color:var(--fg)}
.tp-mbody{padding:18px 22px 22px}
.tp-perfrow{display:flex;gap:12px;flex-wrap:wrap;align-items:stretch}
.tp-mperf{display:grid;grid-template-columns:repeat(4,minmax(54px,1fr));gap:8px;flex:1 1 280px}
.tp-mperf .c{background:var(--panel-2);border:1px solid var(--border);border-radius:10px;padding:9px;text-align:center}
.tp-mperf .c .l{font-size:9px;color:var(--neutral);text-transform:uppercase}.tp-mperf .c .v{font-size:15px;font-weight:800;margin-top:2px}
.tp-etfs{flex:1 1 260px;display:flex;flex-direction:column;gap:6px;justify-content:center}
.tp-etf{display:flex;align-items:center;justify-content:space-between;gap:8px;background:var(--panel-2);border:1px solid var(--border2);border-radius:9px;padding:7px 11px;text-decoration:none;color:var(--fg)}
.tp-etf:hover{border-color:var(--green)}
.tp-etfsym{font-weight:800;font-family:var(--mono);font-size:12.5px}
.tp-etfsym:hover{color:var(--green);text-decoration:underline}
.tp-etfnote{color:var(--neutral);font-size:10.5px}
.tp-mh2{font-size:11px;font-weight:800;text-transform:uppercase;letter-spacing:.07em;color:var(--muted);margin:18px 0 8px}
.tp-table{width:100%;border-collapse:collapse;font-size:12.5px}
.tp-table thead th{text-align:right;font-size:10px;text-transform:uppercase;letter-spacing:.04em;color:var(--neutral);padding:7px 10px;border-bottom:1px solid var(--border2);white-space:nowrap}
.tp-table thead th:first-child{text-align:left}
.tp-table tbody td{text-align:right;padding:7px 10px;border-bottom:1px solid var(--border)}
.tp-table tbody td:first-child{text-align:left}
.tp-table tbody tr:hover{background:rgba(255,255,255,.02)}
.tp-tk{font-weight:700;font-family:var(--mono)}
.tp-tklink{color:var(--fg);text-decoration:underline;text-decoration-style:dotted;text-decoration-color:var(--muted);text-underline-offset:3px}
.tp-tklink:hover{color:var(--green);text-decoration-color:var(--green)}
.tp-fine{font-size:10.5px;color:var(--neutral);margin-top:14px;line-height:1.55}
.tp-addtk{display:flex;gap:8px;align-items:center;margin:4px 0 12px;flex-wrap:wrap}
.tp-addtk input{background:var(--panel-2);border:1px solid var(--border2);color:var(--fg);border-radius:8px;padding:6px 10px;font-size:12px;width:160px}
.tp-addtk button{background:var(--panel-2);border:1px solid var(--border2);color:var(--fg);border-radius:8px;padding:6px 12px;font-size:12px;cursor:pointer}
.tp-addtk button:hover{border-color:var(--green);color:var(--green)}
.tp-rmtk{border:0;background:transparent;color:var(--neutral);cursor:pointer;font-size:11px;padding:0 2px}
.tp-rmtk:hover{color:var(--red)}
</style>
</head>
<body>
<div class="shell">
  <div class="tp-hd">
    <div>
      <div class="tp-title"><span class="tp-dot"></span><span>ThemePulse</span></div>
      <div class="tp-sub">Theme board + rotation · click a theme to open its stocks</div>
    </div>
    <div style="text-align:right">
      <div class="tp-asof" id="asof">—</div>
      <div class="tp-toolbar">
        <span class="tp-trigmsg" id="savedMsg"></span>
        <button id="addThemeBtn">+ Theme</button>
        <button id="refreshBtn">↻ Refresh</button>
      </div>
    </div>
  </div>

  <div class="tp-controls">
    <div class="tp-seg tp-period" id="periodSeg">
      <button data-p="d1" class="on">1D</button>
      <button data-p="w1">1W</button>
      <button data-p="m1">1M</button>
      <button data-p="ytd">YTD</button>
    </div>
    <div style="display:flex;align-items:center">
      <span class="tp-lbl">Category</span>
      <div class="tp-seg" id="catSeg">
        <button data-c="all" class="on">All</button>
        <button data-c="main">Core</button>
        <button data-c="tomo">Frontier</button>
        <button data-c="rising">Gainers</button>
        <button data-c="falling">Decliners</button>
      </div>
    </div>
  </div>

  <div class="tp-strip" id="rotStrip"></div>
  <div class="tp-kpis" id="kpis"></div>
  <div class="tp-sectitle" id="boardTitle"></div>
  <div class="tp-grid" id="grid"></div>

  <div class="tp-fine" id="footFine"></div>
</div>

<div id="modalRoot"></div>

<script>
const FALLBACK = __FALLBACK__;
const PLABEL = {d1:"1D", w1:"1W", m1:"1M", ytd:"YTD"};
const NEXTP  = {d1:"w1", w1:"m1", m1:"ytd", ytd:"m1"};
let DATA = null, THEMES = [], period = "d1", cat = "all", openId = null;

const fmt = v => (v==null) ? "—" : (v>0?"+":"") + Number(v).toFixed(1) + "%";
const cls = v => (v==null) ? "flat" : v>0.05 ? "pos" : v<-0.05 ? "neg" : "flat";
const arr = v => (v==null) ? "▬" : v>0.05 ? "▲" : v<-0.05 ? "▼" : "▬";
const flash = t => { const m=document.getElementById("savedMsg"); m.textContent=t; clearTimeout(flash._t); flash._t=setTimeout(()=>m.textContent="",1800); };

async function boot(){
  try{
    const r = await fetch("themes.json", {cache:"no-store"});
    if(!r.ok) throw 0;
    DATA = await r.json();
  }catch(e){ DATA = FALLBACK; }
  THEMES = DATA.themes.map(t => ({...t, ret:{...t.ret}, stocks:t.stocks.map(s=>({...s}))}));
  render();
}

function ranked(){ return [...THEMES].sort((a,b)=>(b.ret[period]??-1e9)-(a.ret[period]??-1e9)); }
function top5OfPeriod(p){ return new Set([...THEMES].sort((a,b)=>(b.ret[p]??-1e9)-(a.ret[p]??-1e9)).slice(0,5).map(t=>t.id)); }
function filtered(list){
  return list.filter(t=>{
    const r=t.ret[period];
    if(cat==="main")   return t.kind==="main";
    if(cat==="tomo")   return t.kind==="tomo";
    if(cat==="rising") return r>0.05;
    if(cat==="falling")return r<-0.05;
    return true;
  });
}

function render(){
  const list = ranked();
  const rankMap = new Map(list.map((t,i)=>[t.id,i+1]));
  const top5 = top5OfPeriod(period);

  document.getElementById("asof").innerHTML =
    `As of ${DATA.asof} · <b>${PLABEL[period]}</b> return`;

  // KPIs
  const vals = list.map(t=>t.ret[period]).filter(v=>v!=null);
  const avg = vals.reduce((s,v)=>s+v,0)/(vals.length||1);
  const posN = vals.filter(v=>v>0.05).length;
  const lead = list[0], weak = list[list.length-1];
  document.getElementById("kpis").innerHTML = `
    <div class="tp-kpi"><div class="k">Themes</div><div class="v">${THEMES.length}</div><div class="x">curated set</div></div>
    <div class="tp-kpi"><div class="k">Leader</div><div class="v ${cls(lead.ret[period])}">${fmt(lead.ret[period])}</div><div class="x">${lead.name}</div></div>
    <div class="tp-kpi"><div class="k">Average</div><div class="v ${cls(avg)}">${fmt(avg)}</div><div class="x">${posN}/${THEMES.length} positive</div></div>
    <div class="tp-kpi"><div class="k">Weakest</div><div class="v ${cls(weak.ret[period])}">${fmt(weak.ret[period])}</div><div class="x">${weak.name}</div></div>`;

  // Rotation — current period top-5 vs next-longer period top-5
  const np = NEXTP[period], base = top5OfPeriod(np);
  const entered = [...top5].filter(id=>!base.has(id)).map(id=>THEMES.find(t=>t.id===id).name);
  const exited  = [...base].filter(id=>!top5.has(id)).map(id=>THEMES.find(t=>t.id===id).name);
  document.getElementById("rotStrip").innerHTML =
    `<span>Into Top-5 (${PLABEL[period]} vs ${PLABEL[np]}): <b>${entered.join(", ")||"—"}</b></span>`+
    `<span>Out of Top-5: <b>${exited.join(", ")||"—"}</b></span>`;

  document.getElementById("boardTitle").textContent = `Board · by ${PLABEL[period]} return · (click → detail)`;

  // Grid
  const shown = filtered(list);
  const accent = {main:"var(--blue)", tomo:"var(--purple)"};
  document.getElementById("grid").innerHTML = shown.length ? shown.map(t=>{
    const rk = rankMap.get(t.id), r = t.ret[period], hot = top5.has(t.id);
    const chip = hot ? `<span class="tp-chip hot">HOT</span>`
               : t.kind==="main" ? `<span class="tp-chip main">CORE</span>`
               : `<span class="tp-chip tomo">FRONTIER</span>`;
    const cells = ["d1","w1","m1","ytd"].map(p=>`<div class="tp-pcell"><div class="pl">${PLABEL[p]}</div><div class="pv ${cls(t.ret[p])}">${fmt(t.ret[p])}</div></div>`).join("");
    return `<div class="tp-card" data-id="${t.id}">
      <div class="tp-edge" style="background:${hot?'var(--red)':accent[t.kind]}"></div>
      <div class="tp-cardadmin"><button data-act="del" data-id="${t.id}" title="Remove theme">✕</button></div>
      <div class="tp-crow"><span class="tp-rk">#<b>${rk}</b></span><div class="tp-badges">${chip}</div></div>
      <div class="tp-nm">${t.name}</div>
      <div class="tp-big"><span class="tp-arrow ${cls(r)}">${arr(r)}</span><span class="tp-pct ${cls(r)}">${fmt(r)}</span></div>
      <div class="tp-periods">${cells}</div>
      <div class="tp-foot"><span>${t.count} stocks</span><span class="tp-open">detail →</span></div>
    </div>`;
  }).join("") : `<div style="grid-column:1/-1;color:var(--muted);font-size:13px;border:1px solid var(--border);background:var(--panel);border-radius:10px;padding:14px">No themes in this filter.</div>`;

  document.getElementById("footFine").innerHTML =
    `Source: <code>themes.json</code> · ${DATA.note||""} Equal-weight average of constituent returns. `+
    `Ticker–theme membership is curated in <code>scripts/build_themes.py</code>; regenerate to update. `+
    `Generated ${DATA.generated||"—"}.`;
}

function openModal(id){
  openId = id;
  const t = THEMES.find(x=>x.id===id); if(!t) return;
  const list = ranked(), rk = list.findIndex(x=>x.id===id)+1;
  const stocks = [...t.stocks].sort((a,b)=>(b[period]??-1e9)-(a[period]??-1e9));
  const perf = ["d1","w1","m1","ytd"].map(p=>`<div class="c"><div class="l">${PLABEL[p]}</div><div class="v ${cls(t.ret[p])}">${fmt(t.ret[p])}</div></div>`).join("");
  const etfs = (t.etfs||[]).map(e=>`<a class="tp-etf" href="https://finance.yahoo.com/quote/${e.sym}" target="_blank" rel="noopener"><span class="tp-etfsym">${e.sym}</span><span class="tp-etfnote">${e.note||""}</span></a>`).join("") || `<div class="tp-etfnote">No matched ETF.</div>`;
  const rows = stocks.map(s=>`<tr>
      <td><a class="tp-tk tp-tklink" href="https://finance.yahoo.com/quote/${s.sym}" target="_blank" rel="noopener">${s.sym}</a></td>
      <td class="${cls(s.d1)}">${fmt(s.d1)}</td><td class="${cls(s.w1)}">${fmt(s.w1)}</td>
      <td class="${cls(s.m1)}">${fmt(s.m1)}</td><td class="${cls(s.ytd)}">${fmt(s.ytd)}</td>
      <td><button class="tp-rmtk" data-rm="${s.sym}" title="Remove">✕</button></td>
    </tr>`).join("");
  const chip = t.kind==="main" ? `<span class="tp-chip main">CORE</span>` : `<span class="tp-chip tomo">FRONTIER</span>`;
  document.getElementById("modalRoot").innerHTML = `
   <div class="tp-scrim" id="scrim">
    <div class="tp-modal" role="dialog" aria-modal="true">
      <div class="tp-mhead">
        <button class="tp-x" id="closeX" aria-label="Close">×</button>
        <div class="tp-mtag">${chip}<span class="tp-chip" style="background:var(--panel-2);color:var(--muted);border:1px solid var(--border2)">#${rk}</span></div>
        <div class="tp-mh1">${t.name}</div>
        <div class="tp-mdesc">${t.desc||""}</div>
        <div class="tp-mmeta"><span>Stocks <b>${t.count}</b></span><span>${PLABEL[period]} <b class="${cls(t.ret[period])}">${fmt(t.ret[period])}</b></span></div>
      </div>
      <div class="tp-mbody">
        <div class="tp-perfrow">
          <div class="tp-mperf">${perf}</div>
          <div class="tp-etfs">${etfs}</div>
        </div>
        <div class="tp-mh2">Stocks · sorted by ${PLABEL[period]}</div>
        <div class="tp-addtk">
          <input id="newTk" placeholder="Add ticker (e.g. NVDA)" />
          <button id="addTkBtn">+ Add</button>
          <span class="tp-etfnote">Session only — for permanent changes edit build_themes.py.</span>
        </div>
        <table class="tp-table"><thead><tr><th>Ticker</th><th>1D</th><th>1W</th><th>1M</th><th>YTD</th><th></th></tr></thead><tbody>${rows}</tbody></table>
        <div class="tp-fine">Returns from Yahoo Finance adjusted close. Newly added tickers show no returns until the next themes.json rebuild.</div>
      </div>
    </div>
   </div>`;
  const scrim = document.getElementById("scrim");
  scrim.addEventListener("click", e=>{ if(e.target===scrim) closeModal(); });
  document.getElementById("closeX").onclick = closeModal;
  document.getElementById("addTkBtn").onclick = ()=>{
    const v = document.getElementById("newTk").value.trim().toUpperCase();
    if(v && !t.stocks.some(s=>s.sym===v)){ t.stocks.push({sym:v,d1:null,w1:null,m1:null,ytd:null}); t.count++; openModal(id); render(); }
  };
  document.querySelectorAll("[data-rm]").forEach(b=>b.onclick=()=>{
    t.stocks = t.stocks.filter(s=>s.sym!==b.dataset.rm); t.count = Math.max(t.count-1, t.stocks.length); openModal(id); render();
  });
}
function closeModal(){ openId=null; document.getElementById("modalRoot").innerHTML=""; }

function addTheme(){
  const name = prompt("Theme name:"); if(!name) return;
  const kind = (prompt("Type — main (Core) / tomo (Frontier):","tomo")||"tomo").toLowerCase()==="main" ? "main" : "tomo";
  THEMES.push({id:"t"+Date.now(), name, kind, count:0, desc:"", ret:{d1:null,w1:null,m1:null,ytd:null}, etfs:[], stocks:[]});
  render();
}

document.getElementById("periodSeg").addEventListener("click", e=>{ const b=e.target.closest("button"); if(!b)return; period=b.dataset.p; document.querySelectorAll("#periodSeg button").forEach(x=>x.classList.toggle("on",x===b)); render(); });
document.getElementById("catSeg").addEventListener("click", e=>{ const b=e.target.closest("button"); if(!b)return; cat=b.dataset.c; document.querySelectorAll("#catSeg button").forEach(x=>x.classList.toggle("on",x===b)); render(); });
document.getElementById("grid").addEventListener("click", e=>{
  const del=e.target.closest("[data-act=del]");
  if(del){ e.stopPropagation(); if(confirm("Remove this theme?")){ THEMES=THEMES.filter(t=>t.id!==del.dataset.id); render(); } return; }
  const card=e.target.closest(".tp-card"); if(card) openModal(card.dataset.id);
});
document.getElementById("refreshBtn").onclick = ()=>{ boot(); flash("refreshed ↻"); };
document.getElementById("addThemeBtn").onclick = addTheme;
document.addEventListener("keydown", e=>{ if(e.key==="Escape" && openId) closeModal(); });

boot();
</script>
</body>
</html>
"""

open("ThemePulse.html", "w").write(HTML.replace("__FALLBACK__", FALLBACK))
print("Wrote ThemePulse.html")
