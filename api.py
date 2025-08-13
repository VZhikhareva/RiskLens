# api.py
from fastapi import FastAPI
from pydantic import BaseModel, Field
from fastapi.responses import HTMLResponse  # ← NEW
from service import RiskService
from models import RiskReport

app = FastAPI(title="RiskLens API", version="0.3.0")

@app.get("/health")
def health():
    return {"status": "ok"}

class AnalyzeIn(BaseModel):
    scenario: str = Field(..., min_length=1, description="Free-text scenario to analyze")

@app.post("/analyze", response_model=RiskReport)
def analyze(payload: AnalyzeIn):
    svc = RiskService()
    report = svc.analyze(payload.scenario)
    return report

# --- NEW: tiny HTML page with a form + JS ---
@app.get("/", response_class=HTMLResponse)
def home():
    return """
<!doctype html>
<html>
<head>
  <meta charset="utf-8"/>
  <title>RiskLens — Demo</title>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <style>
    :root{
      --bg:#0f172a; --panel:#111827; --muted:#9ca3af; --ok:#10b981; --warn:#f59e0b; --bad:#ef4444; --chip:#1f2937;
    }
    *{box-sizing:border-box}
    body { margin:0; background:var(--bg); color:#e5e7eb; font-family: ui-sans-serif,system-ui,Segoe UI,Roboto,Arial; }
    header { padding:20px 24px; border-bottom:1px solid #1f2937; }
    main { padding:24px; max-width:1100px; margin:0 auto; }
    h1 { margin:0 0 4px 0; font-size:20px; font-weight:700; }
    p.sub { margin:0; color:var(--muted); }
    .grid { display:grid; gap:18px; grid-template-columns: 1fr; }
    @media(min-width:1024px){ .grid{ grid-template-columns: 1fr 1fr; } }
    .panel { background:var(--panel); border:1px solid #1f2937; border-radius:12px; padding:16px; }
    textarea{ width:100%; min-height:160px; background:#0b1220; color:#e5e7eb; border:1px solid #1f2937; border-radius:10px; padding:12px; }
    button{ background:#2563eb; color:white; border:none; padding:10px 14px; border-radius:10px; cursor:pointer; font-weight:600; }
    button:disabled{ opacity:.5; cursor:not-allowed; }
    .status{ margin-left:10px; color:var(--muted); }
    .cards{ display:grid; gap:12px; }
    .card{ background:#0b1220; border:1px solid #1f2937; border-radius:12px; padding:14px; }
    .card h3{ margin:0 0 6px 0; font-size:16px; }
    .row{ display:flex; gap:10px; flex-wrap:wrap; align-items:center; }
    .badge{ padding:2px 8px; border-radius:999px; background:var(--chip); color:#cbd5e1; font-size:12px; border:1px solid #263042;}
    .sev-1,.sev-2{ background:rgba(16,185,129,.15); border-color:#064e3b; color:#a7f3d0;}
    .sev-3{ background:rgba(245,158,11,.15); border-color:#78350f; color:#fde68a;}
    .sev-4,.sev-5{ background:rgba(239,68,68,.15); border-color:#7f1d1d; color:#fecaca;}
    .k{ color:#94a3b8; font-size:12px; }
    ul.inline{ list-style:none; padding:0; margin:6px 0 0 0; display:flex; gap:8px; flex-wrap:wrap; }
    ul.inline li{ background:#0b1220; border:1px dashed #334155; color:#cbd5e1; padding:4px 8px; border-radius:8px; font-size:12px; }
    details{ margin-top:10px; }
    pre{ background:#0b1220; border:1px solid #1f2937; padding:12px; border-radius:10px; color:#e5e7eb; overflow:auto; }
    .empty{ color:var(--muted); font-style:italic; }
  </style>
</head>
<body>
  <header>
    <h1>RiskLens — Minimal Web Demo</h1>
    <p class="sub">Paste a scenario → get a structured risk report.</p>
  </header>

  <main>
    <div class="grid">
      <div class="panel">
        <label for="scenario" class="k">Scenario</label>
        <textarea id="scenario" placeholder="We collect patient forms in S3. Vendor has access. No BAA signed."></textarea>
        <div style="display:flex; align-items:center; gap:8px; margin-top:10px;">
          <button id="sendBtn">Analyze</button>
          <span id="status" class="status"></span>
        </div>
      </div>

      <div class="panel">
        <div class="row" style="justify-content:space-between; margin-bottom:6px;">
          <div class="k">Results</div>
          <details>
            <summary class="k">Raw JSON</summary>
            <pre id="raw">{}</pre>
          </details>
        </div>
        <div id="cards" class="cards">
          <div class="empty">No results yet. Submit a scenario to see risks.</div>
        </div>
      </div>
    </div>
  </main>

  <script>
    const btn = document.getElementById('sendBtn');
    const area = document.getElementById('scenario');
    const statusEl = document.getElementById('status');
    const rawEl = document.getElementById('raw');
    const cardsEl = document.getElementById('cards');

    function sevClass(n){
      if(n>=4) return 'sev-4';
      if(n===3) return 'sev-3';
      return 'sev-1';
    }

    function renderReport(json){
      rawEl.textContent = JSON.stringify(json, null, 2);
      cardsEl.innerHTML = '';

      const items = (json && json.items) ? json.items : [];
      if(!items.length){
        cardsEl.innerHTML = '<div class="empty">No risks extracted.</div>';
        return;
      }

      for(const it of items){
        const controls = (it.controls||[]).map(c=>`<li>${escapeHtml(c)}</li>`).join('');
        const evid = (it.evidence||[]).map(e=>`<li>${escapeHtml(e)}</li>`).join('');
        const stds = (it.standards||[]).map(s=>`<span class="badge">${escapeHtml(s)}</span>`).join(' ');
        const owner = it.owner ? `<span class="badge">${escapeHtml(it.owner)}</span>` : '<span class="badge">owner: n/a</span>';
        const horizon = it.time_horizon ? `<span class="badge">${escapeHtml(it.time_horizon)}</span>` : '';

        const html = `
          <div class="card">
            <h3>${escapeHtml(it.risk || 'Untitled risk')}</h3>
            <div class="row" style="margin-bottom:6px;">
              <span class="badge">${escapeHtml(it.category || 'Uncategorized')}</span>
              <span class="badge ${sevClass(+it.severity||1)}">severity: ${escapeHtml(String(it.severity||1))}</span>
              <span class="badge ${sevClass(+it.likelihood||1)}">likelihood: ${escapeHtml(String(it.likelihood||1))}</span>
              ${owner}
              ${horizon}
            </div>

            ${stds ? `<div class="row" style="margin:6px 0;">${stds}</div>` : ''}

            ${(it.controls||[]).length ? `<div class="k">Controls</div><ul class="inline">${controls}</ul>` : ''}
            ${(it.evidence||[]).length ? `<div class="k" style="margin-top:8px;">Evidence (quotes)</div><ul class="inline">${evid}</ul>` : ''}
          </div>
        `;
        cardsEl.insertAdjacentHTML('beforeend', html);
      }
    }

    function escapeHtml(str){
      return String(str)
        .replaceAll('&','&amp;')
        .replaceAll('<','&lt;')
        .replaceAll('>','&gt;')
        .replaceAll('"','&quot;')
        .replaceAll("'",'&#39;');
    }

    btn.addEventListener('click', async () => {
      const scenario = area.value.trim();
      if (!scenario) {
        renderReport({ items: [] });
        rawEl.textContent = JSON.stringify({error: "Scenario is empty."}, null, 2);
        return;
      }
      btn.disabled = true;
      statusEl.textContent = "Analyzing…";
      try {
        const resp = await fetch('/analyze', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ scenario })
        });
        const json = await resp.json();
        if(!resp.ok){
          throw new Error(JSON.stringify(json));
        }
        renderReport(json);
      } catch (err) {
        renderReport({ items: [] });
        rawEl.textContent = JSON.stringify({ error: String(err) }, null, 2);
      } finally {
        statusEl.textContent = "";
        btn.disabled = false;
      }
    });
  </script>
</body>
</html>
    """

