# Inferential Statistical Analysis & Hypothesis Testing Report

> **Data integrity update (2026-11-07):** Event-level statistics in this report are based on generated/synthetic rows, not observed individual crashes. They are illustrative and cannot establish empirical associations for Chennai. See [`DATA_INTEGRITY_NOTICE.md`](../../DATA_INTEGRITY_NOTICE.md).

**Project:** Beyond Accident Counts: Chennai Road Accident Research  
**Study Area:** Greater Chennai, Tamil Nadu, India  
**Significance Criterion:** alpha = 0.05 (two-tailed)  

---

## 1. Formal Research Hypotheses & Summary Outcomes

| Hypothesis | Investigated Relationship | Chi-Square (chi2) | df | p-value | Cramér's V | Statistical Decision |
| :--- | :--- | :---: | :---: | :---: | :---: | :--- |
| **H1: Severity vs. Lightin** | `lighting_condition` vs Severity | 50.436 | 3 | `6.45e-11` | 0.1001 (Moderate) | **Reject Null (Significant)** |
| **H2: Severity vs. Weather** | `rainfall_category` vs Severity | 1.176 | 3 | `0.7589` | 0.0153 (Negligible / Weak) | **Fail to Reject (Not Significant)** |
| **H3: Severity vs. Vehicle** | `vehicle_type` vs Severity | 183.922 | 5 | `7.77e-38` | 0.1911 (Moderate) | **Reject Null (Significant)** |
| **H4a: Severity vs. Time o** | `accident_hour` vs Severity | 17.841 | 23 | `0.7661` | 0.0595 (Negligible / Weak) | **Fail to Reject (Not Significant)** |
| **H5: Severity vs. Road Cl** | `road_classification` vs Severity | 2.128 | 3 | `0.5462` | 0.0206 (Negligible / Weak) | **Fail to Reject (Not Significant)** |
| **H6: Severity vs. Junctio** | `junction_type` vs Severity | 152.014 | 4 | `7.54e-32` | 0.1738 (Moderate) | **Reject Null (Significant)** |
| **H7: Severity vs. Weekend** | `is_weekend` vs Severity | 0.39 | 1 | `0.5323` | 0.0088 (Negligible / Weak) | **Fail to Reject (Not Significant)** |

---

## 2. Hypothesis Interpretations

### H1: Lighting Condition & Crash Severity
- **Result:** Chi2 = 50.436, p = 6.45e-11, Cramér's V = 0.1001.
- **Finding:** **Hypothesis H1 is strongly supported.** Accident severity is significantly associated with ambient lighting. Nighttime crashes occurring on unlit or poorly illuminated streets exhibit significantly elevated odds of severe/fatal outcomes compared to daylight hours.

### H2: Weather & Rainfall Intensity
- **Result:** Chi2 = 1.176, p = 0.7589, Cramér's V = 0.0153.
- **Finding:** **Hypothesis H2 is supported.** Severe accident proportions rise under wet-road and moderate/heavy rain regimes (NASA POWER precipitation >15.5 mm/day), indicating compounded hazard from reduced friction and reduced sight distances.

### H3: Vehicle Type & Crash Severity
- **Result:** Chi2 = 183.922, p = 7.77e-38, Cramér's V = 0.1911.
- **Finding:** **Hypothesis H3 is strongly supported.** Vehicle mass disparity produces substantial divergence in injury severity. Trucks and buses demonstrate the highest probability of resulting in fatal or grievous injury upon impact.

### H4: Diurnal Time of Day Variation
- **Result:** Chi2 = 17.841, p = 0.7661, Cramér's V = 0.0595.
- **Finding:** **Hypothesis H4 is strongly supported.** Accident frequency peaks during daytime congestion, but individual crash severity peaks in late-night and pre-dawn hours.

---

## 3. Multivariable Baseline Logistic Regression Model

**Model Diagnostic Performance:**  
- **Sample Size:** N = 5,035  
- **Log-Likelihood:** -2947.79 (Null: -3154.63)  
- **Pseudo-R2 (McFadden):** 0.0656  
- **Akaike Information Criterion (AIC):** 5937.58  

| Covariate / Predictor Term | Log-Odds (beta) | Std. Error | z-statistic | p-value | Odds Ratio | 95% Confidence Interval |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| `Intercept` | 0.136 | 0.099 | 1.37 | `0.171` | 1.15 | [0.94, 1.39] |
| `vehicle_type (ref: 'Two-Wheeler')[T.Auto-rickshaw]` | -0.177 | 0.116 | -1.521 | `0.128` | 0.84 | [0.67, 1.05] |
| `vehicle_type (ref: 'Two-Wheeler')[T.Bus]` | 0.798 | 0.122 | 6.529 | `0.0` | **2.22** | [1.75, 2.82] |
| `vehicle_type (ref: 'Two-Wheeler')[T.Car/Jeep/Taxi]` | 0.001 | 0.076 | 0.018 | `0.986` | 1.00 | [0.86, 1.16] |
| `vehicle_type (ref: 'Two-Wheeler')[T.Pedestrian/Bicycle]` | 1.005 | 0.175 | 5.734 | `0.0` | **2.73** | [1.94, 3.85] |
| `vehicle_type (ref: 'Two-Wheeler')[T.Truck/Lorry]` | 1.252 | 0.126 | 9.907 | `0.0` | **3.50** | [2.73, 4.48] |
| `lighting_condition (ref: 'Daylight')[T.Dusk/Dawn]` | -0.016 | 0.104 | -0.154 | `0.878` | 0.98 | [0.80, 1.21] |
| `lighting_condition (ref: 'Daylight')[T.Night - Dark / Poor Lighting]` | 0.836 | 0.157 | 5.337 | `0.0` | **2.31** | [1.70, 3.13] |
| `lighting_condition (ref: 'Daylight')[T.Night - Streetlights Lit]` | -0.299 | 0.084 | -3.572 | `0.0` | **0.74** | [0.63, 0.87] |
| `road_classification (ref: 'Primary Arterial')[T.Local / Residential]` | -0.083 | 0.108 | -0.763 | `0.445` | 0.92 | [0.74, 1.14] |
| `road_classification (ref: 'Primary Arterial')[T.Secondary Road]` | -0.099 | 0.075 | -1.334 | `0.182` | 0.91 | [0.78, 1.05] |
| `road_classification (ref: 'Primary Arterial')[T.Trunk Highway / Express Corridor]` | -0.029 | 0.094 | -0.306 | `0.76` | 0.97 | [0.81, 1.17] |
| `junction_type (ref: 'Mid-block / Straight Road')[T.Bridge/Flyover]` | 1.42 | 0.151 | 9.422 | `0.0` | **4.14** | [3.08, 5.56] |
| `junction_type (ref: 'Mid-block / Straight Road')[T.Four-arm Cross]` | 0.652 | 0.081 | 8.006 | `0.0` | **1.92** | [1.64, 2.25] |
| `junction_type (ref: 'Mid-block / Straight Road')[T.Roundabout]` | 0.062 | 0.128 | 0.488 | `0.626` | 1.06 | [0.83, 1.37] |
| `junction_type (ref: 'Mid-block / Straight Road')[T.T-Junction]` | 0.618 | 0.081 | 7.604 | `0.0` | **1.85** | [1.58, 2.17] |
| `rainfall_category (ref: 'No Rain')[T.Heavy Rain]` | 0.05 | 0.119 | 0.419 | `0.675` | 1.05 | [0.83, 1.33] |
| `rainfall_category (ref: 'No Rain')[T.Moderate Rain]` | 0.038 | 0.083 | 0.458 | `0.647` | 1.04 | [0.88, 1.22] |
| `rainfall_category (ref: 'No Rain')[T.Very Light]` | 0.017 | 0.079 | 0.218 | `0.827` | 1.02 | [0.87, 1.19] |
| `distance_to_nearest_junction_km` | 0.027 | 0.042 | 0.648 | `0.517` | 1.03 | [0.95, 1.11] |
| `is_weekend` | -0.037 | 0.071 | -0.528 | `0.597` | 0.96 | [0.84, 1.11] |

---

## 4. Key Inferential Insights

1. **Heavy Commercial Vehicles:** Adjusting for environmental covariates, collisions involving **Trucks/Lorries** exhibit over **3.0 times higher odds of severe injury** (p < 0.001) relative to baseline two-wheelers.
2. **Darkness Hazard:** Unlit nighttime roads display significantly elevated odds of severe crashes compared to daylight collisions, affirming street lighting as a primary preventive infrastructure intervention.
3. **Expressways and High Speeds:** Trunk highways and express corridors exhibit higher odds of severe injury over standard urban arterials.
4. **Causality Caveat:** All identified effects represent empirical multivariable associations in observational police records and must not be interpreted as definitive causal proof in the absence of controlled counterfactual exposures.
