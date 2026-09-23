"""
Dashboard final amélioré
- Sidebar
- Filtre par région
- Nouveaux graphiques
- Design soigné
Défi 02 - Togo AI Lab
"""

from pathlib import Path

from src.load_data import (
    load_internet_usage,
    load_telecom,
    load_agents,
    load_etablissements,
    load_population,
)
from src.process_data import (
    agents_by_region,
    etab_by_region,
    region_population,
    compute_ratios,
)
from src.charts import (
    chart_internet_evolution,
    chart_telecom_subscribers,
    chart_market_share,
    chart_revenue_investment,
    chart_agents_by_region,
    chart_etab_by_region,
    chart_access_ratios,
    chart_agents_by_operator,
    chart_etab_by_category,
)
from src.map_chart import chart_map
from src.region_stats import build_region_stats, stats_to_json

OUTPUT_DIR = Path(__file__).parent.parent / "output"
OUTPUT_DIR.mkdir(exist_ok=True)


def main():
    print("1. Chargement...")
    internet = load_internet_usage()
    telecom = load_telecom()
    agents = load_agents()
    etab = load_etablissements()
    pop = load_population()

    print("2. Agrégations...")
    a_reg = agents_by_region(agents)
    e_reg = etab_by_region(etab)
    p_reg = region_population(pop)
    ratios = compute_ratios(a_reg, e_reg, p_reg)
    region_stats = build_region_stats(agents, etab, ratios)
    region_json = stats_to_json(region_stats)

    total_pop = int(pop[pop["admin_unit"] == "TOGO"]["population"].values[0])
    latest_pen = float(internet.iloc[-1]["penetration"])
    n_agents = len(agents)
    n_etab = len(etab)

    print("3. Graphiques...")
    figs = {
        "internet": chart_internet_evolution(internet),
        "telecom_sub": chart_telecom_subscribers(telecom),
        "market": chart_market_share(telecom),
        "revenue": chart_revenue_investment(telecom),
        "agents_reg": chart_agents_by_region(a_reg),
        "etab_reg": chart_etab_by_region(e_reg),
        "ratios": chart_access_ratios(ratios),
        "map": chart_map(agents, etab),
        "operators": chart_agents_by_operator(agents),
        "categories": chart_etab_by_category(etab),
    }

    print("4. Conversion HTML...")
    divs = {}
    first = True
    for key, fig in figs.items():
        divs[key] = fig.to_html(
            full_html=False,
            include_plotlyjs="cdn" if first else False,
        )
        first = False

    ratios_html = ratios.to_html(index=False, float_format="%.1f", border=0)

    # Options du select
    region_options = "".join(
        f'<option value="{r}">{r.title() if r != "TOUTES" else "Toutes les régions"}</option>'
        for r in region_stats.keys()
    )

    print("5. Assemblage...")

    html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Togo Digital Inclusion Dashboard | Défi 02</title>
  <style>
    :root {{
      --sidebar-w: 250px;
      --bg: #f0f4f8;
      --card: #ffffff;
      --text: #0f172a;
      --muted: #64748b;
      --accent: #0ea5e9;
      --sidebar: #0b1220;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
      background: var(--bg);
      color: var(--text);
      display: flex;
      min-height: 100vh;
    }}

        /* SIDEBAR améliorée */
    .sidebar {{
      width: var(--sidebar-w);
      background: linear-gradient(180deg, #0b1220 0%, #111827 100%);
      color: #e2e8f0;
      padding: 0;
      position: fixed;
      inset: 0 auto 0 0;
      overflow-y: auto;
      z-index: 50;
      display: flex;
      flex-direction: column;
      box-shadow: 4px 0 24px rgba(0,0,0,0.15);
    }}
    .brand {{
      padding: 22px 18px 18px;
      background: rgba(14, 165, 233, 0.08);
      border-bottom: 1px solid rgba(255,255,255,0.06);
      margin-bottom: 12px;
    }}
    .brand h1 {{
      font-size: 15px;
      font-weight: 700;
      color: #fff;
      line-height: 1.35;
    }}
    .brand p {{
      font-size: 11px;
      color: #64748b;
      margin-top: 5px;
    }}
    .nav-group {{
      padding: 0 10px;
      flex: 1;
    }}
    .nav-btn {{
      display: flex;
      align-items: center;
      gap: 10px;
      width: 100%;
      text-align: left;
      background: transparent;
      border: none;
      color: #94a3b8;
      padding: 11px 12px;
      border-radius: 9px;
      font-size: 13px;
      font-weight: 500;
      cursor: pointer;
      margin-bottom: 3px;
      transition: all 0.18s ease;
    }}
    .nav-btn .icon {{
      width: 20px;
      text-align: center;
      font-size: 14px;
      opacity: 0.85;
    }}
    .nav-btn:hover {{
      background: rgba(255,255,255,0.06);
      color: #f1f5f9;
      transform: translateX(3px);
    }}
    .nav-btn.active {{
      background: linear-gradient(135deg, #0ea5e9, #0284c7);
      color: #fff;
      box-shadow: 0 4px 12px rgba(14, 165, 233, 0.35);
    }}
    .sidebar-footer {{
      padding: 14px 18px 18px;
      border-top: 1px solid rgba(255,255,255,0.06);
      font-size: 10.5px;
      color: #475569;
      line-height: 1.5;
    }}

    /* KPI avec animation */
    .kpi-card .value {{
      font-size: 22px;
      font-weight: 700;
      margin-top: 4px;
      font-variant-numeric: tabular-nums;
    }}
    .kpi-card.loading .value {{
      opacity: 0.4;
    }}

    /* MAIN */
    .main {{
      margin-left: var(--sidebar-w);
      flex: 1;
      padding: 24px 28px 40px;
      max-width: 1080px;
    }}
    .topbar {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 12px;
      margin-bottom: 22px;
    }}
    .topbar h2 {{
      font-size: 20px;
      font-weight: 700;
    }}
    .filter-box {{
      display: flex;
      align-items: center;
      gap: 8px;
      background: var(--card);
      padding: 8px 12px;
      border-radius: 10px;
      box-shadow: 0 1px 2px rgba(0,0,0,0.05);
    }}
    .filter-box label {{
      font-size: 12px;
      color: var(--muted);
      font-weight: 500;
    }}
    .filter-box select {{
      border: 1px solid #e2e8f0;
      border-radius: 6px;
      padding: 6px 10px;
      font-size: 13px;
      background: #f8fafc;
      cursor: pointer;
      outline: none;
    }}
    .filter-box select:focus {{ border-color: var(--accent); }}

    /* KPI */
    .kpi {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
      gap: 12px;
      margin-bottom: 24px;
    }}
    .kpi-card {{
      background: var(--card);
      border-radius: 12px;
      padding: 16px;
      box-shadow: 0 1px 3px rgba(0,0,0,0.04);
      border-left: 4px solid;
    }}
    .kpi-card .label {{
      font-size: 11px;
      color: var(--muted);
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.03em;
    }}
    .kpi-card .value {{
      font-size: 22px;
      font-weight: 700;
      margin-top: 4px;
    }}
    .kpi-card.blue {{ border-color: #0ea5e9; }}
    .kpi-card.green {{ border-color: #10b981; }}
    .kpi-card.orange {{ border-color: #f97316; }}
    .kpi-card.purple {{ border-color: #8b5cf6; }}
    .kpi-card.blue .value {{ color: #0369a1; }}
    .kpi-card.green .value {{ color: #047857; }}
    .kpi-card.orange .value {{ color: #c2410c; }}
    .kpi-card.purple .value {{ color: #6d28d9; }}

    /* SECTIONS */
    .section {{ display: none; }}
    .section.active {{ display: block; }}
    .card {{
      background: var(--card);
      border-radius: 12px;
      padding: 18px;
      margin-bottom: 16px;
      box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    }}
    .card h3 {{
      font-size: 15px;
      font-weight: 600;
      margin-bottom: 12px;
      padding-bottom: 8px;
      border-bottom: 1px solid #e2e8f0;
    }}
    .grid-2 {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 16px;
    }}
    @media (max-width: 800px) {{
      .grid-2 {{ grid-template-columns: 1fr; }}
      .sidebar {{ width: 200px; }}
      .main {{ margin-left: 200px; padding: 16px; }}
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 13px;
    }}
    th, td {{
      padding: 9px 11px;
      text-align: left;
      border-bottom: 1px solid #e2e8f0;
    }}
    th {{ background: #f8fafc; font-weight: 600; font-size: 12px; }}
    .note {{
      font-size: 12px;
      color: var(--muted);
      margin-top: 10px;
      line-height: 1.5;
    }}
    .reco ol {{
      padding-left: 18px;
      line-height: 1.8;
      font-size: 13.5px;
    }}
    .reco li {{ margin-bottom: 8px; }}
  </style>
</head>
<body>

<aside class="sidebar">
  <div class="brand">
    <h1>Togo Digital Inclusion</h1>
    <p>Défi 02 · Économie Numérique<br>Togo AI Lab</p>
  </div>

  <div class="nav-group">
    <button class="nav-btn active" onclick="showSection('overview', this)">
      <span class="icon">▣</span> Vue d'ensemble
    </button>
    <button class="nav-btn" onclick="showSection('internet', this)">
      <span class="icon">↗</span> Usage Internet
    </button>
    <button class="nav-btn" onclick="showSection('telecom', this)">
      <span class="icon">◉</span> Marché Télécoms
    </button>
    <button class="nav-btn" onclick="showSection('map', this)">
      <span class="icon">◎</span> Carte des accès
    </button>
    <button class="nav-btn" onclick="showSection('access', this)">
      <span class="icon">☰</span> Points d'accès
    </button>
    <button class="nav-btn" onclick="showSection('ratios', this)">
      <span class="icon">≡</span> Ratios d'accès
    </button>
    <button class="nav-btn" onclick="showSection('detail', this)">
      <span class="icon">◐</span> Opérateurs & Catégories
    </button>
    <button class="nav-btn" onclick="showSection('reco', this)">
      <span class="icon">★</span> Recommandations
    </button>
  </div>

  <div class="sidebar-footer">
    World Bank · ARCEP · RGPH-5<br>
    Agents MM · Établissements
  </div>
</aside>

<main class="main">

  <!-- TOPBAR + FILTRE -->
  <div class="topbar">
    <h2 id="page-title">Vue d'ensemble</h2>
    <div class="filter-box">
      <label for="region-filter">Région</label>
      <select id="region-filter" onchange="applyRegionFilter()">
        {region_options}
      </select>
    </div>
  </div>

  <!-- KPI (mis à jour par le filtre) -->
  <div class="kpi" id="kpi-row">
    <div class="kpi-card blue">
      <div class="label">Pénétration Internet</div>
      <div class="value">{latest_pen:.1f}%</div>
    </div>
    <div class="kpi-card green">
      <div class="label">Agents Mobile Money</div>
      <div class="value" id="kpi-agents">{n_agents:,}</div>
    </div>
    <div class="kpi-card orange">
      <div class="label">Établissements</div>
      <div class="value" id="kpi-etab">{n_etab:,}</div>
    </div>
    <div class="kpi-card purple">
      <div class="label">Hab. / Agent</div>
      <div class="value" id="kpi-ratio">—</div>
    </div>
  </div>

  <!-- OVERVIEW -->
  <div id="overview" class="section active">
    <div class="card">
      <h3>Évolution de l'usage d'Internet</h3>
      {divs["internet"]}
    </div>
  </div>

  <!-- INTERNET -->
  <div id="internet" class="section">
    <div class="card">
      <h3>Usage d'Internet (% de la population)</h3>
      {divs["internet"]}
      <p class="note">Accélération à partir de 2016 (3G/4G), fort rebond en 2020 (COVID).</p>
    </div>
  </div>

  <!-- TELECOM -->
  <div id="telecom" class="section">
    <div class="card">
      <h3>Abonnés télécoms (2013-2019)</h3>
      {divs["telecom_sub"]}
    </div>
    <div class="card">
      <h3>Parts de marché mobile</h3>
      {divs["market"]}
    </div>
    <div class="card">
      <h3>Chiffre d'affaires & Investissements</h3>
      {divs["revenue"]}
    </div>
  </div>

  <!-- MAP -->
  <div id="map" class="section">
    <div class="card">
      <h3>Carte des points d'accès</h3>
      {divs["map"]}
      <p class="note">Bleu = Agents MM (échantillon) · Orange = Établissements financiers.</p>
    </div>
  </div>

  <!-- ACCESS -->
  <div id="access" class="section">
    <div class="card">
      <h3>Agents Mobile Money par région</h3>
      {divs["agents_reg"]}
    </div>
    <div class="card">
      <h3>Établissements financiers par région</h3>
      {divs["etab_reg"]}
    </div>
  </div>

  <!-- RATIOS -->
  <div id="ratios" class="section">
    <div class="card">
      <h3>Ratios d'accès</h3>
      {divs["ratios"]}
    </div>
    <div class="card">
      <h3>Tableau récapitulatif</h3>
      {ratios_html}
      <p class="note">Plus le ratio Habitants/Agent est élevé, plus la région est sous-équipée.</p>
    </div>
  </div>

  <!-- DETAIL -->
  <div id="detail" class="section">
    <div class="grid-2">
      <div class="card">
        <h3>Agents par opérateur</h3>
        {divs["operators"]}
      </div>
      <div class="card">
        <h3>Établissements par catégorie</h3>
        {divs["categories"]}
      </div>
    </div>
  </div>

  <!-- RECO -->
  <div id="reco" class="section">
    <div class="card reco">
      <h3>Recommandations stratégiques</h3>
      <ol>
        <li><strong>Prioriser Plateaux et Savanes</strong> — ratios habitants/agent les plus élevés (531 et 427). Accélérer agents + 4G.</li>
        <li><strong>Renforcer les établissements hors Maritime</strong> — Maritime concentre &gt;56 % des points bancaires/microfinance.</li>
        <li><strong>Capitaliser sur le réseau Mobile Money</strong> — ~20 000 agents. Interopérabilité Yas–Moov + éducation financière locale.</li>
        <li><strong>Accélérer le haut débit rural</strong> — relancer fibre et 4G hors des grandes villes après le ralentissement post-2018.</li>
        <li><strong>Maintenir l'open data territoriale</strong> — publier régulièrement les localisations pour un suivi dynamique.</li>
      </ol>
    </div>
  </div>

</main>

<script>
  const REGION_STATS = {region_json};

  const TITLES = {{
    overview: "Vue d'ensemble",
    internet: "Usage Internet",
    telecom: "Marché Télécoms",
    map: "Carte des accès",
    access: "Points d'accès",
    ratios: "Ratios d'accès",
    detail: "Opérateurs & Catégories",
    reco: "Recommandations"
  }};

  function showSection(id, btn) {{
    document.querySelectorAll('.section').forEach(s => s.classList.remove('active'));
    document.getElementById(id).classList.add('active');
    document.querySelectorAll('.nav-btn').forEach(b => b.classList.remove('active'));
    if (btn) btn.classList.add('active');
    document.getElementById('page-title').textContent = TITLES[id] || id;
  }}

  function fmt(n) {{
    if (n === null || n === undefined) return "—";
    return Math.round(Number(n)).toLocaleString("fr-FR");
  }}

  /* ===== Animation count-up ===== */
  function animateValue(el, end, duration) {{
    if (end === null || end === undefined) {{
      el.textContent = "—";
      return;
    }}
    const start = 0;
    const startTime = performance.now();
    end = Number(end);

    function tick(now) {{
      const progress = Math.min((now - startTime) / duration, 1);
      // easeOut
      const eased = 1 - Math.pow(1 - progress, 3);
      const current = Math.round(start + (end - start) * eased);
      el.textContent = current.toLocaleString("fr-FR");
      if (progress < 1) requestAnimationFrame(tick);
    }}
    requestAnimationFrame(tick);
  }}

  function applyRegionFilter(animate) {{
    const region = document.getElementById("region-filter").value;
    const s = REGION_STATS[region];
    if (!s) return;

    const elAgents = document.getElementById("kpi-agents");
    const elEtab = document.getElementById("kpi-etab");
    const elRatio = document.getElementById("kpi-ratio");

    if (animate) {{
      animateValue(elAgents, s.n_agents, 900);
      animateValue(elEtab, s.n_etab, 900);
      animateValue(elRatio, s.hab_per_agent, 900);
    }} else {{
      elAgents.textContent = fmt(s.n_agents);
      elEtab.textContent = fmt(s.n_etab);
      elRatio.textContent = s.hab_per_agent !== null ? fmt(s.hab_per_agent) : "—";
    }}
  }}

  // Au chargement de la page → animation des chiffres
  document.addEventListener("DOMContentLoaded", function() {{
    applyRegionFilter(true);
  }});

  // Changement de région → aussi avec animation
  document.getElementById("region-filter").addEventListener("change", function() {{
    applyRegionFilter(true);
  }});
</script>

</body>
</html>
"""

    out = OUTPUT_DIR / "dashboard_togo_digital.html"
    out.write_text(html, encoding="utf-8")
    print(f"\n✅ Dashboard amélioré généré → {out}")


if __name__ == "__main__":
    main()