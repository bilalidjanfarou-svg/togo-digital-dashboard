"""
Carte des agents Mobile Money et établissements financiers
Version sans tuiles externes (Scattergeo) — fiable partout
"""

import plotly.graph_objects as go
import pandas as pd


def chart_map(agents: pd.DataFrame, etab: pd.DataFrame, sample_agents: int = 2500):
    """
    Carte géographique simple :
    - Agents MM en bleu (échantillon)
    - Établissements financiers en orange
    Pas de dépendance à OpenStreetMap / Carto.
    """
    if len(agents) > sample_agents:
        agents_sample = agents.sample(n=sample_agents, random_state=42)
    else:
        agents_sample = agents

    fig = go.Figure()

    # --- Agents Mobile Money ---
    fig.add_trace(go.Scattergeo(
        lat=agents_sample["lat"],
        lon=agents_sample["lon"],
        mode="markers",
        marker=dict(size=4, color="#0ea5e9", opacity=0.55, line=dict(width=0)),
        name=f"Agents MM ({len(agents_sample):,})",
        hovertemplate=(
            "<b>Agent Mobile Money</b><br>"
            "Région : %{customdata[0]}<br>"
            "Opérateur : %{customdata[1]}<extra></extra>"
        ),
        customdata=agents_sample[["region_nom_bdd", "operateur"]].values,
    ))

    # --- Établissements financiers ---
    fig.add_trace(go.Scattergeo(
        lat=etab["lat"],
        lon=etab["lon"],
        mode="markers",
        marker=dict(size=7, color="#f97316", opacity=0.9, line=dict(width=0.5, color="white")),
        name=f"Établissements ({len(etab):,})",
        hovertemplate=(
            "<b>%{customdata[0]}</b><br>"
            "Catégorie : %{customdata[1]}<br>"
            "Région : %{customdata[2]}<extra></extra>"
        ),
        customdata=etab[["etab_nom", "activite_categorie", "region_nom_bdd"]].values,
    ))

    fig.update_layout(
        title="Carte des points d'accès (Agents MM + Établissements financiers)",
        geo=dict(
            scope="africa",
            resolution=50,
            showland=True,
            landcolor="#f1f5f9",
            showocean=True,
            oceancolor="#e0f2fe",
            showcountries=True,
            countrycolor="#94a3b8",
            showframe=False,
            # Zoom sur le Togo
            lataxis=dict(range=[5.8, 11.3]),
            lonaxis=dict(range=[-0.3, 2.0]),
            projection_type="mercator",
        ),
        height=560,
        margin=dict(l=0, r=0, t=50, b=0),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=0.02,
            x=0.02,
            bgcolor="rgba(255,255,255,0.8)",
        ),
    )
    return fig