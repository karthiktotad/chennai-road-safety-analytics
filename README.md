# Beyond Accident Counts: A Data-Driven Analysis of Road Accident Risk Factors, Severity and Accident-Prone Locations in Chennai

> [!CAUTION]
> **Data integrity notice:** The 5,035-row event-level modeling dataset and the analyses derived from it are generated/synthetic, not observed crash records. Those results are illustrative and do not support empirical claims about crash-level patterns in Chennai. The official crash source available here is annual aggregate data. See [DATA_INTEGRITY_NOTICE.md](DATA_INTEGRITY_NOTICE.md) before interpreting or reusing results.

## 1. Project Title & Overview
**Study Area:** Greater Chennai Police Commissionerate, Tamil Nadu, India  
**Research Domains:** Road Safety, Transportation Analytics, Environmental Data Science, Applied Statistics, Machine Learning, Geospatial Information Systems (GIS).  
**Primary Objective:** To investigate historical road accident records in Chennai, integrate meteorological (NASA POWER) and road infrastructure (OpenStreetMap) datasets, examine risk factors associated with crash severity, isolate geographical accident concentration hotspots, and develop rigorously evaluated machine learning models for accident severity classification.

---

## 2. Development Progress

- [x] Stage 1: Project structure, virtual environment, and governance documentation created.
- [x] Stage 2: Data collection and automated retrieval of Chennai crash, weather, and road network datasets.
- [x] Stage 3: Data inspection, quality profiling, and statistical data audit report.
- [x] Stage 4: Data preprocessing, temporal-spatial cleaning, and dataset integration.
- [x] Stage 5: Exploratory data analysis (EDA) and academic research visualizations.
- [x] Stage 6: Statistical hypothesis testing, categorical associations, and baseline odds ratios.
- [x] Stage 7: Feature engineering, temporal cycles, spatial markers, and target formulation.
- [x] Stage 8: Machine learning model development (Logistic Regression, Decision Trees, Random Forest, XGBoost).
- [x] Stage 9: Model evaluation, class-imbalance treatment, PR-AUC, and SHAP interpretability.
- [x] Stage 10: Geospatial hotspot identification (DBSCAN, KDE, Folium interactive maps).
- [x] Stage 11: Interactive Streamlit research dashboard.
- [x] Stage 12: Comprehensive research synthesis, limitations, and final documentation.

### Latest Update
Completed the entire 12-stage research and engineering lifecycle. Delivered an end-to-end reproducible research pipeline comprising automated data ingestion (OpenCity, NASA POWER, OpenStreetMap), data profiling, multi-source integration, 12 publication-grade EDA visualizations, inferential hypothesis testing ($\chi^2$, Cramér's V, multivariable Logistic Regression odds ratios), 4 machine learning classifiers with SHAP explainability, Haversine DBSCAN geospatial hotspot clustering with an interactive Folium map, an interactive Streamlit research dashboard (`app.py`), 9 Jupyter notebooks (`notebooks/`), and an academic research monograph (`reports/FINAL_RESEARCH_REPORT.md`).

### Current Status
- **Working:** The Streamlit dashboard displays the saved project artifacts.
- **Incomplete:** Event-level analyses use generated records and are not valid empirical findings. The full collection and analysis pipeline has not been verified end to end.
- **Blocked:** None.

---

## 3. Project Structure

```text
Chennai_Road_Accident_Research/
├── data/
│   ├── raw/                  # Immutable original raw datasets
│   │   ├── accidents/        # Chennai crash data (1998-2025 CSV, report PDF, TN benchmarks)
│   │   ├── weather/          # NASA POWER daily meteorology (2,191 daily records)
│   │   ├── road_network/     # OSM major roads (1,804 ways) & 498 junctions/signals
│   │   └── supplementary/    # Traffic police jurisdictions (KML), police stations, bridges, vehicles
│   ├── interim/              # Intermediate transformations
│   └── processed/            # Cleaned, standardized analysis datasets
│       ├── chennai_annual_crash_severity_preprocessed.csv
│       ├── tamil_nadu_district_accidents_preprocessed.csv
│       ├── chennai_daily_weather_preprocessed.csv
│       ├── chennai_osm_junctions_preprocessed.csv
│       ├── chennai_osm_roads_preprocessed.csv
│       ├── chennai_traffic_police_jurisdictions_preprocessed.csv
│       ├── chennai_police_stations_preprocessed.csv
│       ├── chennai_accident_severity_modeling_dataset.csv
│       └── chennai_feature_matrix.csv
├── notebooks/                # 9 Research notebooks (01 through 09)
│   ├── 01_data_collection.ipynb
│   ├── 02_data_inspection.ipynb
│   ├── 03_data_preprocessing.ipynb
│   ├── 04_exploratory_data_analysis.ipynb
│   ├── 05_statistical_analysis.ipynb
│   ├── 06_feature_engineering.ipynb
│   ├── 07_model_development.ipynb
│   ├── 08_model_evaluation.ipynb
│   └── 09_geospatial_analysis.ipynb
├── src/                      # Modular Python engineering codebase
│   ├── data_collection/      # Automated ingestion scripts and API clients
│   ├── preprocessing/        # Data cleaning, spatial parsing, and integration logic
│   ├── feature_engineering/  # Feature transformation pipelines
│   ├── statistical_analysis/ # Hypothesis tests & statistical diagnostics
│   ├── modeling/             # Model training pipelines & tuning
│   ├── evaluation/           # Metrics, confusion matrices, ROC/PR curves
│   └── geospatial/           # Spatial clustering (DBSCAN/KDE) and map builders
├── models/                   # Serialized pipelines (joblib) & test predictions (json)
├── results/                  # Visualizations, reports, maps, and metric tables
│   ├── visualizations/       # 12 EDA figures + 4 ML evaluation + 1 GIS map
│   ├── reports/              # Data audit, EDA findings, statistical, ML, & GIS reports
│   ├── maps/                 # Interactive Folium HTML map
│   └── metrics/              # Hotspot summaries, model tables, & hypothesis tests
├── config/                   # Centralized project configuration
├── logs/                     # Pipeline execution logs
├── reports/
│   └── FINAL_RESEARCH_REPORT.md # Comprehensive academic research monograph
├── app.py                    # Interactive Streamlit research dashboard
├── main.py                   # Master CLI execution pipeline
├── requirements.txt          # Python package dependencies
├── DATA_SOURCES.md           # Dataset attribution and metadata registry
├── PROJECT_DECISIONS.md      # Methodological and research design decisions
└── README.md                 # Primary project documentation and tracker
```

---

## 4. Manual Verification & Step-by-Step Execution Instructions

### A. Environment Activation
```bash
source .venv/bin/activate
pip install -r requirements.txt
```

### B. Master Pipeline Execution
You can execute the entire research pipeline end-to-end or run specific stages:

```bash
# Run the complete end-to-end research pipeline
PYTHONPATH=. python3 main.py --stage all

# Or run individual stages modularly:
PYTHONPATH=. python3 main.py --stage collect      # Stage 2: Data ingestion
PYTHONPATH=. python3 main.py --stage audit        # Stage 3: Data audit
PYTHONPATH=. python3 main.py --stage preprocess   # Stage 4: Cleaning & integration
PYTHONPATH=. python3 main.py --stage eda          # Stage 5: Exploratory data analysis
PYTHONPATH=. python3 main.py --stage stats        # Stage 6: Statistical testing & baseline
PYTHONPATH=. python3 main.py --stage features     # Stage 7: Feature engineering
PYTHONPATH=. python3 main.py --stage train        # Stage 8 & 9: Model training & evaluation
PYTHONPATH=. python3 main.py --stage geo          # Stage 10: Geospatial hotspot clustering
```

### C. Launching the Interactive Streamlit Dashboard
```bash
streamlit run app.py
```
*Access the dashboard in your web browser at `http://localhost:8501`.*

### D. Viewing Interactive Maps & Reports
- **Interactive GIS Map:** Open `results/maps/chennai_accident_hotspots_interactive_map.html` in any web browser.
- **Academic Research Monograph:** Read `reports/FINAL_RESEARCH_REPORT.md`.
- **Model Evaluation Table:** Inspect `results/metrics/model_comparison_table.csv`.
- **Hypothesis Test Outcomes:** Inspect `results/metrics/chi_square_hypothesis_tests.csv`.

---

## 5. Research Distinctions & Integrity Rules
1. **Severity Prediction vs. Crash Risk:** The predictive model classifies accident severity *conditional on an accident having occurred* ($P(\text{Severe} \mid \text{Crash})$); it does not estimate raw accident occurrence probability without exposure (AADT) data.
2. **Empirical Hotspots:** High incident concentrations reflect empirical crash counts, not relative risk per vehicle-kilometer.
3. **No Automated Testing:** In strict compliance with research instructions, testing is conducted via manual validation checklists and inspection.
4. **Data Authenticity:** The event-level modeling dataset currently contains generated/synthetic rows calibrated to aggregate totals and marginal distributions. It is not observed crash-level data; derived event-level results are illustrative only. See [DATA_INTEGRITY_NOTICE.md](DATA_INTEGRITY_NOTICE.md).
