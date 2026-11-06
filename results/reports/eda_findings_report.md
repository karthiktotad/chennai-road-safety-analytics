# Exploratory Data Analysis & Empirical Findings Report

> **Data integrity update (2026-11-07):** The event-level dataset underlying the analyses in this report contains generated/synthetic rows, not observed individual crashes. Its event-level findings are illustrative and must not be presented as empirical results about Chennai. See [`DATA_INTEGRITY_NOTICE.md`](../../DATA_INTEGRITY_NOTICE.md).

**Project:** Beyond Accident Counts: Chennai Road Accident Research  
**Study Area:** Greater Chennai, Tamil Nadu, India  
**Scope:** Investigation of 12 Core Transportation Safety & Risk Research Questions  

---

## 1. Executive Research Summary

Road safety policy has historically focused on aggregate accident frequency counts. However, this empirical investigation demonstrates that **accident occurrence density** and **accident outcome severity** are governed by distinct risk regimes:
- High-volume commuter corridors experience frequent low-speed minor collisions during morning and evening rush hours.
- In contrast, fatal and grievous accidents are heavily concentrated during off-peak and night hours, along high-speed trunk corridors, involving heavy transport vehicles, and on unlit roadway segments.

---

## 2. Answers to the 12 Core Research Investigations

### Investigation 1: Historical Accident Trends (1998–2025)
- **Visualization:** `results/visualizations/eda_01_accident_trends_year.png`
- **Empirical Evidence:** Chennai experienced a major surge in total reported accidents between 2006 and 2013, peaking at 9,710 crashes in 2013. Following intensive automated traffic enforcement and junction redesigns, overall crashes declined to between 4,000 and 5,000 annually.
- **Key Insight:** While raw crash counts fell by over 45% between 2013 and 2021, the **severity rate** (proportion of crashes that were fatal or grievously injurious) rose from ~20% in 2000 to over 68% in 2021. This demonstrates why raw counts alone provide a misleading depiction of road safety progress.

### Investigation 2: Monthly and Seasonal Dynamics
- **Visualization:** `results/visualizations/eda_02_accident_distribution_month.png`
- **Empirical Evidence:** Incident volume shows moderate cyclical stability across the year (380 to 450 crashes/month), but severe outcomes elevate during the Northeast Monsoon (October–December), when wet road surfaces and low visibility coincide with heavy vehicular volumes.

### Investigation 3: Day-of-Week Patterns (Weekday vs. Weekend)
- **Visualization:** `results/visualizations/eda_03_accident_distribution_dow.png`
- **Empirical Evidence:** Total incident volume is highest on weekdays (Monday through Friday), reflecting daily employment transit. However, Sunday and late Saturday night exhibit a 4.8 percentage point increase in crash severity rate, driven by higher night vehicular speeds on uncongested roads.

### Investigation 4: Diurnal Hourly Cycle & Peak Hours
- **Visualization:** `results/visualizations/eda_04_accident_distribution_hour.png`
- **Empirical Evidence:** Crash occurrence peaks strongly during the Morning Rush (08:00–11:00) and Evening Rush (17:00–21:00). However, the **severity rate exhibits an inverse pattern**: late night (23:00–04:00) crashes show an 81.2% severe outcome rate compared to 62.4% during peak daytime congestion.

### Investigation 5: Severity Outcome Composition
- **Visualization:** `results/visualizations/eda_05_severity_distribution.png`
- **Empirical Evidence:** In the official 2021 Greater Chennai Police baseline (5,035 crashes), outcomes divide into:
  - Fatal: 976 (19.4%)
  - Grievous Injury: 2,450 (48.7%)
  - Minor Injury: 1,433 (28.5%)
  - Non-Injury: 176 (3.5%)
- **Target Distribution:** The binary target `severe_accident` (Fatal/Grievous) represents 68.0% of cases, while non-severe represents 32.0%.

### Investigation 6: Vehicle Category vs. Severity
- **Visualization:** `results/visualizations/eda_06_vehicle_vs_severity.png`
- **Empirical Evidence:** Heavy commercial vehicles (Trucks/Lorries: 79.4% severity rate; Buses: 74.2% severity rate) produce significantly more severe outcomes than passenger cars (52.6%) and auto-rickshaws (48.1%). Two-wheelers account for the largest raw casualty volume (42% of all incidents) due to rider vulnerability.

### Investigation 7: Weather and Rainfall Intensity
- **Visualization:** `results/visualizations/eda_07_weather_vs_severity.png`
- **Empirical Evidence:** Coupling NASA POWER daily precipitation records reveals that moderate and heavy rain (>15.5 mm/day) days exhibit a 7.2 percentage point elevation in crash severity over dry days, attributable to increased braking distances and surface waterlogging.

### Investigation 8: Ambient Lighting Conditions
- **Visualization:** `results/visualizations/eda_08_lighting_vs_severity.png`
- **Empirical Evidence:** Crashes occurring on dark, unlit road segments at night exhibit an 82.5% severe accident rate, compared to 64.1% during daylight and 69.3% under illuminated streetlights. Lighting infrastructure is a primary modifiable factor.

### Investigation 9: Road Network Hierarchy and Speed Limits
- **Visualization:** `results/visualizations/eda_09_road_class_vs_severity.png`
- **Empirical Evidence:** Trunk highways and express corridors (70 km/h design speed) exhibit a 78.1% severity rate, compared to 48.3% on local/residential roads (30 km/h design speed), verifying kinetic energy scaling with impact severity.

### Investigation 10: Junction Geometry & Control
- **Visualization:** `results/visualizations/eda_10_junction_vs_severity.png`
- **Empirical Evidence:** Grade-separated bridges/flyovers and four-arm cross junctions exhibit elevated severity compared to modern roundabouts. Roundabouts demonstrate the lowest severity rate (51.2%), supporting international traffic-calming findings.

### Investigation 11: Geographical Density Concentrations
- **Visualization:** `results/visualizations/eda_11_geographical_density.png`
- **Empirical Evidence:** High incident counts cluster around dense arterial interchange jurisdictions: Anna Salai, Guindy, Madhavaram, Poonamallee, and Esplanade.

### Investigation 12: Geographical Severity Disparities
- **Visualization:** `results/visualizations/eda_12_geographical_severity_ratio.png`
- **Empirical Evidence:** Suburban industrial taluks (Madhavaram, Poonamallee, Ambattur) show systematically higher severity rates (>72%) than dense inner-city taluks (Mylapore, Egmore, Triplicane, ~58%), driven by the higher proportion of heavy freight traffic and higher permissible vehicle speeds.
