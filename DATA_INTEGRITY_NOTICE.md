# Data Integrity Notice

**Updated:** 2026-11-07

## What the data supports

The OpenCity / Greater Chennai Police crash file in `data/raw/accidents/chennai_road_crashes_1998_2025.csv` contains annual aggregate severity counts. It does not contain one record per crash, incident timestamps, or crash coordinates. The weather and OpenStreetMap files are separate source datasets and are not linked observations of individual crashes.

## What the event-level results represent

`data/processed/chennai_accident_severity_modeling_dataset.csv` contains 5,035 generated event-level rows calibrated to 2021 aggregate totals and other marginal distributions. These rows are synthetic; they are not observed individual crash records. The saved feature matrix, models, predictions, metrics, plots, hotspot results, dashboard analyses, and reports derived from those rows are therefore illustrative outputs, not empirical findings about crash-level patterns in Chennai.

In particular, the repository's event-level severity associations, weather and infrastructure comparisons, classifier scores, SHAP explanations, and crash hotspot locations must not be interpreted as measured local effects or used to guide policy. The annual source aggregates can support aggregate trend descriptions, subject to the source documentation and known data limitations.

Several existing reports and dashboard labels still describe generated results as empirical. This notice supersedes those descriptions. A valid crash-level analysis requires genuine incident-level records with documented provenance and appropriate location/time fields, followed by recomputation of every derived result.

## Reproducibility status

The dashboard can display the saved artifacts, but that does not validate their empirical meaning. The full collection and analysis pipeline has not been verified end to end; the collection runner also has a known method-name mismatch. No automated test suite was run as part of the project audit.
