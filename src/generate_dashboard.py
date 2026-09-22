"""
Génération du dashboard HTML final
Défi 02 - Togo AI Lab - Économie Numérique
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

    # KPI
    total_pop = int(pop[pop["admin_unit"] == "TOGO"]["population"].values[0])
    latest_pen = float(internet.iloc[-1]["penetration"])
    n_agents = len(agents)
    n_etab = len(etab)

    print("3. Création des graphiques...")
    figs = [
        chart_internet_evolution(internet),
        chart_telecom_subscribers(telecom),
        chart_market_share(telecom),
        chart_revenue_investment(telecom),
        chart_agents_by_region(a_reg),
        chart_etab_by_region(e_reg),
        chart_access_ratios(ratios),
    ]

    print("4. Assemblage du HTML...")

    # Conversion des graphiques en HTML
    # Le premier charge la librairie Plotly (CDN), les suivants non
    divs = []
    for i, fig in enumerate(figs):
        divs.append(
            fig.to_html(
                full_html=False,
                include_plotlyjs="cdn" if i == 0 else False
            )
        )

    # Tableau des ratios
    ratios_html = ratios.to_html(
        index=False,
        float_format="%.1f",
        border=0,
        classes="table"
    )

    html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Togo Digital Inclusion Dashboard | Défi 02</title>
  <style>
    * {{ box-sizing: border-box; }}
    body {{
      font-family: system-ui, -apple-system, 'Segoe UI', sans-serif;
      margin: 0;
      background: #f1f5f9;
      color: #0f172a;
      line-height: 1.5;
    }}
    .header {{
      background: linear-gradient(135deg, #0f172a 0%, #1e3a5f 100%);
      color: white;
      padding: 28px 40px;
    }}
    .header h1 {{
      margin: 0 0 6px 0;
      font-size: 24px;
      font-weight: 700;
    }}
    .header p {{
      margin: 0;
      opacity: 0.85;
      font-size: 14px;
    }}
    .container {{
      max-width: 1100px;
      margin: 0 auto;
      padding: 24px 16px;
    }}
    .kpi {{
      display: flex;
      gap: 12px;
      flex-wrap: wrap;
      margin-bottom: 24px;
    }}
    .kpi > div {{
      flex: 1;
      min-width: 160px;
      padding: 18px;
      border-radius: 12px;
      color: white;
    }}
    .kpi .label {{
      font-size: 12px;
      opacity: 0.9;
      margin-bottom: 4px;
    }}
    .kpi .value {{
      font-size: 26px;
      font-weight: 700;
    }}
    .section {{
      background: white;
      border-radius: 12px;
      padding: 20px;
      margin-bottom: 20px;
      box-shadow: 0 1px 3px rgba(0,0,0,0.06);
    }}
    .section h2 {{
      margin: 0 0 12px 0;
      font-size: 17px;
      color: #1e293b;
      border-bottom: 2px solid #e2e8f0;
      padding-bottom: 8px;
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 14px;
      margin-top: 12px;
    }}
    th, td {{
      padding: 10px 12px;
      text-align: left;
      border-bottom: 1px solid #e2e8f0;
    }}
    th {{
      background: #f8fafc;
      font-weight: 600;
    }}
    .reco {{
      background: #f8fafc;
      border-radius: 12px;
      padding: 20px;
      margin-top: 8px;
    }}
    .reco ol {{
      margin: 0;
      padding-left: 20px;
      line-height: 1.7;
    }}
    .footer {{
      text-align: center;
      padding: 24px;
      font-size: 12px;
      color: #64748b;
    }}
  </style>
</head>
<body>
  <div class="header">
    <h1>Tableau de bord — Adoption numérique & Inclusion financière</h1>
    <p>Togo · Défi 02 Économie Numérique · Togo AI Lab</p>
  </div>

  <div class="container">

    <!-- KPI -->
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

    <!-- 1. Internet -->
    <div class="section">
      <h2>1. Évolution de l'usage d'Internet</h2>
      {divs[0]}
    </div>

    <!-- 2. Télécoms -->
    <div class="section">
      <h2>2. Marché des télécommunications</h2>
      {divs[1]}
      {divs[2]}
      {divs[3]}
    </div>

    <!-- 3. Points d'accès -->
    <div class="section">
      <h2>3. Cartographie des points d'accès</h2>
      {divs[4]}
      {divs[5]}
    </div>

    <!-- 4. Ratios -->
    <div class="section">
      <h2>4. Ratios d'accès (Population / Points de service)</h2>
      {divs[6]}
      <h3 style="margin-top:20px; font-size:15px;">Tableau récapitulatif</h3>
      {ratios_html}
      <p style="font-size:13px; color:#64748b; margin-top:12px;">
        Note : La région Maritime inclut le Grand Lomé. 
        Plus le ratio « Habitants / Agent » est élevé, plus la région est sous-équipée.
      </p>
    </div>

    <!-- 5. Recommandations -->
    <div class="section">
      <h2>5. Recommandations stratégiques</h2>
      <div class="reco">
        <ol>
          <li>
            <strong>Prioriser les régions Plateaux et Savanes</strong> — 
            elles présentent les ratios habitants/agent les plus élevés 
            (531 et 427). Accélérer le déploiement d'agents et de la 4G.
          </li>
          <li>
            <strong>Renforcer les établissements financiers hors Maritime</strong> — 
            Maritime concentre plus de 56 % des points bancaires et de microfinance. 
            Soutenir l'ouverture d'agences dans les préfectures sous-dotées.
          </li>
          <li>
            <strong>Capitaliser sur le réseau Mobile Money</strong> — 
            avec près de 20 000 agents, le maillage est déjà dense. 
            Favoriser l'interopérabilité Yas–Moov et l'éducation financière 
            en langues locales.
          </li>
          <li>
            <strong>Accélérer le haut débit en zone rurale</strong> — 
            après le pic de 2018, la progression a ralenti. 
            Relancer les investissements fibre et 4G/5G hors des grandes villes.
          </li>
          <li>
            <strong>Maintenir l'open data territoriale</strong> — 
            publier régulièrement les localisations des agents et établissements 
            pour permettre un suivi dynamique et des analyses actualisées.
          </li>
        </ol>
      </div>
    </div>

  </div>

  <div class="footer">
    Défi 02 · Togo AI Lab · Python + Plotly · 
    Sources : World Bank, ARCEP Togo, RGPH-5, données géolocalisées agents & établissements
  </div>
</body>
</html>
"""

    out_path = OUTPUT_DIR / "dashboard_togo_digital.html"
    out_path.write_text(html, encoding="utf-8")

    print(f"\n✅ Dashboard généré avec succès !")
    print(f"   → {out_path}")
    print("   Ouvre ce fichier dans ton navigateur.")


if __name__ == "__main__":
    main()