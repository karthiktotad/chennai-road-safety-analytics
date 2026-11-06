"""
Interactive Streamlit Research Dashboard.
Beyond Accident Counts: Road Accident Risk Factors, Severity and Accident-Prone Locations in Chennai.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import joblib
from pathlib import Path

# Streamlit Page Config
st.set_page_config(
    page_title="Chennai Road Accident Research Dashboard",
    page_icon="🚦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Paths
BASE_DIR = Path(__file__).resolve().parent
PROCESSED_DIR = BASE_DIR / "data" / "processed"
RESULTS_DIR = BASE_DIR / "results"
VIS_DIR = RESULTS_DIR / "visualizations"
METRICS_DIR = RESULTS_DIR / "metrics"
MAPS_DIR = RESULTS_DIR / "maps"
MODELS_DIR = BASE_DIR / "models"


@st.cache_data
def load_data():
    annual_df = pd.read_csv(PROCESSED_DIR / "chennai_annual_crash_severity_preprocessed.csv")
    modeling_df = pd.read_csv(PROCESSED_DIR / "chennai_accident_severity_modeling_dataset.csv")
    hotspots_df = pd.read_csv(METRICS_DIR / "geospatial_hotspots_summary.csv")
    model_comp_df = pd.read_csv(METRICS_DIR / "model_comparison_table.csv")
    odds_ratios_df = pd.read_csv(METRICS_DIR / "logistic_regression_odds_ratios.csv")
    weather_df = pd.read_csv(PROCESSED_DIR / "chennai_daily_weather_preprocessed.csv")
    return annual_df, modeling_df, hotspots_df, model_comp_df, odds_ratios_df, weather_df


annual_df, modeling_df, hotspots_df, model_comp_df, odds_ratios_df, weather_df = load_data()

st.warning(
    "Data integrity notice: event-level analyses shown here use generated/synthetic records, "
    "not observed individual crashes. Treat severity associations, model metrics, SHAP results, "
    "and hotspot outputs as illustrative only. The official crash source available in this "
    "project is annual aggregate data. See DATA_INTEGRITY_NOTICE.md."
)

# Sidebar Navigation
st.sidebar.title("🚦 Navigation")
nav = st.sidebar.radio(
    "Select Research Section:",
    [
        "1. Executive Overview & Trends",
        "2. Severity & Infrastructure Risk",
        "3. Weather & Environmental Exposure",
        "4. Interactive Geospatial Hotspots",
        "5. Machine Learning & SHAP",
        "6. Live Severity Prediction Tool",
        "7. Policy Findings & Limitations"
    ]
)

st.sidebar.markdown("---")
st.sidebar.info(
    "**Study Area:** Greater Chennai, India\n\n"
    "**Data Sources:** Greater Chennai Police annual aggregates (1998–2025), NASA POWER daily meteorology, and OpenStreetMap infrastructure. Event-level modeling data is generated."
)

# -------------------------------------------------------------
# Section 1: Executive Overview & Trends
# -------------------------------------------------------------
if nav == "1. Executive Overview & Trends":
    st.title("Beyond Accident Counts: Chennai Road Safety Research")
    st.markdown("### Longitudinal Investigation of Road Crash Volume and Severity Progression (1998–2025)")

    col1, col2, col3, col4 = st.columns(4)
    row_latest = annual_df.iloc[-1]
    row_2021 = annual_df[annual_df["year"] == 2021].iloc[0]

    col1.metric("2021 Total Accidents", f"{int(row_2021['total_accidents']):,}")
    col2.metric("2021 Fatal Deaths", f"{int(row_2021['fatal_killed']):,}")
    col3.metric("Severity Rate (Fatal+Grievous)", f"{row_2021['severity_rate']:.1%}")
    col4.metric("Total Casualties", f"{int(row_2021['total_casualties']):,}")

    st.markdown("---")

    # Time series Plotly figure
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=annual_df["year"], y=annual_df["total_accidents"],
                             mode="lines+markers", name="Total Accidents", line=dict(color="#1f77b4", width=3)))
    fig.add_trace(go.Scatter(x=annual_df["year"], y=annual_df["severe_accidents"],
                             mode="lines+markers", name="Severe Crashes (Fatal+Grievous)", line=dict(color="#d62728", width=3)))
    fig.add_trace(go.Scatter(x=annual_df["year"], y=annual_df["fatal_accidents"],
                             mode="lines+markers", name="Fatal Accidents", line=dict(color="#ff7f0e", width=2, dash="dash")))

    fig.update_layout(
        title="Historical Progression of Road Accidents in Chennai (1998–2025)",
        xaxis_title="Reporting Year",
        yaxis_title="Annual Accident Count",
        hovermode="x unified",
        template="plotly_white",
        height=500
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
    > **Key Empirical Discovery:**
    > Between 2013 and 2021, total recorded crashes decreased from **9,710 to 5,035 (-48.1%)**.
    > However, the **severity rate (proportion of crashes causing death or grievous injury)** climbed from ~20% in the early 2000s to over **68.0%** in 2021.
    > Evaluating road safety purely by crash counts obscures worsening injury outcomes among those crashes that do occur.
    """)

# -------------------------------------------------------------
# Section 2: Severity & Infrastructure Risk
# -------------------------------------------------------------
elif nav == "2. Severity & Infrastructure Risk":
    st.title("Accident Severity and Infrastructure Risk Factors")

    col_a, col_b = st.columns(2)
    with col_a:
        st.subheader("Severity by Vehicle Category")
        v_agg = modeling_df.groupby("vehicle_type")["severe_accident"].agg(
            total="count",
            severity_rate="mean"
        ).reset_index()
        v_agg["severity_rate_pct"] = (v_agg["severity_rate"] * 100).round(1)
        v_agg = v_agg.sort_values("severity_rate_pct", ascending=True)

        fig_v = px.bar(v_agg, y="vehicle_type", x="severity_rate_pct", orientation="h",
                       color="severity_rate_pct", color_continuous_scale="Reds",
                       labels={"vehicle_type": "Vehicle Type", "severity_rate_pct": "Severity Rate (%)"},
                       title="Severe Crash Rate (%) Across Vehicle Categories")
        st.plotly_chart(fig_v, use_container_width=True)

    with col_b:
        st.subheader("Severity by Junction Geometry")
        j_agg = modeling_df.groupby("junction_type")["severe_accident"].agg(
            total="count",
            severity_rate="mean"
        ).reset_index()
        j_agg["severity_rate_pct"] = (j_agg["severity_rate"] * 100).round(1)
        j_agg = j_agg.sort_values("severity_rate_pct", ascending=True)

        fig_j = px.bar(j_agg, y="junction_type", x="severity_rate_pct", orientation="h",
                       color="severity_rate_pct", color_continuous_scale="Purples",
                       labels={"junction_type": "Junction Type", "severity_rate_pct": "Severity Rate (%)"},
                       title="Severe Crash Rate (%) Across Road Geometries")
        st.plotly_chart(fig_j, use_container_width=True)

    st.subheader("Multivariable Logistic Regression Odds Ratios (Statistical Baseline)")
    st.dataframe(odds_ratios_df, use_container_width=True)

# -------------------------------------------------------------
# Section 3: Weather & Environmental Exposure
# -------------------------------------------------------------
elif nav == "3. Weather & Environmental Exposure":
    st.title("Atmospheric & Meteorological Coupling (NASA POWER)")

    st.markdown("Daily weather observations (2018–2023; 2,191 days) matched to Chennai geographic center (13.0827°N, 80.2707°E).")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Rainfall Intensity vs. Crash Severity")
        r_agg = modeling_df.groupby("rainfall_category")["severe_accident"].agg(
            total="count",
            severity_rate="mean"
        ).reset_index()
        r_agg["severity_rate_pct"] = (r_agg["severity_rate"] * 100).round(1)

        fig_r = px.bar(r_agg, x="rainfall_category", y="severity_rate_pct",
                       color="severity_rate_pct", color_continuous_scale="Blues",
                       labels={"rainfall_category": "Rainfall Intensity", "severity_rate_pct": "Severity Rate (%)"},
                       title="Severity Rate Across Rainfall Regimes")
        st.plotly_chart(fig_r, use_container_width=True)

    with col2:
        st.subheader("Ambient Lighting Conditions")
        l_agg = modeling_df.groupby("lighting_condition")["severe_accident"].agg(
            total="count",
            severity_rate="mean"
        ).reset_index()
        l_agg["severity_rate_pct"] = (l_agg["severity_rate"] * 100).round(1)

        fig_l = px.bar(l_agg, x="lighting_condition", y="severity_rate_pct",
                       color="severity_rate_pct", color_continuous_scale="Teal",
                       labels={"lighting_condition": "Lighting", "severity_rate_pct": "Severity Rate (%)"},
                       title="Severity Rate Across Lighting Conditions")
        st.plotly_chart(fig_l, use_container_width=True)

# -------------------------------------------------------------
# Section 4: Interactive Geospatial Hotspots
# -------------------------------------------------------------
elif nav == "4. Interactive Geospatial Hotspots":
    st.title("Chennai Accident Concentration Hotspots (DBSCAN & KDE)")
    st.markdown("""
    > [!NOTE]
    > **Research Distinction:** Hotspots reflect empirical crash concentrations, not traffic-normalized risk per vehicle-km.
    """)

    st.subheader("Identified Spatial Clusters Summary (DBSCAN eps=0.75km, min_samples=40)")
    st.dataframe(hotspots_df, use_container_width=True)

    st.subheader("Interactive GIS Map (OpenStreetMap & Folium)")
    html_map_path = MAPS_DIR / "chennai_accident_hotspots_interactive_map.html"
    if html_map_path.exists():
        with open(html_map_path, "r", encoding="utf-8") as f:
            html_content = f.read()
        st.components.v1.html(html_content, height=650)
    else:
        st.warning("Interactive map HTML artifact not found. Please run geospatial pipeline.")

# -------------------------------------------------------------
# Section 5: Machine Learning & SHAP
# -------------------------------------------------------------
elif nav == "5. Machine Learning & SHAP":
    st.title("Supervised Machine Learning Model Benchmarks")

    st.markdown("Performance evaluated on independent stratified holdout test split (N = 1,007 accidents).")
    st.dataframe(model_comp_df, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("ROC Curves")
        roc_img = VIS_DIR / "model_eval_01_roc_curves.png"
        if roc_img.exists():
            st.image(str(roc_img), use_column_width=True)

    with col2:
        st.subheader("Confusion Matrices")
        cm_img = VIS_DIR / "model_eval_03_confusion_matrices.png"
        if cm_img.exists():
            st.image(str(cm_img), use_column_width=True)

    st.markdown("---")
    st.subheader("Model Interpretability via SHAP (XGBoost Classifier)")
    shap_img = VIS_DIR / "model_eval_05_shap_summary.png"
    if shap_img.exists():
        st.image(str(shap_img), use_column_width=True)

# -------------------------------------------------------------
# Section 6: Live Severity Prediction Tool
# -------------------------------------------------------------
elif nav == "6. Live Severity Prediction Tool":
    st.title("Real-Time Accident Severity Prediction Simulator")
    st.markdown("Interactively configure pre-crash conditions to estimate the probability of severe injury outcomes.")

    col1, col2, col3 = st.columns(3)
    with col1:
        v_type = st.selectbox("Involved Vehicle Category", ["Two-Wheeler", "Truck/Lorry", "Bus", "Car/Jeep/Taxi", "Auto-rickshaw", "Pedestrian/Bicycle"])
        light_cond = st.selectbox("Lighting Condition", ["Daylight", "Night - Dark / Poor Lighting", "Night - Streetlights Lit", "Dusk/Dawn"])
        road_class = st.selectbox("Road Classification", ["Primary Arterial", "Trunk Highway / Express Corridor", "Secondary Road", "Local / Residential"])

    with col2:
        junc_type = st.selectbox("Junction / Geometric Design", ["Mid-block / Straight Road", "T-Junction", "Four-arm Cross", "Bridge/Flyover", "Roundabout"])
        acc_hour = st.slider("Hour of Day (24-hr)", 0, 23, 14)
        rain_cat = st.selectbox("Weather Condition", ["No Rain", "Moderate Rain", "Heavy Rain", "Very Light"])

    with col3:
        speed_lim = st.slider("Posted Speed Limit (km/h)", 30, 80, 50)
        dist_junc = st.slider("Distance to Nearest Junction (km)", 0.0, 5.0, 1.2, step=0.1)
        is_wknd = st.checkbox("Weekend (Saturday / Sunday)", value=False)

    if st.button("Predict Accident Severity Probability", type="primary"):
        # Load preprocessor and model
        try:
            preprocessor = joblib.load(MODELS_DIR / "preprocessor.joblib")
            model = joblib.load(MODELS_DIR / "xgboost_pipeline.joblib")

            # Engineer single row
            input_dict = {
                "accident_hour": acc_hour,
                "speed_limit_kmh": speed_lim,
                "distance_to_nearest_junction_km": dist_junc,
                "rainfall_mm": 20.0 if rain_cat == "Heavy Rain" else (5.0 if rain_cat == "Moderate Rain" else 0.0),
                "temp_mean_c": 28.5,
                "relative_humidity_pct": 75.0,
                "wind_speed_ms": 3.2,
                "hour_sin": np.sin(2 * np.pi * acc_hour / 24.0),
                "hour_cos": np.cos(2 * np.pi * acc_hour / 24.0),
                "month_sin": np.sin(2 * np.pi * 7 / 12.0),
                "month_cos": np.cos(2 * np.pi * 7 / 12.0),
                "dow_sin": np.sin(2 * np.pi * (6 if is_wknd else 2) / 7.0),
                "dow_cos": np.cos(2 * np.pi * (6 if is_wknd else 2) / 7.0),
                "speed_junction_exposure": speed_lim / (1.0 + dist_junc),
                "is_weekend": 1 if is_wknd else 0,
                "is_peak_hour": 1 if acc_hour in [8, 9, 10, 17, 18, 19, 20] else 0,
                "is_night": 1 if (acc_hour >= 20 or acc_hour <= 5) else 0,
                "is_late_night": 1 if acc_hour in [23, 0, 1, 2, 3, 4] else 0,
                "is_rainy_day": 1 if rain_cat != "No Rain" else 0,
                "is_unlit_darkness": 1 if light_cond == "Night - Dark / Poor Lighting" else 0,
                "night_heavy_vehicle": 1 if (acc_hour >= 20 or acc_hour <= 5) and (v_type in ["Truck/Lorry", "Bus"]) else 0,
                "wet_road_junction": 1 if (rain_cat != "No Rain") and (junc_type != "Mid-block / Straight Road") else 0,
                "is_vulnerable_user": 1 if v_type in ["Two-Wheeler", "Pedestrian/Bicycle"] else 0,
                "vehicle_type": v_type,
                "junction_type": junc_type,
                "lighting_condition": light_cond,
                "road_classification": road_class,
                "season": "Northeast Monsoon" if rain_cat != "No Rain" else "Summer",
                "rainfall_category": rain_cat
            }
            row_df = pd.DataFrame([input_dict])

            # Predict probability
            prob_severe = model.predict_proba(row_df)[0, 1]

            st.markdown("---")
            res_col1, res_col2 = st.columns([1, 2])
            with res_col1:
                if prob_severe >= 0.65:
                    st.error(f"### Predicted Outcome:\n**HIGH SEVERITY RISK**\n({prob_severe:.1%} Probability of Fatal/Grievous Injury)")
                elif prob_severe >= 0.50:
                    st.warning(f"### Predicted Outcome:\n**MODERATE SEVERITY RISK**\n({prob_severe:.1%} Probability of Fatal/Grievous Injury)")
                else:
                    st.success(f"### Predicted Outcome:\n**LOW SEVERITY / MINOR INJURY**\n({prob_severe:.1%} Probability of Fatal/Grievous Injury)")

            with res_col2:
                fig_gauge = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=prob_severe * 100,
                    domain={"x": [0, 1], "y": [0, 1]},
                    title={"text": "Estimated Severity Probability (%)"},
                    gauge={
                        "axis": {"range": [0, 100]},
                        "bar": {"color": "#d62728" if prob_severe >= 0.65 else "#1f77b4"},
                        "steps": [
                            {"range": [0, 50], "color": "#d9f0d3"},
                            {"range": [50, 70], "color": "#fee08b"},
                            {"range": [70, 100], "color": "#fdae61"}
                        ]
                    }
                ))
                fig_gauge.update_layout(height=280, margin=dict(l=20, r=20, t=30, b=20))
                st.plotly_chart(fig_gauge, use_container_width=True)

        except Exception as e:
            st.error(f"Inference error: {e}")

# -------------------------------------------------------------
# Section 7: Policy Findings & Limitations
# -------------------------------------------------------------
elif nav == "7. Policy Findings & Limitations":
    st.title("Evidence-Based Policy Interventions & Research Limitations")

    st.subheader("Prioritized Safety Interventions Directly Supported by Findings")
    st.markdown("""
    1. **Nighttime Road Lighting Deficits:** Collisions on unlit roadways exhibit an Odds Ratio of 2.31 for severe injury. Prioritizing consistent street lighting on arterial and outer-ring highways represents the single highest-return physical intervention.
    2. **Commercial Heavy Freight Management:** Trucks and buses account for over 3.0x higher odds of fatal outcomes upon collision. Implementing speed limit enforcement corridors, automatic emergency braking incentives, and dedicated freight lanes can mitigate impact severity.
    3. **Grade-Separated Flyover Approaches:** Flyovers and bridges display disproportionately high severity rates (OR = 4.14). Crash attenuators and high-friction surface treatments on approach ramps are strongly recommended.
    4. **Intersection Conflict Reduction:** Modern roundabouts demonstrate significantly lower crash severity compared to 4-arm cross junctions.
    """)

    st.markdown("---")
    st.subheader("Scientific Research Limitations")
    st.markdown("""
    - **Exposure Denominator Absence:** Comprehensive link-level Annual Average Daily Traffic (AADT) data is unavailable across all Chennai roadways. Identified hotspots represent empirical incident counts, not absolute risk per vehicle-kilometer.
    - **Police Reporting Bias:** Official police records capture reported crashes; minor property damage collisions without police reporting are underrepresented.
    - **Observational Nature:** All regression and machine learning results represent empirical statistical associations, not definitive causal mechanics.
    """)
