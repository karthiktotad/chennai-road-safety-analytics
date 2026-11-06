# Project Decisions & Research Governance

This document records architectural, statistical, and methodological decisions taken during the execution of the Chennai Road Accident Research project.

---

## 1. Research Objectives & Conceptual Framing

### Decision: Distinguishing Severity Classification vs. Risk vs. Hotspots
- **Severity Prediction:** The primary predictive objective is classifying accident severity *conditional on an accident having occurred*.
- **Hotspot Analysis:** High accident concentration areas represent empirical spatial clusters of past incidents. Without comprehensive traffic volume / exposure denominators, these will be strictly reported as "Accident Hotspots / Empirical Density Clusters", not "Absolute Probability of Crash per Vehicle-Kilometer".
- **Risk Estimation:** True accident occurrence risk requires exposure data (Annual Average Daily Traffic - AADT). Any statements regarding risk will be carefully qualified with analytical boundaries.

### Target Variable Formulation:
- **Binary Target (`severe_accident`):**
  - `1` = Fatal or Grievous / Serious Injury.
  - `0` = Minor Injury or Property Damage Only (Non-injury).
- **Multiclass Extension:** Where supported by sample sizes in granular sub-categories, multiclass evaluation (Fatal vs. Grievous vs. Minor vs. Non-Injury) will be analyzed as a secondary task.

---

## 2. Data Engineering & Integrity Protocols

### Decision: Raw Data Immutability
- Files deposited in `data/raw/` are strictly write-once and read-only.
- All cleaning, filtering, and imputation output must reside in `data/interim/` or `data/processed/`.
- **Implementation status:** The current event-level modeling dataset is generated/synthetic, contrary to this design decision. It must not be treated as observed crash data; see [DATA_INTEGRITY_NOTICE.md](DATA_INTEGRITY_NOTICE.md). Rebuild event-level analyses only with genuine incident-level records or label them explicitly as simulations.

### Decision: Handling Missing Values
- Explicit documentation of missingness patterns.
- High-missingness columns (>50%) will be evaluated for informative missingness indicators before feature inclusion.
- No arbitrary constant imputation for physical measurements (e.g. fabricating rainfall or speed limits).

---

## 3. Machine Learning & Statistical Governance

### Decision: Leakage Prevention
- Feature transformations and scalers must be fit exclusively on the training split.
- Class rebalancing techniques (e.g., class weighting or SMOTE) will be applied *strictly within training folds* and never on validation/testing sets.
- Post-crash outcome features (e.g. number of ambulances called, post-incident hospital days) will not be utilized as predictors.

### Decision: Baseline & Interpretability
- Logistic Regression will serve as the interpretable statistical baseline with reported Odds Ratios and 95% Confidence Intervals.
- Complex tree models (Random Forest, XGBoost) will be interpreted using SHAP (SHapley Additive exPlanations) values to explain feature contributions.

---

## 4. Quality Assurance & Testing Protocol

### Decision: Human-Centric Manual Validation (Strict Prohibition on Automated Testing)
- In strict adherence to project specifications, no automated testing frameworks (`pytest`, `unittest`, CI test runners) will be authored or executed.
- Quality assurance is enforced via:
  1. Systematic data audit checkpoints.
  2. Manual command line execution walkthroughs provided for each stage.
  3. Interactive artifact review (tables, distributions, confusion matrices, and maps).
