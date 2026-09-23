"""
Statistiques par région pour le filtre interactif
"""

import pandas as pd
import json


def build_region_stats(agents: pd.DataFrame, etab: pd.DataFrame, ratios: pd.DataFrame) -> dict:
    """
    Construit un dictionnaire de stats par région
    (utilisé par le filtre JavaScript du dashboard).
    """
    stats = {
        "TOUTES": {
            "n_agents": int(len(agents)),
            "n_etab": int(len(etab)),
            "population": int(ratios["population"].sum()) if len(ratios) else 0,
            "hab_per_agent": None,
            "agents_per_etab": None,
        }
    }

    # Stats globales TOUTES
    if stats["TOUTES"]["n_agents"] > 0 and stats["TOUTES"]["population"] > 0:
        stats["TOUTES"]["hab_per_agent"] = round(
            stats["TOUTES"]["population"] / stats["TOUTES"]["n_agents"]
        )
    if stats["TOUTES"]["n_etab"] > 0:
        stats["TOUTES"]["agents_per_etab"] = round(
            stats["TOUTES"]["n_agents"] / stats["TOUTES"]["n_etab"], 1
        )

    # Par région
    for _, row in ratios.iterrows():
        region = row["region_norm"]
        stats[region] = {
            "n_agents": int(row["n_agents"]),
            "n_etab": int(row["n_etab"]),
            "population": int(row["population"]),
            "hab_per_agent": float(row["hab_per_agent"]) if pd.notna(row["hab_per_agent"]) else None,
            "agents_per_etab": float(row["agents_per_etab"]) if pd.notna(row["agents_per_etab"]) else None,
        }

    return stats


def stats_to_json(stats: dict) -> str:
    """Convertit les stats en JSON pour injection dans le HTML."""
    return json.dumps(stats, ensure_ascii=False)