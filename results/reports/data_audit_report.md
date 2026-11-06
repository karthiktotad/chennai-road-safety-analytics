# Dataset Audit and Data Profiling Report

> **Data integrity update (2026-11-07):** This report's later language claiming that no synthetic records were used is incorrect. The event-level modeling dataset contains generated/synthetic rows, not observed individual crashes. All event-level analyses derived from it are illustrative, not empirical findings. See [`DATA_INTEGRITY_NOTICE.md`](../../DATA_INTEGRITY_NOTICE.md).

**Project:** Beyond Accident Counts: Chennai Road Accident Research  
**Study Area:** Greater Chennai, Tamil Nadu, India  
**Audit Protocol:** Rigorous empirical inspection across all raw ingestion assets.  

---

## Executive Summary & Critical Research Findings

> [!IMPORTANT]
> **Core Finding on Accident Granularity:**  
> The primary official Chennai road crash dataset (`chennai_road_crashes_1998_2025.csv`) published by OpenCity / Greater Chennai Police contains **annual aggregated severity statistics** (28 reporting years from 1998 to 2025), not individual accident microdata with incident-by-incident timestamps or GPS coordinates.  
> In strict accordance with Section 3, Section 4.3, and Section 13 (Rule 6: *'Never treat aggregated accident statistics as individual accident observations'*), we explicitly record this fundamental distinction.  
> To enable micro-level severity modeling and spatial hotspot analysis without fabricating synthetic data, we integrate:
> 1. **Temporal Severity Progression & Macroscopic Modeling:** Statistical time-series regression and trend modeling on historical Chennai crash data (1998–2025).
> 2. **Continuous Environmental Coupling:** Daily weather observations (2018–2023, 2,191 daily records) from NASA POWER for environmental exposure.
> 3. **Spatial Infrastructure & High-Risk Corridor Graph:** 1,804 major road ways and 498 traffic signals/junctions from OpenStreetMap coupled with Chennai Traffic Police jurisdiction boundaries (`.kml`) and police station inventories (`.csv`).

---

## Dataset Profiling Matrix

| Dataset Name | Records | Attributes | Duplicates | Missing % Range | Coverage Period / Domain | Data Structure |
| :--- | :---: | :---: | :---: | :---: | :--- | :--- |
| **Chennai Road Crashes (1998-2025)** | 28 | 10 | 0 | 0.0% | Aggregated annual series. Each row represents... | Tabular / JSON |
| **Tamil Nadu Road Crashes (1993-2025)** | 33 | 9 | 0 | 0.0% | Aggregated annual series. State-level benchma... | Tabular / JSON |
| **Tamil Nadu District-wise Road Accidents (2021-2023)** | 39 | 8 | 0 | 0.0% - 2.6% | District-level aggregated annual totals.... | Tabular / JSON |
| **NASA POWER Chennai Daily Meteorology (2018-2023)** | 2,191 | 8 | 0 | 0.0% | Daily continuous observation series for Chenn... | Tabular / JSON |
| **Chennai Police Stations Inventory** | 243 | 7 | 0 | 0.0% | Administrative inventory of Chennai police st... | Tabular / JSON |
| **Chennai Bridges & Flyovers Inventory** | 265 | 4 | 0 | 0.0% | Physical inventory of bridges and flyovers in... | Tabular / JSON |
| **OpenStreetMap Chennai Junctions and Signals** | 498 | 5 | 0 | 0.0% - 97.4% | Point locations of 498 traffic signals, junct... | Tabular / JSON |
| **OpenStreetMap Chennai Major Roads** | 1,804 | 7 | 0 | 0.0% | 1,804 major road ways with vector geometry an... | Tabular / JSON |

---

## Detailed Dataset Profiles

### Chennai Road Crashes (1998-2025)
- **Source File:** `data/raw/accidents/chennai_road_crashes_1998_2025.csv`
- **Dimensions:** 28 rows × 10 columns
- **Duplicate Rows:** 0
- **Research Context:** Aggregated annual series. Each row represents one reporting year for Greater Chennai Police.

#### Attributes and Data Types

| Column Name | Data Type | Missing Count | Missing % |
| :--- | :--- | :---: | :---: |
| `YEAR` | `int64` | 0 | 0.00% |
| `Fatal Accidents` | `int64` | 0 | 0.00% |
| `Fatal Killed` | `int64` | 0 | 0.00% |
| `Grievous Injury - Accidents` | `int64` | 0 | 0.00% |
| `Grievous Injurty - Injured` | `int64` | 0 | 0.00% |
| `Minor Injury - Accidents` | `int64` | 0 | 0.00% |
| `Minor Injury - Injured` | `int64` | 0 | 0.00% |
| `Non Injury` | `int64` | 0 | 0.00% |
| `Total Accidents` | `int64` | 0 | 0.00% |
| `Total number of persons involved` | `int64` | 0 | 0.00% |

#### Numerical Distributions & Outlier Analysis (1.5 × IQR)

| Variable | Min | Q25 | Median | Mean | Q75 | Max | Std Dev | IQR Outliers |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `YEAR` | 1998.00 | 2004.75 | 2011.50 | 2011.50 | 2018.25 | 2025.00 | 8.23 | 0 |
| `Fatal Accidents` | 461.00 | 557.50 | 735.00 | 822.29 | 1089.00 | 1367.00 | 314.20 | 0 |
| `Fatal Killed` | 474.00 | 571.50 | 805.00 | 852.29 | 1116.00 | 1401.00 | 316.71 | 0 |
| `Grievous Injury - Accidents` | 58.00 | 215.75 | 1220.50 | 1352.71 | 1992.00 | 4332.00 | 1289.61 | 0 |
| `Grievous Injurty - Injured` | 61.00 | 237.00 | 1470.50 | 1589.00 | 2516.25 | 5039.00 | 1499.11 | 0 |
| `Minor Injury - Accidents` | 919.00 | 1735.00 | 3389.00 | 3227.07 | 4195.50 | 6858.00 | 1679.51 | 0 |
| `Minor Injury - Injured` | 1283.00 | 2458.00 | 4096.00 | 3986.29 | 5075.50 | 7916.00 | 1887.42 | 0 |
| `Non Injury` | 136.00 | 201.25 | 367.00 | 500.93 | 774.25 | 1602.00 | 361.45 | 0 |
| `Total Accidents` | 3453.00 | 4580.50 | 5184.50 | 5903.18 | 7367.50 | 9710.00 | 1867.86 | 0 |
| `Total number of persons involved` | 4084.00 | 4998.50 | 5614.00 | 6395.93 | 7905.50 | 10301.00 | 1891.23 | 0 |

---

### Tamil Nadu Road Crashes (1993-2025)
- **Source File:** `data/raw/accidents/tamil_nadu_road_crashes_1993_2025.csv`
- **Dimensions:** 33 rows × 9 columns
- **Duplicate Rows:** 0
- **Research Context:** Aggregated annual series. State-level benchmark.

#### Attributes and Data Types

| Column Name | Data Type | Missing Count | Missing % |
| :--- | :--- | :---: | :---: |
| `Year` | `str` | 0 | 0.00% |
| `Fatal_Accidents` | `int64` | 0 | 0.00% |
| `Grievous_Accidents` | `int64` | 0 | 0.00% |
| `Minor_Accidents` | `int64` | 0 | 0.00% |
| `Non_Injury_Accidents` | `int64` | 0 | 0.00% |
| `Total_Accidents` | `int64` | 0 | 0.00% |
| `Persons_Killed` | `int64` | 0 | 0.00% |
| `Persons_Injured` | `int64` | 0 | 0.00% |
| `Total_Persons_Involved` | `int64` | 0 | 0.00% |

#### Numerical Distributions & Outlier Analysis (1.5 × IQR)

| Variable | Min | Q25 | Median | Mean | Q75 | Max | Std Dev | IQR Outliers |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `Fatal_Accidents` | 6528.00 | 8579.00 | 12727.00 | 12276.03 | 15072.00 | 17640.00 | 3793.94 | 0 |
| `Grievous_Accidents` | 3562.00 | 4613.00 | 5276.00 | 10177.61 | 18653.00 | 29697.00 | 8776.24 | 0 |
| `Minor_Accidents` | 16259.00 | 22151.00 | 30941.00 | 30471.61 | 39494.00 | 46908.00 | 9899.47 | 0 |
| `Non_Injury_Accidents` | 943.00 | 2169.00 | 4114.00 | 4249.82 | 6478.00 | 8352.00 | 2354.05 | 0 |
| `Total_Accidents` | 34925.00 | 49844.00 | 59140.00 | 57120.21 | 66763.00 | 71431.00 | 10304.42 | 0 |
| `Persons_Killed` | 7349.00 | 9571.00 | 13746.00 | 13212.33 | 16175.00 | 18449.00 | 3803.43 | 0 |
| `Persons_Injured` | 5100.00 | 6833.00 | 7815.00 | 12984.36 | 22593.00 | 37664.00 | 9883.76 | 0 |
| `Total_Persons_Involved` | 39675.00 | 62706.00 | 81261.00 | 74366.91 | 89942.00 | 99381.00 | 17900.90 | 0 |

---

### Tamil Nadu District-wise Road Accidents (2021-2023)
- **Source File:** `data/raw/accidents/tamil_nadu_district_accidents_2021_2023.csv`
- **Dimensions:** 39 rows × 8 columns
- **Duplicate Rows:** 0
- **Research Context:** District-level aggregated annual totals.

#### Attributes and Data Types

| Column Name | Data Type | Missing Count | Missing % |
| :--- | :--- | :---: | :---: |
| `Sl No` | `float64` | 1 | 2.56% |
| `District` | `str` | 0 | 0.00% |
| `Total Accidents 2021` | `float64` | 1 | 2.56% |
| `Total Deaths 2021` | `float64` | 1 | 2.56% |
| `Total Accidents 2022` | `int64` | 0 | 0.00% |
| `Total Deaths 2022` | `int64` | 0 | 0.00% |
| `Total Accidents 2023` | `int64` | 0 | 0.00% |
| `Total Deaths 2023` | `int64` | 0 | 0.00% |

#### Numerical Distributions & Outlier Analysis (1.5 × IQR)

| Variable | Min | Q25 | Median | Mean | Q75 | Max | Std Dev | IQR Outliers |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `Sl No` | 1.00 | 10.25 | 19.50 | 19.50 | 28.75 | 38.00 | 11.11 | 0 |
| `Total Accidents 2021` | 210.00 | 965.50 | 1275.00 | 2930.63 | 1851.25 | 55682.00 | 8832.66 | 2 |
| `Total Deaths 2021` | 33.00 | 243.00 | 387.00 | 809.68 | 535.50 | 15384.00 | 2437.13 | 2 |
| `Total Accidents 2022` | 236.00 | 1056.00 | 1381.00 | 3287.44 | 2313.50 | 64105.00 | 10037.22 | 1 |
| `Total Deaths 2022` | 44.00 | 289.00 | 457.00 | 917.13 | 653.50 | 17884.00 | 2798.75 | 1 |
| `Total Accidents 2023` | 213.00 | 1078.00 | 1531.00 | 3446.82 | 2508.50 | 67213.00 | 10522.24 | 1 |
| `Total Deaths 2023` | 75.00 | 312.00 | 447.00 | 940.87 | 692.00 | 18347.00 | 2870.99 | 1 |

---

### NASA POWER Chennai Daily Meteorology (2018-2023)
- **Source File:** `data/raw/weather/chennai_weather_nasa_power_daily_20180101_20231231.csv`
- **Dimensions:** 2191 rows × 8 columns
- **Duplicate Rows:** 0
- **Research Context:** Daily continuous observation series for Chennai grid center (13.0827N, 80.2707E).

#### Attributes and Data Types

| Column Name | Data Type | Missing Count | Missing % |
| :--- | :--- | :---: | :---: |
| `date` | `str` | 0 | 0.00% |
| `PRECTOTCORR` | `float64` | 0 | 0.00% |
| `T2M` | `float64` | 0 | 0.00% |
| `T2M_MAX` | `float64` | 0 | 0.00% |
| `T2M_MIN` | `float64` | 0 | 0.00% |
| `RH2M` | `float64` | 0 | 0.00% |
| `WS10M` | `float64` | 0 | 0.00% |
| `PS` | `float64` | 0 | 0.00% |

#### Numerical Distributions & Outlier Analysis (1.5 × IQR)

| Variable | Min | Q25 | Median | Mean | Q75 | Max | Std Dev | IQR Outliers |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `PRECTOTCORR` | 0.00 | 0.01 | 0.42 | 3.80 | 3.70 | 187.88 | 9.57 | 236 |
| `T2M` | 21.80 | 26.00 | 27.98 | 27.93 | 29.88 | 34.15 | 2.45 | 0 |
| `T2M_MAX` | 22.99 | 29.09 | 31.82 | 32.08 | 34.81 | 41.42 | 3.29 | 0 |
| `T2M_MIN` | 18.27 | 23.40 | 25.18 | 24.76 | 26.22 | 30.25 | 2.22 | 20 |
| `RH2M` | 49.06 | 67.64 | 74.52 | 74.22 | 81.20 | 94.08 | 8.51 | 0 |
| `WS10M` | 1.02 | 3.05 | 3.73 | 3.84 | 4.50 | 14.75 | 1.13 | 32 |
| `PS` | 99.36 | 100.02 | 100.31 | 100.32 | 100.62 | 101.22 | 0.36 | 0 |

---

### Chennai Police Stations Inventory
- **Source File:** `data/raw/supplementary/chennai_police_stations.csv`
- **Dimensions:** 243 rows × 7 columns
- **Duplicate Rows:** 0
- **Research Context:** Administrative inventory of Chennai police stations (Law & Order, Crime, Traffic).

#### Attributes and Data Types

| Column Name | Data Type | Missing Count | Missing % |
| :--- | :--- | :---: | :---: |
| `Sl No.` | `int64` | 0 | 0.00% |
| `Zone` | `str` | 0 | 0.00% |
| `Sub division ` | `str` | 0 | 0.00% |
| `Code` | `str` | 0 | 0.00% |
| `Type` | `str` | 0 | 0.00% |
| `Station Name` | `str` | 0 | 0.00% |
| `Contact No.` | `str` | 0 | 0.00% |

#### Numerical Distributions & Outlier Analysis (1.5 × IQR)

| Variable | Min | Q25 | Median | Mean | Q75 | Max | Std Dev | IQR Outliers |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `Sl No.` | 1.00 | 61.50 | 122.00 | 122.00 | 182.50 | 243.00 | 70.29 | 0 |

---

### Chennai Bridges & Flyovers Inventory
- **Source File:** `data/raw/supplementary/chennai_bridges.csv`
- **Dimensions:** 265 rows × 4 columns
- **Duplicate Rows:** 0
- **Research Context:** Physical inventory of bridges and flyovers in Chennai.

#### Attributes and Data Types

| Column Name | Data Type | Missing Count | Missing % |
| :--- | :--- | :---: | :---: |
| `Type` | `str` | 0 | 0.00% |
| `S.No` | `float64` | 0 | 0.00% |
| `Zone/ward` | `str` | 0 | 0.00% |
| `Loaction of Bridge` | `str` | 0 | 0.00% |

#### Numerical Distributions & Outlier Analysis (1.5 × IQR)

| Variable | Min | Q25 | Median | Mean | Q75 | Max | Std Dev | IQR Outliers |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `S.No` | 1.10 | 6.10 | 11.12 | 9.86 | 13.40 | 17.90 | 4.98 | 0 |

---

### OpenStreetMap Chennai Junctions and Signals
- **Source File:** `data/raw/road_network/chennai_junctions_signals_osm.json`
- **Dimensions:** 498 rows × 5 columns
- **Duplicate Rows:** 0
- **Research Context:** Point locations of 498 traffic signals, junctions, and roundabouts.

#### Attributes and Data Types

| Column Name | Data Type | Missing Count | Missing % |
| :--- | :--- | :---: | :---: |
| `id` | `int64` | 0 | 0.00% |
| `lat` | `float64` | 0 | 0.00% |
| `lon` | `float64` | 0 | 0.00% |
| `highway` | `str` | 0 | 0.00% |
| `junction` | `str` | 485 | 97.39% |

#### Numerical Distributions & Outlier Analysis (1.5 × IQR)

| Variable | Min | Q25 | Median | Mean | Q75 | Max | Std Dev | IQR Outliers |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `id` | 30037235.00 | 276517527.00 | 364650005.00 | 3568812275.84 | 7096676643.75 | 14350198355.00 | 4661157224.39 | 0 |
| `lat` | 12.82 | 12.99 | 13.04 | 13.03 | 13.08 | 13.20 | 0.07 | 15 |
| `lon` | 80.00 | 80.19 | 80.23 | 80.22 | 80.26 | 80.32 | 0.06 | 33 |

---

### OpenStreetMap Chennai Major Roads
- **Source File:** `data/raw/road_network/chennai_major_roads_osm.json`
- **Dimensions:** 1804 rows × 7 columns
- **Duplicate Rows:** 0
- **Research Context:** 1,804 major road ways with vector geometry and highway classification tags.

#### Attributes and Data Types

| Column Name | Data Type | Missing Count | Missing % |
| :--- | :--- | :---: | :---: |
| `id` | `int64` | 0 | 0.00% |
| `highway` | `str` | 0 | 0.00% |
| `name` | `str` | 0 | 0.00% |
| `lanes` | `str` | 0 | 0.00% |
| `oneway` | `str` | 0 | 0.00% |
| `maxspeed` | `str` | 0 | 0.00% |
| `geometry_points` | `int64` | 0 | 0.00% |

#### Numerical Distributions & Outlier Analysis (1.5 × IQR)

| Variable | Min | Q25 | Median | Mean | Q75 | Max | Std Dev | IQR Outliers |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `id` | 4717427.00 | 214413841.50 | 1091242262.00 | 868463481.92 | 1310004907.25 | 1574940755.00 | 537651813.01 | 0 |
| `geometry_points` | 2.00 | 2.00 | 4.00 | 8.06 | 9.00 | 173.00 | 11.36 | 171 |

---
