"""
Dashboard interactif avec barre latérale
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
)
from src.map_chart import chart_map

OUTPUT_DIR = Path(__file__).parent.parent / "output"
OUTPUT_DIR.mkdir(exist_ok=True)


def main():
    print("1. Chargement des données...")
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

    total_pop = int(pop[pop["admin_unit"] == "TOGO"]["population"].values[0])
    latest_pen = float(internet.iloc[-1]["penetration"])
    n_agents = len(agents)
    n_etab = len(etab)

    print("3. Création des graphiques...")
    figs = {
        "internet": chart_internet_evolution(internet),
        "telecom_sub": chart_telecom_subscribers(telecom),
        "market": chart_market_share(telecom),
        "revenue": chart_revenue_investment(telecom),
        "agents_reg": chart_agents_by_region(a_reg),
        "etab_reg": chart_etab_by_region(e_reg),
        "ratios": chart_access_ratios(ratios),
        "map": chart_map(agents, etab),
    }

    print("4. Conversion HTML des graphiques...")
    # Premier graphique charge Plotly (CDN), les autres non
    divs = {}
    first = True
    for key, fig in figs.items():
        divs[key] = fig.to_html(
            full_html=False,
            include_plotlyjs="cdn" if first else False,
        )
        first = False

    ratios_html = ratios.to_html(
        index=False, float_format="%.1f", border=0
    )

    print("5. Assemblage du dashboard avec sidebar...")

    html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Togo Digital Inclusion Dashboard | Défi 02</title>
  <style>
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: system-ui, -apple-system, 'Segoe UI', sans-serif;
      background: #f1f5f9;
      color: #0f172a;
      display: flex;
      min-height: 100vh;
    }}

    /* ===== SIDEBAR ===== */
    .sidebar {{
      width: 260px;
      background: #0f172a;
      color: white;
      padding: 24px 16px;
      position: fixed;
      top: 0; left: 0; bottom: 0;
      overflow-y: auto;
      z-index: 100;
    }}
    .sidebar h1 {{
      font-size: 16px;
      font-weight: 700;
      margin-bottom: 4px;
      line-height: 1.3;
    }}
    .sidebar .subtitle {{
      font-size: 12px;
      color: #94a3b8;
      margin-bottom: 28px;
    }}
    .nav-btn {{
      display: block;
      width: 100%;
      text-align: left;
      background: transparent;
      border: none;
      color: #cbd5e1;
      padding: 11px 14px;
      border-radius: 8px;
      font-size: 13.5px;
      font-weight: 500;
      cursor: pointer;
      margin-bottom: 4px;
      transition: all 0.15s;
    }}
    .nav-btn:hover {{
      background: #1e293b;
      color: white;
    }}
    .nav-btn.active {{
      background: #0ea5e9;
      color: white;
    }}
    .sidebar-footer {{
      position: absolute;
      bottom: 16px;
      left: 16px;
      right: 16px;
      font-size: 11px;
      color: #64748b;
      border-top: 1px solid #1e293b;
      padding-top: 12px;
    }}

    /* ===== CONTENU PRINCIPAL ===== */
    .main {{
      margin-left: 260px;
      flex: 1;
      padding: 28px 32px;
      max-width: 1100px;
    }}
    .page-title {{
      font-size: 22px;
      font-weight: 700;
      margin-bottom: 6px;
    }}
    .page-desc {{
      font-size: 14px;
      color: #64748b;
      margin-bottom: 24px;
    }}

    /* KPI */
    .kpi {{
      display: flex;
      gap: 12px;
      flex-wrap: wrap;
      margin-bottom: 28px;
    }}
    .kpi > div {{
      flex: 1;
      min-width: 150px;
      padding: 16px 18px;
      border-radius: 12px;
      color: white;
    }}
    .kpi .label {{ font-size: 12px; opacity: 0.9; }}
    .kpi .value {{ font-size: 24px; font-weight: 700; margin-top: 2px; }}

    /* Sections */
    .section {{
      display: none;
      background: white;
      border-radius: 12px;
      padding: 20px;
      margin-bottom: 20px;
      box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }}
    .section.active {{ display: block; }}
    .section h2 {{
      font-size: 17px;
      margin-bottom: 14px;
      padding-bottom: 8px;
      border-bottom: 2px solid #e2e8f0;
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 13.5px;
      margin-top: 12px;
    }}
    th, td {{
      padding: 9px 12px;
      text-align: left;
      border-bottom: 1px solid #e2e8f0;
    }}
    th {{ background: #f8fafc; font-weight: 600; }}
    .reco ol {{
      padding-left: 20px;
      line-height: 1.75;
      font-size: 14px;
    }}
    .note {{
      font-size: 12.5px;
      color: #64748b;
      margin-top: 10px;
    }}
  </style>
</head>
<body>

  <!-- ========== SIDEBAR ========== -->
  <aside class="sidebar">
    <h1>Togo Digital Inclusion</h1>
    <p class="subtitle">Défi 02 · Économie Numérique<br>Togo AI Lab</p>

    <button class="nav-btn active" onclick="showSection('overview')">Vue d'ensemble</button>
    <button class="nav-btn" onclick="showSection('internet')">Usage Internet</button>
    <button class="nav-btn" onclick="showSection('telecom')">Marché Télécoms</button>
    <button class="nav-btn" onclick="showSection('map')">Carte des accès</button>
    <button class="nav-btn" onclick="showSection('access')">Points d'accès</button>
    <button class="nav-btn" onclick="showSection('ratios')">Ratios d'accès</button>
    <button class="nav-btn" onclick="showSection('reco')">Recommandations</button>

    <div class="sidebar-footer">
      Sources : World Bank · ARCEP · RGPH-5<br>
      Agents MM · Établissements financiers
    </div>
  </aside>

  <!-- ========== CONTENU ========== -->
  <main class="main">

    <!-- VUE D'ENSEMBLE -->
    <div id="overview" class="section active">
      <p class="page-title">Vue d'ensemble</p>
      <p class="page-desc">Adoption numérique et inclusion financière au Togo</p>

      <div class="kpi">
        <div style="background:#0ea5e9">
          <div class="label">Pénétration Internet</div>
          <div class="value">{latest_pen:.1f}%</div>
        </div>
        <div style="background:#10b981">
          <div class="label">Agents Mobile Money</div>
          <div class="value">{n_agents:,}</div>
        </div>
        <div style="background:#f97316">
          <div class="label">Établissements financiers</div>
          <div class="value">{n_etab:,}</div>
        </div>
        <div style="background:#8b5cf6">
          <div class="label">Population 2022</div>
          <div class="value">{total_pop:,}</div>
        </div>
      </div>

      <h2 style="font-size:16px; margin-bottom:10px;">Évolution rapide de l'Internet</h2>
      {divs["internet"]}
    </div>

    <!-- INTERNET -->
    <div id="internet" class="section">
      <h2>1. Évolution de l'usage d'Internet</h2>
      {divs["internet"]}
      <p class="note">
        Accélération nette à partir de 2016 (déploiement 3G/4G), 
        puis bond important en 2020 (période COVID).
      </p>
    </div>

    <!-- TELECOMS -->
    <div id="telecom" class="section">
      <h2>2. Marché des télécommunications (2013-2019)</h2>
      {divs["telecom_sub"]}
      {divs["market"]}
      {divs["revenue"]}
    </div>

    <!-- CARTE -->
    <div id="map" class="section">
      <h2>3. Carte des points d'accès</h2>
      {divs["map"]}
      <p class="note">
        Bleu = Agents Mobile Money (échantillon) · 
        Orange = Établissements financiers (banques, microfinance, assurances…).
        Concentration visible autour de Lomé et des chefs-lieux.
      </p>
    </div>

    <!-- POINTS D'ACCES -->
    <div id="access" class="section">
      <h2>4. Répartition des points d'accès par région</h2>
      {divs["agents_reg"]}
      {divs["etab_reg"]}
    </div>

    <!-- RATIOS -->
    <div id="ratios" class="section">
      <h2>5. Ratios d'accès (Population / Points de service)</h2>
      {divs["ratios"]}
      <h3 style="margin-top:18px; font-size:15px;">Tableau récapitulatif</h3>
      {ratios_html}
      <p class="note">
        Plus le ratio « Habitants / Agent » est élevé, plus la région est sous-équipée.
        Plateaux et Savanes sont prioritaires.
      </p>
    </div>

    <!-- RECOMMANDATIONS -->
    <div id="reco" class="section">
      <h2>6. Recommandations stratégiques</h2>
      <div class="reco">
        <ol>
          <li>
            <strong>Prioriser Plateaux et Savanes</strong> — 
            ratios habitants/agent les plus élevés (531 et 427). 
            Accélérer le déploiement d'agents et de la 4G.
          </li>
          <li>
            <strong>Renforcer les établissements hors Maritime</strong> — 
            Maritime concentre plus de 56 % des points bancaires/microfinance.
          </li>
          <li>
            <strong>Capitaliser sur le réseau Mobile Money</strong> — 
            ~20 000 agents déjà présents. Favoriser l'interopérabilité Yas–Moov 
            et l'éducation financière en langues locales.
          </li>
          <li>
            <strong>Accélérer le haut débit rural</strong> — 
            après le ralentissement post-2018, relancer fibre et 4G hors des grandes villes.
          </li>
          <li>
            <strong>Maintenir l'open data territoriale</strong> — 
            publier régulièrement les localisations pour un suivi dynamique.
          </li>
        </ol>
      </div>
    </div>

  </main>

  <script>
    function showSection(id) {{
      // Masquer toutes les sections
      document.querySelectorAll('.section').forEach(s => s.classList.remove('active'));
      // Afficher la section demandée
      document.getElementById(id).classList.add('active');
      // Mettre à jour le bouton actif
      document.querySelectorAll('.nav-btn').forEach(b => b.classList.remove('active'));
      event.target.classList.add('active');
    }}
  </script>

</body>
</html>
"""

    out_path = OUTPUT_DIR / "dashboard_togo_digital.html"
    out_path.write_text(html, encoding="utf-8")
    print(f"\n✅ Dashboard avec sidebar généré !")
    print(f"   → {out_path}")
    print("   Ouvre ce fichier dans ton navigateur.")


if __name__ == "__main__":
    main()