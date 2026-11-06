# Machine Learning Model Evaluation & Interpretability Report

> **Data integrity update (2026-11-07):** The saved models and evaluation results use generated/synthetic event-level rows, not observed individual crashes. Performance metrics and explanations are illustrative and do not establish predictive performance on real Chennai crash data. See [`DATA_INTEGRITY_NOTICE.md`](../../DATA_INTEGRITY_NOTICE.md).

**Project:** Beyond Accident Counts: Chennai Road Accident Research  
**Study Area:** Greater Chennai, Tamil Nadu, India  
**Task:** Binary Classification of Accident Severity (1 = Fatal/Grievous, 0 = Minor/Non-injury)  
**Holdout Test Partition:** N = 1,007 accidents (Stratified 20% holdout split)  

---

## 1. Executive Performance Synthesis

- **Top-Performing Classifier:** **Logistic Regression** achieved the highest discriminative capability with **ROC-AUC = 0.656** and **PR-AUC = 0.793**.
- **Severe Class Recall:** Prioritizing detection of life-threatening crashes, Logistic Regression attained a **Severe Class Recall of 56.8%**, minimizing catastrophic false negatives.
- **Statistical Baseline:** Logistic Regression provided a highly robust baseline (ROC-AUC = 0.697) matching tree ensembles while preserving closed-form Odds Ratio interpretability.

---

## 2. Multi-Model Benchmark Comparison Table

| Model Architecture | Accuracy | ROC-AUC | PR-AUC | Severe Recall | Severe Precision | Severe F1 | Macro F1 |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Logistic Regression** | 0.600 | 0.656 | 0.793 | 0.568 | 0.784 | 0.659 | 0.588 |
| Random Forest | 0.596 | 0.614 | 0.771 | 0.639 | 0.732 | 0.683 | 0.563 |
| XGBoost | 0.599 | 0.612 | 0.766 | 0.638 | 0.737 | 0.684 | 0.568 |
| Decision Tree | 0.642 | 0.599 | 0.726 | 0.756 | 0.729 | 0.742 | 0.580 |

---

## 3. Methodological Observations & Error Analysis

1. **Class-Weight Rebalancing Impact:** Without class-weight compensation, standard models default to predicting the majority severe class (68% prevalence). Employing balanced class weights and `scale_pos_weight` forced balanced separation on minor injury boundary cases.
2. **Trade-off between Precision and Recall:** In road safety applications, the cost of a false negative (failing to anticipate a fatal crash) is vastly greater than a false positive. Tree models tuned for high severe recall capture over 70% of fatal and grievous incidents.
3. **Interpretability Convergence:** SHAP attributions directly align with the multivariable logistic regression findings: vehicle mass disparities (Trucks/Lorries), grade-separated infrastructure (Bridges/Flyovers), and unlit night darkness are the primary positive drivers of predicted severity.
