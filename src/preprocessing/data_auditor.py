"""
Data Quality and Profiling Auditor.
Inspects all raw collected datasets and produces a comprehensive data audit report.
Evaluates dimensions, data types, missingness, duplicates, distributions, and
distinguishes between aggregated statistics and individual incident observations.
"""

import json
import logging
from pathlib import Path
import pandas as pd
import numpy as np

from config.settings import (
    RAW_ACCIDENTS_DIR, RAW_WEATHER_DIR, RAW_ROAD_DIR,
    RAW_SUPPLEMENTARY_DIR, REPORTS_DIR
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


def audit_dataframe(df: pd.DataFrame, name: str, source_path: str, notes: str = "") -> dict:
    """Computes comprehensive audit metrics for a DataFrame."""
    audit = {
        "name": name,
        "source_path": source_path,
        "row_count": len(df),
        "column_count": len(df.columns),
        "columns": list(df.columns),
        "dtypes": {col: str(dtype) for col, dtype in df.dtypes.items()},
        "missing_counts": df.isna().sum().to_dict(),
        "missing_pcts": (df.isna().sum() / len(df) * 100).round(2).to_dict() if len(df) > 0 else {},
        "duplicate_rows": int(df.duplicated().sum()),
        "notes": notes,
        "numerical_summary": {},
        "sample_head": df.head(3).to_dict(orient="records")
    }

    num_cols = df.select_dtypes(include=[np.number]).columns
    for col in num_cols:
        series = df[col].dropna()
        if not series.empty:
            q25 = series.quantile(0.25)
            q75 = series.quantile(0.75)
            iqr = q75 - q25
            lower_bound = q25 - 1.5 * iqr
            upper_bound = q75 + 1.5 * iqr
            outliers_count = int(((series < lower_bound) | (series > upper_bound)).sum())

            audit["numerical_summary"][col] = {
                "min": float(series.min()),
                "q25": float(q25),
                "median": float(series.median()),
                "mean": float(series.mean()),
                "q75": float(q75),
                "max": float(series.max()),
                "std": float(series.std()),
                "iqr_outliers": outliers_count
            }

    return audit


def run_full_data_audit():
    logger.info("Executing full data audit across raw repositories...")
    audits = []

    # 1. Chennai Road Crashes (1998-2025)
    f1 = RAW_ACCIDENTS_DIR / "chennai_road_crashes_1998_2025.csv"
    if f1.exists():
        df1 = pd.read_csv(f1)
        # Strip potential BOM in headers
        df1.columns = [c.replace("\ufeff", "").strip() for c in df1.columns]
        audits.append(audit_dataframe(
            df1, "Chennai Road Crashes (1998-2025)", str(f1),
            notes="Aggregated annual series. Each row represents one reporting year for Greater Chennai Police."
        ))

    # 2. Tamil Nadu Road Crashes (1993-2025)
    f2 = RAW_ACCIDENTS_DIR / "tamil_nadu_road_crashes_1993_2025.csv"
    if f2.exists():
        df2 = pd.read_csv(f2)
        df2.columns = [c.replace("\ufeff", "").strip() for c in df2.columns]
        audits.append(audit_dataframe(
            df2, "Tamil Nadu Road Crashes (1993-2025)", str(f2),
            notes="Aggregated annual series. State-level benchmark."
        ))

    # 3. Tamil Nadu District-wise Accidents (2021-2023)
    f3 = RAW_ACCIDENTS_DIR / "tamil_nadu_district_accidents_2021_2023.csv"
    if f3.exists():
        df3 = pd.read_csv(f3)
        df3.columns = [c.replace("\ufeff", "").strip() for c in df3.columns]
        audits.append(audit_dataframe(
            df3, "Tamil Nadu District-wise Road Accidents (2021-2023)", str(f3),
            notes="District-level aggregated annual totals."
        ))

    # 4. NASA POWER Daily Weather
    f4 = RAW_WEATHER_DIR / "chennai_weather_nasa_power_daily_20180101_20231231.csv"
    if f4.exists():
        df4 = pd.read_csv(f4)
        audits.append(audit_dataframe(
            df4, "NASA POWER Chennai Daily Meteorology (2018-2023)", str(f4),
            notes="Daily continuous observation series for Chennai grid center (13.0827N, 80.2707E)."
        ))

    # 5. Chennai Police Stations
    f5 = RAW_SUPPLEMENTARY_DIR / "chennai_police_stations.csv"
    if f5.exists():
        df5 = pd.read_csv(f5)
        audits.append(audit_dataframe(
            df5, "Chennai Police Stations Inventory", str(f5),
            notes="Administrative inventory of Chennai police stations (Law & Order, Crime, Traffic)."
        ))

    # 6. Chennai Bridges
    f6 = RAW_SUPPLEMENTARY_DIR / "chennai_bridges.csv"
    if f6.exists():
        df6 = pd.read_csv(f6)
        audits.append(audit_dataframe(
            df6, "Chennai Bridges & Flyovers Inventory", str(f6),
            notes="Physical inventory of bridges and flyovers in Chennai."
        ))

    # 7. OpenStreetMap Junctions & Signals
    f7 = RAW_ROAD_DIR / "chennai_junctions_signals_osm.json"
    if f7.exists():
        with open(f7, "r") as f:
            osm_junc = json.load(f)
        elements = osm_junc.get("elements", [])
        junc_df = pd.DataFrame([{
            "id": el.get("id"),
            "lat": el.get("lat"),
            "lon": el.get("lon"),
            "highway": el.get("tags", {}).get("highway"),
            "junction": el.get("tags", {}).get("junction")
        } for el in elements])
        audits.append(audit_dataframe(
            junc_df, "OpenStreetMap Chennai Junctions and Signals", str(f7),
            notes="Point locations of 498 traffic signals, junctions, and roundabouts."
        ))

    # 8. OpenStreetMap Major Roads
    f8 = RAW_ROAD_DIR / "chennai_major_roads_osm.json"
    if f8.exists():
        with open(f8, "r") as f:
            osm_roads = json.load(f)
        elements = osm_roads.get("elements", [])
        roads_df = pd.DataFrame([{
            "id": el.get("id"),
            "highway": el.get("tags", {}).get("highway"),
            "name": el.get("tags", {}).get("name", "Unnamed"),
            "lanes": el.get("tags", {}).get("lanes", "Unknown"),
            "oneway": el.get("tags", {}).get("oneway", "Unknown"),
            "maxspeed": el.get("tags", {}).get("maxspeed", "Unknown"),
            "geometry_points": len(el.get("geometry", []))
        } for el in elements])
        audits.append(audit_dataframe(
            roads_df, "OpenStreetMap Chennai Major Roads", str(f8),
            notes="1,804 major road ways with vector geometry and highway classification tags."
        ))

    # Generate Markdown Audit Report
    report_path = REPORTS_DIR / "data_audit_report.md"
    generate_markdown_report(audits, report_path)
    logger.info(f"Data audit report generated successfully at {report_path}")

    return audits, report_path


def generate_markdown_report(audits, output_file: Path):
    """Formats audit dictionary into a publication-grade markdown document."""
    lines = [
        "# Dataset Audit and Data Profiling Report",
        "",
        "**Project:** Beyond Accident Counts: Chennai Road Accident Research  ",
        "**Study Area:** Greater Chennai, Tamil Nadu, India  ",
        "**Audit Protocol:** Rigorous empirical inspection across all raw ingestion assets.  ",
        "",
        "---",
        "",
        "## Executive Summary & Critical Research Findings",
        "",
        "> [!IMPORTANT]",
        "> **Core Finding on Accident Granularity:**  ",
        "> The primary official Chennai road crash dataset (`chennai_road_crashes_1998_2025.csv`) published by OpenCity / Greater Chennai Police contains **annual aggregated severity statistics** (28 reporting years from 1998 to 2025), not individual accident microdata with incident-by-incident timestamps or GPS coordinates.  ",
        "> In strict accordance with Section 3, Section 4.3, and Section 13 (Rule 6: *'Never treat aggregated accident statistics as individual accident observations'*), we explicitly record this fundamental distinction.  ",
        "> To enable micro-level severity modeling and spatial hotspot analysis without fabricating synthetic data, we integrate:",
        "> 1. **Temporal Severity Progression & Macroscopic Modeling:** Statistical time-series regression and trend modeling on historical Chennai crash data (1998–2025).",
        "> 2. **Continuous Environmental Coupling:** Daily weather observations (2018–2023, 2,191 daily records) from NASA POWER for environmental exposure.",
        "> 3. **Spatial Infrastructure & High-Risk Corridor Graph:** 1,804 major road ways and 498 traffic signals/junctions from OpenStreetMap coupled with Chennai Traffic Police jurisdiction boundaries (`.kml`) and police station inventories (`.csv`).",
        "",
        "---",
        "",
        "## Dataset Profiling Matrix",
        "",
        "| Dataset Name | Records | Attributes | Duplicates | Missing % Range | Coverage Period / Domain | Data Structure |",
        "| :--- | :---: | :---: | :---: | :---: | :--- | :--- |"
    ]

    for a in audits:
        max_missing = max(a["missing_pcts"].values()) if a["missing_pcts"] else 0.0
        min_missing = min(a["missing_pcts"].values()) if a["missing_pcts"] else 0.0
        missing_str = f"{min_missing:.1f}% - {max_missing:.1f}%" if min_missing != max_missing else f"{min_missing:.1f}%"
        lines.append(
            f"| **{a['name']}** | {a['row_count']:,} | {a['column_count']} | {a['duplicate_rows']} | {missing_str} | {a['notes'][:45]}... | Tabular / JSON |"
        )

    lines.extend([
        "",
        "---",
        "",
        "## Detailed Dataset Profiles",
        ""
    ])

    for a in audits:
        lines.extend([
            f"### {a['name']}",
            f"- **Source File:** `{a['source_path']}`",
            f"- **Dimensions:** {a['row_count']} rows × {a['column_count']} columns",
            f"- **Duplicate Rows:** {a['duplicate_rows']}",
            f"- **Research Context:** {a['notes']}",
            "",
            "#### Attributes and Data Types",
            "",
            "| Column Name | Data Type | Missing Count | Missing % |",
            "| :--- | :--- | :---: | :---: |"
        ])

        for col in a["columns"]:
            dtype = a["dtypes"].get(col, "unknown")
            mc = a["missing_counts"].get(col, 0)
            mp = a["missing_pcts"].get(col, 0.0)
            lines.append(f"| `{col}` | `{dtype}` | {mc} | {mp:.2f}% |")

        if a["numerical_summary"]:
            lines.extend([
                "",
                "#### Numerical Distributions & Outlier Analysis (1.5 × IQR)",
                "",
                "| Variable | Min | Q25 | Median | Mean | Q75 | Max | Std Dev | IQR Outliers |",
                "| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |"
            ])
            for col, stats in a["numerical_summary"].items():
                lines.append(
                    f"| `{col}` | {stats['min']:.2f} | {stats['q25']:.2f} | {stats['median']:.2f} | "
                    f"{stats['mean']:.2f} | {stats['q75']:.2f} | {stats['max']:.2f} | {stats['std']:.2f} | {stats['iqr_outliers']} |"
                )

        lines.extend(["", "---", ""])

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


if __name__ == "__main__":
    run_full_data_audit()

