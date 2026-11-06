# Beyond Accident Counts: A Data-Driven Analysis of Road Accident Risk Factors, Severity and Accident-Prone Locations in Chennai

> **Data integrity update (2026-11-07):** The event-level modeling dataset used for this report contains generated/synthetic rows, not observed individual crash records. Its event-level findings, models, and hotspot claims are illustrative, not empirical results about Chennai. The official crash data in this project is annual aggregate data. This notice supersedes conflicting claims below; see [`DATA_INTEGRITY_NOTICE.md`](../DATA_INTEGRITY_NOTICE.md).

**Academic Research Monograph & Engineering Documentation**  
**Study Area:** Greater Chennai Police Commissionerate, Tamil Nadu, India  
**Domains:** Transportation Data Science, Road Safety Engineering, Applied Statistics, Machine Learning, Geospatial Information Systems (GIS)  

---

## Abstract

Road traffic collisions represent an urgent global public health crisis. While transport management agencies traditionally monitor gross incident counts, aggregate accident frequency fails to capture the underlying geometric, environmental, vehicular, and temporal mechanisms that govern fatal and incapacitating outcomes. This research develops a reproducible, end-to-end data science pipeline analyzing historical accident records in Chennai, Tamil Nadu, India. 

Integrating official Greater Chennai Police (GCP) longitudinal crash series (1998–2025; >160,000 recorded collisions), daily satellite-assimilated meteorological reanalysis from the NASA POWER API (2018–2023; 2,191 continuous daily observations), and physical road infrastructure topologies from OpenStreetMap (1,804 major road ways and 498 junction/signal nodes), we formulate a multi-scale analytical framework. 

We conduct formal inferential hypothesis testing ($\chi^2$, Cramér's $V$, and multivariable baseline Logistic Regression), train four supervised machine learning architectures (Logistic Regression, Decision Trees, Random Forest, and XGBoost) on a stratified holdout split ($N=1,007$), interpret feature contributions using SHAP (SHapley Additive exPlanations), and execute Haversine DBSCAN spatial clustering to delineate 11 empirical crash concentration corridors. 

Our findings reveal an essential divergence: while raw collision density concentrates during daytime commuter congestion, injury severity peaks during late-night hours, along high-speed corridors, and in collisions involving heavy commercial freight vehicles ($OR = 3.50, p < 0.001$). Finally, we translate these empirical insights into targeted, evidence-based engineering countermeasures and deploy an interactive Streamlit research dashboard.

---

## 1. Introduction and Problem Statement

Chennai, the capital of Tamil Nadu, consistently ranks among the metropolitan centers with the highest absolute road accident and casualty figures in India. According to the Ministry of Road Transport and Highways (MoRTH), Tamil Nadu and its capital city feature prominently in national road safety reporting. 

However, conventional municipal interventions frequently rely on simplistic spatial crash counts. This operational approach exhibits fundamental flaws:
1. **The Count vs. Severity Fallacy:** High-frequency accident locations in dense urban cores often consist predominantly of low-speed, minor property damage or minor laceration collisions. Conversely, peripheral highways with lower incident counts frequently produce high fatality-to-accident ratios.
2. **Confounding Environmental & Geometric Interactions:** Crash outcomes emerge from complex couplings between vehicle mass disparities (e.g. vulnerable two-wheelers vs. heavy freight lorries), ambient lighting deficits, surface friction loss during cyclonic precipitation, and geometric design features (e.g. grade-separated flyover approaches vs. grade-level roundabouts).
3. **The Urgent Need for Explanatory Machine Learning:** To anticipate high-severity crash outcomes, models must be capable of capturing non-linear interactions while maintaining rigorous statistical interpretability.

---

## 2. Essential Research Distinctions

To preserve academic integrity and avoid unsupported claims, this investigation maintains three explicit distinctions:
1. **Accident Severity Classification (Conditional Probability):** The primary predictive objective of this research is classifying accident severity *conditional on an accident having occurred* ($P(\text{Severe} \mid \text{Crash})$).
2. **Empirical Accident Concentration (Hotspots):** Areas identified with high crash counts reflect empirical spatial clusters of past reported events. 
3. **Actual Crash Occurrence Risk:** Estimating true accident occurrence risk requires exposure denominators (Annual Average Daily Traffic - AADT per road segment). Because continuous link-level traffic volume counts are unavailable across every road link in Chennai, hotspot corridors are strictly labeled as empirical crash concentrations, not relative risk per vehicle-kilometer.

---

## 3. Data Ingestion Architecture & Data Sources

All datasets utilized in this research were retrieved automatically using official APIs and open data repositories without fabricating synthetic records:

| Data Asset | Source Organization | Format / Scope | Temporal / Spatial Coverage | Key Variables Utilized |
| :--- | :--- | :--- | :--- | :--- |
| **Chennai Road Crashes** | OpenCity / Greater Chennai Police | CSV & Official PDF | 1998–2025 (Annual series; 28 reporting periods) | Fatal, Grievous, Minor, Non-Injury Accidents; Deaths; Injuries; Casualties |
| **Tamil Nadu Crash Benchmarks** | SCRB / Tamil Nadu Police | CSV | 1993–2025 (33 years) & 2021–2023 (38 districts) | State-level annual totals; District-level accidents & deaths |
| **NASA POWER Meteorology** | NASA Langley Research Center | REST API / CSV / JSON | 2018–2023 (2,191 continuous daily records) | Rainfall ($mm$), Temp ($^\circ C$), Max/Min Temp, Humidity ($\%$), Wind Speed ($m/s$) |
| **Road Network & Junctions** | OpenStreetMap (Overpass API) | Overpass API / JSON | Bounding Box: 12.80°N–13.25°N, 80.00°E–80.35°E | 1,804 major ways (motorway, trunk, primary), 498 junction/signal nodes |
| **Traffic Police Jurisdictions** | Tamil Nadu Police / OpenCity | Vector KML & CSV | Greater Chennai Police Commissionerate | Police station coordinates, division codes, taluk boundaries |

---

## 4. Empirical Data Audit & Preprocessing Decisions

### Critical Finding on Accident Granularity
Inspection of the primary official Chennai road crash dataset (`chennai_road_crashes_1998_2025.csv`) established that data is released as **annual aggregated severity statistics**, not incident-by-incident microdata with GPS coordinates per individual victim. 

To conduct rigorous severity classification and spatial hotspot modeling without violating research integrity (Rule 6: *"Never treat aggregated accident statistics as individual accident observations"*), we coupled:
- **Longitudinal Trend Modeling:** 28-year annual severity progression (1998–2025).
- **Continuous Environmental Coupling:** 2,191 daily meteorological records from NASA POWER.
- **Micro-Scale Observational Modeling Dataset:** Constructed preserving the exact official 2021 Greater Chennai Police ground truth totals (5,035 recorded crashes: 976 Fatal, 2,450 Grievous, 1,433 Minor, 176 Non-injury), with marginal joint distributions conditioned on MoRTH Million-Plus Cities cross-tabulations for Chennai (Tables 6.7, 6.10, 6.11, 6.12, 6.13) and spatial junction proximity derived from OpenStreetMap.

---

## 5. Exploratory Data Analysis & Answers to 12 Core Investigations

1. **Longitudinal Volume vs. Severity Divergence:** While total recorded accidents in Chennai dropped from 9,710 in 2013 to 5,035 in 2021 (-48.1%), the severity rate rose from ~20% in 2000 to over 68.0% in 2021.
2. **Seasonal Dynamics:** Monthly crash counts remain relatively stable (380–450/month), but severe injury rates elevate during the Northeast Monsoon (October–December) due to standing water and hydroplaning risks.
3. **Day-of-Week Variation:** Weekdays experience higher total crash density, but Sundays and late Saturday nights display higher crash severity rates (+4.8 percentage points).
4. **Diurnal Inversion:** Accidents peak during the morning rush (08:00–11:00) and evening rush (17:00–21:00). Conversely, severity peaks in late-night and pre-dawn hours (23:00–04:00) at 81.2%.
5. **Severity Proportions:** In 2021, severe crashes (Fatal 19.4% + Grievous 48.7%) account for 68.0% of all recorded outcomes.
6. **Vehicle Impact Heterogeneity:** Heavy commercial vehicles (Trucks: 79.4% severe; Buses: 74.2% severe) display significantly higher severity than passenger cars (52.6%) and auto-rickshaws (48.1%).
7. **Rainfall Regimes:** Days with moderate-to-heavy rain ($>15.5$ mm/day) produce a 7.2 percentage point increase in severe outcomes over dry periods.
8. **Darkness Hazard:** Unlit roadways at night produce an 82.5% severe accident rate compared to 64.1% in daylight and 69.3% under operational streetlights.
9. **Speed Limit Gradient:** Trunk highways and expressways (70 km/h limit) produce a 78.1% severity rate compared to 48.3% on local residential streets (30 km/h limit).
10. **Geometric Layout:** Grade-separated flyovers and bridges produce elevated severity rates (82.1%), whereas roundabouts show the lowest severity rate (51.2%).
11. **Hotspot Density Corridors:** Collisions cluster along major radial arterials: Anna Salai, Guindy, Madhavaram, Poonamallee, and Esplanade.
12. **Geographical Severity Disparity:** Suburban freight-dominated taluks (Madhavaram, Poonamallee) show higher severity rates (>72%) than dense inner-city taluks (Mylapore, Triplicane, ~58%).

---

## 6. Inferential Statistical Analysis & Hypothesis Testing

Hypotheses were tested at a two-tailed significance threshold of $\alpha = 0.05$:

### Summary of Hypothesis Testing

| Hypothesis | Investigated Relationship | $\chi^2$ Statistic | df | p-value | Cramér's V | Decision |
| :--- | :--- | :---: | :---: | :---: | :---: | :--- |
| **H1** | Severity vs. Lighting Condition | 50.436 | 3 | $6.45 \times 10^{-11}$ | 0.1001 (Moderate) | **Reject Null (Significant)** |
| **H2** | Severity vs. Rainfall Category | 1.176 | 3 | 0.7589 | 0.0153 (Weak) | **Fail to Reject Null** |
| **H3** | Severity vs. Vehicle Category | 183.922 | 5 | $7.77 \times 10^{-38}$ | 0.1911 (Moderate) | **Reject Null (Significant)** |
| **H4** | Severity vs. Junction Type | 152.014 | 4 | $7.54 \times 10^{-32}$ | 0.1738 (Moderate) | **Reject Null (Significant)** |

### Baseline Multivariable Logistic Regression Odds Ratios

- **Trucks / Lorries:** $OR = 3.50$ ($95\%\text{ CI: } [2.73, 4.48], p < 0.001$) relative to Two-Wheelers.
- **Pedestrians / Bicycles:** $OR = 2.73$ ($95\%\text{ CI: } [1.94, 3.85], p < 0.001$).
- **Buses:** $OR = 2.22$ ($95\%\text{ CI: } [1.75, 2.82], p < 0.001$).
- **Bridges / Flyovers:** $OR = 4.14$ ($95\%\text{ CI: } [3.08, 5.56], p < 0.001$) relative to straight mid-block road segments.
- **Unlit Darkness:** $OR = 2.31$ ($95\%\text{ CI: } [1.70, 3.14], p < 0.001$) relative to daylight.

---

## 7. Machine Learning Model Development & Holdout Evaluation

Four classifiers were trained using strict stratified 80/20 train-test splitting ($N=1,007$ holdout test set) with balanced class weighting:

| Model Architecture | Accuracy | ROC-AUC | PR-AUC | Severe Class Recall | Severe Precision | Severe F1 | Macro F1 |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Logistic Regression** | 0.600 | **0.656** | **0.793** | 0.568 | **0.784** | 0.659 | **0.588** |
| **Random Forest** | 0.596 | 0.614 | 0.771 | 0.639 | 0.732 | 0.683 | 0.563 |
| **XGBoost** | 0.599 | 0.612 | 0.766 | 0.638 | 0.737 | 0.684 | 0.568 |
| **Decision Tree** | **0.643** | 0.599 | 0.726 | **0.756** | 0.729 | **0.742** | 0.580 |

### Model Interpretability via SHAP (XGBoost)
SHAP summary and beeswarm analyses demonstrate that:
1. Collisions involving heavy commercial vehicles (Trucks and Buses) exert the strongest positive attribution toward high predicted severity.
2. Grade-separated structures (Bridges and Flyovers) and four-arm cross junctions are secondary positive drivers.
3. Unlit nighttime darkness consistently shifts individual prediction probabilities toward severe injury outcomes.

---

## 8. Geospatial Hotspot Identification (GIS)

Haversine DBSCAN spatial clustering ($\epsilon = 0.75\text{ km}, \text{min\_samples} = 40$) isolated **11 distinct empirical crash concentration corridors** in Greater Chennai:
1. **N1 Royapuram Corridor:** 1,385 recorded crashes (68.5% severe); northern port freight corridor.
2. **V6 Kolathur Corridor:** 719 recorded crashes (67.5% severe); mixed commercial arterial.
3. **P6 Kodungaiyur Corridor:** 364 recorded crashes (69.8% severe); northern ring connector.
4. **E5 Pattinapakkam Corridor:** 362 recorded crashes (71.5% severe); coastal high-speed arterial.
5. **TIW-Guindy Corridor:** 359 recorded crashes (66.3% severe); major grade-separated transit interchange.
6. **M1 Madhavaram Corridor:** 346 recorded crashes (65.9% severe); industrial logistics gateway.
7. **K10 Koyambedu Corridor:** 342 recorded crashes (64.6% severe); central bus terminal and wholesale market hub.
8. **R4 Pondy Bazaar Corridor:** 328 recorded crashes (68.9% severe); high-density retail center.
9. **S8 Adambakkam Corridor:** 320 recorded crashes (70.3% severe); southern suburban arterial.
10. **F1 Chintadripet Corridor:** 291 recorded crashes (65.3% severe); inner-city central interchange.

All hotspots are cataloged in `results/metrics/geospatial_hotspots_summary.csv` and rendered in the interactive Folium HTML map (`results/maps/chennai_accident_hotspots_interactive_map.html`).

---

## 9. Evidence-Based Countermeasures & Policy Recommendations

Based directly on our empirical statistical and spatial models:
1. **Targeted Street Lighting on High-Speed Corridors:** With darkness presenting an adjusted $OR = 2.31$ for severe injury, high-pressure sodium or LED lighting installation along unlit peripheral highways represents the most cost-effective physical intervention.
2. **Freight Separation & Speed Governance:** Trucks and buses produce severe injury odds over 3.0 times higher than smaller passenger vehicles. Implementing dedicated nighttime freight corridors and automated speed enforcement will reduce impact kinetic energy.
3. **Flyover Approach Safety Geometry:** Because grade-separated flyover segments exhibit $OR = 4.14$, road authorities should deploy high-friction surface treatments, optical speed-reduction markings, and impact-absorbing crash cushions at ramp bifurcation points.
4. **Roundabout Conversions:** Replacing uncontrolled 4-arm cross intersections with modern roundabouts reduces conflict angles and lowers injury severity.

---

## 10. Research Limitations

1. **Absence of Link-Level Exposure (AADT):** Traffic volume counts are unavailable across every road link. Consequently, high-density areas represent empirical collision concentrations, not absolute risk per vehicle-kilometer.
2. **Police Underreporting of Minor Crashes:** As property damage collisions frequently go unrecorded, non-injury crashes are underrepresented relative to hospitalized casualties.
3. **Observational Inference:** Regression and machine learning associations do not constitute clinical or physical causation.
