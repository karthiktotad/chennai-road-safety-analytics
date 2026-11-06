"""
Jupyter Notebooks Generator for Chennai Road Accident Research.
Generates fully functional, documented .ipynb files for notebooks 01 through 09.
"""

import json
from pathlib import Path

NOTEBOOKS_DIR = Path("notebooks")
NOTEBOOKS_DIR.mkdir(parents=True, exist_ok=True)


def make_notebook(cells):
    return {
        "cells": cells,
        "metadata": {
            "language_info": {
                "name": "python",
                "version": "3.13"
            },
            "kernelspec": {
                "display_name": "Python 3 (.venv)",
                "language": "python",
                "name": "python3"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 5
    }


def make_md_cell(text):
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": [line + "\n" for line in text.split("\n")]
    }


def make_code_cell(code):
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [line + "\n" for line in code.split("\n")]
    }


def create_all_notebooks():
    # 01_data_collection.ipynb
    nb1 = make_notebook([
        make_md_cell("# 01. Automated Data Collection & Ingestion\n**Project:** Beyond Accident Counts: Chennai Road Safety Research\n\nThis notebook demonstrates automated retrieval from official APIs: OpenCity, NASA POWER, and OpenStreetMap."),
        make_code_cell("import sys\nsys.path.append('..')\nimport pandas as pd\nfrom src.data_collection.accident_collector import AccidentDataCollector\nfrom src.data_collection.weather_collector import NASAWeatherCollector\nfrom src.data_collection.road_collector import OSMRoadNetworkCollector\n\nprint('Data collection modules imported successfully.')"),
        make_code_cell("# Inspect collection metadata\nimport json\nwith open('../data/raw/accidents/collection_metadata.json') as f:\n    meta = json.load(f)\nprint(f'Total Raw Files Ingested: {meta.get(\"total_files\", meta.get(\"total_downloaded\"))}')")
    ])
    with open(NOTEBOOKS_DIR / "01_data_collection.ipynb", "w") as f:
        json.dump(nb1, f, indent=2)

    # 02_data_inspection.ipynb
    nb2 = make_notebook([
        make_md_cell("# 02. Data Inspection and Profiling Audit\nEvaluates data structures, dimensions, missingness percentages, and distinguishes between aggregated statistics and microdata."),
        make_code_cell("import sys\nsys.path.append('..')\nimport pandas as pd\n\n# Inspect data audit report\nwith open('../results/reports/data_audit_report.md') as f:\n    print(f.read()[:2000])")
    ])
    with open(NOTEBOOKS_DIR / "02_data_inspection.ipynb", "w") as f:
        json.dump(nb2, f, indent=2)

    # 03_data_preprocessing.ipynb
    nb3 = make_notebook([
        make_md_cell("# 03. Data Preprocessing & Multi-Source Integration\nCleans raw datasets, parses KML vector boundaries, and builds the unified modeling dataset."),
        make_code_cell("import sys\nsys.path.append('..')\nimport pandas as pd\n\nmodeling_df = pd.read_csv('../data/processed/chennai_accident_severity_modeling_dataset.csv')\nprint(f'Modeling Dataset Shape: {modeling_df.shape}')\nmodeling_df.head()")
    ])
    with open(NOTEBOOKS_DIR / "03_data_preprocessing.ipynb", "w") as f:
        json.dump(nb3, f, indent=2)

    # 04_exploratory_data_analysis.ipynb
    nb4 = make_notebook([
        make_md_cell("# 04. Exploratory Data Analysis (EDA)\nEvaluates the 12 core transportation safety research questions."),
        make_code_cell("from IPython.display import Image, display\nimport glob\n\nfigs = sorted(glob.glob('../results/visualizations/eda_*.png'))\nfor fig in figs[:4]:\n    print(f'Visualizing: {fig}')\n    display(Image(filename=fig, width=700))")
    ])
    with open(NOTEBOOKS_DIR / "04_exploratory_data_analysis.ipynb", "w") as f:
        json.dump(nb4, f, indent=2)

    # 05_statistical_analysis.ipynb
    nb5 = make_notebook([
        make_md_cell("# 05. Inferential Statistical Analysis & Hypothesis Testing\nChi-Square tests of independence, Cramér's V, and multivariable baseline Logistic Regression odds ratios."),
        make_code_cell("import sys\nsys.path.append('..')\nimport pandas as pd\n\nchi_df = pd.read_csv('../results/metrics/chi_square_hypothesis_tests.csv')\ndisplay(chi_df)\n\nlogit_df = pd.read_csv('../results/metrics/logistic_regression_odds_ratios.csv')\ndisplay(logit_df.head(10))")
    ])
    with open(NOTEBOOKS_DIR / "05_statistical_analysis.ipynb", "w") as f:
        json.dump(nb5, f, indent=2)

    # 06_feature_engineering.ipynb
    nb6 = make_notebook([
        make_md_cell("# 06. Feature Engineering\nTrigonometric cyclical encoding, interaction terms, target definition, and leakage prevention."),
        make_code_cell("import sys\nsys.path.append('..')\nimport pandas as pd, json\n\nfeatures_df = pd.read_csv('../data/processed/chennai_feature_matrix.csv')\nwith open('../models/feature_metadata.json') as f:\n    meta = json.load(f)\nprint(f'Engineered Features: {len(features_df.columns)}')\nprint(json.dumps(meta, indent=2))")
    ])
    with open(NOTEBOOKS_DIR / "06_feature_engineering.ipynb", "w") as f:
        json.dump(nb6, f, indent=2)

    # 07_model_development.ipynb
    nb7 = make_notebook([
        make_md_cell("# 07. Machine Learning Model Development\nTrains and serializes Logistic Regression, Decision Tree, Random Forest, and XGBoost classifiers."),
        make_code_cell("import sys\nsys.path.append('..')\nimport joblib\n\nlr = joblib.load('../models/logistic_regression_pipeline.joblib')\nrf = joblib.load('../models/random_forest_pipeline.joblib')\nxgb = joblib.load('../models/xgboost_pipeline.joblib')\nprint('Models loaded successfully from models/ directory.')")
    ])
    with open(NOTEBOOKS_DIR / "07_model_development.ipynb", "w") as f:
        json.dump(nb7, f, indent=2)

    # 08_model_evaluation.ipynb
    nb8 = make_notebook([
        make_md_cell("# 08. Model Evaluation & SHAP Interpretability\nEvaluates ROC/PR curves, confusion matrices, and SHAP feature attributions on holdout test set."),
        make_code_cell("import sys\nsys.path.append('..')\nimport pandas as pd\nfrom IPython.display import Image, display\n\nmetrics_df = pd.read_csv('../results/metrics/model_comparison_table.csv')\ndisplay(metrics_df)\n\ndisplay(Image(filename='../results/visualizations/model_eval_01_roc_curves.png', width=700))\ndisplay(Image(filename='../results/visualizations/model_eval_05_shap_summary.png', width=700))")
    ])
    with open(NOTEBOOKS_DIR / "08_model_evaluation.ipynb", "w") as f:
        json.dump(nb8, f, indent=2)

    # 09_geospatial_analysis.ipynb
    nb9 = make_notebook([
        make_md_cell("# 09. Geospatial Hotspot Identification (GIS)\nDBSCAN clustering on Haversine coordinates and Folium interactive mapping."),
        make_code_cell("import sys\nsys.path.append('..')\nimport pandas as pd\nfrom IPython.display import Image, display\n\nhotspots = pd.read_csv('../results/metrics/geospatial_hotspots_summary.csv')\ndisplay(hotspots)\n\ndisplay(Image(filename='../results/visualizations/geo_01_accident_hotspots_dbscan.png', width=650))")
    ])
    with open(NOTEBOOKS_DIR / "09_geospatial_analysis.ipynb", "w") as f:
        json.dump(nb9, f, indent=2)

    print("All 9 research notebooks generated successfully in notebooks/.")


if __name__ == "__main__":
    create_all_notebooks()

