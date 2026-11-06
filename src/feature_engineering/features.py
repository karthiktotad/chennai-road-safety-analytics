"""
Feature Engineering Pipeline.
Transforms raw accident attributes, environmental observations, and road geometry
into high-utility predictive features:
- Cyclical temporal transformations (hour, month, day-of-week sine/cosine)
- Behavioral & operational indicators (is_night, is_peak_hour, night_heavy_vehicle)
- Environmental friction and weather interaction terms
- Strict leakage prevention: zero post-crash consequence features included.
"""

import json
import logging
from pathlib import Path
import pandas as pd
import numpy as np

from config.settings import (
    PROCESSED_DATA_DIR, MODELS_DIR, TARGET_COLUMN
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


class ChennaiFeatureEngineer:
    """Constructs engineered feature matrix for severity classification."""

    def __init__(self):
        self.input_file = PROCESSED_DATA_DIR / "chennai_accident_severity_modeling_dataset.csv"
        self.output_file = PROCESSED_DATA_DIR / "chennai_feature_matrix.csv"
        self.metadata_file = MODELS_DIR / "feature_metadata.json"

    def build_features(self) -> pd.DataFrame:
        logger.info(f"Loading modeling dataset from {self.input_file}...")
        df = pd.read_csv(self.input_file)

        df["accident_date"] = pd.to_datetime(df["accident_date"])
        df["month"] = df["accident_date"].dt.month
        df["day_of_week_num"] = df["accident_date"].dt.dayofweek

        # 1. Cyclical Temporal Encodings (sine and cosine transforms)
        logger.info("Computing cyclical temporal transformations...")
        # Hour (24-hour cycle)
        df["hour_sin"] = np.sin(2 * np.pi * df["accident_hour"] / 24.0).round(4)
        df["hour_cos"] = np.cos(2 * np.pi * df["accident_hour"] / 24.0).round(4)

        # Month (12-month cycle)
        df["month_sin"] = np.sin(2 * np.pi * df["month"] / 12.0).round(4)
        df["month_cos"] = np.cos(2 * np.pi * df["month"] / 12.0).round(4)

        # Day of Week (7-day cycle)
        df["dow_sin"] = np.sin(2 * np.pi * df["day_of_week_num"] / 7.0).round(4)
        df["dow_cos"] = np.cos(2 * np.pi * df["day_of_week_num"] / 7.0).round(4)

        # 2. Behavioral & Domain Specific Temporal Markers
        # Peak Commute Hours: 08:00-11:00 and 17:00-20:00
        df["is_peak_hour"] = df["accident_hour"].isin([8, 9, 10, 17, 18, 19, 20]).astype(int)
        # Night Window: 20:00 to 05:00
        df["is_night"] = ((df["accident_hour"] >= 20) | (df["accident_hour"] <= 5)).astype(int)
        # Late Night High-Speed Hazard: 23:00 to 04:00
        df["is_late_night"] = df["accident_hour"].isin([23, 0, 1, 2, 3, 4]).astype(int)

        # 3. Domain Interaction Terms
        logger.info("Generating safety interaction terms...")
        # Heavy vehicle involved at night (commercial freight operating during night restrictions)
        is_heavy_vehicle = df["vehicle_type"].isin(["Truck/Lorry", "Bus"]).astype(int)
        df["night_heavy_vehicle"] = df["is_night"] * is_heavy_vehicle

        # Dark unlit road hazard
        df["is_unlit_darkness"] = (df["lighting_condition"] == "Night - Dark / Poor Lighting").astype(int)

        # Adverse weather and junction compounding hazard
        is_at_junction = (df["junction_type"] != "Mid-block / Straight Road").astype(int)
        df["wet_road_junction"] = df["is_rainy_day"] * is_at_junction

        # Vulnerable Road User (VRU) indicator: Pedestrians, Bicycles, Two-Wheelers
        df["is_vulnerable_user"] = df["vehicle_type"].isin(["Two-Wheeler", "Pedestrian/Bicycle"]).astype(int)

        # Kinetic Severity Exposure Proxy: Speed limit normalized by junction distance
        df["speed_junction_exposure"] = (
            df["speed_limit_kmh"] / (1.0 + df["distance_to_nearest_junction_km"])
        ).round(3)

        # 4. Target Formulation
        # Primary Binary Target (1 = Fatal or Grievous injury; 0 = Minor or Non-injury)
        # Target column is already TARGET_COLUMN ("severe_accident")
        # Multiclass target encoding for secondary evaluation
        multiclass_map = {
            "Non-Injury": 0,
            "Minor Injury": 1,
            "Grievous Injury": 2,
            "Fatal": 3
        }
        df["severity_multiclass"] = df["accident_severity"].map(multiclass_map).fillna(1).astype(int)

        # 5. Select Feature Matrix & Audit Against Target Leakage
        # Explicitly omit identifiers, post-crash counts, or uninformative text
        metadata = {
            "target_binary": TARGET_COLUMN,
            "target_multiclass": "severity_multiclass",
            "numerical_features": [
                "accident_hour", "speed_limit_kmh", "distance_to_nearest_junction_km",
                "rainfall_mm", "temp_mean_c", "relative_humidity_pct", "wind_speed_ms",
                "hour_sin", "hour_cos", "month_sin", "month_cos", "dow_sin", "dow_cos",
                "speed_junction_exposure"
            ],
            "binary_features": [
                "is_weekend", "is_peak_hour", "is_night", "is_late_night",
                "is_rainy_day", "is_unlit_darkness", "night_heavy_vehicle",
                "wet_road_junction", "is_vulnerable_user"
            ],
            "categorical_features": [
                "vehicle_type", "junction_type", "lighting_condition",
                "road_classification", "season", "rainfall_category"
            ]
        }

        # Save feature matrix
        df.to_csv(self.output_file, index=False)
        logger.info(f"Saved feature matrix ({len(df)} rows, {len(df.columns)} columns) to {self.output_file}")

        # Save feature schema metadata
        with open(self.metadata_file, "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2)
        logger.info(f"Saved feature metadata dictionary to {self.metadata_file}")

        return df, metadata


if __name__ == "__main__":
    fe = ChennaiFeatureEngineer()
    fe.build_features()

