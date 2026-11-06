"""
Master Data Collection Runner.
Executes automated ingestion for:
1. Chennai Road Accident Records (OpenCity / Official Portals)
2. Atmospheric & Weather Observations (NASA POWER API)
3. Road Infrastructure & Junctions (OpenStreetMap Overpass API)
"""

import sys
import logging
from datetime import datetime

from src.data_collection.accident_collector import AccidentDataCollector
from src.data_collection.weather_collector import NASAWeatherCollector
from src.data_collection.road_collector import OSMRoadNetworkCollector

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


def run_all_collections():
    start_time = datetime.now()
    logger.info("=== Starting Chennai Road Safety Research Data Ingestion ===")

    # 1. Collect Road Accident Records
    logger.info("\n--- Step 1: Collecting Chennai Road Accident Records ---")
    accident_collector = AccidentDataCollector()
    accident_results = accident_collector.collect_all_opencity_accident_data()
    logger.info(f"Accident collection complete. Retrieved {len(accident_results)} resource files.")

    # 2. Collect Weather Data
    logger.info("\n--- Step 2: Collecting NASA POWER Weather Observations ---")
    weather_collector = NASAWeatherCollector()
    try:
        # Collect daily meteorology for 2018 through 2024
        csv_path, json_path = weather_collector.fetch_daily_weather(start_date="20180101", end_date="20241231")
        logger.info(f"Weather collection complete. Saved CSV to {csv_path}")
    except Exception as e:
        logger.error(f"Weather collection encountered an error: {e}")

    # 3. Collect Road Network Data
    logger.info("\n--- Step 3: Collecting OpenStreetMap Road Infrastructure ---")
    road_collector = OSMRoadNetworkCollector()
    try:
        roads_file = road_collector.fetch_major_roads()
        junctions_file = road_collector.fetch_intersections_and_junctions()
        logger.info(f"Road network collection complete. Roads: {roads_file}, Junctions: {junctions_file}")
    except Exception as e:
        logger.error(f"Road network collection encountered an error: {e}")

    duration = datetime.now() - start_time
    logger.info(f"\n=== Data Collection Stage Finished in {duration.total_seconds():.1f}s ===")


if __name__ == "__main__":
    run_all_collections()

