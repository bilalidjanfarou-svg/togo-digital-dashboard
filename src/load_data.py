"""
Chargement des données du Défi 02
"""

import pandas as pd
import re
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"


def load_internet_usage():
    """% de la population utilisant Internet (1996-2022)"""
    df = pd.read_csv(DATA_DIR / "individus-utilisant-internet-de-la-population-.csv")
    df = df[["date", "value"]].dropna(subset=["value"])
    df["year"] = df["date"].astype(int)
    df["penetration"] = pd.to_numeric(df["value"], errors="coerce")
    df = df.dropna(subset=["penetration"]).sort_values("year")
    return df[["year", "penetration"]]


def load_telecom():
    """Indicateurs télécoms 2013-2019 (abonnés, CA, parts de marché...)"""
    df = pd.read_csv(DATA_DIR / "observationdata-mesqyx.csv")
    df["Value"] = pd.to_numeric(df["Value"], errors="coerce")
    
    result = {}
    for name in df["indicateur"].unique():
        sub = df[df["indicateur"] == name][["Date", "Value"]].copy()
        sub["year"] = sub["Date"].astype(int)
        result[name] = sub[["year", "Value"]].rename(columns={"Value": "value"})
    return result


def load_internet_subscribers():
    """Abonnés Internet par technologie 2013-2019"""
    df = pd.read_csv(DATA_DIR / "observationdata-cxnvmoc.csv")
    df["Value"] = pd.to_numeric(df["Value"], errors="coerce")
    
    result = {}
    for name in df["indicateur"].unique():
        sub = df[df["indicateur"] == name][["Date", "Value"]].copy()
        sub["year"] = sub["Date"].astype(int)
        result[name] = sub[["year", "Value"]].rename(columns={"Value": "value"})
    return result


def load_population():
    """Population par découpage administratif (RGPH-5 2022)"""
    df = pd.read_csv(DATA_DIR / "observationdata-kwwolwb.csv")
    df = df[df["sexe"] == "Total"].copy()
    df["population"] = pd.to_numeric(df["Value"], errors="coerce")
    df = df.rename(columns={"découpage-administratif": "admin_unit"})
    return df[["admin_unit", "population"]].dropna()


def parse_point(geometry):
    """Extrait longitude et latitude depuis une géométrie POINT (lon lat)"""
    if pd.isna(geometry):
        return None, None
    match = re.search(r"POINT\s*\(\s*([-\d.]+)\s+([-\d.]+)\s*\)", str(geometry))
    if match:
        return float(match.group(1)), float(match.group(2))
    return None, None


def load_agents():
    """Agents Mobile Money géolocalisés"""
    df = pd.read_csv(DATA_DIR / "file-agents-mobile-money-19-12-2024-16-55-32.csv")
    coords = df["geometry"].apply(parse_point)
    df["lon"] = coords.apply(lambda x: x[0])
    df["lat"] = coords.apply(lambda x: x[1])
    df = df.dropna(subset=["lon", "lat"])
    df["operateur"] = df["operateur"].fillna("Nsp").str.strip()
    return df


def load_etablissements():
    """Établissements financiers géolocalisés"""
    df = pd.read_csv(DATA_DIR / "file-finance-etablissements-08-01-2025-17-49-30.csv")
    coords = df["geometry"].apply(parse_point)
    df["lon"] = coords.apply(lambda x: x[0])
    df["lat"] = coords.apply(lambda x: x[1])
    df = df.dropna(subset=["lon", "lat"])
    df["activite_categorie"] = df["activite_categorie"].fillna("Autre")
    return df