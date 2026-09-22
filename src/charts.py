"""
Graphiques Plotly pour le dashboard
Défi 02 - Togo AI Lab
"""

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots


def chart_internet_evolution(internet_df):
    """
    Courbe de l'évolution de l'usage d'Internet (% de la population).
    """
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=internet_df["year"],
        y=internet_df["penetration"],
        mode="lines+markers",
        name="% population",
        line=dict(color="#0ea5e9", width=3),
        marker=dict(size=6)
    ))

    # Lignes verticales pour marquer les périodes importantes
    fig.add_vline(
        x=2016, line_dash="dash", line_color="#94a3b8",
        annotation_text="Accélération", annotation_position="top"
    )
    fig.add_vline(
        x=2020, line_dash="dash", line_color="#f59e0b",
        annotation_text="COVID", annotation_position="top"
    )

    fig.update_layout(
        title="Évolution de l'usage d'Internet au Togo (% de la population)",
        xaxis_title="Année",
        yaxis_title="% de la population",
        template="plotly_white",
        height=450,
        hovermode="x unified"
    )
    return fig


def chart_telecom_subscribers(telecom_dict):
    """
    Évolution du nombre d'abonnés mobile et fixe (2013-2019).
    """
    mobile = telecom_dict.get("Le nombre total d'abonnées mobiles GSM")
    fixed = telecom_dict.get("Le nombre total d'abonnés fixe")

    fig = go.Figure()

    if mobile is not None:
        fig.add_trace(go.Scatter(
            x=mobile["year"],
            y=mobile["value"],
            name="Mobile GSM",
            line=dict(color="#0ea5e9", width=2.5)
        ))

    if fixed is not None:
        fig.add_trace(go.Scatter(
            x=fixed["year"],
            y=fixed["value"],
            name="Fixe",
            line=dict(color="#f97316", width=2.5)
        ))

    fig.update_layout(
        title="Évolution des abonnés télécoms (2013-2019)",
        xaxis_title="Année",
        yaxis_title="Nombre d'abonnés",
        template="plotly_white",
        height=400
    )
    return fig


def chart_market_share(telecom_dict):
    """
    Parts de marché mobile : Togo Cellulaire vs Moov (2013-2019).
    """
    tc = telecom_dict.get("Part de marché Togo Cellulaire (en abonnées) en %")
    moov = telecom_dict.get("Part de marché Atlantique Telecom Togo (en abonnées)")

    fig = go.Figure()

    if tc is not None:
        fig.add_trace(go.Bar(
            x=tc["year"],
            y=tc["value"],
            name="Togo Cellulaire / Yas",
            marker_color="#0ea5e9"
        ))

    if moov is not None:
        fig.add_trace(go.Bar(
            x=moov["year"],
            y=moov["value"],
            name="Moov Africa",
            marker_color="#f97316"
        ))

    fig.update_layout(
        title="Parts de marché mobile (abonnés) 2013-2019",
        barmode="group",
        xaxis_title="Année",
        yaxis_title="Part de marché (%)",
        template="plotly_white",
        height=400
    )
    return fig


def chart_revenue_investment(telecom_dict):
    """
    Chiffre d'affaires et investissements du secteur (2013-2019).
    """
    rev = telecom_dict.get("Chiffres d'Affaires")
    inv = telecom_dict.get("Investissement")

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    if rev is not None:
        fig.add_trace(
            go.Bar(
                x=rev["year"],
                y=rev["value"] / 1e9,  # conversion en milliards
                name="Chiffre d'affaires (Mds FCFA)",
                marker_color="#0ea5e9"
            ),
            secondary_y=False
        )

    if inv is not None:
        fig.add_trace(
            go.Scatter(
                x=inv["year"],
                y=inv["value"] / 1e9,
                name="Investissements (Mds FCFA)",
                mode="lines+markers",
                line=dict(color="#10b981", width=3)
            ),
            secondary_y=True
        )

    fig.update_layout(
        title="Chiffre d'affaires et Investissements (2013-2019)",
        template="plotly_white",
        height=400
    )
    fig.update_yaxes(title_text="CA (Mds FCFA)", secondary_y=False)
    fig.update_yaxes(title_text="Investissements (Mds FCFA)", secondary_y=True)

    return fig


def chart_agents_by_region(agents_reg):
    """
    Nombre d'agents Mobile Money par région.
    """
    fig = px.bar(
        agents_reg,
        x="region",
        y="n_agents",
        text="n_agents",
        color="n_agents",
        color_continuous_scale="Blues",
        title="Nombre d'agents Mobile Money par région"
    )
    fig.update_traces(texttemplate="%{text:,}", textposition="outside")
    fig.update_layout(template="plotly_white", height=400, showlegend=False)
    return fig


def chart_etab_by_region(etab_reg):
    """
    Nombre d'établissements financiers par région.
    """
    fig = px.bar(
        etab_reg,
        x="region",
        y="n_etab",
        text="n_etab",
        color="n_etab",
        color_continuous_scale="Oranges",
        title="Nombre d'établissements financiers par région"
    )
    fig.update_traces(texttemplate="%{text:,}", textposition="outside")
    fig.update_layout(template="plotly_white", height=400, showlegend=False)
    return fig


def chart_access_ratios(ratios):
    """
    Ratios d'accès : habitants/agent et agents/établissement.
    """
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=(
            "Habitants par agent Mobile Money",
            "Agents MM par établissement financier"
        )
    )

    fig.add_trace(
        go.Bar(
            x=ratios["region_norm"],
            y=ratios["hab_per_agent"],
            marker_color="#0ea5e9",
            text=ratios["hab_per_agent"],
            name="Hab/Agent"
        ),
        row=1, col=1
    )

    fig.add_trace(
        go.Bar(
            x=ratios["region_norm"],
            y=ratios["agents_per_etab"],
            marker_color="#f97316",
            text=ratios["agents_per_etab"],
            name="Agents/Etab"
        ),
        row=1, col=2
    )

    fig.update_traces(textposition="outside")
    fig.update_layout(
        title_text="Ratios d'accès aux services financiers numériques",
        template="plotly_white",
        height=450,
        showlegend=False
    )
    return fig