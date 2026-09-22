"""
Agrégations et calculs de ratios
Défi 02 - Togo AI Lab
"""

import pandas as pd
import numpy as np


def agents_by_region(agents: pd.DataFrame) -> pd.DataFrame:
    """
    Compte le nombre d'agents Mobile Money par région.
    """
    df = (
        agents
        .groupby("region_nom_bdd")
        .size()
        .reset_index(name="n_agents")
        .rename(columns={"region_nom_bdd": "region"})
        .sort_values("n_agents", ascending=False)
    )
    return df


def etab_by_region(etab: pd.DataFrame) -> pd.DataFrame:
    """
    Compte le nombre d'établissements financiers par région.
    """
    df = (
        etab
        .groupby("region_nom_bdd")
        .size()
        .reset_index(name="n_etab")
        .rename(columns={"region_nom_bdd": "region"})
        .sort_values("n_etab", ascending=False)
    )
    return df


def region_population(pop: pd.DataFrame) -> pd.DataFrame:
    """
    Extrait la population des grandes régions + total national.
    """
    regions = ["TOGO", "SAVANES", "KARA", "CENTRALE", "PLATEAUX", "MARITIME"]
    mask = pop["admin_unit"].str.upper().isin(regions)
    return pop[mask].copy()


def compute_ratios(
    agents_reg: pd.DataFrame,
    etab_reg: pd.DataFrame,
    pop_reg: pd.DataFrame
) -> pd.DataFrame:
    """
    Calcule les ratios d'accès :
    - habitants par agent Mobile Money
    - agents MM par établissement financier
    """
    # Copies pour ne pas modifier les originaux
    agents_reg = agents_reg.copy()
    etab_reg = etab_reg.copy()
    pop_reg = pop_reg.copy()

    # Normalisation des noms de région (majuscules)
    agents_reg["region_norm"] = agents_reg["region"].str.upper().str.strip()
    etab_reg["region_norm"] = etab_reg["region"].str.upper().str.strip()
    pop_reg["region_norm"] = pop_reg["admin_unit"].str.upper().str.strip()

    # Jointure des trois tables
    merged = agents_reg.merge(etab_reg, on="region_norm", how="outer")
    merged = merged.merge(
        pop_reg[["region_norm", "population"]],
        on="region_norm",
        how="left"
    )

    # Remplir les valeurs manquantes
    merged["n_agents"] = merged["n_agents"].fillna(0).astype(int)
    merged["n_etab"] = merged["n_etab"].fillna(0).astype(int)
    merged["population"] = merged["population"].fillna(0).astype(int)

    # Calcul des ratios
    merged["hab_per_agent"] = np.where(
        merged["n_agents"] > 0,
        (merged["population"] / merged["n_agents"]).round(0),
        np.nan
    )

    merged["agents_per_etab"] = np.where(
        merged["n_etab"] > 0,
        (merged["n_agents"] / merged["n_etab"]).round(1),
        np.nan
    )

    # Colonnes finales
    return merged[[
        "region_norm",
        "population",
        "n_agents",
        "n_etab",
        "hab_per_agent",
        "agents_per_etab"
    ]].sort_values("hab_per_agent", ascending=False)