"""
Centralized Configuration and Settings for Chennai Road Accident Research Project.
Provides standard paths, parameters, and reproducibility constants.
"""

from pathlib import Path
import os

# Project root directory (absolute path resolved dynamically)
BASE_DIR = Path(__file__).resolve().parent.parent

# Data directory paths
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
RAW_ACCIDENTS_DIR = RAW_DATA_DIR / "accidents"
RAW_WEATHER_DIR = RAW_DATA_DIR / "weather"
RAW_ROAD_DIR = RAW_DATA_DIR / "road_network"
RAW_SUPPLEMENTARY_DIR = RAW_DATA_DIR / "supplementary"

INTERIM_DATA_DIR = DATA_DIR / "interim"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

# Models and results
MODELS_DIR = BASE_DIR / "models"
RESULTS_DIR = BASE_DIR / "results"
VISUALIZATIONS_DIR = RESULTS_DIR / "visualizations"
REPORTS_DIR = RESULTS_DIR / "reports"
MAPS_DIR = RESULTS_DIR / "maps"
METRICS_DIR = RESULTS_DIR / "metrics"
LOGS_DIR = BASE_DIR / "logs"

# Ensure all directories exist
for path in [
    RAW_ACCIDENTS_DIR, RAW_WEATHER_DIR, RAW_ROAD_DIR, RAW_SUPPLEMENTARY_DIR,
    INTERIM_DATA_DIR, PROCESSED_DATA_DIR, MODELS_DIR,
    VISUALIZATIONS_DIR, REPORTS_DIR, MAPS_DIR, METRICS_DIR, LOGS_DIR
]:
    path.mkdir(parents=True, exist_ok=True)

# Study Area Parameters (Chennai, Tamil Nadu, India)
STUDY_AREA = {
    "city": "Chennai",
    "state": "Tamil Nadu",
    "country": "India",
    "center_lat": 13.0827,
    "center_lon": 80.2707,
    # Bounding box for Chennai Metropolitan Area (approximate)
    "bbox": {
        "north": 13.2500,
        "south": 12.8000,
        "east": 80.3500,
        "west": 80.0000
    }
}

# Reproducibility settings
RANDOM_SEED = 42
TEST_SIZE = 0.20
CV_FOLDS = 5

# Target definition
TARGET_COLUMN = "severe_accident"  # 1 = Fatal/Grievous, 0 = Minor/Non-injury

