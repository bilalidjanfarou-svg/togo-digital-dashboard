# Togo Digital Inclusion Dashboard

**Défi 02 · Économie Numérique · Togo AI Lab**

Tableau de bord interactif mesurant l'adoption du numérique et le rôle du mobile money dans l'inclusion financière au Togo.

## Structure

togo_digital_dashboard/
├── data/           # Fichiers CSV sources
├── src/            # Code Python
├── output/         # Dashboard HTML généré
├── requirements.txt
└── README.md


## Installation

```bash
pip install -r requirements.txt
python -m src.generate_dashboard

Puis ouvrir output/dashboard_togo_digital.html dans un navigateur.
text### 4. Créer `requirements.txt`

```txt
pandas>=2.0
plotly>=5.0

# Togo Digital Inclusion Dashboard

**Défi 02 · Économie Numérique · Togo AI Lab**

## Lancement rapide

```bash
pip install -r requirements.txt
python -m src.generate_dashboard
Ouvrir ensuite : output/dashboard_togo_digital.html
Structure

src/load_data.py → chargement des CSV
src/process_data.py → agrégations et ratios
src/charts.py → graphiques Plotly
src/generate_dashboard.py → assemblage HTML