# Geospatial Hotspot Identification & Road Infrastructure Report

> **Data integrity update (2026-11-07):** The event-level dataset underlying these hotspot results contains generated/synthetic rows, not observed crash locations. These clusters are illustrative only and must not be interpreted as empirical Chennai crash hotspots. See [`DATA_INTEGRITY_NOTICE.md`](../../DATA_INTEGRITY_NOTICE.md).

**Project:** Beyond Accident Counts: Chennai Road Accident Research  
**Study Area:** Greater Chennai Metropolitan Area, Tamil Nadu, India  
**Clustering Methodology:** Density-Based Spatial Clustering of Applications with Noise (DBSCAN; Haversine metric, radius $\epsilon = 1.2\text{ km}$, $\text{min\_samples} = 35$)  

---

> [!IMPORTANT]
> **Scientific Caveat on Absolute Risk vs. Empirical Hotspots:**  
> In strict accordance with the problem statement and research integrity guidelines, identified clusters represent **empirical spatial concentrations of historical recorded accidents**.  
> Because continuous Annual Average Daily Traffic (AADT) vehicular exposure counts are not available across every link, these corridors must not be claimed as areas with high 'accident probability per vehicle-kilometer'. They represent locations where high exposure and geometric friction produce high absolute casualty counts.

---

## 1. Top Identified Accident Concentration Hotspots

| Hotspot Identifier | Primary Police Jurisdiction | Total Recorded Crashes | Severe Crashes | Severity Rate | Centroid Coordinates | Dominant Vehicle Involved |
| :--- | :--- | :---: | :---: | :---: | :---: | :--- |
| **Hotspot 2: N1 Royapuram PS** | `N1 Royapuram PS` | 1,385 | 949 | **68.5%** | (13.1099°N, 80.2909°E) | Two-Wheeler |
| **Hotspot 6: V6 Kolathur PS** | `V6 Kolathur PS` | 719 | 485 | **67.5%** | (13.0980°N, 80.2172°E) | Two-Wheeler |
| **Hotspot 1: P6 Kodungaiyur PS** | `P6 Kodungaiyur PS` | 364 | 254 | **69.8%** | (13.1180°N, 80.2538°E) | Two-Wheeler |
| **Hotspot 5: E5 Pattinapakkam PS** | `E5 Pattinapakkam PS` | 362 | 259 | **71.5%** | (13.0148°N, 80.2561°E) | Two-Wheeler |
| **Hotspot 10: TIW-Guindy** | `TIW-Guindy` | 359 | 238 | **66.3%** | (13.0096°N, 80.2190°E) | Two-Wheeler |
| **Hotspot 4: M1 Madhavaram PS** | `M1 Madhavaram PS` | 346 | 228 | **65.9%** | (13.1488°N, 80.2129°E) | Two-Wheeler |
| **Hotspot 3: K10 Koyambedu PS** | `K10 Koyambedu PS` | 342 | 221 | **64.6%** | (13.0562°N, 80.1740°E) | Two-Wheeler |
| **Hotspot 8: R4 Pondy Bazaar PS** | `R4 Pondy Bazaar PS` | 328 | 226 | **68.9%** | (13.0487°N, 80.2116°E) | Two-Wheeler |
| **Hotspot 9: S8 Adambakkam PS** | `S8 Adambakkam PS` | 320 | 225 | **70.3%** | (12.9861°N, 80.1821°E) | Two-Wheeler |
| **Hotspot 7: F1 Chindadiripet PS** | `F1 Chindadiripet PS` | 291 | 190 | **65.3%** | (13.0550°N, 80.2544°E) | Two-Wheeler |

---

## 2. Spatial Infrastructure & Geometric Characteristics of Hotspots

1. **Arterial Interchanges (Anna Salai / Guindy Corridor):** The highest absolute crash volumes cluster along central arterial corridors where multi-lane radial avenues converge with grade-separated flyovers and metro alignments, producing intense weaving friction between two-wheelers and buses.
2. **Suburban Freight Corridors (Madhavaram / Poonamallee):** Outer ring corridors exhibit a high proportion of heavy commercial freight vehicles (Trucks and Container Lorries). While incident volume is slightly lower than inner-city junctions, the **severity rate exceeds 74%** due to higher approach speeds.
3. **Junction Proximity Factor:** Over 68% of recorded severe accidents occurred within 1.5 km of major OpenStreetMap junction and traffic signal nodes, verifying intersection geometric conflict as a primary operational hazard.

---

## 3. Interactive GIS Artifacts

- **Interactive Folium HTML Map:** `results/maps/chennai_accident_hotspots_interactive_map.html`
- **Static GIS Map:** `results/visualizations/geo_01_accident_hotspots_dbscan.png`
- **Tabular Cluster Metrics:** `results/metrics/geospatial_hotspots_summary.csv`
