"""
Data Preprocessing & Cleaning Module.
Standardizes column names, cleans date and numeric fields, handles missing values,
and computes foundational road safety indicators.
"""

import logging
from pathlib import Path
import pandas as pd
import numpy as np

from config.settings import (
    RAW_ACCIDENTS_DIR, RAW_WEATHER_DIR, PROCESSED_DATA_DIR, INTERIM_DATA_DIR
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


def clean_chennai_annual_crashes() -> pd.DataFrame:
    """
    Cleans and enriches the historical Chennai Road Crashes (1998-2025) dataset.
    Standardizes schema, calculates severity ratios, casualty rates, and trends.
    """
    input_path = RAW_ACCIDENTS_DIR / "chennai_road_crashes_1998_2025.csv"
    logger.info(f"Loading raw Chennai crash series from {input_path}...")
    df = pd.read_csv(input_path)

    # Clean headers (strip BOM and whitespace)
    df.columns = [c.replace("\ufeff", "").strip() for c in df.columns]

    # Standardize column naming convention
    rename_map = {
        "YEAR": "year",
        "Fatal Accidents": "fatal_accidents",
        "Fatal Killed": "fatal_killed",
        "Grievous Injury - Accidents": "grievous_accidents",
        "Grievous Injurty - Injured": "grievous_injured",  # Fix upstream typo in source
        "Minor Injury - Accidents": "minor_accidents",
        "Minor Injury - Injured": "minor_injured",
        "Non Injury": "non_injury_accidents",
        "Total Accidents": "total_accidents",
        "Total number of persons involved": "total_persons_involved"
    }
    df = df.rename(columns=rename_map)

    # Ensure all columns are numeric integer types
    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(int)

    df = df.sort_values("year").reset_index(drop=True)

    # Research indicators & derived severity metrics
    # Severe Accidents = Fatal + Grievous Injury accidents
    df["severe_accidents"] = df["fatal_accidents"] + df["grievous_accidents"]
    df["non_severe_accidents"] = df["minor_accidents"] + df["non_injury_accidents"]

    # Severity rate: Proportion of all accidents that resulted in death or grievous injury
    df["severity_rate"] = (df["severe_accidents"] / df["total_accidents"]).round(4)

    # Fatality rate: Proportion of accidents that are fatal
    df["fatality_rate"] = (df["fatal_accidents"] / df["total_accidents"]).round(4)

    # Total casualties (killed + all injured)
    df["total_casualties"] = df["fatal_killed"] + df["grievous_injured"] + df["minor_injured"]
    df["casualty_to_accident_ratio"] = (df["total_casualties"] / df["total_accidents"]).round(4)

    # Year-over-Year changes
    df["yoy_total_accidents_pct"] = df["total_accidents"].pct_change().round(4) * 100
    df["yoy_fatal_accidents_pct"] = df["fatal_accidents"].pct_change().round(4) * 100

    output_path = PROCESSED_DATA_DIR / "chennai_annual_crash_severity_preprocessed.csv"
    df.to_csv(output_path, index=False)
    logger.info(f"Saved cleaned Chennai annual crash dataset ({len(df)} records) to {output_path}")
    return df


def clean_tamil_nadu_district_accidents() -> pd.DataFrame:
    """
    Cleans the Tamil Nadu District-wise road accident records (2021-2023).
    Extracts Chennai's relative state standing and comparative mortality rates.
    """
    input_path = RAW_ACCIDENTS_DIR / "tamil_nadu_district_accidents_2021_2023.csv"
    logger.info(f"Loading Tamil Nadu district accidents from {input_path}...")
    df = pd.read_csv(input_path)
    df.columns = [c.replace("\ufeff", "").strip() for c in df.columns]

    rename_map = {
        "Sl No": "sl_no",
        "District": "district",
        "Total Accidents 2021": "accidents_2021",
        "Total Deaths 2021": "deaths_2021",
        "Total Accidents 2022": "accidents_2022",
        "Total Deaths 2022": "deaths_2022",
        "Total Accidents 2023": "accidents_2023",
        "Total Deaths 2023": "deaths_2023"
    }
    df = df.rename(columns=rename_map)

    # Replace 'NA' strings with median imputation by year or forward fill
    metric_cols = [c for c in df.columns if c not in ["sl_no", "district"]]
    for col in metric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")
        # Impute missing values with district column median
        df[col] = df[col].fillna(df[col].median()).astype(int)

    # Calculate 3-year aggregated crash totals & mortality rates per 100 crashes
    df["accidents_3yr_total"] = df["accidents_2021"] + df["accidents_2022"] + df["accidents_2023"]
    df["deaths_3yr_total"] = df["deaths_2021"] + df["deaths_2022"] + df["deaths_2023"]
    df["fatality_rate_pct"] = (df["deaths_3yr_total"] / df["accidents_3yr_total"] * 100).round(2)

    # Flag Chennai City
    df["is_chennai"] = df["district"].str.upper().str.contains("CHENNAI")

    output_path = PROCESSED_DATA_DIR / "tamil_nadu_district_accidents_preprocessed.csv"
    df.to_csv(output_path, index=False)
    logger.info(f"Saved cleaned TN district accidents ({len(df)} districts) to {output_path}")
    return df


def clean_chennai_weather_data() -> pd.DataFrame:
    """
    Cleans daily NASA POWER meteorological series (2018-2023).
    Extracts temporal cycles (month, day of week, season), computes diurnal temperature
    variations, rainfall intensity categories, and extreme weather indicators.
    """
    input_path = RAW_WEATHER_DIR / "chennai_weather_nasa_power_daily_20180101_20231231.csv"
    logger.info(f"Loading NASA POWER daily weather from {input_path}...")
    df = pd.read_csv(input_path)

    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date").reset_index(drop=True)

    # Standardize column naming
    rename_map = {
        "PRECTOTCORR": "rainfall_mm",
        "T2M": "temp_mean_c",
        "T2M_MAX": "temp_max_c",
        "T2M_MIN": "temp_min_c",
        "RH2M": "relative_humidity_pct",
        "WS10M": "wind_speed_ms",
        "PS": "surface_pressure_kpa"
    }
    df = df.rename(columns=rename_map)

    # Ensure no negative rainfall values
    df["rainfall_mm"] = df["rainfall_mm"].clip(lower=0.0)

    # Temporal feature extraction
    df["year"] = df["date"].dt.year
    df["month"] = df["date"].dt.month
    df["day"] = df["date"].dt.day
    df["day_of_week"] = df["date"].dt.day_name()
    df["day_of_week_num"] = df["date"].dt.dayofweek  # 0=Monday, 6=Sunday
    df["is_weekend"] = df["day_of_week_num"].isin([5, 6]).astype(int)

    # Chennai Climate Season definition:
    # 1. Northeast Monsoon (Primary rainy season): October, November, December
    # 2. Winter: January, February
    # 3. Summer (Hot weather): March, April, May
    # 4. Southwest Monsoon: June, July, August, September
    def assign_season(m):
        if m in [10, 11, 12]:
            return "Northeast Monsoon"
        elif m in [1, 2]:
            return "Winter"
        elif m in [3, 4, 5]:
            return "Summer"
        else:
            return "Southwest Monsoon"

    df["season"] = df["month"].apply(assign_season)

    # Diurnal temperature range (Max - Min)
    df["diurnal_temp_range_c"] = (df["temp_max_c"] - df["temp_min_c"]).round(2)

    # Environmental indicator categories:
    # Rainfall categories according to IMD criteria:
    # - No Rain: 0.0 mm
    # - Very Light Rain: 0.1 - 2.4 mm
    # - Light to Moderate Rain: 2.5 - 15.5 mm
    # - Heavy Rain: > 15.5 mm
    def categorize_rain(r):
        if r < 0.1:
            return "No Rain"
        elif r <= 2.4:
            return "Very Light"
        elif r <= 15.5:
            return "Moderate Rain"
        else:
            return "Heavy Rain"

    df["rainfall_category"] = df["rainfall_mm"].apply(categorize_rain)
    df["is_rainy_day"] = (df["rainfall_mm"] >= 0.1).astype(int)
    df["is_heavy_rain"] = (df["rainfall_mm"] > 15.5).astype(int)

    # Extreme weather threshold flags
    df["is_extreme_heat"] = (df["temp_max_c"] >= 38.0).astype(int)
    df["is_high_humidity"] = (df["relative_humidity_pct"] >= 85.0).astype(int)
    df["is_high_wind"] = (df["wind_speed_ms"] >= 8.0).astype(int)

    # 3-day and 7-day rolling rainfall accumulation (soil saturation & waterlogging marker)
    df["rainfall_3d_sum_mm"] = df["rainfall_mm"].rolling(window=3, min_periods=1).sum().round(2)
    df["rainfall_7d_sum_mm"] = df["rainfall_mm"].rolling(window=7, min_periods=1).sum().round(2)

    output_path = PROCESSED_DATA_DIR / "chennai_daily_weather_preprocessed.csv"
    df.to_csv(output_path, index=False)
    logger.info(f"Saved cleaned Chennai weather dataset ({len(df)} daily records) to {output_path}")
    return df


def run_all_preprocessing():
    logger.info("Starting baseline data cleaning and preprocessing pipeline...")
    crashes_df = clean_chennai_annual_crashes()
    district_df = clean_tamil_nadu_district_accidents()
    weather_df = clean_chennai_weather_data()
    logger.info("Baseline preprocessing completed successfully.")
    return crashes_df, district_df, weather_df


if __name__ == "__main__":
    run_all_preprocessing()

