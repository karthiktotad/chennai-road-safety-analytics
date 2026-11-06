# Data Sources Registry

This document catalogs all datasets retrieved, integrated, and evaluated for the Chennai Road Accident Risk Analysis and Severity Prediction research project.

---

## 1. Chennai Road Accident Records

### A. Chennai Road Crashes Data (1998–2025)
- **Source Organization:** OpenCity India / Greater Chennai Police
- **Original Download URL:** https://data.opencity.in/dataset/2c742a2c-c559-4d9c-9987-8566aadb933c/resource/29162b87-f1a7-4011-b309-b14d904f9a7d/download/chennai-road-crashes-1998-2025.csv
- **Local File:** `data/raw/accidents/chennai_road_crashes_1998_2025.csv` (1.50 KB)
- **Official Report:** `data/raw/accidents/chennai_road_crashes_1998_2025_report.pdf` (28.97 KB)
- **Download Date:** 2026-11-06
- **Geographic Coverage:** Greater Chennai Police Commissionerate jurisdiction.
- **Historical Coverage:** 1998 – 2025 (Annual series; 28 reporting periods).
- **Frequency:** Annual aggregated severity statistics.
- **Variables:**
  - `YEAR`: Reporting year (1998–2025)
  - `Fatal Accidents`: Count of fatal accident incidents
  - `Fatal Killed`: Number of persons killed in fatal accidents
  - `Grievous Injury - Accidents`: Count of grievous injury accident incidents
  - `Grievous Injurty - Injured`: Persons grievously injured
  - `Minor Injury - Accidents`: Count of minor injury accident incidents
  - `Minor Injury - Injured`: Persons sustaining minor injuries
  - `Non Injury`: Property damage / non-injury accidents
  - `Total Accidents`: Total reported road accidents
  - `Total number of persons involved`: Total victims and involved individuals
- **Data Format:** CSV
- **Known Limitations:** Annual aggregated series by police commissionerate; does not contain individual incident microdata (individual crash timestamp or GPS coordinates per row).
- **License / Terms of Use:** Open Access (OpenCity / Greater Chennai Police).

### B. Tamil Nadu Road Crashes Data (1993–2025)
- **Source Organization:** OpenCity India / Tamil Nadu State Crime Records Bureau
- **Original Download URL:** https://data.opencity.in/dataset/2c742a2c-c559-4d9c-9987-8566aadb933c/resource/c1fe08c4-9871-4c0b-b79b-c446f24f2c03/download/tn-road-crashes-1993-2025.csv
- **Local File:** `data/raw/accidents/tamil_nadu_road_crashes_1993_2025.csv` (1.79 KB)
- **Download Date:** 2026-11-06
- **Geographic Coverage:** Tamil Nadu State.
- **Historical Coverage:** 1993 – 2025 (33 reporting years).
- **Variables:** `YEAR`, `Fatal Accidents`, `Fatal Killed`, `Grievous Injury - Accidents`, `Grievous Injury - Injured`, `Minor Injury - Accidents`, `Minor Injury - Injured`, `Non Injury`, `Total Accidents`, `Total number of persons involved`.

### C. Tamil Nadu District-wise Road Accidents (2021–2023)
- **Source Organization:** OpenCity India / Tamil Nadu State Police
- **Original Download URL:** https://data.opencity.in/dataset/2fc34e49-936f-4255-a4c3-1ef92f25adf3/resource/764579ad-22e0-4f27-a694-34d0d2f843ea/download/d23e7ba9-6a60-41db-b37b-62413cc72365.csv
- **Local File:** `data/raw/accidents/tamil_nadu_district_accidents_2021_2023.csv` (1.69 KB)
- **Download Date:** 2026-11-06
- **Geographic Coverage:** All 38 Tamil Nadu districts including Chennai City.
- **Variables:** `Sl No`, `District`, `Total Accidents 2021`, `Total Deaths 2021`, `Total Accidents 2022`, `Total Deaths 2022`, `Total Accidents 2023`, `Total Deaths 2023`.

---

## 2. Atmospheric & Meteorological Data

### NASA POWER Daily Point Meteorology (Chennai)
- **Source Organization:** National Aeronautics and Space Administration (NASA) - Langley Research Center
- **Original Download URL:** https://power.larc.nasa.gov/api/temporal/daily/point
- **Local Files:**
  - `data/raw/weather/chennai_weather_nasa_power_daily_20180101_20231231.csv` (109 KB)
  - `data/raw/weather/chennai_weather_nasa_power_20180101_20231231_20261106_200330.json` (401 KB)
- **Download Date:** 2026-11-06
- **Geographic Coverage:** Chennai City Center Grid Point ($13.0827^\circ\text{ N}, 80.2707^\circ\text{ E}$).
- **Historical Coverage:** 2018-01-01 to 2023-12-31 (2,191 continuous daily observations).
- **Frequency:** Daily.
- **Units & Variables:**
  - `date`: Calendar date (`YYYY-MM-DD`)
  - `PRECTOTCORR`: Precipitation corrected ($mm/day$)
  - `T2M`: Daily Mean Temperature at 2m ($^\circ C$)
  - `T2M_MAX`: Maximum Temperature at 2m ($^\circ C$)
  - `T2M_MIN`: Minimum Temperature at 2m ($^\circ C$)
  - `RH2M`: Relative Humidity at 2m ($\%$)
  - `WS10M`: Wind Speed at 10m ($m/s$)
  - `PS`: Surface Atmospheric Pressure ($kPa$)
- **Data Format:** CSV & JSON
- **Known Limitations:** Grid-cell level reanalysis (~0.5° spatial resolution); local micro-urban rainfall variations are spatially integrated.
- **License / Terms of Use:** NASA Open Data Policy (Public Domain).

---

## 3. Road Infrastructure & Spatial Geometry Data

### A. OpenStreetMap Road Network (Chennai Major Roads)
- **Source Organization:** OpenStreetMap Foundation & Contributors
- **Endpoint:** Overpass API (`https://overpass-api.de/api/interpreter`)
- **Local File:** `data/raw/road_network/chennai_major_roads_osm.json` (1.2 MB)
- **Download Date:** 2026-11-06
- **Geographic Coverage:** Chennai Metropolitan Bounding Box ($12.95^\circ\text{ N} - 13.18^\circ\text{ N}, 80.12^\circ\text{ E} - 80.30^\circ\text{ E}$).
- **Contents:** 1,804 major road ways (motorway, trunk, primary) with line geometries and highway attributes.
- **Data Format:** OSM JSON
- **License / Terms of Use:** Open Database License (ODbL).

### B. OpenStreetMap Junctions and Traffic Signals
- **Local File:** `data/raw/road_network/chennai_junctions_signals_osm.json` (64 KB)
- **Download Date:** 2026-11-06
- **Contents:** 498 junction nodes, traffic signals, and roundabouts in Chennai with precise latitude and longitude coordinates.

### C. Chennai Traffic Police Jurisdictions (Vector Polygons)
- **Source Organization:** Tamil Nadu Police / OpenCity
- **Original Download URL:** https://data.opencity.in/dataset/fbc38d27-c621-42ba-ae0e-b9fa9463f394/resource/14c3bedd-bb59-49ed-ab80-c5fb93fafcd6/download/chennai_traffic_police_jurisdictions.kml
- **Local File:** `data/raw/supplementary/chennai_traffic_police_jurisdictions.kml` (130 KB)
- **Contents:** Spatial polygon boundaries for all traffic police jurisdictions across Greater Chennai.

### D. Chennai Police Stations Registry
- **Local File:** `data/raw/supplementary/chennai_police_stations.csv` (14 KB)
- **Contents:** List of all Law & Order, Crime, and Traffic police stations in Chennai with division codes and zones.

### E. Chennai Bridges Infrastructure
- **Local File:** `data/raw/supplementary/chennai_bridges.csv` (31 KB)
- **Contents:** Inventory of road bridges, flyovers, and rail overbridges across Chennai.

### F. Tamil Nadu District Vehicle Registrations (2022–2023)
- **Local File:** `data/raw/supplementary/tn_district_non_commercial_vehicles_2022_23.csv` (6.1 KB)
- **Contents:** District-level private vehicle population for exposure analysis.
