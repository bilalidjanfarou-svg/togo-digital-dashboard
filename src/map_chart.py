"""
Carte interactive des agents Mobile Money et établissements financiers
Compatible Plotly récent (Scattermap)
"""

import plotly.graph_objects as go
import pandas as pd


def chart_map(agents: pd.DataFrame, etab: pd.DataFrame, sample_agents: int = 2000):
    """
    Carte Plotly (OpenStreetMap) :
    - Agents MM en bleu (échantillon pour la performance)
    - Établissements financiers en orange
    """
    # Échantillon aléatoire des agents (évite de surcharger le navigateur)
    if len(agents) > sample_agents:
        agents_sample = agents.sample(n=sample_agents, random_state=42)
    else:
        agents_sample = agents

    fig = go.Figure()

    # --- Agents Mobile Money ---
    fig.add_trace(go.Scattermap(
        lat=agents_sample["lat"],
        lon=agents_sample["lon"],
        mode="markers",
        marker=dict(size=5, color="#0ea5e9", opacity=0.6),
        name=f"Agents MM (échantillon {len(agents_sample):,})",
        hovertemplate=(
            "<b>Agent Mobile Money</b><br>"
            "Région : %{customdata[0]}<br>"
            "Opérateur : %{customdata[1]}<extra></extra>"
        ),
        customdata=agents_sample[["region_nom_bdd", "operateur"]].values,
    ))

    # --- Établissements financiers ---
    fig.add_trace(go.Scattermap(
        lat=etab["lat"],
        lon=etab["lon"],
        mode="markers",
        marker=dict(size=8, color="#f97316", opacity=0.85),
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
        map=dict(
            style="open-street-map",
            center=dict(lat=8.5, lon=1.2),  # centre approximatif du Togo
            zoom=6,
        ),
        height=550,
        margin=dict(l=0, r=0, t=40, b=0),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=0.01,
            x=0.01,
        ),
    )
    return fig